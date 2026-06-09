---
name: snapp-pay
description: "When working with the SnappPay (Snapp! Pay) payment gateway — an Iranian installment/BNPL payment provider. Use this for implementing or debugging SnappPay integration: OAuth2 JWT authentication, merchant eligibility, payment token creation with cart data, callback handling, verify/settle/revert/cancel/update/status API operations, error code classification, iPhone/Android PDP component styling, on-site messaging guidelines, and commission type mapping."
metadata:
    version: 2.0.0
---

# Snapp! Pay — Payment Gateway Integration Skill

Comprehensive reference for integrating SnappPay (اسنپ‌پی), an Iranian BNPL/installment payment gateway.

---

## 1. API Overview

### Base URL

- **Staging**: Provided by SnappPay on demo (Usually available in .env as SNAPP_PAY_BASE_URL)
- **Production**: Provided by SnappPay after pre-demo approval

### Response Format

**Success (HTTP 2xx)**:

```json
{
  "successful": true,
  "response": { ... }
}
```

**Error (HTTP 4xx/5xx)**:

```json
{
    "errorData": {
        "errorCode": 400,
        "message": "",
        "data": null
    },
    "successful": false
}
```

### API Endpoints

| #   | Method | Endpoint                        | Purpose                                    |
| --- | ------ | ------------------------------- | ------------------------------------------ |
| 1   | POST   | `/api/online/v1/oauth/token`    | OAuth2 JWT authentication (password grant) |
| 2   | GET    | `/api/online/offer/v1/eligible` | Check installment eligibility              |
| 3   | POST   | `/api/online/payment/v1/token`  | Create payment token                       |
| 4   | POST   | `/api/online/payment/v1/verify` | Verify completed payment                   |
| 5   | POST   | `/api/online/payment/v1/settle` | Settle/confirm payment                     |
| 6   | POST   | `/api/online/payment/v1/revert` | Revert payment before settle               |
| 7   | POST   | `/api/online/payment/v1/cancel` | Cancel payment after settle                |
| 8   | GET    | `/api/online/payment/v1/status` | Check payment status                       |
| 9   | POST   | `/api/online/payment/v1/update` | Update order/cart after settle             |

### Possible Statuses

- `SETTLE` — Finalized
- `CANCEL` — Cancelled
- `VERIFY` — Verified (awaiting settle)
- `PENDING` — Pending
- `REVERT` — Reverted

---

## 2. Authentication

### OAuth2 JWT Token

**Endpoint**: `POST /api/online/v1/oauth/token`

**Headers**:

- `Authorization: Basic base64_encode(client_id:client_secret)`
- `Content-Type: application/x-www-form-urlencoded`

**Body** (form-urlencoded):
| Field | Value |
|-------|-------|
| `grant_type` | `password` |
| `scope` | `online-merchant` |
| `username` | `{username}` |
| `password` | `{password}` |

**Response**:

```json
{
    "access_token": "eyJhbGciOiJ...",
    "token_type": "bearer",
    "expires_in": 3600,
    "scope": "online-merchant",
    "iat": 1645369630,
    "jti": "ogYjKGgZACeJ_Qc7Jb5e7v2AWWU"
}
```

**Important**: Token expires in **3600 seconds**. Cache it but refresh before expiry. Subsequent API calls use `Authorization: Bearer {access_token}`.

### Merchant IP Whitelisting

- Merchant's outgoing server IP **must be whitelisted** by SnappPay before API calls work
- Contact `merchant@snapppay.ir` with your static IP
- To find your IP: `curl -X GET https://whatisip.snapppay.ir/whatis/ip`
- Iran IP required (foreign IPs not accepted)

---

## 3. Eligibility Check

**Endpoint**: `GET /api/online/offer/v1/eligible`

**Headers**: `Authorization: Bearer {jwt}`

**Query Parameters**:
| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `amount` | ✅ Yes | int | Amount in **Rial (IRR)** |
| `paymentMethodTypes` | ❌ No | string (comma-separated) | `POSTPAID`, `INSTALLMENT`, `FINANCING`. Optional — leave empty to show all available methods |

**Response**:

```json
{
    "response": {
        "eligible": true,
        "title_message": "string",
        "description": "string"
    },
    "successful": true
}
```

**Rules**:

- Call this dynamically on **every amount change** — don't cache the result
- `eligible: false` → do NOT show SnappPay as a payment option
- `title` and `description` are **dynamic** from SnappPay — never hardcode them
- For staging: amounts below 4,000 Toman and above 10,000,000 Toman return `false`
- Production thresholds differ from staging

