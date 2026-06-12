<div align="center">
  <h1>
    <img src="https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/opensourceinitiative.svg" width="0" />
    ⚡ opencode‑skills
  </h1>
  <p><strong>The Ultimate Agent Skill Hub</strong> — <em>256 skills · 13 shared packages · 6 apps · 150+ design systems · full CI/CD</em></p>
  <p>A curated, batteries‑included collection of agent skills, automations, design systems, plugins, and full‑stack tooling for <a href="https://opencode.ai"><b>OpenCode</b></a> — now supercharged by the <a href="README-OPEN-DESIGN.md">Open Design</a> monorepo.</p>
</div>

<p align="center">
  <a href="#-quick-start"><img src="https://img.shields.io/badge/install-3_commands-blueviolet?style=for-the-badge" alt="install" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache_2.0-blue.svg?style=for-the-badge" alt="license" /></a>
  <a href="https://github.com/hosseinmirzapur/opencode-skills"><img src="https://img.shields.io/github/stars/hosseinmirzapur/opencode-skills?style=for-the-badge&logo=github&color=gold" alt="stars" /></a>
  <a href="CHANGELOG.md"><img src="https://img.shields.io/badge/changelog-keep_a_changelog-teal?style=for-the-badge" alt="changelog" /></a>
  <a href="TRANSLATIONS.md"><img src="https://img.shields.io/badge/i18n-18_languages-forestgreen?style=for-the-badge" alt="i18n" /></a>
  <br>
  <a href="AGENTS.md"><img src="https://img.shields.io/badge/agents-2_defined-6a0dad?style=flat-square" alt="agents" /></a>
  <a href="skills/"><img src="https://img.shields.io/badge/skills-256-ff69b4?style=flat-square" alt="skills" /></a>
  <a href="plugins/"><img src="https://img.shields.io/badge/plugins-200+-orange?style=flat-square" alt="plugins" /></a>
  <a href="design-systems/"><img src="https://img.shields.io/badge/design_systems-150+-brightgreen?style=flat-square" alt="design-systems" /></a>
  <a href="apps"><img src="https://img.shields.io/badge/apps-6-1e90ff?style=flat-square" alt="apps" /></a>
  <a href="packages"><img src="https://img.shields.io/badge/packages-13-32CD32?style=flat-square" alt="packages" /></a>
  <a href="docs/"><img src="https://img.shields.io/badge/docs-translated_7_languages-8A2BE2?style=flat-square" alt="docs" /></a>
</p>

<br>

---

## 🗺️ At a Glance

This repo started as a lightweight skill collection for OpenCode and grew into a **full‑spectrum agent‑native studio** — combining battle‑tested marketing, dev, and design skills with the entire [Open Design](README-OPEN-DESIGN.md) monorepo (apps, packages, CI/CD, design systems, 150+ brand guides, plugin ecosystem, end‑to‑end tests, and everything in between).

| Layer | What's Here | Path |
|-------|-------------|------|
| 🤖 **Skills** | 256 ready‑to‑inject agent skills | [`skills/`](skills/) |
| 🧩 **Plugins** | Full plugin ecosystem (official, community, registry, spec) | [`plugins/`](plugins/) |
| ⚙️ **Automations** | 42 TypeScript + Python build/release scripts | [`scripts/`](scripts/) |
| 🏗️ **Apps** | 6 apps — daemon, web (Next.js 16), desktop (Electron), packaged, landing, telemetry worker | [`apps/`](apps/) |
| 📦 **Packages** | 13 shared TypeScript packages (contracts, sidecar, platform, components, runtime…) | [`packages/`](packages/) |
| 🛠️ **Tools** | 3 CLI tools — dev lifecycle, packaged build/serve, fixture service | [`tools/`](tools/) |
| 🎨 **Design Systems** | 150+ brand‑grade `DESIGN.md` guides w/ tokens, components, Tailwind configs | [`design-systems/`](design-systems/) |
| 📐 **Design Templates** | 111 rendering templates (decks, prototypes, video, audio) | [`design-templates/`](design-templates/) |
| 📝 **Craft Rules** | Universal brand‑agnostic craft (a11y, color, typography, animation) | [`craft/`](craft/) |
| 🧪 **E2E Tests** | Playwright + Vitest suites, visual regression, mock CLIs | [`e2e/`](e2e/), [`mocks/`](mocks/) |
| 🌐 **Docs** | Full documentation in 7 translated languages | [`docs/`](docs/) |
| 🚀 **Deploy** | Docker, AWS SAM, Azure bicep, Helm chart, Nix packaging | [`deploy/`](deploy/), [`nix/`](nix/), [`charts/`](charts/) |
| 📋 **Specs** | Architecture specs, RFCs, change documents | [`specs/`](specs/) |

