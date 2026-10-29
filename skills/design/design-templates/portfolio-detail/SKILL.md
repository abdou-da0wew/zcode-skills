---
name: portfolio-detail
description: Generate a single-file CJK atelier-style portfolio website (horizontal-row list + hover-reveal thumb interaction, art lishu typography "Alimama DaoLiTi" via CDN, light/dark theme, hash-routed detail pages). Takes a natural-language description of the studio (name, director, discipline, works) and outputs ONE working .html file. Runs in BOTH local agent environments with a filesystem such as the DiveeOI agent (OpenCode-based) (writes to ~/Desktop) and plain online chat without a filesystem (outputs HTML inline). Trigger phrases include "make a Chinese-style atelier portfolio", "make a lishu portfolio", "lishu-portfolio-gen ...", "make a BAIWU-style portfolio", or when the user drags this skill folder into chat asking for an atelier-style site.
visibility: public
mode: template
carrier: web-page
scenario: portfolio
pattern_source: reference.html
source_priority: skill-first
triggers:
  - "make a Chinese-style atelier portfolio"
  - "make a lishu portfolio"
  - "make a BAIWU-style portfolio"
  - "horizontal-row portfolio"
  - "daoli typeface portfolio"
related_patterns: vr-canvas, digital-eguide
legacy_gen: true
---

# portfolio-detail — CJK atelier / lishu portfolio (with second-level detail pages)

## One-line signature
Horizontal text rows + hover-revealed large image on the right + Alimama DaoLiTi display type + pure black & white + light/dark themes + hash-routed detail pages + list/album dual views.

## How it differs from the other portfolio skills

| skill | Core pattern | Best for |
|---|---|---|
| `portfolio-gen` | Infinite drag canvas + tile grid | Photographers / graphic designers showing samples |
| `portfolio-museum-gen` | Hero carousel + big cards + masonry + detail pages (image-curation feel) | Video / moving-image / installation artists |
| `industrial-archive-gen` | Black-frame flipping covers + archive sidebar + Nordic industrial | Physical products / objects / hardware |
| **`lishu-portfolio-gen`** | **Horizontal text rows + hover thumbnail on the right + lishu display type + Chinese restraint** | **Bookbinding / typeface / craft / CJK ateliers** |

If the user's project is of the "book / typeface / exhibition / still life / herbal plates / tea / ceramics / wood / paper / incense" kind that needs a restrained, elegant temperament — use this one.

## When to trigger

The user says:
- "Make a Chinese / Eastern / classical-style portfolio"
- "Make a lishu-style website / studio homepage"
- "Make a BAIWU-style portfolio" / "Make a horizontal-list site like Gurgel D'Alfonso's"
- "lishu-portfolio-gen ..."

and provides:
- **Studio description** (required): name, director, city, discipline, titles and stories of a few works
- **Work images** (optional): URLs / uploads / paths. It also runs without them (picsum placeholders)

If the user **gives no work titles at all** → ask once which works should be shown.
If the user **gives only titles without details** → write them yourself: for each work generate 1 lead + 3 prose paragraphs + 6-8 spec rows + 3-6 picsum images + a few credits. Match tone to the work type (book → bookbinding / type → lettering / object → still life / exhibition → exhibition graphics).

## Two runtime modes

### Mode A · Local agent such as DiveeOI (has a filesystem)
- Use `Bash` to list folders and `sips` to probe each image's width/height
- Output location: `~/Desktop/{slug}-portfolio.html` (**single file**, all images via URLs)
- If the user provides local images: copy them to `~/Desktop/{slug}-portfolio-images/` and change src to relative paths

### Mode B · Online chat (no filesystem)
- After the user drags in the zip, 4 files are visible
- **Output exactly one complete HTML string**, wrapped in a ` ```html ` code block
- User uploaded images but gave no URLs → use `https://picsum.photos/id/{id}/{w}/{h}` placeholders (use known-good IDs)
- Do not try to access local files; do not suggest command-line operations