---

## 4. Payment Token

**Endpoint**: `POST /api/online/payment/v1/token`

**Headers**: `Authorization: Bearer {jwt}`, `Content-Type: application/json`

**Request Body**:

```json
{
    "amount": 20000000,
    "cartList": [
        {
            "cartId": 1,
            "cartItems": [
                {
                    "amount": 20000000,
                    "category": "test",
                    "count": 1,
                    "id": 1,
                    "name": "test",
                    "commissionType": "1"
                }
            ],
            "isShipmentIncluded": true,
            "isTaxIncluded": true,
            "shippingAmount": 0,
            "taxAmount": 0,
            "totalAmount": 20000000
        }
    ],
    "discountAmount": 0,
    "externalSourceAmount": 0,
    "mobile": "+989121111111",
    "forcedPaymentMethodTypes": ["INSTALLMENT"],
    "paymentMethodTypeDto": "INSTALLMENT",
    "returnURL": "https://your-domain.com/payment/callback",
    "transactionId": "unique_tx_id_12345"
}
```

### Field Reference

| Field                           | Required | Type   | Description                                                                   |
| ------------------------------- | -------- | ------ | ----------------------------------------------------------------------------- |
| `amount`                        | ✅       | int    | Total order amount (IRR/Rial)                                                 |
| `discountAmount`                | ✅       | int    | Discount amount (IRR)                                                         |
| `externalSourceAmount`          | ✅       | int    | External source amount (IRR)                                                  |
| `mobile`                        | ✅       | string | User mobile (+98XXXXXXXXXX format)                                            |
| `returnURL`                     | ✅       | string | POST callback URL (domain must be whitelisted)                                |
| `transactionId`                 | ✅       | string | Unique ID per purchase (5-10 digits; if >10 must include a letter)            |
| `cartList`                      | ✅       | array  | Array of cart objects                                                         |
| `forcedPaymentMethodTypes`      | ❌       | array  | `POSTPAID`, `INSTALLMENT`, `FINANCING`. Requires activation by SnappPay team. |
| `cartList[].cartId`             | ✅       | int    | Cart identifier                                                               |
| `cartList[].isShipmentIncluded` | ✅       | bool   | Whether shipping cost is included in item amounts                             |
| `cartList[].isTaxIncluded`      | ✅       | bool   | Whether tax is included in item amounts                                       |
| `cartList[].shippingAmount`     | ✅       | int    | Shipping cost (IRR)                                                           |
| `cartList[].taxAmount`          | ✅       | int    | Tax amount (IRR)                                                              |
| `cartList[].totalAmount`        | ✅       | int    | Total of this cart (IRR)                                                      |
| `cartList[].cartItems`          | ✅       | array  | Items in this cart                                                            |
| `cartItems[].id`                | ✅       | int    | Item ID                                                                       |
| `cartItems[].amount`            | ✅       | int    | Item unit price (IRR)                                                         |
| `cartItems[].category`          | ✅       | string | Item category                                                                 |
| `cartItems[].count`             | ✅       | int    | Quantity                                                                      |
| `cartItems[].name`              | ✅       | string | Item name                                                                     |
| `cartItems[].commissionType`    | ✅       | string | Commission category code (default: `"1"` or `"100"`)                          |

### Amount Calculation Formula

```
Per cart: totalAmount = (count × item amount) + shipment (if not included) + tax (if not included)
Per order: amount = cartList[0].totalAmount + ... + cartList[n].totalAmount - discountAmount - externalSourceAmount
```

### Commission Type

- Default: `"100"` if you have a single category
- Use the category code from your contract for multi-category merchants
- Incorrect commission type is the merchant's responsibility

### Response

```json
{
    "response": {
        "paymentToken": "string",
        "paymentPageUrl": "string"
    },
    "successful": true
}
```

**Payment URL Priority**: Use `paymentPageUrl` from response → fallback to constructing from template → fallback to raw `paymentToken`

---

## 5. Callback Parameters

When SnappPay redirects the user back to your `returnURL`, it sends a **POST** form with:

| Parameter       | Type   | Description                                         |
| --------------- | ------ | --------------------------------------------------- |
| `transactionId` | string | The unique transaction ID sent in the token request |
| `state`         | string | `OK` (success) or `FAILED`                          |
| `amount`        | int    | Amount in IRR                                       |

Store the `paymentToken` from step 4 — you'll need it for verify/settle/revert/cancel/status.

---

## 6. Verify

**Endpoint**: `POST /api/online/payment/v1/verify`

**Headers**: `Authorization: Bearer {jwt}`, `Content-Type: application/json`

