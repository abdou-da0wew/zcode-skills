---
name: guizang-ppt
description: Generate "digital magazine × e-ink" style horizontal page-flip web PPT decks (single HTML file) with a WebGL fluid background, serif headlines + sans body text, chapter-divider covers, big-number stat slides, image grids and more. Use when the user needs a share / talk / launch-event style web PPT, or mentions "magazine-style PPT", "horizontal swipe deck", "editorial magazine", "e-ink presentation".
visibility: public
mode: template
carrier: deck
scenario: marketing
pattern_source: assets/template.html, assets/pattern-slides.html
source_priority: skill-first
triggers:
  - "ppt"
  - "deck"
  - "slides"
  - "presentation"
  - "magazine"
  - "magazine-style PPT"
  - "horizontal swipe"
  - "horizontal swipe deck"
  - "editorial magazine"
  - "e-ink presentation"
  - "web PPT"
  - "launch event"
  - "sharing deck"
od:
  default_for: deck
  upstream: "https://github.com/op7418/guizang-ppt-skill"
  preview:
    type: html
    entry: index.html
  design_system:
    requires: false
  example_prompt: "Help me build a magazine-style PPT — about 'the one-person company · an organization folded by AI', a 25-minute talk, audience is designers + founders. First recommend a direction (Monocle / WIRED / Kinfolk / Domus / Lab) for me to choose."
---

# Magazine Web Ppt

## What this skill does

Generates a **single-file HTML** horizontally paged PPT whose visual foundation is:

- A **digital magazine + e-ink** hybrid style
- **WebGL fluid / contour / chromatic-aberration background** (visible on hero pages)
- **Serif headlines (Playfair Display + a CJK serif such as Noto Serif SC when writing Chinese) + sans body (Inter + a CJK sans such as Noto Sans SC) + monospace metadata (IBM Plex Mono)**
- **Lucide line icons** (no emoji)
- **Horizontal left/right page flips** (keyboard ← →, wheel, touch swipe, bottom dots, ESC index)
- **Smooth theme interpolation**: colors and the shader transition softly when flipping to hero pages

The aesthetic is not "business PPT" nor "consumer-web UI" — it is what *Monocle* magazine would look like pasted onto code.

## When to use

**Good fits**:
- In-person talks / industry briefings / private salons
- AI product launches / demo days
- Presentations with a strong personal voice
- Web slides that must be "built once, no slide-tool round-trip"

**Poor fits**:
- Large data tables, stacked charts (use a regular PPT)
- Training courseware (information density is too low)
- Multi-user collaborative editing (this is static HTML)

## Workflow

### Step 0 · Pick a direction (mandatory first step)

**Before asking the 6 clarifying questions, have the user pick one of the 5 magazine directions**. Each direction bundles "theme color / recommended layouts / chrome style / recommended slide count" — picking a direction answers half the clarifying questions.

Open `references/styles.md`, **copy the whole section** showing the 5 directions' one-line summaries, and let the user choose:

```
1. Monocle Editorial · international magazine style ✦ default
2. WIRED Tech · data + engineering
3. Kinfolk Slow · slow living / humanities
4. Domus Architectural · architecture / spatial feel
5. Lab / Reference · academic + craft manual
```

If the user says "not sure, you recommend" — **default to Monocle Editorial**, it has the lowest failure rate. If the user mentions "AI / benchmark / tech launch" — recommend WIRED; "reading / salon / social sharing" — Kinfolk; "design / architecture / portfolio" — Domus; "research / academic / methodology" — Lab.

After picking the direction, create or update `project-notes.md` in the project directory; the first line states direction + theme color + audience + duration (template at the end of `styles.md`). **Never switch direction midway** — switching midway = starting over.

### Step 1 · Requirement clarification (mandatory before building)

**If the user already provided a complete outline + images**, skip ahead to Step 2.

**If the user only gave a topic or a vague idea**, align on these 6 questions one by one before building. Do not start writing slides on guesses — a wrong structure is expensive to rework later:

#### 6-question clarification checklist

> Question 5 is already answered in Step 0 when picking the direction (direction → theme color). Leave question 5 blank in the list below.

