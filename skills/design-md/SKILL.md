---
name: design-md
description: |
  Collection of 70+ DESIGN.md files from popular brand design systems. Drop one into your project and let AI agents generate a matching UI. Bundled top 20 locally; all 74+ available via fetch.
triggers:
  - "design system"
  - "DESIGN.md"
  - "design md"
  - "google stitch"
  - "vercel design"
  - "apple design"
  - "stripe design"
  - "figma design"
  - "spotify design"
  - "airbnb design"
  - "notion design"
  - "nike design"
  - "shopify design"
  - "uber design"
  - "tesla design"
  - "ibm design"
  - "linear design"
  - "supabase design"
  - "coinbase design"
  - "claude design"
  - "raycast design"
  - "cursor design"
  - "intercom design"
  - "sentry design"
  - "vercel style"
  - "apple style"
  - "stripe style"
  - "figma style"
  - "spotify style"
---

# Design MD Skill

Provides access to DESIGN.md files from 70+ popular brand design systems. DESIGN.md is a plain-text design system document (introduced by Google Stitch) that AI agents read to generate consistent UI. It defines colors, typography, components, layout, depth, and design rules.

## How to Use

When the user asks to use a specific brand's design system (e.g. "use Vercel design", "build this like Apple", "apply Stripe's style"):

### 1. Identify the brand slug

Match the user's request to the slug from the catalog below. Slugs are directory names.

### 2. Get the DESIGN.md

- **Bundled brands** (top 20): Read the file directly from `brands/{slug}/DESIGN.md` relative to this skill's directory.
- **All other brands**: Use `webfetch` to fetch from:
  `https://raw.githubusercontent.com/voltagent/awesome-design-md/main/design-md/{slug}/DESIGN.md`

### 3. Write DESIGN.md to project root

Write the fetched/read content to `./DESIGN.md` in the user's project root.

### 4. Read and apply

Read `./DESIGN.md` to understand the full design system, then build whatever the user requested (landing page, component, dashboard, etc.) using the design tokens specified in the file — colors, typography hierarchy, component stylings, spacing, elevation, and do's/don'ts.

## Complete Brand Catalog

### AI & LLM Platforms

| Slug | Brand | Description |
|------|-------|-------------|
| `claude` | Claude | Anthropic's AI assistant. Warm terracotta accent, clean editorial layout |
| `cohere` | Cohere | Enterprise AI platform. Vibrant gradients, data-rich dashboard aesthetic |
| `elevenlabs` | ElevenLabs | AI voice platform. Dark cinematic UI, audio-waveform aesthetics |
| `minimax` | Minimax | AI model provider. Bold dark interface with neon accents |
| `mistral.ai` | Mistral AI | Open-weight LLM provider. French-engineered minimalism, purple-toned |
| `ollama` | Ollama | Run LLMs locally. Terminal-first, monochrome simplicity |
| `opencode.ai` | OpenCode AI | AI coding platform. Developer-centric dark theme |
| `replicate` | Replicate | Run ML models via API. Clean white canvas, code-forward |
| `runwayml` | Runway | AI creative-tools. Cinematic dark heroes, paper-white bands |
| `together.ai` | Together AI | Open-source AI infrastructure. Technical, blueprint-style |
| `voltagent` | VoltAgent | AI agent framework. Void-black canvas, emerald accent |
| `x.ai` | xAI | Elon Musk's AI lab. Stark monochrome, futuristic minimalism |

### Developer Tools & IDEs

| Slug | Brand | Description |
|------|-------|-------------|
| `cursor` | Cursor | AI-first code editor. Sleek dark interface, gradient accents |
| `expo` | Expo | React Native platform. Dark theme, tight letter-spacing, code-centric |
| `lovable` | Lovable | AI full-stack builder. Playful gradients, friendly dev aesthetic |
| `raycast` | Raycast | Productivity launcher. Sleek dark chrome, vibrant gradient accents |
| `superhuman` | Superhuman | Fast email client. Premium dark UI, keyboard-first, purple glow |
| `vercel` | Vercel | Frontend deployment. Black and white precision, Geist font |
| `warp` | Warp | Modern terminal. Dark IDE-like interface, block-based command UI |