**Body**:

```json
{ "paymentToken": "a2bd8159-5d8e-474c-b464-ec106df2de61" }
```

**Response**:

```json
{
    "response": { "transactionId": "string" },
    "successful": true
}
```

**Rules**:

- Call verify **only once** per transaction (idempotent)
- Must be called within a **limited time window** or payment auto-reverts
- Set a **30-second timeout** for the verify request
- If timeout occurs → call `Get Payment Status` to check state

### Verify Management Flow

1. Call verify with 30s timeout
2. **Timeout** (no response in 30s) → call `Get Payment Status`
3. If status is `VERIFY` → call settle
4. If status is `PENDING` → retry verify
5. If status is anything else → mark as failed

---

## 7. Settle

**Endpoint**: `POST /api/online/payment/v1/settle`

**Headers**: `Authorization: Bearer {jwt}`, `Content-Type: application/json`

**Body**:

```json
{ "paymentToken": "a2bd8159-5d8e-474c-b464-ec106df2de61" }
```

**Response**:

```json
{
    "response": { "transactionId": "string" },
    "successful": true
}
```

**Rules**:

- **MANDATORY** — all verified orders must be settled
- After settle, only cancel is possible (no revert)
- If settle fails/no response → call `Get Payment Status`

### Settle Management Flow

1. Call settle
2. **Fails/no response** → call `Get Payment Status`
3. If status is `VERIFY` → retry settle
4. If status is `SETTLE` → success, finalize order

---

## 8. Revert

**Endpoint**: `POST /api/online/payment/v1/revert`

**Headers**: `Authorization: Bearer {jwt}`, `Content-Type: application/json`

**Body**:

```json
{ "paymentToken": "a2bd8159-5d8e-474c-b464-ec106df2de61" }
```

**Warning**: Revert is only needed if **explicitly instructed** by SnappPay support. Most merchants don't need to implement it. Only works for statuses `PENDING` or `VERIFY` (not `SETTLE`).

---

## 9. Cancel

**Endpoint**: `POST /api/online/payment/v1/cancel`

**Headers**: `Authorization: Bearer {jwt}`, `Content-Type: application/json`

**Body**:

```json
{ "paymentToken": "a2bd8159-5d8e-474c-b464-ec106df2de61" }
```

**Rules**:

- **MANDATORY** to implement
- Only works for `SETTLE` status
- **Irreversible** — require admin confirmation before calling
- After successful cancel, refund the user and mark order as unpaid

---

## 10. Get Payment Status

**Endpoint**: `GET /api/online/payment/v1/status?paymentToken={token}`

**Headers**: `Authorization: Bearer {jwt}`, `Content-Type: application/json`

**Response**:

```json
{
    "response": {
        "transactionId": "string",
        "status": "string",
        "amount": 0
    },
    "successful": true
}
```

**Use case**: Recovery/inquiry when verify or settle fails or times out.

---

## 11. Update

**Endpoint**: `POST /api/online/payment/v1/update`

**Headers**: `Authorization: Bearer {jwt}`, `Content-Type: application/json`

**Body**:

```json
{
  "amount": 15000000,
  "cartList": [ ... ],
  "discountAmount": 0,
  "externalSourceAmount": 0,
  "paymentToken": "68f08aa7-f1f8-40c8-97b2-c9526e8fa69e"
}
```

**Rules**:

- **MANDATORY** for multi-item stores
- Only works for `SETTLE` status
- Updated amount must be **≤ original** amount
- If removing items, remove from `cartItems` array
- **Irreversible** — require admin confirmation
- If item completely removed, delete from cartItems

---

## 12. Complete Error Reference

All errors per endpoint with `http status`, `error code`, description, and action:

### Token Endpoint Errors

| HTTP | Code | Message                                  | Action                             |
| ---- | ---- | ---------------------------------------- | ---------------------------------- |
| 500  | 1000 | GENERAL                                  | Retry with interval                |
| 400  | 1005 | Invalid mobile (must match `\+98\d{10}`) | Fix mobile format                  |
| 409  | 1009 | Duplicate transaction ID                 | Generate new unique transaction ID |
| 403  | 1051 | Invalid return URL domain                | Ensure domain is whitelisted       |
| 400  | —    | Empty payment token (400 status)         | Check request body                 |

### Verify Endpoint Errors