Decision rule: if you **cannot Read local images** → default to Mode B.

## File roles

| File | Role | How to use it |
|---|---|---|
| `reference.html` | **Complete finished reference** — BAIWU (White House) with 6 works | Read for: list-item wording, prose tone, specs vocabulary, JSON field density |
| `template.html` | **Empty skeleton** — same CSS/JS/routing system, 2 sample works + 20 SWAP markers | Build on it to produce the final HTML |
| `README.md` | User-facing usage notes | The model doesn't need it |
| `SKILL.md` | Workflow for the model (this file) | **Required reading** |

**Core rule**: all edits are based on `template.html`; learn **how to write** from `reference.html` (tone, length, tag wording), but do not copy its concrete content.

## Workflow

### 1. Read both HTML files
- Read `reference.html` first to absorb "what the finished piece looks like" (especially the `works-data` JSON field density and prose tone)
- Then read `template.html` and find the 20 SWAP locations

**Do not change the JS / do not change the CSS / do not change the detail-page routing system / do not change the font imports**.
All SWAPs live in the HTML text and the JSON data.

### 2. Parse user input and extract

Extract:
- **ATELIER_NAME_ZH** — studio name in CJK characters (2-4 characters ideal, e.g. Baiwu "White House", Suyuan "Plain Garden", Moji "Ink Log", Qinglu "Green Hut", Zhuoxuan "Clumsy Studio")
- **PINYIN** — romanization (5-6 letters, all caps: BAIWU / SUYUAN / MOJI)
- **CHAR** — single character for the logo (usually the first character of the studio name)
- **CITY** — city
- **DIRECTOR_ZH / DIRECTOR_EN** — director's name + romanization
- **DISCIPLINE** — 3 discipline words ("bookbinding · lettering · still life")
- **TAGLINE** — one-line positioning (20-40 characters, kaiti flavor)
- **YEAR_FOUNDED** — founding year (may use the sexagenary style: "Yiwei winter" / "Jiachen spring")

Per work, extract:
- **slug** — URL ID, lowercase English hyphenated (`kong-shan-ji` / `wu-ming-shu`)
- **title_zh** — CJK title (2-5 characters ideal; the more distilled, the stronger the tone)
- **title_en** — English subtitle (title-page style: `An Anthology of Empty Mountains`)
- **year** — year or sexagenary-style year (`Jiachen / 2024` / `2025` / `Yisi / 2025`)
- **tag** — top category, wrapped in brackets, e.g. `[ poetry collection · bookbinding ]` / `[ lettering · herbal plates ]`
- **cover** — detail-page hero image URL
- **list row location** — `city, year · craft/spec` (revealed on hover)
- **meta** — 4 key-value pairs (4-column summary on the detail page)
- **lead** — 30-70 character opening display text; may use `<em>keyword</em>` on one phrase
- **prose** — 3-4 essay paragraphs, 80-150 characters each
- **specs** — 6-10 spec rows (format / paper / binding / typeface / edition / printing / craft / price …)
- **gallery** — 3-6 images, layout one of: `g-wide` / `g-half` / `g-third`
- **credits** — 4-7 role/name pairs

If the user gives only a line or no story → **invent it**: based on the work titles and type, write lead and prose matching the work's tone. Reference tone: reference.html — never marketing language; aim for "museum wall-text + studio notebook" (restrained, concrete, slow, with traces of handwork).

### 3. List works + probe sizes (Mode A only)

```bash
ls -la "{works_path}"
sips -g pixelWidth -g pixelHeight "{works_path}/{file}" 2>/dev/null
```

This yields (filename, w, h, aspect) per image. Prefer portrait images for list thumbnails (the container is 4:3; portraits sit better).

### 4. Fill the 20 SWAPs

