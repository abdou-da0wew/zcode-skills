---
name: industrial-archive
description: Generate a single-file industrial-archive product landing page (Nordic museum aesthetic, hash-routed detail pages). Takes a natural-language description of one or more "exhibit-style" products (objects, tools, hardware, watches, kitchenware, lighting, audio, instruments, anything with a designed/forged/restrained quality); outputs ONE working .html file. Visitors see a black-framed cover that flips between exhibits, sidebar index, side meta column (material/origin/year/dimension), and click any exhibit → full detail page (giant italic title, spec table, hero image, lead + 3 prose paragraphs, gallery, prev/next). Runs in BOTH local agent environments with a filesystem such as the DiveeOI agent (OpenCode-based) (writes to ~/Desktop) and plain online chat without a filesystem (outputs HTML inline). Trigger: "make an industrial-style product landing page", "make an exhibit page for restrained objects", "industrial-archive-gen ...", or when the user drags this skill folder into chat asking for a product page in the Nordic-industrial archive style.
visibility: public
mode: template
carrier: web-page
scenario: brand-landing
pattern_source: reference.html
source_priority: skill-first
triggers:
  - "make an industrial-style product landing page"
  - "make an exhibit page for restrained objects"
  - "Nordic museum collection style"
  - "industrial archive"
  - "curated exhibition-style product page"
related_patterns: portfolio-detail
legacy_gen: true
---

# industrial-archive — industrial exhibit / product landing page generator

Turn "a natural-language description" into a single-file HTML: a **Nordic industrial archive / museum-curated** product landing page:

- Large product images in a black frame, flipping left/right on click
- An exhibit index with an indicator bar on the left
- 4 meta blocks on the right (material / origin / year / dimensions)
- A ticker marquee in the top bar
- Click the frame or the bottom CTA → enter the exhibit detail page (giant italic title, spec table, hero image, big-type lead + 3 prose paragraphs, 6-image gallery, prev/next)
- The entry page has an intro splash

## When to trigger

The user says "make an industrial-style product landing page / exhibit page for restrained objects / industrial-archive-gen ..." and provides:
- **Product description** (required): a passage of prose describing 1–N exhibits — name, era, origin, material, provenance
- **Image URLs** (optional): at least 1 hero image per exhibit, ideally 3–6 detail images. It also runs without any (picsum grayscale placeholders)
- **Style** (optional): default is cold steel blue-gray; presets in styles.md can be swapped in

If the user **gives no exhibit names/story at all** → ask once which exhibits should be shown and roughly what category they are (vessels / lighting / seating / instruments / tools / ...).

If the user **gives only names without a story** → invent it: for each exhibit generate 1 lead + 3 prose paragraphs + 4-6 spec rows. Match the tone of `reference.html`: **museum wall-text** — restrained, concrete, slow; never marketing language.

## Two runtime modes

### Mode A · Local agent such as DiveeOI (has a filesystem)
- Output: `~/Desktop/{slug}-archive.html` (**single file**, all images via URLs)
- If the user provides local images, suggest they switch to URLs, or copy the images next to the file and use relative paths

### Mode B · Online chat (no filesystem)
- **Output one complete HTML string**, wrapped in a ` ```html ` code block
- User gave no image URLs → use `https://picsum.photos/seed/{slug}-{nn}/{w}/{h}?grayscale` placeholders throughout
- Do not try to access local files

Decision rule: if you **cannot Read local images** → default to Mode B.

## File roles

| File | Role | How to use it |
|---|---|---|
| `reference.html` | **Complete finished reference** — 4 Nordic industrial pieces of "restrained objects" | Read for: how leads are written, prose tone, spec wording, tagline format, maker naming |
| `template.html` | **Empty skeleton** — same CSS/JS/routing, 2 sample exhibits + 17 SWAP markers | Build on it to produce the final HTML |
| `styles.md` | Style preset library | Consult when the user specifies a style |
| `README.md` | User-facing usage notes | The model doesn't need it |
| `SKILL.md` | Workflow for the model (this file) | **Required reading** |

**Core rule**: all edits are based on `template.html`; learn **how to write** from `reference.html` (tone, length, vocabulary), but do not copy its concrete content.

## Key difference — reference uses SVG, template uses `<img>`

- The 4 exhibits in `reference.html` are **hand-drawn SVGs** (cast-iron kettle / bearing lamp / birch chair / rangefinder); that's custom content
- `template.html` has already replaced the SVG system with `<img src="cover URL">`: user-provided URL if given, picsum otherwise
- You don't need to write SVG. If the user explicitly asks to "draw" the objects, consider writing an SVG function into `coverHTML()`

## Workflow

### 1. Read both HTML files
- Read `reference.html` first to absorb "what the finished piece looks like", especially the field density and prose tone of the `exhibits-data` JSON (restrained, concrete, with period context)
- Then read `template.html` and find the 17 SWAP markers (search `SWAP-`)

**Do not change the JS / do not change the CSS / do not change the detail-page routing system**.
All SWAPs live in the HTML text and the JSON data.

### 2. Parse user input and extract