| # | Question | Why ask |
|---|------|-----------|
| 1 | **Who is the audience? What's the setting?** (industry briefing / commercial launch / demo day / private salon) | Determines tone and depth |
| 2 | **Talk duration?** | 15 min ≈ 10 slides, 30 min ≈ 20 slides, 45 min ≈ 25-30 slides (recommended ranges per direction in `styles.md`) |
| 3 | **Any source material?** (docs / data / old PPT / article links) | Build on material if present, scaffold otherwise |
| 4 | **Any images? Where are they?** | See "image conventions" below |
| 5 | ~~**Which theme palette?**~~ | ✓ Already decided by the direction in Step 0 |
| 6 | **Any hard constraints?** (must include XX data / must not mention YY) | Avoid rework |

#### Outline help (if the user has no outline)

Scaffold with the "narrative arc" template, then fill in content:

```
Hook            → 1 slide   : open with a contrast / question / hard number that stops people
Context         → 1-2 slides: background / who you are / why this topic
Core            → 3-5 slides: the main content, alternating Layouts 4/5/6/9/10
Shift           → 1 slide   : break expectations / introduce a new viewpoint
Takeaway        → 1-2 slides: punchline / open question / call to action
```

Narrative arc + slide-count plan + theme rhythm table (see `layouts.md`) — **align all three** before moving to Step 2.

Save the outline as `project-notes.md` or `outline-v1.md` for later iteration.

#### Image conventions (tell the user)

Before building, make these clear to the user:

- **Folder location**: `project/XXX/ppt/images/` (same level as `index.html`)
- **Naming convention**: `{page-number}-{semantic}.{ext}`, e.g. `01-cover.jpg` / `03-figma.jpg` / `05-dashboard.png`
  - Zero-padded page numbers sort correctly
  - Semantic names in English: short, specific, matching the content
- **Spec recommendations**:
  - Each image ≥ 1600px wide (avoids blur on large screens)
  - JPG for photos/screenshots, PNG for transparent UI/charts
  - Keep total size under 10MB (affects flip smoothness)
- **How to replace**: keeping **same-name overwrite** is safest (no HTML path edits); if filenames change, globally search `images/old-name` and update
- **No images?**: align with the user; you can scaffold with placeholder color blocks first and drop images in later — but warn that image-led layouts (4/5/10) can't be visually validated without images

### Step 2 · Copy the template

Copy `assets/template.html` to the target location (usually `project/XXX/ppt/index.html`) and create a sibling `images/` folder ready to receive images.

```bash
mkdir -p "project/XXX/ppt/images"
cp "<SKILL_ROOT>/assets/template.html" "project/XXX/ppt/index.html"
```

`template.html` is a **complete, runnable** file — CSS, WebGL shader, page-flip JS, font/icon CDNs are all preconfigured; only `<main id="deck">` contains 3 example slides (cover, chapter divider, blank filler).

#### 2.1 · Required placeholder edits (easy to miss)

Right after copying, replace these placeholders or the browser tab will show the awkward "[REQUIRED] replace with PPT title" text:

| Location | Original | Change to |
|------|------|--------|
| `<title>` | `[REQUIRED] replace with PPT title · Deck Title` | The actual deck title (e.g. `A New Way to Work · Luke Wroblewski`) |

First thing after every copy: grep for "[REQUIRED]" to confirm all placeholders are replaced.

#### 2.2 · Pick the theme palette (5 presets · no custom values)

This skill **only allows choosing one of 5 carefully tuned presets**; user-supplied hex values are not accepted — a bad color pairing ruins the page instantly, and protecting the aesthetic beats offering freedom.

| # | Theme | Best for |
|---|------|------|
| 1 | 🖋 Ink Classic | general / business launches / the safe default |
| 2 | 🌊 Indigo Porcelain | tech / research / data / technical launches |
| 3 | 🌿 Forest Ink | nature / sustainability / culture / non-fiction |
| 4 | 🍂 Kraft Paper | nostalgia / humanities / literary / indie magazines |
| 5 | 🌙 Dune | art / design / creative / galleries |

**Steps**:
1. Recommend one based on the content, or directly ask the user to pick
2. Open `references/themes.md`, find the matching theme's `:root` block
3. **Wholesale replace** the lines tagged with the theme-color comment in the `:root{` block at the top of the copied `assets/template.html` (`--ink` / `--ink-rgb` / `--paper` / `--paper-rgb` / `--paper-tint` / `--ink-tint`)
4. All other CSS reads `var(--...)`, so nothing else needs changing