| SWAP | Location | Content |
|---|---|---|
| 1 | `<title>` | `{ATELIER_NAME} {PINYIN} — {DIRECTOR} Portfolio / Studio` |
| 2 | meta description | one-line site summary |
| 3 | curtain single character | first character of the studio name |
| 4 | single character inside logo SVG | same as SWAP-3 |
| 5 | romanization inside logo SVG | `{PINYIN}` uppercase |
| 6 | main nav li | usually 3 items: Works / About / Contact |
| 7 | brand-block CJK name | `{ATELIER_NAME}` spaced per character (e.g. `BAI&nbsp;&nbsp;WU` for two glyphs) |
| 8 | brand-block English | `{PINYIN} Studio · {CITY}` |
| 9 | tagline | one-line kaiti positioning, 20-40 characters; may use `<br>` for lines |
| 10 | **N list items** | each `<a class="item" href="#work/{slug}">` with num/project-name/en-name/location/photo-thumb |
| 11 | **N gallery items** | the same N works in a tighter grid — slugs must match the list |
| 12 | about title | `{name}&nbsp;small-caps<span class="en">About</span>` |
| 13 | about paragraphs | 1-3 kaiti paragraphs (founding background / director / design philosophy), 60-120 characters each |
| 14 | about facts table | 4-6 li items (Founded/Location/Discipline/Director/Hours) |
| 15 | contact title | local-language contact heading `<span class="en">Get in Touch</span>` |
| 16 | contact paragraphs | 1-2 paragraphs inviting letters + promised reply window |
| 17 | contact facts table | 4-6 items (E-mail/Phone/Address/Instagram/WeChat) |
| 18 | rotating credit | `Site by {WHO}` (usually the studio name) |
| 19 | footer three blocks | © / ICP / social links |
| 20 | **works-data JSON** | **complete detail data for N works (critical!)** |

### 5. Write the works-data JSON (the most critical step)

Every work needs one entry in the JSON array; **the slug must exactly match the `#work/SLUG` in the list/gallery card hrefs**.

JSON fields:
```json
{
  "slug": "kong-shan-ji",
  "title_zh": "Kong Shan Ji",
  "title_en": "An Anthology of Empty Mountains",
  "year": "Jiachen / 2024",
  "tag": "[ poetry collection · bookbinding ]",
  "cover": "https://picsum.photos/id/143/1800/1100",
  "meta": [
    {"label": "Type", "value": "poetry binding"},
    {"label": "Year", "value": "2024"},
    {"label": "Edition", "value": "first printing 320 copies"},
    {"label": "Format", "value": "130 × 195 mm"}
  ],
  "lead": "Thirty-six poems about mountains. We wanted a book where — once opened — you first hear the <em>wind</em>, then read the words.",
  "prose": [
    "Para 1: manuscript origin / design context. 80-150 characters.",
    "Para 2: key decisions during production — typeface, paper, binding choices.",
    "Para 3: final presentation / what it leaves with the reader."
  ],
  "specs": [
    ["Format", "130 × 195 mm"],
    ["Pages", "144 pages"],
    ["Paper", "unbleached cotton paper 90gsm"],
    ["Binding", "four-hole thread stitching"],
    ["Typeface", "old songti (titles) · kaiti (body)"],
    ["Printing", "monochrome letterpress"],
    ["Edition", "first printing 320 copies"],
    ["Price", "¥ 388"]
  ],
  "gallery": [
    {"src": "...", "layout": "g-wide", "caption": "cover"},
    {"src": "...", "layout": "g-half"},
    {"src": "...", "layout": "g-half"},
    {"src": "...", "layout": "g-third"},
    {"src": "...", "layout": "g-third"},
    {"src": "...", "layout": "g-third"}
  ],
  "credits": [
    ["Design", "Zhou Mobai"],
    ["Hand binding", "Chen Shushi (Hangzhou · bookbindery)"]
  ]
}
```

