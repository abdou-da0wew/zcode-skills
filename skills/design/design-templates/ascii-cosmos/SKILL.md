---
name: ascii-cosmos
description: Generate a single-file product landing page with a layered ASCII cosmos hero (rotating ASCII planet, drifting irregular asteroids, comet trails, nebula gas clouds — each in its own harmonious color) plus full marketing sections (about / features grid / showcase / spec / pricing / CTA / footer). Takes a natural-language description of one product (any kind — a note app, a coffee subscription, a CLI tool, indie hardware, a hosting service…) and outputs ONE working .html file with a deep-space dark or warm-letterpress theme. Runs in BOTH local agent environments with a filesystem such as the DiveeOI agent (OpenCode-based) (writes to ~/Desktop) and plain online chat without a filesystem (outputs HTML inline). Trigger phrases: "make a cosmos-style product landing page", "generate an ASCII product website", "ascii-cosmos-gen ...", "make an indie software / indie hardware landing page", or when the user drags this skill folder into chat asking for an atmospheric product landing page.
visibility: public
mode: template
carrier: web-page
scenario: marketing-landing
pattern_source: reference.html
source_priority: skill-first
triggers:
  - "make a cosmos-style product landing page"
  - "generate an ASCII product website"
  - "make an indie software landing page"
  - "make an indie hardware landing page"
  - "ascii landing page"
  - "ascii hero"
legacy_gen: true
---

# ascii-cosmos — ASCII cosmos-vibe product landing page generator

## What the output looks like

A single-file HTML product website whose hero is a dynamic layered ASCII cosmos:

- **Nebula gas clouds** (purple, soft scattered dots)
- **Twinkling stars** (cool white, with ★ ✦ accents)
- **Rotating ASCII planet** (cyan, with 3 satellite orbit rings)
- **Floating irregular asteroids** (amber gold, 6 multi-line ASCII shapes with craters, self-rotating + slowly drifting)
- **Comet trails** (pink, sweeping across the screen)

Below are the regular marketing sections: About / 6-card core-features grid / 2 interface previews / tech specs / 3-tier pricing / CTA / footer. All emphasized text has a "scramble-then-decode on hover" character-roll effect (the `.pt` class).

Good fit for: indie software, note/writing tools, local-first AI, CLIs, indie hardware, subscription services, SaaS, ebooks, podcasts — any product with a "quiet / restrained / handcrafted" personality.

## When to trigger

The user says:
- "Make a cosmos-style product landing page"
- "Make an ASCII-style product website"
- "Generate a landing page like Mozi — my product is ..."
- "ascii-cosmos-gen ..."
- Drags this skill folder into the chat and describes a product

Inputs to collect:
- **Product name + one-line positioning** (required)
- **Core selling points / feature list** (recommended — feeds the 6 feature cards)
- **Pricing tiers** (optional — if unspecified, invent 3 tiers: Free / Pro / Team)
- **Style** (optional — deep-space cyan / warm parchment / cyber purple / terminal green …, copy a preset name from `styles.md` or describe freely. Defaults to deep-space cyan)

If the user **only gives a product name and one line**: invent all 6 features, 3 price tiers, and tech specs yourself around that product. Keep the tone restrained and handcrafted — no marketing hype.

## Two runtime modes

### Mode A · Local agent such as DiveeOI (has a filesystem)
- Output location: `~/Desktop/{slug}.html` (**single file**, all images via unsplash URLs or user-provided links)
- slug: lowercase English product name with hyphens
- One-line report: path + which style was used + how many cards

### Mode B · Online chat (no filesystem)
- Output the complete HTML wrapped in a ` ```html ` code block
- Use only `https://images.unsplash.com/photo-XXX?...` or `https://picsum.photos/seed/{slug}-NN/W/H` placeholder images
- Do not try to access local files; do not suggest command-line operations
- End with one line: save as .html and double-click to open

Decision rule: if you **cannot Read local images** or the working directory is not the user's home directory → default to Mode B.

## Workflow