**Hard rules**:
- One deck, one theme — never swap colors midway
- Don't accept arbitrary hex values from the user — politely decline and show the 5 presets
- Don't mix palettes (e.g. ink from Ink Classic, paper from Dune) — it breaks the harmony completely

### Step 3 · Fill in content

#### 3.0 · Pre-flight: class names must exist in template.html (most important)

**This is the root of all generation bugs**. The layouts.md skeletons use many class names (`h-hero` / `h-xl` / `stat-card` / `pipeline` / `grid-2-7-5` etc.); if `assets/template.html`'s `<style>` doesn't define them, the browser falls back to default styles — headlines render as sans, stat cards crumple together, the pipeline smears into one line, images pile at the page bottom.

**Before writing any slide code:**

1. **Read `assets/template.html` first** (at least through the end of the `<style>` block)
2. **Cross-check against layouts.md's Pre-flight list** — confirm every class you plan to use exists in `<style>`
3. If a class is missing: **add it to template.html's `<style>`**, don't inline-redefine it per slide
4. **template.html is the single source of class names** — don't invent new ones; for one-offs use inline `style="..."`

Classes commonly missed (confirm they exist up front):
`h-hero` / `h-xl` / `h-sub` / `h-md` / `lead` / `kicker` / `meta-row` / `stat-card` / `stat-label` / `stat-nb` / `stat-unit` / `stat-note` / `pipeline-section` / `pipeline-label` / `pipeline` / `step` / `step-nb` / `step-title` / `step-desc` / `grid-2-7-5` / `grid-2-6-6` / `grid-2-8-4` / `grid-3-3` / `grid-6` / `grid-3` / `grid-4` / `frame` / `frame-img` / `img-cap` / `callout` / `callout-src` / `chrome` / `foot`

#### 3.0.5 · Plan the theme rhythm (as important as the class pre-flight)

**Before choosing layouts**, list each slide's theme class (`hero dark` / `hero light` / `light` / `dark`) and write it into the doc or draft for alignment. Full rules in the "theme rhythm planning" section at the top of `references/layouts.md`.

**Mandatory rules**:

- Every section must carry one of `light` / `dark` / `hero light` / `hero dark` — never a bare `hero`
- 3+ consecutive same-theme slides = visual fatigue, not allowed
- Decks of 8+ slides must have ≥1 `hero dark` + ≥1 `hero light`
- A deck of only `light` body slides is not allowed; `dark` body slides create breathing room
- Insert 1 hero slide every 3-4 slides (cover / divider / question / big quote)

**Self-check after generating**: `grep 'class="slide' index.html` lists every theme; eyeball the rhythm before delivering.

#### 3.1 · Pick layouts

**Don't write slides from scratch**. Open `references/layouts.md` — it has 10 ready-made layout skeletons, each a complete paste-ready `<section>` code block:

| Layout | Use |
|---|---|
| 1. Opening cover | Slide 1 |
| 2. Chapter divider | Start of each chapter |
| 3. Big-number stat | Hard data |
| 4. Text left, image right (Quote + Image) | Identity contrast / stories |
| 5. Image grid | Multi-image comparison / screenshot evidence |
| 6. Two-column pipeline | Workflows |
| 7. Suspense close / question page | Chapter end / closing |
| 8. Big quote | Serif pull-quote / takeaway |
| 9. Before / After comparison | Old way vs new way |
| 10. Lead image + side text | Dense image-text pages |

Pick the layout, paste it, swap copy and image paths. **Always complete the 3.0 pre-flight first**.

#### 3.2 · Image aspect ratios

Always use **standard ratios**, never oddball original ratios (e.g. `2592/1798`):

| Scenario | Recommended ratio |
|------|---------|
| Main image, text-left/image-right | 16:10 or 4:3 + `max-height:56vh` |
| Image grid (multi-image compare) | **fixed `height:26vh`**, no aspect-ratio |
| Small image left + text right | 1:1 or 3:2 |
| Full-screen hero visual | 16:9 + `max-height:64vh` |
| Small inline illustration | 3:2 or 3:4 |