**JSON pitfalls ⚠️**:
- If CJK prose needs quotes → use curly `"..."` (U+201C / U+201D) or full-width corner brackets, **never** ASCII `"` (it breaks the JSON)
- Do not put literal line breaks inside JSON strings; for new paragraphs add another prose array item
- `<em>word</em>` is written **directly as HTML tags in the lead** — it renders via innerHTML
- gallery `layout` must be one of: `g-wide` (full) / `g-half` (half) / `g-third` (one-third)

### 6. Choosing image sources
- **picsum placeholders**: use the `id/X` form rather than `seed/X` (more stable). Known-good IDs: 0, 20, 40, 51, 64, 76, 88, 91, 96, 119, 121, 130, 143, 145, 158, 164, 165, 175, 177, 180, 187, 195, 200
- For the same work, use adjacent IDs for cover / gallery to create a consistent palette
- Do not use the `?grayscale` parameter (images should stay in color)

### 7. Atelier naming inspiration (if the user provides none)
If the user says "make one up" → pick 2 CJK characters, archaic flavor. Ideas: Baiwu (White House), Suyuan (Plain Garden), Moji (Ink Log), Qinglu (Green Hut), Zhuoxuan (Clumsy Studio), Tingyu (Listening Rain), Yishao (One Spoon), Banmu (Half Acre); or Suzbai (Plain White), Zijin, Yanchi (Inkstone Pool), Banshan (Mid-Slope), Xunchang (Ordinary), Fuyun (Drifting Cloud).
- Avoid functional words like "studio / design / Studio"; the name itself should be a poem

### 8. Video support
If a work's cover is .mp4 / .webm / .mov, the detail page automatically uses `<video autoplay muted loop>` instead of `<img>`. Just put the video path in the cover URL.

### 9. Report

**Mode A**: one-line report.
> Generated ~/Desktop/baiwu-portfolio.html — 6 works, hover a row to see the thumbnail, click to enter the detail page. Light/Dark bottom-left; list/album toggle top-center.

**Mode B**: full HTML code block + one line of notes.
> Save the block above as `index.html` and double-click to open. Hover any work name to see the thumbnail appear on the right; click to jump to the detail page. To swap images, replace the picsum URLs with your own.

## Must keep unchanged (do not modify)

- **Font imports**: `@font-face` loading the Alimama DaoLiTi woff2 URL (do not change the font source)
- **CSS variable system**: light/dark dual themes
- **All JS**: theme toggle, view-mode toggle, hover-row interaction, rotating credit, detail-page hash routing `applyRoute()`, `renderDetail()`
- **`<script id="works-data">`** node must be kept
- **`<main id="detail-root">`** must be kept (detail-page mount point)
- **`body[data-view="home/detail"]` and `body[data-mode="list/gallery"]`** state system
- The five fixed-position elements **#logo / #main-menu / .theme-toggle / #project-view / #svp-credit**

## Pitfalls checklist

- **Slug mismatch**: list item `#work/kong-shan-ji` ↔ gallery item `#work/kong-shan-ji` ↔ JSON `"slug": "kong-shan-ji"` — all three must be identical
- **JSON quotes**: quotes inside CJK content must be full-width corner brackets or curly `"..."`, not ASCII `"`
- **Too many gallery images**: max 6 per work; more breaks the layout
- **Overlong prose**: 80-150 characters per paragraph; past 200 the reading experience drops
- **list / gallery out of sync**: must contain the same works (one-to-one)
- **picsum seeds**: use `id/X` not `seed/X`, avoiding random IDs that hit deleted images
- **Fewer than 3 works**: fine; 2 is the minimum to run
- **More than 8 works**: consider two batches; too many list rows lengthen the page
- **Drop cap**: the detail page's `.detail__prose p:first-of-type::first-letter` uses the DaoLi face — the first paragraph must start with a CJK glyph (not with `<em>` or an English letter)
- **Don't kill the color**: images should stay in color; don't add `filter: grayscale()` in CSS