| HTTP | Code | Message                               | Action                                         |
| ---- | ---- | ------------------------------------- | ---------------------------------------------- |
| 500  | 1000 | GENERAL                               | Use timeout recovery flow (Get Payment Status) |
| 400  | 1011 | Invalid status (must be PENDING)      | Check payment status first                     |
| 429  | 1053 | Ongoing transition locked             | Retry after short delay                        |
| 400  | 1048 | Token doesn't belong to this merchant | Verify merchant config                         |
| 404  | —    | Payment token not found               | Check token value                              |
| 400  | 1005 | Empty payment token                   | Check request body                             |

### Revert Endpoint Errors

| HTTP | Code | Message                                    | Action                  |
| ---- | ---- | ------------------------------------------ | ----------------------- |
| 500  | 1000 | GENERAL                                    | Use recovery flow       |
| 400  | 1011 | Invalid status (must be PENDING or VERIFY) | Check before reverting  |
| 429  | 1053 | Ongoing transition locked                  | Retry after short delay |
| 400  | 1048 | Merchant mismatch                          | Verify merchant config  |
| 404  | 1007 | Payment token not found                    | Check token value       |

### Settle Endpoint Errors

| HTTP | Code | Message                         | Action                                           |
| ---- | ---- | ------------------------------- | ------------------------------------------------ |
| 500  | 1000 | GENERAL                         | Auto-settle happens at night if verify succeeded |
| 400  | 1011 | Invalid status (must be VERIFY) | Verify first                                     |
| 400  | 1048 | Merchant mismatch               | Verify merchant config                           |
| 404  | 1007 | Payment token not found         | Check token value                                |

### Cancel Endpoint Errors

| HTTP | Code | Message                         | Action                  |
| ---- | ---- | ------------------------------- | ----------------------- |
| 500  | 1000 | GENERAL                         | Manual retry            |
| 400  | 1011 | Invalid status (must be SETTLE) | Check before cancelling |
| 429  | 1053 | Ongoing transition locked       | Retry after short delay |
| 400  | 1048 | Merchant mismatch               | Verify merchant config  |
| 404  | 1007 | Payment token not found         | Check token value       |

### Update Endpoint Errors

| HTTP | Code | Message                         | Action                          |
| ---- | ---- | ------------------------------- | ------------------------------- |
| 400  | 1005 | Empty values                    | Check request body              |
| 404  | 1036 | Order not found for this token  | Verify token                    |
| 409  | 1042 | Update amount > original        | Reduce amount                   |
| 400  | 1011 | Invalid status (must be SETTLE) | Settle first                    |
| 429  | 1053 | Ongoing transition locked       | Retry after short delay         |
| 400  | 1048 | Merchant mismatch               | Verify merchant config          |
| 404  | 1007 | Payment token not found         | Check token value               |
| 400  | 1078 | Has SnappPay discount code      | Cannot update discounted orders |

### Status Endpoint Errors

| HTTP | Code | Message                 | Action                 |
| ---- | ---- | ----------------------- | ---------------------- |
| 404  | 1007 | Payment token not found | Check token value      |
| 404  | 1048 | Merchant mismatch       | Verify merchant config |
| 400  | 1005 | Empty payment token     | Check request body     |

### Error Classification Categories

| Category          | Condition                          | Action                        |
| ----------------- | ---------------------------------- | ----------------------------- |
| **retryable**     | HTTP 500+ or codes 1000, 1053      | Auto-retry with backoff       |
| **terminal**      | Codes 1005, 1009, 1051, 1042, 1078 | Show error to user, fix input |
| **manual_review** | Codes 1007, 1048, 1011, HTTP 404   | Log for admin review          |

---

## 13. On-Site UI / Style Guide

### PDP Component (Product Details Page)

SnappPay must appear as a payment method option at checkout, designed per these specs:

**Desktop/Tablet Layout**:

```
display: flex; flex-direction: row; justify-content: flex-end;
align-items: flex-start; padding: 0px; gap: 16px;
width: 388px; height: 52px;
```

**Mobile Layout**:

```
display: flex; flex-direction: row; justify-content: flex-end;
align-items: flex-start; padding: 0px; gap: 12px;
width: 288px; height: 64px;
```

### Logo Usage

| Device         | Logo Size        | Shape         |
| -------------- | ---------------- | ------------- |
| Desktop/Tablet | **40×40px**      | Round or Flat |
| Mobile         | **32×32px**      | Round or Flat |
| Smaller areas  | 24×24px, 16×16px | —             |

**Logo Colors**:

- **Blue Background**: `#008EFA` — primary logo
- **White Background**: `#FFFFFF` — for dark backgrounds
- No other colors allowed

**Logo Files Available**:

- Blue BG / White BG
- Round / Flat shapes
- Sizes: 16, 24, 32, 40 (SVG + PNG @2x/@3x)