#### Site-wide level (SWAPs 1-15 and 17 of 17)
- **COLLECTION_TITLE / COLLECTION_SUB** — collection big title + subtitle, e.g. "Restrained Objects / A Nordic Industrial Archive 1948—1988". SWAP-1
- **INTRO_VOLUME_TAG** — tag at the top of the entry page, e.g. "Nordic Industrial Archive · Vol.01". SWAP-2
- **INTRO_TITLE_HTML** — splash-page big title, 2-4 characters + a `<span class="accent">·</span>` separator in the middle. E.g. `Restrained<span class="accent">·</span>Objects`. SWAP-3
- **INTRO_TITLE_EN** — splash-page English subtitle, all caps + em-dash, e.g. `Restrained Objects — A Nordic Industrial Archive 1948 — 1988`. SWAP-4
- **INTRO_QUOTE** — one curatorial quote, 60–100 characters, essay-like. SWAP-5
- **INTRO_ATTRIBUTION** — quote attribution, e.g. `— Curatorial Preface / Curatorial Note`. SWAP-6
- **HEAD_GLYPH** — top-left logo character. 1-2 serif characters; letters with character are recommended, like `Æ` `Ø` `ʘ`. SWAP-7
- **HEAD_GLYPH_SUB** — one line under the logo, e.g. `Restrained Objects / No. N°01—04`. SWAP-8
- **HEAD_CENTER_CN / HEAD_CENTER_EN** — two small lines at the top center. SWAP-9, 10
- **HEAD_RIGHT_TOP / HEAD_RIGHT_BOTTOM** — two lines at the top right: date/city + coordinates/number. SWAP-11, 12
- **CURATOR_NAME / CURATOR_EMAIL** — curator name + email. SWAP-13, 14
- **CRUMB_ROOT / CRUMB_VOLUME** — the two fixed breadcrumb items on detail pages. SWAP-15
- **TICKER_TAIL** — the closing slogan of the marquee. SWAP-17

#### Per-exhibit fields (SWAP-16, the most critical)
```json
{
  "slug": "iron-kettle",
  "num": "N°01",
  "title": "Iron Kettle",
  "en": "IRON KETTLE",
  "year": "1958",
  "place": "Copenhagen, Denmark",
  "maker": "Carl Hansen Værksted / Carl Hansen Workshop",
  "material": "Gray cast iron · beech handle<br/>black glazed coating",
  "origin": "Copenhagen, Denmark<br/>Carl Hansen Værksted",
  "dim": "H 18 cm · 1.2 L<br/>base Ø 14 cm",
  "tagline": "FORGED ESSENTIAL / the forged essential",
  "lead": "A vessel designed for <em>silence and the low temperature of water</em> — the thickness of the body exists so heat lingers a little longer, not so it heats faster.",
  "spec": [
    ["Catalog no.", "1958 · K-04"],
    ["Material", "gray cast iron + beech"],
    ["Process", "sand casting / black glaze firing"],
    ["Weight", "1.86 kg"],
    ["Production", "limited to 240 · 31 extant"]
  ],
  "prose": [
    "Para 1, 80–160 characters. Origin / context / year / workshop background.",
    "Para 2, 80–160 characters. Craft / handwork details / key decisions.",
    "Para 3, 80–160 characters. State today / influence / still-in-use facts."
  ],
  "cover": "https://example.com/kettle-cover.jpg or picsum URL",
  "gallery": [
    {"src": "...", "layout": "f-3", "caption": "front elevation of the body"},
    {"src": "...", "layout": "f-2", "caption": "beech handle"},
    {"src": "...", "layout": "f-2", "caption": "spout detail"},
    {"src": "...", "layout": "f-2", "caption": "sand-mold imprint on the base"},
    {"src": "...", "layout": "f-4", "caption": "workshop blueprint"},
    {"src": "...", "layout": "f-6", "caption": "display cross-section"}
  ]
}
```

### 3. Replace the SWAPs

Replace all 17 `{{...}}` placeholders in `template.html` with the content you extracted.
**Note**: `{{INTRO_TITLE_HTML}}` is HTML, not plain text; it must contain the `<span class="accent">·</span>`.

### 4. Write the exhibits-data JSON (the most critical step)

Replace the 2 sample objects inside `<script id="exhibits-data" type="application/json">` **entirely** with N real exhibit objects.

#### How many exhibits
- Minimum 1 (a single-object landing page is fine — the JS already handles N=1 by disabling autoplay)
- Best 3–6
- More than 8 crowds the exhibit index; consider splitting

#### Title length
- `title` of 2-4 characters looks best ("Iron Kettle", "Bearing Lamp", "Rangefinder"). If the product name is long, use the subtitle, e.g. `"title": "Rangefinder"`, `tagline: "MARITIME RANGEFINDER / the measured horizon"`
- `en` all-caps English, 2 words ideal

#### tagline format
Fixed: `English phrase + space/space + translated phrase`, e.g.:
- `FORGED ESSENTIAL / the forged essential`
- `PIVOT & LIGHT / pivot and light`
- `FOUR LEGS, NO MORE / four legs, no more`
- `MEASURED HORIZON / the measured horizon`