<br>

---

## ⚡ Quick Start

```bash
# One‑line install (bootstraps + launches the wizard):
curl -fsSL https://raw.githubusercontent.com/hosseinmirzapur/opencode-skills/main/scripts/setup.py | python3

# Or clone manually:
git clone https://github.com/hosseinmirzapur/opencode-skills.git
cd opencode-skills
python3 scripts/setup.py

# After install, use the `osk` CLI:
osk                    # Full‑screen interactive TUI dashboard
osk status             # Check installation status
osk install all        # Install everything
osk install graphify   # Install graphify only
osk doctor             # Diagnose your setup
osk --help             # Show all commands
```

The installer will:
- 📦 Install the **`osk` CLI** — your command center for everything in this repo
- 🔗 Install [graphify](https://graphifylabs.ai) — queryable code knowledge graph with **71.5× token reduction**
- 📥 Sync all **256 skills**, agents, and plugins into your OpenCode config
- 🔑 Prompt for API provider configuration
- 🧠 Register graphify with OpenCode

<br>

---

## 🧩 Skills Ecosystem

<details>
<summary><b>📢 Marketing & Growth</b> — <i>ads, SEO, CRO, email, social, content, analytics</i></summary>

| Skill | What It Does |
|-------|-------------|
| [`ab-testing`](skills/ab-testing) | Plan, design, implement A/B tests and experimentation programs |
| [`ad-creative`](skills/ad-creative) | Generate/iterate/scale ad creative for any paid platform |
| [`ads`](skills/ads) | Campaign strategy for Google Ads, Meta, LinkedIn, Twitter/X |
| [`ai-seo`](skills/ai-seo) | Optimize content for AI search engines & LLM citations |
| [`analytics`](skills/analytics) | Set up, audit, and improve analytics tracking and measurement |
| [`aso`](skills/aso) | Audit and optimize App Store / Google Play listings |
| [`churn-prevention`](skills/churn-prevention) | Reduce churn, build cancel flows, save offers, dunning |
| [`cold-email`](skills/cold-email) | B2B cold emails & follow‑up sequences that get replies |
| [`content-strategy`](skills/content-strategy) | Plan content strategy, topic clusters, editorial calendar |
| [`copy-editing`](skills/copy-editing) | Edit, review, and refresh existing marketing copy |
| [`copywriting`](skills/copywriting) | Write persuasive copy for any page — homepage to pricing |
| [`cro`](skills/cro) | Optimize conversions on marketing pages and forms |
| [`customer-research`](skills/customer-research) | Synthesize research, build personas, JTBD, review mining |
| [`directory-submissions`](skills/directory-submissions) | Submit to startup, SaaS, AI, and review directories |
| [`emails`](skills/emails) | Drip campaigns, lifecycle emails, onboarding sequences |
| [`lead-magnets`](skills/lead-magnets) | Create and optimize lead magnets for email capture |
| [`marketing-ideas`](skills/marketing-ideas) | Brainstorm marketing ideas and growth strategies |
| [`marketing-plan`](skills/marketing-plan) | Build AARRR‑structured comprehensive marketing plans |
| [`marketing-psychology`](skills/marketing-psychology) | Apply 50+ psychological models to marketing |
| [`popups`](skills/popups) | Optimize exit‑intent popups, modals, slide‑ins, banners |
| [`pricing`](skills/pricing) | Pricing strategy, packaging, monetization decisions |
| [`product-marketing`](skills/product-marketing) | Positioning, ICP definition, product context docs |
| [`programmatic-seo`](skills/programmatic-seo) | Build SEO‑driven pages at scale with templates |
| [`seo`](skills/seo) | General search engine visibility and ranking |
| [`seo-audit`](skills/seo-audit) | Diagnose technical SEO, Core Web Vitals, ranking issues |
| [`signup`](skills/signup) | Optimize registration, trial activation flows |
| [`sms`](skills/sms) | SMS/MMS marketing campaigns and flows |
| [`social`](skills/social) | Create & schedule content for LinkedIn, X, IG, TikTok |
</details>

<details>
<summary><b>🎨 Design & Creative</b> — <i>frontend, UI/UX, branding, figma, design systems</i></summary>

| Skill | What It Does |
|-------|-------------|
| [`creative-director`](skills/creative-director) | AI creative director — 20+ methodologies, 3‑axis evaluation |
| [`design-brief`](skills/design-brief) | Parse I‑Lang briefs into concrete DESIGN.md specs |
| [`design-shotgun`](skills/design-shotgun) | Generate 4–6 mockup variants and iterate on feedback |
| [`design-consultation`](skills/design-consultation) | Create complete design systems and DESIGN.md docs |
| [`design-md`](skills/design-md) | Collection of 70+ DESIGN.md files from popular brand design systems (awesome-design-md) |
| [`design-review`](skills/design-review) | Systematic design review and critique |
| [`figma`](skills/figma) | Fetch Figma context, screenshots, variables, assets |
| [`figma-use`](skills/figma-use) | Translate Figma nodes into production code |
| [`frontend-design`](skills/frontend-design) | Production‑grade frontend UI with HTML/CSS/JS |
| [`frontend-dev`](skills/frontend-dev) | Full frontend development workflow |
| [`frontend-skill`](skills/frontend-skill) | Frontend implementation skill |
| [`gstack-design-consultation`](skills/gstack-design-consultation) | GStack‑style design system creation |
| [`gstack-design-html`](skills/gstack-design-html) | Turn designs into production HTML/CSS |
| [`impeccable-design-polish`](skills/impeccable-design-polish) | Audit, critique, polish, animate, harden web pages |
| [`plan-design-review`](skills/plan-design-review) | 10‑dimension scoring design review (Garry Tan's gstack) |
| [`ui-ux-pro-max`](skills/ui-ux-pro-max) | 50+ styles, 161 palettes, 57 font pairings, 99 UX guidelines |
| [`web-design-guidelines`](skills/web-design-guidelines) | Web design standards and best practices |
</details>

<details>
<summary><b>⚛️ GSAP Animation</b> — <i>complete GSAP ecosystem skills</i></summary>

| Skill | What It Does |
|-------|-------------|
| [`gsap-core`](skills/gsap-core) | Core API — to(), from(), fromTo(), easing, stagger, matchMedia |
| [`gsap-react`](skills/gsap-react) | useGSAP hook, refs, context, cleanup in React/Next.js |
| [`gsap-frameworks`](skills/gsap-frameworks) | GSAP integration with various frameworks |
| [`gsap-performance`](skills/gsap-performance) | GSAP performance optimization |
| [`gsap-plugins`](skills/gsap-plugins) | GSAP plugin usage and configuration |
| [`gsap-scrolltrigger`](skills/gsap-scrolltrigger) | Scroll‑driven animations with ScrollTrigger |
| [`gsap-timeline`](skills/gsap-timeline) | Complex timeline sequencing |
| [`gsap-utils`](skills/gsap-utils) | GSAP utility methods and helpers |
</details>

<details>
<summary><b>🐍 Solana & Web3</b> — <i>Helius, SVM, Jupiter, DFlow, Phantom</i></summary>

| Skill | What It Does |
|-------|-------------|
| [`helius`](skills/helius) | Build Solana apps with Helius infrastructure |
| [`helius-dflow`](skills/helius-dflow) | Solana trading with DFlow + Helius |
| [`helius-jupiter`](skills/helius-jupiter) | Solana DeFi with Jupiter + Helius |
| [`helius-okx`](skills/helius-okx) | Solana trading with OKX DEX + Helius |
| [`helius-phantom`](skills/helius-phantom) | Frontend Solana with Phantom SDK + Helius |
| [`svm`](skills/svm) | Solana VM internals, account model, consensus |
</details>

<details>
<summary><b>🖼️ Image & Video</b> — <i>generation, editing, templates</i></summary>

| Skill | What It Does |
|-------|-------------|
| [`image`](skills/image) | Create, edit, optimize marketing images |
| [`imagegen`](skills/imagegen) | AI image generation workflows |
| [`fal-generate`](skills/fal-generate) | FAL.ai image generation |
| [`fal-image-edit`](skills/fal-image-edit) | FAL.ai image editing |
| [`fal-video-edit`](skills/fal-video-edit) | FAL.ai video editing |
| [`sora`](skills/sora) | OpenAI Sora video generation |
| [`remotion`](skills/remotion) | Programmatic video with Remotion |
| [`video-hyperframes`](skills/video-hyperframes) | HyperFrames motion graphics |
| [`video-downloader`](skills/video-downloader) | Video downloading utility |
</details>

<details>
<summary><b>📄 Documents & PDF</b> — <i>resumes, cover letters, PDF processing</i></summary>

| Skill | What It Does |
|-------|-------------|
| [`pdf`](skills/pdf) | Read, merge, split, create, OCR PDF files |
| [`docx`](skills/docx) | Generate DOCX documents |
| [`pptx`](skills/pptx) | PowerPoint presentation generation |
| [`pptx-generator`](skills/pptx-generator) | Bulk PPTX generation |
| [`resume-bullet-writer`](skills/resume-bullet-writer) | Achievement‑focused resume bullets |
| [`resume-tailor`](skills/resume-tailor) | Customize resumes for specific job postings |
| [`cover-letter-generator`](skills/cover-letter-generator) | Personalized cover letters |
| And **10 more resume skills** in [`skills/`](skills/) |

</details>

<details>
<summary><b>🧰 Developer & Framework</b> — <i>Next.js, Redis, code review, prompt engineering</i></summary>

| Skill | What It Does |
|-------|-------------|
| [`best-practices`](skills/best-practices) | Web security, compatibility, code quality |
| [`evaluation`](skills/evaluation) | Agent eval systems, rubrics, quality gates |
| [`graphify`](skills/graphify) | Code knowledge graph — 71.5× token reduction |
| [`next-best-practices`](skills/next-best-practices) | Next.js 16 conventions, RSC, data patterns |
| [`next-cache-components`](skills/next-cache-components) | PPR, cacheLife, cacheTag, updateTag |
| [`next-upgrade`](skills/next-upgrade) | Upgrade Next.js via official codemods |
| [`prompt-engineering`](skills/prompt-engineering) | Optimize prompts for LLM interactions |
| [`redis-core`](skills/redis-core) | Redis data structures, key naming, caching |
| [`redis-query-engine`](skills/redis-query-engine) | FT.CREATE, FT.SEARCH, index design |
| [`review`](skills/review) | Staff‑engineer level code review |
| [`shadcn-ui`](skills/shadcn-ui) | shadcn/ui component usage |
| [`threejs`](skills/threejs) | Three.js 3D graphics |
</details>

<details>
<summary><b>🧑‍💼 Sales & Revenue</b> — <i>prospecting, sales enablement, revops</i></summary>

| Skill | What It Does |
|-------|-------------|
| [`competitor-profiling`](skills/competitor-profiling) | Research/profile competitors from URLs |
| [`competitors`](skills/competitors) | Create competitor comparison & alternative pages |
| [`launch`](skills/launch) | Product launch planning, PH, GTM strategy |
| [`onboarding`](skills/onboarding) | Post‑signup activation and time‑to‑value |
| [`paywalls`](skills/paywalls) | In‑product paywalls, upgrade screens, feature gates |
| [`prospecting`](skills/prospecting) | Find, qualify, build prospect lists |
| [`referrals`](skills/referrals) | Referral & affiliate programs, viral loops |
| [`revops`](skills/revops) | Revenue operations, lead scoring, pipeline |
| [`sales-enablement`](skills/sales-enablement) | Pitch decks, one‑pagers, objection handling |
| [`co-marketing`](skills/co-marketing) | Co‑marketing partnerships, joint campaigns |
| [`community-marketing`](skills/community-marketing) | Discord/Slack community strategy, CLG |
| [`schema`](skills/schema) | Schema markup, JSON‑LD, rich snippets |
</details>

<details>
<summary><b>🎯 Framework Skills</b> — <i>Laravel, SwiftUI, Flutter</i></summary>

| Skill | What It Does |
|-------|-------------|
| [`laravel-cloud-deploy`](skills/laravel-cloud-deploy) | Deploy/manage Laravel on Laravel Cloud |
| [`laravel-nightwatch`](skills/laravel-nightwatch) | Configure Nightwatch data collection |
| [`laravel-starter-kit-upgrade`](skills/laravel-starter-kit-upgrade) | Pull starter kit improvements upstream |
| [`swiftui-design`](skills/swiftui-design) | SwiftUI interface design |
| [`flutter-animating-apps`](skills/flutter-animating-apps) | Flutter animation |
</details>

<details>
<summary><b>🎬 Creative Templates</b> — <i>decks, cards, editorial, brand, video</i></summary>

| Skill | What It Does |
|-------|-------------|
| [`article-magazine`](skills/article-magazine) | Magazine‑style article layouts |
| [`brand-guidelines`](skills/brand-guidelines) | Brand guideline document creation |
| [`canvas-design`](skills/canvas-design) | Canvas‑based design layouts |
| [`card-twitter`](skills/card-twitter) | Twitter/X card designs |
| [`card-xiaohongshu`](skills/card-xiaohongshu) | Xiaohongshu (RED) card designs |
| [`color-expert`](skills/color-expert) | Color palette expertise |
| [`d3-visualization`](skills/d3-visualization) | D3.js data visualization |
| [`data-report`](skills/data-report) | Data report layouts |
| [`deck-*`](skills/deck-guizang-editorial) | Multiple deck templates (guizang, open‑slide, swiss) |
| [`domain-name-brainstormer`](skills/domain-name-brainstormer) | Domain name ideation |
| [`faq-page`](skills/faq-page) | FAQ page layouts |
| [`hand-drawn-diagrams`](skills/hand-drawn-diagrams) | Hand‑drawn style diagrams |
| [`theme-factory`](skills/theme-factory) | Theme generation |
| And **40+ more** creative and media skills in [`skills/`](skills/) |

</details>

<details>
<summary><b>🔌 Figma Integrations</b> — <i>7 dedicated Figma skills</i></summary>

| Skill | What It Does |
|-------|-------------|
| [`figma`](skills/figma) | Fetch design context, screenshots, assets |
| [`figma-use`](skills/figma-use) | Translate Figma nodes → production code |
| [`figma-code-connect-components`](skills/figma-code-connect-components) | Wire components to code |
| [`figma-create-design-system-rules`](skills/figma-create-design-system-rules) | DS rules from Figma |
| [`figma-create-new-file`](skills/figma-create-new-file) | Create Figma files |
| [`figma-generate-design`](skills/figma-generate-design) | Generate designs from Figma |
| [`figma-generate-library`](skills/figma-generate-library) | Generate design libraries |
| [`figma-implement-design`](skills/figma-implement-design) | Implement Figma designs |
</details>

<details>
<summary><b>🤝 Agent & Workflow</b> — <i>meta skills, prompts, agents</i></summary>

| Skill | What It Does |
|-------|-------------|
| [`agent-browser`](skills/agent-browser) | Browser agent control |
| [`brainstorming`](skills/brainstorming) | Structured brainstorming |
| [`enhance-prompt`](skills/enhance-prompt) | Prompt enhancement |
| [`output-skill`](skills/output-skill) | Standardized output formatting |
| [`soft-skill`](skills/soft-skill) | Soft skills training |
| [`using-superpowers`](skills/using-superpowers) | Agent skill discovery protocol |
| [`gpt-tasteskill`](skills/gpt-tasteskill) | Taste‑based GPT prompting |
| [`taste-skill`](skills/taste-skill) | Design taste skill |
| [`reference-design-contract`](skills/reference-design-contract) | Design contract management |
| [`iran-skill`](skills/iran-skill) | Geopolitical intelligence OS — Iran, Middle East, strategic analysis |
| [`receiving-code-review`](skills/receiving-code-review) | Process code review feedback with verification |
| [`requesting-code-review`](skills/requesting-code-review) | Request code review before merging |
| [`subagent-driven-development`](skills/subagent-driven-development) | Drive development through subagents |
| [`systematic-debugging`](skills/systematic-debugging) | Systematic bug investigation before fixes |
| [`test-driven-development`](skills/test-driven-development) | TDD workflow before implementation |
| [`using-git-worktrees`](skills/using-git-worktrees) | Isolated workspace via git worktrees |
| [`verification-before-completion`](skills/verification-before-completion) | Verify before claiming completion |
| [`writing-plans`](skills/writing-plans) | Write multi-step implementation plans |
| [`writing-skills`](skills/writing-skills) | Create and test agent skills |
| [`dispatching-parallel-agents`](skills/dispatching-parallel-agents) | Dispatch parallel agents for independent tasks |
| [`executing-plans`](skills/executing-plans) | Execute plans in isolated sessions |
| [`finishing-a-development-branch`](skills/finishing-a-development-branch) | Complete branches with PR/merge/cleanup |
</details>

<br>

---

## 🏛️ Project Structure

```
opencode-skills/
├── 📁 agents/                 # Agent definitions (akravonomist, laravel-simplifier)
├── 📁 apps/                   # 6 application packages
│   ├── daemon/                #   Express+SQLite daemon + `od` CLI
│   ├── web/                   #   Next.js 16 App Router web UI
│   ├── desktop/               #   Electron shell
│   ├── packaged/              #   Thin packaged Electron runtime
│   ├── landing-page/          #   Astro landing page
│   └── telemetry-worker/      #   Cloudflare Worker
├── 📁 assets/                 # Static assets (device frames, community pets)
├── 📁 charts/                 # Kubernetes Helm chart
├── 📁 config/                 # OpenCode configuration templates
├── 📁 craft/                  # Universal design craft rules (a11y, color, typography)
├── 📁 data/                   # Structured data (contributors, events)
├── 📁 deploy/                 # Docker, AWS SAM, Azure Bicep deployment
├── 📁 design-systems/         # 150+ brand DESIGN.md guides
├── 📁 design-templates/       # 111 rendering templates
├── 📁 docs/                   # Full documentation (30+ files, 7 languages)
├── 📁 e2e/                    # End-to-end tests (Playwright + Vitest)
├── 📁 mocks/                  # 18 replay-based mock CLI agents
├── 📁 nix/                    # Nix flake packaging (NixOS, Home Manager)
├── 📁 packages/               # 13 shared TypeScript packages
├── 📁 plugins/                # Plugin ecosystem (spec, registry, 200+ plugins)
├── 📁 prompt-templates/       # AI prompt templates (image, video)
├── 📁 scripts/                # 42+ automation scripts
├── 📁 skills/                 # 256 agent skills
├── 📁 specs/                  # Architecture specs & change documents
├── 📁 story/                  # Project origin story
├── 📁 templates/              # HTML framework templates
├── 📁 tools/                  # Dev/pack/serve CLI tooling
│   ├── dev/                   #   Local dev lifecycle control
│   ├── pack/                  #   Packaged build & deploy
│   └── serve/                 #   Fixture service
├── 📄 AGENTS.md               # Root agent guidance
├── 📄 CLAUDE.md               # Claude Code config
├── 📄 CONTRIBUTING.md         # Contribution guide
├── 📄 LICENSE                 # Apache 2.0
├── 📄 README.md               # You are here ✨
└── 📄 README-OPEN-DESIGN.md   # Open Design upstream README
```

<br>

---

## 📦 Stats

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Skills       256   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
  Plugins      200+  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
  Packages      13   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
  Apps           6   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━-------------  80%
  Scripts       43   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
  Design Sys.  150+  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
  Templates    111   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
  CI Workflows  40   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
  E2E Tests     60+  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
  I18n Locales   18  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

<br>

---

## 🚀 Developer Tooling

This monorepo is powered by a full `pnpm` workspace:

```bash
# Install all dependencies
pnpm install

# Type-check everything
pnpm typecheck

# Run CI guard
pnpm guard

# Start local dev environment (daemon + web)
pnpm tools-dev start web

# Build a specific app
pnpm --filter @open-design/web build
pnpm --filter @open-design/daemon build
```

<br>

---

## 🤝 Contributing

We welcome contributions of all kinds — skills, design systems, plugins, bug fixes, docs, translations, and ideas.

- 📖 Read [`CONTRIBUTING.md`](CONTRIBUTING.md) for the full guide
- 🌐 Help translate — check [`TRANSLATIONS.md`](TRANSLATIONS.md) (18 locales)
- 🐛 Found a bug? Open an [issue](https://github.com/hosseinmirzapur/opencode-skills/issues)
- 💬 Join the [Open Design Discord](https://discord.gg/qhbcCH8Am4)

<br>

---

<div align="center">
  <sub>
    Built with ❤️ for the agent ecosystem · Powered by <a href="https://opencode.ai">OpenCode</a> · 
    Core engine from <a href="README-OPEN-DESIGN.md">Open Design</a>
  </sub>
  <br>
  <sub>Apache 2.0 Licensed</sub>
</div>