**Never use `align-self:end` on images** — they slide to the cell bottom and get clipped by browser toolbars. Use a grid container + `align-items:start` (preconfigured in the template) so images hug the top; to bottom-align a left column use flex column + `justify-content:space-between`.

Component details (fonts, colors, grids, icons, callouts, stat-cards etc.) are in `references/components.md`.

### Step 4 · Self-check against the checklist

After generating, open `references/checklist.md` and check every item. It captures **all the pits stepped in during real iterations**; P0 issues (emoji, image overflow, headline wrapping, font roles) must all pass.

Watch especially:

1. **Headlines must be serif** — if they render sans, 99% chance Step 3.0 pre-flight was skipped and `h-hero` is missing from template.html
2. **Image grids use only `height:Nvh`, never `aspect-ratio`** (it overflows)
3. **Images must not pile at the page bottom** — no `align-self:end`; use grid + `align-items:start` (see Step 3.2)
4. **Images use standard ratios only** (16:10 / 4:3 / 3:2 / 1:1 / 16:9); never copy oddball original ratios
5. **CJK headlines ≤ 5 characters with `nowrap`** (avoids one character per line)
6. **Lucide, not emoji**
7. **Serif headlines, sans body, mono metadata**

### Step 5 · Local preview

Just open `index.html` in a browser. On macOS:

```bash
open "project/XXX/ppt/index.html"
```

No local server needed. Images use relative paths `images/xxx.png`.

### Step 6 · Iterate

Modify based on feedback — the template CSS is highly parameterized; 90% of tweaks are inline style edits (font size `font-size:Xvw` / height `height:Yvh` / spacing `gap:Zvh`).

---

## Resource map

```
magazine-web-ppt/
├── SKILL.md              ← you are here
├── assets/
│   ├── template.html     ← complete runnable template (seed file)
│   └── pattern-slides.html ← 9-slide sample deck (for Examples preview)
└── references/
    ├── styles.md         ← 5 magazine directions (Monocle / WIRED / Kinfolk / Domus / Lab)
    ├── components.md     ← component manual (fonts, colors, grids, icons, callouts, stats, pipeline...)
    ├── layouts.md        ← 10 page-layout skeletons (paste-ready)
    ├── themes.md         ← 5 theme palettes (choose only, no customization)
    └── checklist.md      ← quality checklist (P0/P1/P2/P3 graded)
```

**Suggested loading order**:
1. Read `SKILL.md` (this file) end to end first
2. **At Step 0, read `styles.md`** — the 5 directions each bundle theme color + recommended layouts + chrome style
3. After Step 1 clarification, if the direction needs confirming, read `themes.md` for palette details
4. **Read the `<style>` block of `assets/template.html` before building** — it is the single source of class names; missing classes collapse whole pages
5. Read `layouts.md` to pick layouts (Pre-flight class list and theme rhythm planning at the top)
6. Read `components.md` for component details when fine-tuning
7. After generating, run through `checklist.md` (the P0-0 rule forces the pre-flight)

## Core design principles (philosophy)

> These principles come from 5 rounds of iterating a "one-person company" talk deck. Break any one and the visual quality collapses.

1. **Restraint over showing off** — the WebGL background only peeks through on hero pages; barely visible elsewhere
2. **Structure over decoration** — no shadows, no floating cards, no padding boxes; all information carried by **large type + font contrast + grid whitespace**
3. **Hierarchy defined by size and font together** — largest serif = main title, medium serif = subtitle, large sans = lead, small sans = body, mono = metadata
4. **Images are first-class citizens** — crop only the bottom of images, keep top/left/right intact; grids use fixed `height:Nvh`, never `aspect-ratio`
5. **Rhythm comes from hero pages** — alternate hero and non-hero so eyes don't tire
6. **Consistent terminology** — "Skills" stays "Skills"; don't mix translated terms

## Reference works

The visual foundation draws on:

- Guizang's "The One-Person Company: An Organization Folded by AI" talk (2026-04-22, 27 slides)
- *Monocle* magazine layout language
- The demo in YC president Garry Tan's blog post "Thin Harness, Fat Skills"

Treat them as style anchors.