### Typography

| Property                     | Spec                                                          |
| ---------------------------- | ------------------------------------------------------------- |
| Font                         | **IranSans** (IranSansX)                                      |
| Title size (when >40px logo) | 12px **Bold** minimum                                         |
| Title size (when ≤40px logo) | 14px **Bold** minimum                                         |
| Subtitle size                | 10px **Regular** minimum                                      |
| Color palette                | High: `#1A1C23`, Medium: `#616475`, White, Disable: `#9B9EB1` |
| WCAG compliance              | Must meet contrast standards                                  |

### Component Text (Persian)

```
هر قسط با اسنپ‌پی ۱۲۳,۴۵۶ تومان
۴ ماهه، بدون بهره، کوچک و منعطف
```

The component includes: **Logo** → **Title** → **Subtitle**

### Background Colors

| Background       | Color                  |
| ---------------- | ---------------------- |
| White            | `#FFFFFF`              |
| Gray             | `#DDDDDD`              |
| Light Gray       | `#EBEBEB`              |
| Active/Highlight | `#C2EBEF`              |
| Dark             | Dark background colors |

### Responsive Behavior

- Below **360px** width: use mobile layout
- Only the `Add to Cart` component can appear on the PDP (as per guidelines)
- Component must adapt to both light and dark backgrounds

---

## 14. Implementation Workflow

### Step 1: Authentication Setup

- Implement OAuth2 JWT token endpoint
- Cache token for 3300s (leave 300s buffer before 3600s expiry)
- Use Basic auth with base64(client_id:client_secret)

### Step 2: Eligibility Check

- Before showing SnappPay option, call eligibility endpoint with current amount
- Only show SnappPay if `eligible: true`
- Re-check on every amount change (discount, quantity change)

### Step 3: Payment Flow

```
Select SnappPay → Check eligibility → Create payment token → Redirect to paymentPageUrl
    → User completes payment → Callback received → Verify → Settle → Done
```

### Step 4: Callback Handling

- Receive POST callback with `transactionId`, `state`, `amount`
- Call verify with `paymentToken` (saved from step 3)
- If verify succeeds → call settle → finalize order
- If verify fails/times out → use Get Payment Status for reconciliation

### Step 5: Error Recovery

- Implement retry logic for retryable errors (2 attempts, 250ms delay)
- Log terminal errors with user-friendly messages
- Flag manual_review errors for admin dashboard
- Admin tooling for retry/settle/revert/cancel

### Step 6: Post-Payment Operations

- Implement cancel (mandatory) for admin refunds after settle
- Implement update (mandatory for multi-item stores)
- Implement status check for reconciliation

---

## 15. Important Implementation Notes

1. **Currency**: All amounts in **Rial (IRR)**. If your system uses Toman, multiply by 10.
2. **Mobile**: Normalize to `+98XXXXXXXXXX` format (12 digits after +98).
3. **transactionId**: Must be unique per purchase. 5-10 digits recommended. If exceeding 10 digits, include at least one letter.
4. **returnURL**: Domain must exactly match the domain registered with SnappPay.
5. **Idempotency**: Verify only once per transaction. If callback fires multiple times, check order status before re-verifying.
6. **Auto-revert**: If verify is not called within the time window, the payment auto-reverts and user is refunded.
7. **Nightly auto-settle**: If verify succeeded but settle wasn't called, SnappPay auto-settles at end of day.
8. **Testing**: Use the Postman collection and PHP/Node.js/C# sample codes for testing. Staging uses a sandbox bank gateway — amounts aren't actually charged.
9. **Staging test cards**: On the sandbox bank page, enter any card number for first field, keep defaults for others, click "Send Anyway" if prompted.
10. **Commission type**: Default `"100"` for single-category merchants. Use contract-specified codes for multi-category.

---

## 16. Sample Code Reference

PHP cURL examples available in `Sample Code/php/`:

- `jwt-php.docx` — Authentication
- `eligible-php.docx` — Eligibility check
- `get-payment-token-php.docx` — Payment token
- `verify-php.docx` — Verify
- `settle-php.docx` — Settle
- `revert-php.docx` — Revert
- `cancel-php.docx` — Cancel
- `status-php.docx` — Status check
- `update-php.docx` — Update order

Equivalent samples also in Node.js, C# (RestSharp), and raw cURL.

**Staging Test Credentials** (from samples):

- username: `bamilo-user1`
- password: `123456789`
- client_id: `bamilo1`
- client_secret: `987654321`
- Mobile test: `+989121111111`