### Backend, Database & DevOps

| Slug | Brand | Description |
|------|-------|-------------|
| `clickhouse` | ClickHouse | Fast analytics database. Yellow-accented, technical docs |
| `composio` | Composio | Tool integration platform. Modern dark, colorful icons |
| `hashicorp` | HashiCorp | Infrastructure automation. Enterprise-clean, black and white |
| `mongodb` | MongoDB | Document database. Green leaf branding, developer docs |
| `posthog` | PostHog | Product analytics. Playful hedgehog, developer-friendly dark UI |
| `sanity` | Sanity | Headless CMS. Dark-first editorial, 112px display type, coral CTA |
| `sentry` | Sentry | Error monitoring. Dark dashboard, data-dense, pink-purple accent |
| `supabase` | Supabase | Open-source Firebase alternative. Dark emerald, code-first |

### Productivity & SaaS

| Slug | Brand | Description |
|------|-------|-------------|
| `cal` | Cal.com | Open-source scheduling. Clean neutral UI, developer-oriented |
| `intercom` | Intercom | Customer messaging. Friendly blue, conversational UI patterns |
| `linear.app` | Linear | Project management. Ultra-minimal, precise, purple accent |
| `mintlify` | Mintlify | Documentation platform. Clean, green-accented, reading-optimized |
| `notion` | Notion | All-in-one workspace. Warm minimalism, serif headings, soft surfaces |
| `resend` | Resend | Email API for developers. Minimal dark theme, monospace accents |
| `zapier` | Zapier | Automation platform. Warm orange, friendly illustration-driven |

### Design & Creative Tools

| Slug | Brand | Description |
|------|-------|-------------|
| `airtable` | Airtable | Spreadsheet-database hybrid. Colorful, friendly, structured data |
| `clay` | Clay | Creative agency. Organic shapes, soft gradients, art-directed |
| `figma` | Figma | Collaborative design tool. Vibrant multi-color, playful yet professional |
| `framer` | Framer | Website builder. Bold black and blue, motion-first, design-forward |
| `miro` | Miro | Visual collaboration. Bright yellow accent, infinite canvas aesthetic |
| `webflow` | Webflow | Visual web builder. Blue-accented, polished marketing site |

### Fintech & Crypto

| Slug | Brand | Description |
|------|-------|-------------|
| `binance` | Binance | Crypto exchange. Bold Binance Yellow on monochrome, trading-floor |
| `coinbase` | Coinbase | Crypto exchange. Clean blue identity, trust-focused, institutional |
| `kraken` | Kraken | Crypto trading. Purple-accented dark UI, data-dense dashboards |
| `mastercard` | Mastercard | Global payments. Warm cream canvas, orbital pill shapes |
| `revolut` | Revolut | Digital banking. Sleek dark interface, gradient cards |
| `stripe` | Stripe | Payment infrastructure. Signature purple gradients, weight-300 |
| `wise` | Wise | International money transfer. Bright green accent, friendly |

### E-commerce & Retail

| Slug | Brand | Description |
|------|-------|-------------|
| `airbnb` | Airbnb | Travel marketplace. Warm coral accent, photography-driven, rounded UI |
| `meta` | Meta | Tech retail store. Photography-first, Meta Blue CTAs |
| `nike` | Nike | Athletic retail. Monochrome UI, massive uppercase Futura |
| `shopify` | Shopify | E-commerce platform. Dark-first cinematic, neon green accent |
| `starbucks` | Starbucks | Coffee flagship. Four-tier earth-green system, warm cream canvas |

### Media & Consumer Tech