#### How to write the lead
30–80 characters. **Must put `<em>...</em>` on one or two key phrases** — the CSS draws a thin steel-blue line under them.
Bad: `This is a very good kettle.` ← no em, no concrete detail
Good: `A vessel designed for <em>silence and the low temperature of water</em> — the thickness of the body exists so heat lingers a little longer.`

#### How to write the prose
3 paragraphs, 80–160 characters each. Tone: **museum wall-text** — restrained, concrete, with period context; never marketing language.
- Para 1: origin / context (place, year, workshop, that era)
- Para 2: craft / decisions (key design choices, craft details, why it was done this way)
- Para 3: presence / influence (how many exist today, still in use, influence on what came after)

#### How to write the spec
4-6 rows, one key-value pair per row.
- Row 1 is usually `["Catalog no.", "{year} · {model}"]`
- The last row is usually production/extant: `["Production", "limited to 240 · 31 extant"]` (the JS shows the last row's value in the detail page's "EXTANT" block)

#### gallery layout — exactly one of four
- `f-3` — landscape, 16:10, half width (3 of 6 columns)
- `f-2` — portrait, 4:5, one-third width
- `f-4` — landscape, 16:9, two-thirds width
- `f-6` — full width, 21:8

**Rhythm suggestion**: 1× f-3 + 3× f-2 + 1× f-4 + 1× f-6 = 6 images, exactly two and a half rows.

#### Image URLs
Mode A with user URLs → use the URLs;
Mode B without → use picsum: `https://picsum.photos/seed/{slug}-{nn}/{w}/{h}?grayscale`
- cover recommended `1600/1000`
- f-3 recommended `900/600`
- f-2 recommended `600/750`
- f-4 recommended `1200/675`
- f-6 recommended `1600/610`
- Add `?grayscale` so placeholders keep the industrial gray tone

### 5. Style variants (optional)
If the user specifies a style, change the 8 `:root` CSS variables per `styles.md`. The default cold steel blue-gray is closest to the original "restrained objects" look.

### 6. Report

**Mode A**: one-line report.
> Generated `~/Desktop/{slug}-archive.html` — N exhibits, default cold steel blue. Double-click to open; click the frame or the bottom CTA to enter the detail page. To swap images, replace the picsum URLs in cover/gallery with your own.

**Mode B**: full HTML code block + one line of notes.
> Save the block above as `index.html` and double-click to open. Click the frame for details; use ← → to switch exhibits. To swap images, replace all picsum URLs with your own.

## Must keep unchanged (do not modify)

- All JS: translate/flip animation, the `coverHTML()` function, `renderSidebar()`, `applyMeta()`, `renderDetail()`, keyboard / autoplay / cursor
- All CSS (except `:root` changes via the style-variant path)
- The `<script id="exhibits-data" type="application/json">` node must be kept
- The `<div id="proj-list" class="proj-list">` node must be kept (but do **not** hand-write the li items — `renderSidebar()` generates them)
- The flipper two-sided structure inside `<div id="cover-stage">`
- The `<main class="stage">` 9-cell grid

## JSON pitfalls checklist

- **Curly quotes**: if prose / lead needs quotation marks, use curly `"..."` (U+201C / U+201D), **never** ASCII `"` (it breaks the JSON)
- **Real line breaks**: do not put literal line breaks inside JSON strings (pressing Enter), nor `\n`. For paragraphs use multiple prose array items; for line breaks use `<br/>`
- **`<em>` tags**: write the HTML tags `<em>...</em>` **directly in the lead** — they render via innerHTML and the CSS adds the steel-blue underline
- **Unique slugs**: every exhibit's slug must be unique, lowercase English with hyphens (`iron-kettle`, not `IronKettle` or `iron_kettle`)
- **gallery layout spelling**: must be exactly one of `f-3` `f-2` `f-4` `f-6`, or it won't render
- **Unique picsum seeds**: give each image a unique seed, or different slots show the same picture
- **num format**: `N°01` — the N plus ° is required (° is U+00B0); don't type `No.01` or `N01`
- **maker must contain "/"**: `"English workshop / localized workshop"`, the JS splits on `/` and shows the left half in the bottom-right corner

## Length / count boundaries

- title ≤ 4 characters; put longer subtitles in the tagline
- lead ≤ 80 characters (about 1.5 lines)
- prose 80–160 characters per paragraph (150 is the sweet spot)
- spec 4-6 rows
- gallery 3-6 images (fewer than 3 feels empty, more than 6 breaks the layout)
- 1–8 exhibits total (best 3–6)
- ticker count is automatic — the JS walks DATA and builds it

## Style trigger words

User says → which style you use:
- nothing / "restrained" / "Nordic" / "industrial" → default cold steel blue (already the template default)
- "warm" / "vintage" / "brown tones" / "leather" → styles.md `warm-leather`
- "dark" / "deep" / "night" → styles.md `night-iron`
- "paper" / "print" / "report" → styles.md `paper-press`
- "solid color" / "navy blue" → styles.md `navy-blueprint`
