---
name: configure-nightwatch
description: "Configures Laravel Nightwatch data collection, sampling rates, filtering rules, and redaction policies. Use when setting up Nightwatch, managing data volume, protecting sensitive data (PII), or optimizing event collection for production workloads."
---
# Nightwatch Configuration Guide

This skill helps configure Laravel Nightwatch data collection to balance observability, performance, and privacy. Covers sampling strategies, filtering rules, and redaction methods across all event types.

## Documentation Reference

The [Nightwatch Documentation](https://nightwatch.laravel.com/docs) is the definitive and up-to-date source of information for all Nightwatch configuration options. This skill provides practical guidance and common patterns, but always consult the official documentation as the primary source of truth for specific details, environment variables, and API behavior. The documentation includes comprehensive coverage of:

- [Filtering and Configuration](https://nightwatch.laravel.com/docs/filtering) - Core concepts for sampling, filtering, and redaction
- Individual event type pages with specific configuration options:
  - [Requests](https://nightwatch.laravel.com/docs/requests) - Request sampling, header handling, payload capture
  - [Commands](https://nightwatch.laravel.com/docs/commands) - Command sampling and redaction
  - [Queries](https://nightwatch.laravel.com/docs/queries) - Query filtering and redaction
  - [Cache](https://nightwatch.laravel.com/docs/cache) - Cache event filtering by key or pattern
  - [Jobs](https://nightwatch.laravel.com/docs/jobs) - Job filtering and sampling decoupling
  - [Mail](https://nightwatch.laravel.com/docs/mail) - Mail event filtering
  - [Notifications](https://nightwatch.laravel.com/docs/notifications) - Notification filtering by channel
  - [Exceptions](https://nightwatch.laravel.com/docs/exceptions) - Exception sampling and throttling
  - [Outgoing Requests](https://nightwatch.laravel.com/docs/outgoing-requests) - HTTP request filtering
- [reference.md](reference.md) - Quick lookup table by event type, production presets, and verification checklist

## Data Collection Flow

Nightwatch processes events through three stages:

1. **Sampling** - Controls which entry points are captured (requests, commands, scheduled tasks)
2. **Filtering** - Excludes specific events after sampling (queries, cache, mail, etc.)
3. **Redaction** - Modifies captured data to remove/obfuscate sensitive information

```
Request/Command/Scheduled Task
       |
       v
   [Sampling?] ----NO----> Drop entire trace
       | YES
       v
   Events generated
       |
       v
   [Filtering?] ----YES---> Drop specific event
       | NO
       v
   [Redaction] ----------> Store modified data
```

---

## Sampling Configuration

Sampling determines which entry points (requests, commands, scheduled tasks) trigger full trace collection. When an entry point is sampled, all related events are captured.

### Global Sample Rates

Configure via environment variables:

```bash
NIGHTWATCH_REQUEST_SAMPLE_RATE=0.1      # Recommended: 10% of requests
NIGHTWATCH_COMMAND_SAMPLE_RATE=1.0      # Capture all commands
NIGHTWATCH_EXCEPTION_SAMPLE_RATE=1.0    # Always capture exceptions
```

**Recommendation**: Start with `0.1` (10%) for requests in production, adjust based on volume and needs.

### Route-Based Sampling

Apply different rates to specific routes using the `Sample` middleware:

```php
use Illuminate\Support\Facades\Route;
use Laravel\Nightwatch\Http\Middleware\Sample;

Route::middleware(Sample::rate(1.0))->prefix('admin')->group(function () {
    // All admin routes sampled fully
});

Route::middleware(Sample::rate(0.05))->prefix('api')->group(function () {
    // API routes sampled sparingly
});

Route::post('/checkout', [CheckoutController::class, 'process'])
    ->middleware(Sample::always());

Route::get('/health', [HealthController::class, 'check'])
    ->middleware(Sample::never());
```

### Unmatched Route Sampling

```php
Route::fallback(fn () => abort(404))
    ->middleware(Sample::rate(0.01));
```

### Dynamic Sampling

```php
use Closure;
use Illuminate\Http\Request;
use Laravel\Nightwatch\Facades\Nightwatch;

class SampleAdminRequests
{
    public function handle(Request $request, Closure $next)
    {
        if ($request->user()?->isAdmin()) {
            Nightwatch::sample();
        }
        return $next($request);
    }
}
```

### Command Sampling

```php
use Illuminate\Console\Events\CommandStarting;
use Illuminate\Support\Facades\Event;
use Laravel\Nightwatch\Facades\Nightwatch;

public function boot(): void
{
    Event::listen(function (CommandStarting $event) {
        if (in_array($event->command, ['schedule:finish', 'horizon:snapshot'])) {
            Nightwatch::dontSample();
        }
    });
}
```

### Vendor Commands

```php
Nightwatch::captureDefaultVendorCommands();
```

---

## Filtering Configuration

Filtering excludes specific events from collection after sampling.

### Database Queries

```bash
NIGHTWATCH_IGNORE_QUERIES=true
```

```php
use Laravel\Nightwatch\Facades\Nightwatch;
use Laravel\Nightwatch\Records\Query;

public function boot(): void
{
    Nightwatch::rejectQueries(function (Query $query) {
        return str_contains($query->sql, 'into "jobs"');
    });

    Nightwatch::rejectQueries(function (Query $query) {
        return str_contains($query->sql, 'from `cache`')
            || str_contains($query->sql, 'into `cache`');
    });
}
```

### Cache Events

```bash
NIGHTWATCH_IGNORE_CACHE_EVENTS=true
```

```php
Nightwatch::rejectCacheKeys([
    'my-app:users',
    '/^my-app:posts:/',
    '/^[a-zA-Z0-9]{40}$/',
]);
```

```php
use Laravel\Nightwatch\Records\CacheEvent;

Nightwatch::rejectCacheEvents(function (CacheEvent $cacheEvent) {
    return str_starts_with($cacheEvent->key, 'temp:');
});
```

### Mail Events

```bash
NIGHTWATCH_IGNORE_MAIL=true
```

```php
use Laravel\Nightwatch\Records\Mail;

Nightwatch::rejectMail(function (Mail $mail) {
    return str_contains($mail->subject, 'Newsletter');
});
```

### Notification Events

```bash
NIGHTWATCH_IGNORE_NOTIFICATIONS=true
```

```php
use Laravel\Nightwatch\Records\Notification;

Nightwatch::rejectNotifications(function (Notification $notification) {
    return $notification->channel === 'database';
});
```

### Outgoing HTTP Requests

```bash
NIGHTWATCH_IGNORE_OUTGOING_REQUESTS=true
```

```php
use Laravel\Nightwatch\Records\OutgoingRequest;

Nightwatch::rejectOutgoingRequests(function (OutgoingRequest $request) {
    return str_contains($request->url, 'analytics.example.com');
});
```

### Queued Jobs

```php
use Laravel\Nightwatch\Records\QueuedJob;

Nightwatch::rejectQueuedJobs(function (QueuedJob $job) {
    return $job->name === 'App\Jobs\LowPriorityJob';
});
```

### Decoupling Job Sampling

```php
use Illuminate\Support\Facades\Queue;

public function boot(): void
{
    Queue::before(fn () => Nightwatch::sample(rate: 0.5));
}
```

---

## Redaction Configuration

Redaction modifies captured data to remove or obfuscate sensitive information.

### Request Redaction

```bash
NIGHTWATCH_REDACT_HEADERS=Authorization,Cookie,Proxy-Authorization,X-API-Key
NIGHTWATCH_CAPTURE_REQUEST_PAYLOAD=true
NIGHTWATCH_REDACT_PAYLOAD_FIELDS=password,password_confirmation,ssn,credit_card
```

```php
use Laravel\Nightwatch\Facades\Nightwatch;
use Laravel\Nightwatch\Records\Request;

Nightwatch::redactRequests(function (Request $request) {
    $request->url = str_replace('secret', '***', $request->url);
    $request->ip = preg_replace('/\d+$/', '***', $request->ip);
});
```

### Query Redaction

```php
use Laravel\Nightwatch\Records\Query;

Nightwatch::redactQueries(function (Query $query) {
    $query->sql = str_replace('secret_token', '***', $query->sql);
});
```

### Cache Redaction

```php
use Laravel\Nightwatch\Records\CacheEvent;

Nightwatch::redactCacheEvents(function (CacheEvent $cacheEvent) {
    $cacheEvent->key = str_replace('user:', 'user:***:', $cacheEvent->key);
});
```

### Command Redaction

```php
use Laravel\Nightwatch\Records\Command;

Nightwatch::redactCommands(function (Command $command) {
    $command->command = preg_replace('/--password=\S+/', '--password=***', $command->command);
});
```

### Exception Redaction

```php
use Laravel\Nightwatch\Records\Exception;

Nightwatch::redactExceptions(function (Exception $exception) {
    $exception->message = str_replace('secret', '***', $exception->message);
});
```

### Mail Redaction

```php
use Laravel\Nightwatch\Records\Mail;

Nightwatch::redactMail(function (Mail $mail) {
    $mail->subject = str_replace('Invoice #', 'Invoice ***', $mail->subject);
});
```

### Outgoing Request Redaction

```php
use Laravel\Nightwatch\Records\OutgoingRequest;

Nightwatch::redactOutgoingRequests(function (OutgoingRequest $outgoingRequest) {
    $outgoingRequest->url = preg_replace('/api_key=\w+/', 'api_key=***', $outgoingRequest->url);
});
```
