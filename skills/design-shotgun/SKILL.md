---
name: design-shotgun
version: 1.0.0
description: "Design exploration from gstack: generate 4-6 design mockup variants, open a comparison board, collect feedback, and iterate until you love something."
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - WebSearch
triggers:
  - show me options
  - design variants
  - explore designs
  - mockup variations
  - design exploration
---

# Design Shotgun — Explore Design Variants

"Show me options." You generate multiple design mockup variants, present them for comparison, collect feedback, and iterate. Repeat until the user loves something.

## Step 0: Input

Ask the user:
1. What are you designing? (screen name, page type)
2. What's the product/brand context? (existing DESIGN.md? CEO plan? README?)
3. Any specific direction or preferences? (dark theme, playful, serious, minimalist, etc.)
4. How many variants? (default: 4-6)

```bash
[ -f DESIGN.md ] && echo "DESIGN_MD_FOUND" || echo "NO_DESIGN_MD"
```

If DESIGN.md exists, read it for design tokens.

## Step 1: Generate Variants

Generate 4-6 distinct design variants as HTML mockups. Each variant should be a single self-contained HTML file.

Each variant should have a DIFFERENT design direction:

### Approach A: Layout Divergence
- **V1 — Centered Hero:** Traditional centered layout with large hero, headline, CTA
- **V2 — Asymmetric:** Side-by-side content, bold color blocking, unconventional layout
- **V3 — Card Grid:** Bento-grid layout, multiple content zones, dashboard-like
- **V4 — Editorial:** Text-forward layout, wide measure, generous whitespace, magazine feel
- **V5 — Minimal:** Maximum whitespace, sparse content, focused on one action
- **V6 — Dense:** Information-rich, compact, data-dashboard feel

### Approach B: Aesthetic Divergence
- **V1 — Bold & Modern:** Strong colors, large typography, confident spacing
- **V2 — Soft & Friendly:** Rounded corners, warm colors, approachable feel
- **V3 — Premium & Dark:** Dark mode, muted colors, refined typography, subtle gradients
- **V4 — Technical & Clean:** Monospace touches, grid-heavy, blue/gray palette, developer-friendly
- **V5 — Playful:** Colorful, irregular shapes, illustrated elements, unexpected details
- **V6 — Editorial:** Serif typography, wide layout, magazine-style, high contrast

## Step 2: Write Variant Files

Create each variant as a self-contained HTML file:

```bash
mkdir -p design-variants
```

Each variant file should:
- Be a complete, valid HTML document
- Include inline CSS (no external dependencies)
- Include a visible label (V1, V2, etc.) for identification
- Use realistic placeholder content (not lorem ipsum — real-sounding text)
- Be responsive (mobile + desktop preview within the page)
- Show both light and dark mode (side by side or toggled)
- Demonstrate the full page, not just the hero section

## Step 3: Variant Summary

Create a comparison summary:

```markdown
## Design Variants

### V1 — [Title]
**Layout:** [description]
**Colors:** [palette]
**Typography:** [fonts]
**Vibe:** [one-line description]
**Best for:** [when to choose this]

### V2 — [Title]
...
```

## Step 4: Present & Collect Feedback

Offer to open the comparison board:

```bash
open design-variants/index.html
```

Ask the user structured questions:
1. Which variant(s) resonate? Why?
2. What do you like from each?
3. What would you change?
4. Are there elements from different variants you'd like to combine?

## Step 5: Iterate

Based on feedback:
1. Identify the winning direction
2. Apply changes (combine elements from other variants, adjust based on feedback)
3. Present the refined version
4. Repeat until approved

Track what the user likes/dislikes (taste learning):

```markdown
## Taste Signals
- Approved: [specific elements the user liked]
- Rejected: [specific elements the user rejected]
- Preferences: [patterns emerging]
```

## Step 6: Finalize

When the user approves a direction:

1. Refine the final variant
2. Save to the project:

```bash
cp design-variants/v-final.html index.html
```

3. Update DESIGN.md with the chosen design tokens if they differ from existing:

```bash
# Extract colors, typography, spacing from the approved variant
# Update DESIGN.md with the new tokens
```

4. Summarize what was decided:

```markdown
## Design Decision

**Chosen direction:** [variant title]
**Key decisions:**
- Layout: [description]
- Colors: [palette details]
- Typography: [font choices]
- Key rejected alternatives: [what was tried and rejected, with reasoning]
```