| Slug | Brand | Description |
|------|-------|-------------|
| `apple` | Apple | Consumer electronics. Premium white space, SF Pro, cinematic |
| `hp` | HP | PC and printer maker. White canvas, HP Electric Blue CTA |
| `ibm` | IBM | Enterprise technology. Carbon design system, structured blue |
| `nvidia` | NVIDIA | GPU computing. Green-black energy, technical power aesthetic |
| `pinterest` | Pinterest | Visual discovery. Red accent, masonry grid, image-first |
| `playstation` | PlayStation | Gaming console. Three-surface channel layout, cyan hover-scale |
| `slack` | Slack | Team communication. Purple accent, friendly, collaborative |
| `spacex` | SpaceX | Space technology. Stark black and white, full-bleed imagery |
| `spotify` | Spotify | Music streaming. Vibrant green on dark, bold type |
| `theverge` | The Verge | Tech editorial. Acid-mint and ultraviolet, Manuka display |
| `uber` | Uber | Mobility platform. Bold black and white, tight type, urban |
| `vodafone` | Vodafone | Global telecom. Monumental uppercase display, Vodafone Red |
| `wired` | WIRED | Tech magazine. Paper-white broadsheet, custom serif |

### Automotive

| Slug | Brand | Description |
|------|-------|-------------|
| `bmw` | BMW | Luxury automotive. Dark premium surfaces, German engineering |
| `bmw-m` | BMW M | Performance automotive. Motorsport-inspired contrast |
| `bugatti` | Bugatti | Luxury hypercar. Cinema-black canvas, monochrome austerity |
| `ferrari` | Ferrari | Luxury automotive. Chiaroscuro black-white, Ferrari Red |
| `lamborghini` | Lamborghini | Luxury automotive. True black cathedral, gold accent |
| `renault` | Renault | French automotive. Vivid aurora gradients, NouvelR typeface |
| `tesla` | Tesla | Electric vehicles. Radical subtraction, cinematic photography |

### Retro Web Nostalgia

| Slug | Brand | Description |
|------|-------|-------------|
| `dell-1996` | Dell (1996) | Catalog-era web. Black page frame, color-block cards, GIF stickers |
| `nintendo-2001` | Nintendo (2001) | Y2K console chrome. Brushed metal panels, amber glow nav |

## Bundled Brands

The following 20 brands have their DESIGN.md bundled locally (no network needed):

vercel, apple, stripe, figma, spotify, airbnb, nike, notion, shopify, uber, tesla, ibm, linear.app, supabase, coinbase, claude, raycast, cursor, intercom, sentry

All other brands in the catalog above use `webfetch` from the GitHub raw URL.

## Auto-Apply Instructions

After writing DESIGN.md to the project:

1. Read the DESIGN.md file thoroughly
2. Extract the key design tokens: color palette, typography scale, component stylings, spacing, elevation, and layout principles
3. Apply them when generating any UI for the user — whether it's a landing page, a component, a dashboard, or a full site
4. Follow the Do's and Don'ts section of the DESIGN.md strictly
5. If the task is to build something specific, use the design tokens to inform every visual decision: colors for backgrounds/text/accents, font choices and sizes from the typography hierarchy, component shapes from the component stylings section, and spacing from the spacing scale

## What Each DESIGN.md Contains

Every file follows the Google Stitch DESIGN.md format with these sections:

| Section | What it captures |
|---------|-----------------|
| Visual Theme & Atmosphere | Mood, density, design philosophy |
| Color Palette & Roles | Semantic name + hex + functional role |
| Typography Rules | Font families, full hierarchy table |
| Component Stylings | Buttons, cards, inputs, navigation with states |
| Layout Principles | Spacing scale, grid, whitespace philosophy |
| Depth & Elevation | Shadow system, surface hierarchy |
| Do's and Don'ts | Design guardrails and anti-patterns |
| Responsive Behavior | Breakpoints, touch targets, collapsing strategy |