### 1. Read the template
Read `template.html` in this skill's directory. It is the complete skeleton and includes:
- All CSS (deep-space theme colors + 5 ASCII layers + cards / pricing / specs / hero dot-matrix type …)
- All JS (5-layer ASCII rendering, info-section orbit, character scramble, tag filtering, smooth scrolling, live clock)
- 12 `<!-- SWAP-N -->` comment markers showing what to replace

**Do NOT change JS / CSS** (except theme color variables and fonts, which may follow the chosen style).

### 2. Read the style presets
See `styles.md`: 5 presets. If the user's style description matches a preset name, replace `:root` with that preset's CSS variables. Otherwise design your own 6 variables from the user's description (`--bg / --fg / --dim / --accent / --accent2 / --accent3 / --line / --paper`) + 5 ASCII layer colors (`#ascii-nebula / -stars / -planet / -asteroids / -comets`).

> Color iron rule: the 5 ASCII layer colors must be **mutually harmonious AND all readable against the background**. Dark background → high-saturation glowing colors; light background → mid-to-low lightness colors with visual weight.

### 3. Parse user input and extract

Extract:
- **PRODUCT_EN** — English logo name, uppercase ASCII letters (used for the hero's big ASCII title)
- **PRODUCT_CN** — 1-2 CJK display characters (hero subtitle big type, rendered as dot-matrix)
- **TAGLINE** — one-line sub-slogan (30-50 characters)
- **VERSION / TYPE / PLATFORM** — 3 meta tags
- **ABOUT_PARAGRAPH** — 80-150 character about paragraph with 3-5 `<span class="pt">` emphasized phrases
- **3 HIGHLIGHT** — 3 cells (title + one-line description)
- **6 FEATURES** — 6 cards: image URL + ASCII overlay (5-6 line mini art) + title + subtitle + 1-2 tags + category (ai/write/graph/sync or custom)
- **2 SHOWCASE** — 2 interface intros (screenshot URL + mini-ascii decoration + title with `<em>` emphasis + 2 paragraphs of 60-100 characters each)
- **10 SPEC ROWS** — 10 key-value rows (version / platform / engine / data format / sync protocol …)
- **3 PRICING** — 3 tiers (name / price number / price unit / description / 5-6 features / CTA button label). **Add the `featured` class to the middle tier**
- **CTA_BIG** — large-type CTA copy (with `<em>` emphasis) + sub-copy + 3 buttons + 6-7 platform tags

### 4. Fill the 12 SWAPs

| SWAP | Location | Content |
|---|---|---|
| 1 | `<title>` | `{PRODUCT_CN}{PRODUCT_EN} — {TAGLINE}` |
| 2 | header logo + 5 nav items | logo text + nav anchors (defaults: Features / Interface / Specs / Pricing / About) |
| 3 | hero ASCII title | ANSI Shadow-style ASCII of `PRODUCT_EN` (see https://patorjk.com/software/taag style, 5 lines tall) |
| 4 | hero CJK big type + tagline + 3 meta | `PRODUCT_CN` + `TAGLINE` + 3 meta spans |
| 5 | intro paragraph + 3 cells | `ABOUT_PARAGRAPH` (with `<span class="pt">` emphasis) + 3 `<div class="cell">` |
| 6 | 6 feature cards | each: `data-cat` + `<img src>` + ASCII overlay + title + small + tags |
| 7 | 4 filter tags | category chips (all + the 3-4 categories you chose, matching card data-cat) |
| 8 | 2 showcase blocks | each: screenshot + mini-ascii + h3 (with em) + 2 p (with pt emphasis) |
| 9 | 10 spec table rows | each: `<b>` field name + `<span class="pt">` value |
| 10 | 3 pricing tiers | name / num / desc / ul li / btn |
| 11 | info-section CTA | info-big big type (with em) + hero-sub copy + 3 buttons + platforms |
| 12 | footer | copyright + one-line signature |

**Must keep unchanged** (do not touch):
- All `<script>` blocks (5-layer ASCII rendering / info orbit / scramble / tag filtering / smooth scroll / clock)
- The `.pt` character-scramble mechanism (you manually sprinkle `<span class="pt" data-text="...">...</span>` into the user's copy)
- The 5 ascii-layer `<pre id="ascii-...">` nodes
- The `<pre id="info-ascii">` node
- The cards' data-cat attributes and the filter logic
- The featured pricing tier styles

### 5. Write the big ASCII title (SWAP-3)

Use 5-line ASCII text in the ANSI Shadow / ANSI Regular style. Each letter is built from line-drawing characters like ╗╔═║║║╝╚═╝. For example INKWEAVE:
```
██╗███╗   ██╗██╗  ██╗██╗    ██╗███████╗ █████╗ ██╗   ██╗███████╗
██║████╗  ██║██║ ██╔╝██║    ██║██╔════╝██╔══██╗██║   ██║██╔════╝
██║██╔██╗ ██║█████╔╝ ██║ █╗ ██║█████╗  ███████║██║   ██║█████╗
██║██║╚██╗██║██╔═██╗ ██║███╗██║██╔══╝  ██╔══██║╚██╗ ██╔╝██╔══╝
██║██║ ╚██╗██║██║  ██╗╚███╔███╔╝███████╗██║  ██║ ╚████╔╝ ███████╗
╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝
```

**If the English product name exceeds 8 letters** → shorten it to ≤8 letters (e.g. `INTERSTELLAR` → `STELLAR`), or use a narrower ANSI font (thinner `▌▐█`).

**If you are unsure what the letterforms look like** → at least produce a passable 5-line ASCII; never leave it empty.

### 6. Write card ASCII overlays (embedded in SWAP-6)

Each card's bottom-right gets a 4-5 line mini ASCII decoration matching that card's feature. Examples:
- "Smart continue-writing" → `╭─────╮ │ ... │ ╰──→──╯`
- "Knowledge graph" → `●─●─● │\\ │/│ ●─●`
- "Search" → `┌─────┐ │ ⌕ found │ │  3 hits │ └─────┘`
- "Sync" → `▣ ⇄ ▢ ╲ ╱ ⇅ ╱ ╲ ▤ ⇄ ▥`
- "Timeline" → `←─◆─◆─◆─→ ░░▒▒▓▓██`

No more than 5 lines, no wider than 14 characters.

### 7. Sprinkle `<span class="pt" data-text="...">` emphasis

Every emphasized phrase that should "scramble on hover then decode" uses:
```html
<span class="pt" data-text="original">original</span>
```
- Sprinkle 3-5 in the intro paragraph
- Sprinkle 1-2 per paragraph in showcase p blocks
- Wrap every spec row's value in `<span class="pt">`
- Add `pt` to pricing button labels too
- Use `<span class="em">...</span>` for colored words in headings (not `pt`)

### 8. Style variants (optional)
If the user specifies a style, follow `styles.md` and change:
- The 8 `:root` variables
- The `.hero` background gradient
- The 5 `#ascii-{layer}` colors
- The image filter (dark themes use `hue-rotate(200deg) brightness(.7)`, warm themes use `sepia(.3) saturate(.85)`)

> **When no style is specified**: pick colors automatically from the product's "tone words" — see the "tone → palette mapping" below.

### 8.5 Swap the ASCII scene motif (recommended!)

The template's hero defaults to a cosmos (planet + asteroids + comets + nebula). **This motif should follow the product's personality** — a coffee subscription shouldn't float asteroids, a forest-walk app shouldn't have comets.

The fix touches **exactly one object**: find the `// SWAP-13 · ASCII scene assets` marker in the `<script>` and replace the whole `SCENE = { ... }` inside it. Touch no other JS.

The roles of SCENE's 11 keys:

| Key | Default (cosmos) | Role / visual job |
|---|---|---|
| `floaters` | 6 irregular asteroid ASCII shapes (multi-line arrays) | The drifting + spinning "main objects" on screen |
| `centerShade` | `" .,:;-~+*=%#@█"` | Shading ramp of the central rotating sphere (dark→light, 14 chars) |
| `diffuseChars` | `"·∙∶⋮⋯░▒"` | Density ramp of the diffuse background "gas cloud" (light→dense) |
| `sparkRare` | `"★"` | Rare big bright spark (4% chance) |
| `sparkBright` | `"✦"` | Medium-frequency spark (15%) |
| `sparkDim` | `".∙"` | Ordinary dim dots |
| `streakHead` | `"☄"` | The streaking object's "head" (brightest cell) |
| `streakTailNear/Mid/Far/End` | `"*","∙","·","."` | Trail fading from near to far in 4 segments |
| `centerSats` | `"◉◎○"` | The 3 "satellites" around the central sphere, inner to outer |
| `orbitDots` | `".∙•"` | Dot characters for the 3 orbit rings, inner to outer |

#### Motif library (pick by product type)

| Product type | floaters theme | centerShade | diffuseChars | sparks | streakHead/tail | centerSats | Visual story |
|---|---|---|---|---|---|---|---|
| **Coffee / tea / drinks** | coffee bean / tea leaf shapes | `" .'-=+oO0@#"` | `"·~,'\""` (steam) | `★ ✧ . ∙` | `"☕"` head + `"*∙·."` trail | `"●◐○"` (three roasts) | A cup of coffee + drifting beans + steam + the occasional falling bean |
| **Forest / nature / outdoors** | leaf / pinecone shapes | `" .,;:!|tT#"` (tree rings) | `"~^,'\""` (mist) | `"⁂"` fireflies + `"·"` dew | `"𓅯"` bird + `"~~~~"` flight path | `"❀✿✾"` (flowers) | A tree + falling leaves + mist + fireflies + the occasional bird |
| **Music / podcast / audio** | notes / vinyl fragments | `" .─=≡▪▫■□"` | `"·∶⋮⁞"` (grain) | `"♪♫"` + `"·"` | `"♬"` head + `"~∼≈"` waves | `"◉◎○"` (vinyl rings) | A record + floating notes + spectrum grain + beats |
| **Code / CLI / developer** | small ASCII blocks wrapped in `{}` `[]` `()` `<>` | `" 01[](){}<>#"` | `"·.,:|"` | `"★ ✦ . _"` | `"_"` cursor + `"   "` (blink type) | `"◉⊞⊟"` modules | A call graph + flying commits + blinking cursor + matrix rain |
| **Handcraft / craft / objects** | hammer / shavings / nails / rust | `" .·°*+x#X@"` | `"·:.,"` (dust) | `"✦ ▪ ▫"` | `"→"` head + `"-—"` cut line | `"◉○⊙"` (gears) | A workbench + drifting shavings + sawdust + the occasional strike |
| **Meditation / wellness / slow living** | ripple / circle / wave shapes | `" ··∘○●"` | `"~∼≈"` (breath waves) | `". ∙ °"` | `"◌"` head + `"·· ··"` scatter | `"◯◌○"` (empty circles) | A breathing circle + ripples + warm dust + slowness |
| **Geek hardware / electronics** | chips / circuit blocks (`├┤├ ┐└┘`) | `" .·•◊◆■"` | `"⋅¨"` (electrical noise) | `"⚡"` occasional + `"·"` | `"►"` head + `"==="` data stream | `"⊙⊚⊛"` (LEDs) | PCB + floating capacitors + data streaming past |
| **Writing / notes / thinking** | `"…"` `"——"` `"§"` punctuation shapes | `" .,;:!?¶§"` | `"··¨"` | `". ∶ ⋮"` | `"✒"` head + `"~~~"` ink trail | `"◉◯●"` (ink dots) | A pen + drifting punctuation + an ink stroke crossing + thought dots |
| **Retro / vintage / 80s** | pixel squares / clashing geometry | `" .░▒▓█"` | `"·:|"` | `"◆ ◇ ▰"` | `"◉"` head + `"━━"` solid line | `"■□▣"` | A CRT + pixel particles + scanlines |
| **Ocean / travel / faraway** | fish / sails / boats / waves | `" .~≈≋"` water waves | `"~∼≈≋"` (ripples) | `"·°"` (bubbles) | `"⛵"` head + `"~~~"` wake | `"◐◑◯"` (moon phases) | A boat + waves + bubbles + gulls crossing |

#### How to write floater shapes

Each shape is 3-4 lines of multi-line ASCII, 8-12 characters wide. Always:
- Close the outline (e.g. leaf `,/^\,` `(   )` `'\_/'`)
- Don't make every variant identical — provide at least 3-6 distinct ones
- Single-character width only; never full-width
- Leave 1 cell of padding so the rotation jitter looks good

**Leaf example**:
```js
floaters: [
  [" ,-^-, ",
   "|     |",
   " '---' "],
  ["  /\\\\  ",
   " /  \\\\ ",
   " \\__/ "],
  ["  *_*  ",
   " /...\\\\ ",
   " '___' "]
]
```

**Music note example**:
```js
floaters: [
  ["  ♪    ",
   " /|    ",
   "♪ |____♪"],
  ["    ♫  ",
   "    /\\\\ ",
   "♪__/  \\\\"],
  ["  ♩    ",
   "  |    ",
   "  o    "]
]
```

**Check when done**: paste SCENE directly into a console; if `JSON.stringify(SCENE)` runs without errors you're OK.

#### When to improvise

If the user's product **isn't in the 10 categories above** → design your own motif following these principles:
1. **floaters**: pick 3-6 small shapes with a concrete link to the product ("it should make people think of this product")
2. **centerShade**: a 14-character shading ramp starting dark (` .,`), ending bright (`@#█`), gradient in between
3. **diffuseChars**: 5-8 "translucent" characters (dots / ticks / small squares / waves) for the ambient background
4. **streak**: the whole set must fade "strong in front, light behind"
5. **sats / orbitDots**: 3 each, expressing three levels of visual weight

> One-line principle: **someone without glasses, glancing from 3 meters away, should guess what kind of product this site is for.**

### 9. Tone → palette mapping (use when the user hasn't specified a style)

| Keywords in the user's description | Recommended preset | Main color |
|---|---|---|
| Quiet / restrained / thoughtful / writing / notes / local-first | **Deep-space cyan** (default) | `#8be9ff` cyan |
| Warm / handcrafted / Chinese-classic / literary / slow / tea / vintage | **Warm parchment** | `#660125` wine red |
| High-energy / futuristic / AI / Web3 / gaming / geek | **Cyber purple** | `#ff00aa` neon magenta |
| CLI / terminal / security / retro 80s / phosphor | **Terminal green** | `#00ff66` |
| Nature / wellness / meditation / travel / Nordic | **Aurora** | `#7fe3c4` aurora green |
| Coffee / baking / craft / food / desert / earth | **Desert sunset** | `#ff8b3d` toasted orange |
| Ocean / faraway / blue / calm / data | free design | `#4fc3f7` ocean blue |
| Black-gold / luxury / precision / watchmaking / high-end hardware | free design | `#d4af37` champagne gold + black |

Decision flow:
1. **User explicitly named a style** → follow `styles.md`
2. **User didn't say, but the product has a clear tone** → pick the closest preset from the table above
3. **Fully open** → default deep-space cyan

### 10. Report

**Mode A**: one line.
> Generated ~/Desktop/{slug}.html — {product} landing page, 6 feature cards + 3 pricing tiers, deep-space-cyan style. Double-click to open.

**Mode B**: full HTML code block + one line of notes.
> Save as `{slug}.html` and double-click to open. To swap images, replace the image URLs with your own. To change the main ASCII title, replace the glyphs in the `<pre class="ascii-title lg">` at the top.

## Common mistakes checklist

- **The 5 ASCII layer colors clash**: test that all 5 colors stay readable on the background. Pink too bright or purple too dark will fall apart
- **ASCII big-type template misaligned**: ANSI Shadow letterforms must be strictly 5-6 lines tall, never 3
- **Use real newlines inside `<pre>`**, not `\n` string literals
- **Card data-cat doesn't match filters** → filtering breaks. Do a consistency check
- **Forgot `featured` on the middle pricing tier** → the visual anchor is lost
- **Curly quotes in JSON / objects**: any quotes inside an ASCII overlay must be full-width `""`
- **Deleted a layer like `<pre id="ascii-comets">`** → JS errors. All 5 layer nodes must be kept
- **No image URL provided** → use an unsplash landscape image (`?auto=format&fit=crop&w=900&q=70`) or picsum
