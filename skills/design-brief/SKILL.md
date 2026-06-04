---
name: design-brief
description: |
  Parse a structured design brief written in I-Lang protocol format into a
  concrete design spec. Eliminates ambiguity from vague requests like
  "make it professional" by requiring explicit dimensions: palette, typography,
  layout, mood, density, and constraints.
triggers:
  - "design brief"
  - "create a design brief"
  - "ilang brief"
  - "structured brief"
od:
  mode: design-system
  platform: desktop
  scenario: planning
  design_system:
    requires: false
    generates: true
    sections: [visual-theme, color-palette, typography, component-stylings, layout, depth-elevation, dos-and-donts, responsive, agent-prompt-guide]
  inputs:
    - name: brief
      type: string
      required: true
      description: "I-Lang formatted design brief or natural language description"
  outputs:
    primary: DESIGN.md
---

# Design Brief Skill

Parse a structured design brief into a concrete DESIGN.md. Agent, follow this workflow exactly.

## Background

The 8 dimensions in this skill are derived from analysis of 71 design systems. Every DESIGN.md resolves at minimum: color palette, accent, typography, display font, layout model, and component style. Mood and density fix the two most common sources of ambiguity in natural language briefs ("make it clean").

## 1. Accept input

The user provides a design brief in one of two formats:

### Option A: I-Lang structured brief

```
[PLAN:@DESIGN|type=saas_landing]
  |palette=navy_and_white|accent=coral
  |typography=inter|display=space_grotesk
  |layout=single_column|max_width=1200px
  |mood=professional_minimal
  |density=spacious|section_gap=96px
  |hero=headline+subhead+cta
  |sections=features,pricing,testimonials,footer
  |exclude=animations,parallax,gradients
  |responsive=mobile_first
```

### Option B: Natural language

If the user provides natural language, convert it to the structured format using the mapping table below.

### Natural language to I-Lang mapping

| Phrase | Dimension | Value |
|--------|-----------|-------|
| "dark mode", "dark theme" | palette | `monochrome_dark` |
| "light", "white background" | palette | `light_clean` |
| "earthy", "warm tones" | palette | `earth_tones` |
| "pop of color", "vibrant" | accent | `electric_blue` or `coral` |
| "subtle accent" | accent | `muted_sage` or `slate` |
| "clean", "minimal", "simple" | mood | `professional_minimal` |
| "playful", "fun", "friendly" | mood | `playful` |
| "bold", "brutalist", "raw" | mood | `brutalist` |
| "editorial", "magazine-like" | mood | `editorial` |
| "spacious", "lots of whitespace" | density | `spacious` |
| "compact", "dense" | density | `compact` |
| "Inter", "system font" | typography | `inter` |
| "serif", "traditional" | typography | `georgia` or `playfair` |
| "monospace", "code-like" | typography | `jetbrains_mono` |
| "single page" | layout | `single_column` |
| "two columns", "sidebar" | layout | `two_column` |
| "mobile first" | responsive | `mobile_first` |

## 2. Validate 8 dimensions

Every brief must resolve these 8 dimensions:

| # | Dimension | Key | Values |
|---|-----------|-----|--------|
| 1 | Color palette | `palette` | navy_and_white, earth_tones, monochrome_dark, light_clean |
| 2 | Accent color | `accent` | coral, electric_blue, emerald, muted_sage |
| 3 | Body typography | `typography` | inter, system_ui, dm_sans, georgia |
| 4 | Display typography | `display` | space_grotesk, clash_display, same_as_body, playfair |
| 5 | Layout model | `layout` | single_column, two_column, asymmetric |
| 6 | Mood | `mood` | professional_minimal, playful, brutalist, editorial |
| 7 | Density | `density` | compact, balanced, spacious |
| 8 | Constraints | `exclude` | animations, gradients, stock_photos, carousel |

### Token resolution

| Symbolic | Concrete |
|----------|----------|
| `palette=navy_and_white` | bg: #0F172A, surface: #1E293B, text: #F8FAFC, secondary: #94A3B8 |
| `palette=monochrome_dark` | bg: #09090B, surface: #18181B, text: #FAFAFA, secondary: #A1A1AA |
| `palette=light_clean` | bg: #FFFFFF, surface: #F8FAFC, text: #0F172A, secondary: #64748B |
| `palette=earth_tones` | bg: #FFFBEB, surface: #FEF3C7, text: #451A03, secondary: #92400E |
| `accent=coral` | accent: #F97316, hover: #EA580C |
| `accent=electric_blue` | accent: #3B82F6, hover: #2563EB |
| `accent=emerald` | accent: #10B981, hover: #059669 |
| `accent=muted_sage` | accent: #84A98C, hover: #6B8F73 |
| `typography=inter` | body: Inter 400, 1rem/1.6 |
| `typography=system_ui` | body: system-ui 400, 1rem/1.6 |
| `display=space_grotesk` | display: Space Grotesk 700, clamp(2rem, 5vw, 3.5rem) |
| `display=playfair` | display: Playfair Display 700, clamp(2rem, 5vw, 3.5rem) |
| `density=spacious` | section spacing: 96px, content padding: 24px/48px |
| `density=balanced` | section spacing: 72px, content padding: 24px/40px |

### Default resolution rules

| Unspecified | Default |
|-------------|---------|
| palette | depends on mood: editorial -> light_clean, brutalist -> monochrome_dark, else -> light_clean |
| accent | dark palette -> coral, light palette -> electric_blue |
| typography | inter |
| display | editorial -> playfair, brutalist -> space_grotesk, else -> same_as_body |
| layout | single_column |
| mood | professional_minimal |
| density | balanced |

## 3. Generate DESIGN.md

Produce a DESIGN.md following the 9-section convention:

### 1. Visual Theme & Atmosphere
Mood, feel, references.

### 2. Color Palette & Roles
Background, Surface, Text primary, Text secondary, Accent, Accent hover — all from resolved tokens.

### 3. Typography Rules
Display, Body, Mono.

### 4. Component Stylings
Buttons, Cards, Inputs shaped by mood.

### 5. Layout Principles
Max width: 1200px. Grid from layout model. Section spacing from density.

### 6. Depth & Elevation
Shadows and borders matching mood.

### 7. Dos and Don'ts
- DO use declared color tokens exclusively.
- DO maintain consistent spacing.
- DO ensure WCAG AA contrast.
- DON'T invent colors outside palette.
- DON'T use more than 2 typefaces.

### 8. Responsive Behavior
Breakpoints: 640/768/1024/1280px. Stack on mobile, grids on desktop.

### 9. Agent Prompt Guide
Rules for downstream agents consuming this DESIGN.md.

## 4. Report defaults

At the end, list any dimensions that were resolved from defaults:
```
Dimensions resolved from defaults:
- display: set to "same_as_body" (rule: mood=professional_minimal -> same_as_body)
- density: set to "balanced" (rule: static fallback)
```
