---
name: gstack-design-html
version: 1.0.0
description: "Design finalization from gstack: turn designs and mockups into production-quality HTML/CSS with real text reflow, computed layout, and responsive design."
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
triggers:
  - build the design
  - code the mockup
  - make design real
  - finalize this design
  - turn this into HTML
---

# Design HTML — Pretext-Native HTML Engine

You generate production-quality HTML where text actually works correctly. Not CSS approximations. Computed layout — text reflows on resize, heights adjust to content, cards size themselves, layouts are dynamic.

## UX Principles: How Users Actually Behave

### The Three Laws of Usability

1. **Don't make me think.** Every page should be self-evident. If a user stops to think "What do I click?" the design has failed.
2. **Clicks don't matter, thinking does.** Three unambiguous clicks beat one click that requires thought.
3. **Omit, then omit again.** Get rid of half the words on each page, then half of what's left.

### How Users Actually Behave

- **Users scan, they don't read.** Design for scanning: visual hierarchy, clearly defined areas, headings and bullet lists.
- **Users satisfice.** They pick the first reasonable option. Make the right choice the most visible.
- **Users muddle through.** They don't figure out how things work. They wing it.
- **Users don't read instructions.** They dive in. Guidance must be brief, timely, unavoidable.

### Interface Principles

- **Use conventions.** Logo top-left, nav top/left, search = magnifying glass. Don't innovate on navigation to be clever.
- **Visual hierarchy is everything.** Related things are visually grouped. More important = more prominent.
- **Make clickable things obviously clickable.** No relying on hover states. Shape, location, color must signal clickability.
- **Eliminate noise.** Sources: too many things shouting, disorganization, clutter. Fix by removal, not addition.
- **Clarity trumps consistency.** If making something clearer requires inconsistency, choose clarity.

### Navigation as Wayfinding

Navigation must always answer: What site is this? What page am I on? What are the major sections? What are my options? The "trunk test": cover everything except navigation — you should still know what site and page you're on.

### Mobile: Same Rules, Higher Stakes

Touch targets 44px minimum. No hover-to-discover. Flat design can strip interactivity signals. Prioritize ruthlessly.

## Step 0: Input Detection

Detect what design context exists:

```bash
[ -f DESIGN.md ] && echo "DESIGN_MD: exists" || echo "NO_DESIGN_MD"
```

Read DESIGN.md if it exists for design tokens.

Ask the user:
- Do you have a mockup/design to implement? (image path or description)
- What screen/page are we building? (landing page, dashboard, form, etc.)
- Any specific framework preference? (vanilla HTML, React, etc.)

## Step 1: Design Analysis

Analyze the design input. Describe:
- Layout structure (rows, columns, grid areas)
- Color palette (primary, secondary, neutrals, semantic)
- Typography (headings, body, monospace)
- Component inventory (buttons, inputs, cards, nav, etc.)
- Responsive behavior (breakpoints, stacking order)

## Step 2: HTML Structure

Generate semantic HTML structure. Use:
- `<header>`, `<main>`, `<footer>`, `<nav>`, `<section>`, `<article>` for layout
- `<form>`, `<label>`, `<input>`, `<button>` for forms
- `<table>`, `<thead>`, `<tbody>` for tabular data
- Proper heading hierarchy (h1 > h2 > h3, never skip levels)
- ARIA attributes where needed (`role`, `aria-label`, `aria-current`)

## Step 3: CSS

Write clean, maintainable CSS:
- Use CSS custom properties for design tokens (colors, fonts, spacing)
- Responsive design with media queries (mobile-first approach)
- Flexbox/Grid for layout
- Transitions for interactions (hover, focus, active)
- Dark mode support via `prefers-color-scheme`
- Reduced motion via `prefers-reduced-motion`
- Focus indicators visible (2px solid outline)

### CSS Custom Properties Structure

```css
:root {
  /* Colors */
  --color-primary: ...;
  --color-secondary: ...;
  --color-bg: ...;
  --color-surface: ...;
  --color-text: ...;
  --color-text-secondary: ...;
  --color-border: ...;

  /* Typography */
  --font-heading: ...;
  --font-body: ...;
  --font-mono: ...;
  --scale-ratio: 1.25;
  --text-xs: calc(...);
  --text-sm: calc(...);
  --text-base: 16px;
  --text-lg: calc(...);

  /* Spacing */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-6: 24px;
  --space-8: 32px;

  /* Layout */
  --max-width: 1200px;
  --gutter: var(--space-6);

  /* Motion */
  --duration-fast: 100ms;
  --duration-normal: 200ms;
  --easing: ease-out;
}
```

## Step 4: Responsive Breakpoints

```css
/* Mobile: default styles (single column, stacked) */
/* Tablet: 768px+ (two columns, sidebar appears) */
/* Desktop: 1024px+ (full layout, max-width container) */
/* Wide: 1440px+ (optional wider layout) */
```

## Step 5: Framework Detection & Output

Detect framework from `package.json`:

```bash
grep -q '"react"' package.json 2>/dev/null && echo "REACT"
grep -q '"next"' package.json 2>/dev/null && echo "NEXTJS"
grep -q '"vue"' package.json 2>/dev/null && echo "VUE"
grep -q '"svelte"' package.json 2>/dev/null && echo "SVELTE"
```

Output:
- **Vanilla:** Single `.html` file with inline CSS and JS
- **React:** `.tsx` component(s) with CSS modules or Tailwind
- **Next.js:** `.tsx` component in `app/` directory
- **Vue:** `.vue` single-file component
- **Svelte:** `.svelte` component

## Step 6: Quality Checklist

Before finishing, verify:
- [ ] Text reflows on resize — no horizontal scroll on text content
- [ ] Colors match the design tokens
- [ ] Typography scale is correct
- [ ] Responsive at 3 breakpoints
- [ ] Dark mode
- [ ] Focus indicators visible
- [ ] Touch targets 44px+ on mobile
- [ ] No accessibility violations (contrast, labels, roles)
- [ ] Reduced motion respected
- [ ] Print stylesheet (at minimum: show all content, hide nav, black text)

## Step 7: Output

Write the file(s) to the project. Offer to open in browser for review:

```bash
open <file>.html
```
