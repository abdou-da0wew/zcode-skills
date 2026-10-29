---
name: vr-canvas
description: Generate a single-file VR-style portfolio website — works are tiled on the inside of a 3D cylinder/sphere (concave wraparound, like an immersive headset), with mouse-controlled head tilt, long-press to drag and browse the infinite canvas, click to open work detail. Includes overlays for About / CV / Contact / Filter. Takes a natural-language description of the studio and works (images + brief copy); outputs ONE working .html file. Runs in BOTH local agent environments with a filesystem such as the DiveeOI agent (OpenCode-based) (writes to ~/Desktop) and plain online chat without a filesystem (outputs HTML inline). Trigger phrases: "make a VR portfolio", "make an infinite-canvas portfolio", "make a dome-wrapped portfolio", "vr-canvas-gen ...", or when the user drags this skill folder into chat asking for a wraparound/immersive portfolio site.
visibility: public
mode: template
carrier: web-page
scenario: portfolio
pattern_source: reference.html
source_priority: skill-first
triggers:
  - "make a VR portfolio"
  - "make an infinite-canvas portfolio"
  - "make a dome-wrapped portfolio"
  - "curved-screen portfolio"
  - "wraparound portfolio"
related_patterns: portfolio-detail, digital-eguide
legacy_gen: true
---

# vr-canvas — VR curved-screen portfolio generator

## When to trigger
The user says "make a VR portfolio" / "make a dome / curved-screen / wraparound portfolio" / "make an infinite-canvas portfolio" / "vr-canvas-gen ..." and provides:
- **Work files** (images, a folder path or several file paths) — in chat mode, a description may suffice
- **Natural-language description** (studio intro + the story of each work — prose is fine, no need to be structured)

## Input parsing
Extract from the user's message:
- **works_path** (required in Mode A): work folder path or a set of file paths
- **bio_text** (required): studio self-introduction + background per project. May include: studio name, city, field, founding year, team, client types, and each work's story
- **Style variant** (optional): default is the dark "material/studio" mood; if the user says "light / magazine / cyber / minimal", adjust the `:root` palette

If the user only says "make a VR portfolio" without works → **ask once** for the works and the studio name.
Works given but no description → **don't follow up**; infer titles and categories from filenames/visual content.

## Runtime environments (two modes)

### A. Local agent such as DiveeOI (has a filesystem)
- Use `Bash` to list files, `sips` to probe sizes, `cp` to copy images
- Output to `~/Desktop/{slug}-vr-canvas/index.html` + `images/`
- Images use relative paths `images/work-NN.jpg`
- The template ships with `images/p-01-color-macro.jpg ... p-18-magazine.jpg` — 18 design-oriented real photos (≈2.2MB); if the user provides no images, just open template.html to see the full VR sphere effect

### B. Online chat (no filesystem)
- You **output exactly one complete HTML string** (wrapped in a ```html code block)
- User uploaded images but gave no URLs → use `https://picsum.photos/seed/{description-NN}/1080/1080` placeholders
- User gave URLs → use `<img src="https://...">` directly
- Do not try to access local files; do not suggest command-line operations (other than "save this as index.html")

Decision rule: **if you cannot Read local images** → default to Mode B.

## File roles

| File | Role | How to use it |
|---|---|---|
| `reference.html` | **Complete finished piece** (Xubai studio, 20 works + full about/cv/contact/filter copy) | Read for: tile copy tone, tag vocabulary, desc length, about/cv information density, overall mood |
| `template.html` | **Empty skeleton** (same CSS/JS, 2 samples + all SWAP markers) | Build on it to produce the final HTML |

**Core rule**: all edits are based on `template.html`; learn **how to write like it** from `reference.html`, but do not copy its concrete content (Xubai, the Kyoto residency, the Aokicha tea room … — those belong to someone else).

## Workflow

### 1. Read both HTML files
- Read `template.html` first and locate the SWAP markers (12 total)
- Then skim `reference.html` to absorb the work copy and about/cv density and rhythm

**Do not change the JS, the .work / .frame / .sphere / .viewport / .overlay CSS, or any #sphere / #viewport / .splash logic**.

### 2. (Mode A only) List works + probe sizes
```bash
ls -la "{works_path}"
sips -g pixelWidth -g pixelHeight "{works_path}/{file}" 2>/dev/null
```

Per work, judge from filename + visuals (Read a few representative ones) → (title, brand, year, tags, desc).

### 3. Parse bio_text and extract

**Studio level** (every value has a default fallback):
- **STUDIO_NAME_CN / STUDIO_NAME_EN** (e.g. "Xubai / Void White", "Mingchuan / Bright River")
- **STUDIO_TYPE** (e.g. "design studio", "moving-image studio", "architecture office", "independent designer")
- **TAGLINE** (two lines: long sentence + short conclusion, cf. `Xubai is a design studio that works through material and situation, committed to finding the still point between brand, visual, and space`)
- **LOCATION_PRIMARY / SECONDARY** (e.g. "Shanghai, China", "Kyoto, Japan"; with only one city, drop the second line)
- **TIMEZONE_PRIMARY / SECONDARY** (e.g. "UTC+8"; JST/EST etc. for the second city)
- **YEAR_FOUNDED** (e.g. 2017)
- **CTA_TEXT** (default "Let's talk."; may become "Let's Talk", "Get in touch", etc.)
- **TAB_LABELS** (default `Works / About / CV`, editable)
- **CAPABILITIES** (4–5 capabilities for the about overlay)
- **TEAM** (3–5 members for the about overlay; a personal portfolio lists just yourself)
- **CV_YEARS** (project timeline grouped by year)
- **AWARDS** (3–8 exhibitions/awards)
- **CONTACT_EMAILS** (three addresses: new project / press / hiring)
- **OFFICE_ADDRESSES** (1–2 office addresses)
- **SOCIAL** (IG / WeChat / Twitter / Behance etc.)
- **FILTER_CATEGORIES / YEARS** (checkboxes for the filter overlay, derived automatically from WORKS)

**Per work**:
- **id** ('01'—'NN', two-character string)
- **brand** (client name, or "Personal project" / "Independent work")
- **title** (concise, 4–12 characters)
- **year** (YYYY number)
- **tags** (array, 1–3 single English words, e.g. Identity / Editorial / Web / Installation / Poster / Sound / Motion / Print / Type / Packaging / Exhibition / Light)
- **img** (cover, 1080×1080 square)
- **hero** (detail hero, 1600×1000 landscape)
- **g1, g2** (two detail images, 800×600)
- **desc** (one line, ~20–50 characters, shown as the detail-page subtitle)
- **long** (detail body, 2–3 paragraphs, 60–120 characters each)
- **spec** (4 key-value rows: `[['Client','xxx'],['Year','xxx'],['Scope','xxx'],['Duration / Pages / Edition','xxx']]`)

If bio_text is scattered with no concrete stories → **invent** brief narratives matching the overall mood, but **never fabricate client names** (write 'Personal' / 'Independent work' / `studio-initiated`).

### 4. WORKS count
- At least **8 works** (otherwise the sphere looks empty); below 8, repeat-fill: let `workFor()` loop with mod
- Cap **30 works** (more is pointless — the sphere repeats)
- Recommended **15–25**

### 5. Fill the 12 SWAPs

| SWAP | Location | Content |
|---|---|---|
| 1 | `<title>` | `{STUDIO_NAME_EN} — {STUDIO_TYPE} · Index {YEAR}` |
| 2 | `.brand-block` (top-left logo + text) | custom SVG logo or swap the mark; the "Sound [off]" chip may stay or go |
| 3 | `.tagline` (two lines, top center) | `{TAGLINE}` long sentence + `<br>` + short conclusion |
| 4 | `.col-meta` (top-right location) | 1–2 `<div class="row"><span class="loc-dot live"></span>{LOCATION}</div>` |
| 5 | `.col-times` (top-right timezones) | `UTC+8` etc. / leave `<div id="time1">` empty for JS to fill / leave `<div id="time2">` empty too |
| 6 | `.cta` button | `{CTA_TEXT}` |
| 7 | `.bottombar .tabs` | three `<button class="tab">` labels (default `Works / About / CV`) |
| 8 | `#overlay-about` | full about content: eyebrow + title + body + capabilities + team members |
| 9 | `#overlay-cv` | project timeline grouped by year + exhibitions/awards |
| 10 | `#overlay-contact` | emails / addresses / social / hiring — 6 contact-cells |
| 11 | `#overlay-filter` | three checkbox groups — category / year / client type (derived from your final WORKS) |
| 12 | `const WORKS = [...]` | the complete WORKS array |

### 6. Style variants (optional)

Default palette (dark "material / studio" mood):
```css
--bg: #0d0c0b;
--ink: #f0e9df;
--ink-soft: #8a8278;
--accent: #c89a5a;
```

If the user says:
- **Light / magazine** → bg `#f4f1ec`, ink `#1a1714`, accent `#8a4a1a`
- **Minimal white** → bg `#ffffff`, ink `#0a0a0a`, accent `#666666`
- **Cyber purple** → bg `#0a0612`, ink `#e8d8ff`, accent `#9b6dff`
- **Warm brown vintage** → bg `#1f1610`, ink `#e8d4b6`, accent `#c8895a`

Change only the four `:root` variables; do not touch layout / JS.

### 7. Write the file / output the HTML

**Mode A (local agent)**:
```
~/Desktop/{slug}-vr-canvas/
├── index.html
└── images/
    ├── work-01.jpg ... work-NN.jpg
    └── (hero / g1 / g2 use the same name with -hero / -g1 / -g2 suffixes)
```
slug: romanized studio name, hyphenated (xubai / mingchuan / li-ming).

**Mode B (online chat)**:
Output one complete HTML in the reply, wrapped in a ```html code block. All `<img src>` use picsum placeholders or user-provided URLs.

End the reply with one line:
> Save the block above as `index.html` and double-click to open. To swap images, replace `img / hero / g1 / g2` in the WORKS array with your own URLs.

### 8. Report

**Mode A**: one line — path + count + style.
> Generated ~/Desktop/xubai-vr-canvas/index.html — 18 works, dark "material" palette. Double-click to open; moving the mouse gives a VR head-turn feel, long-press and drag to browse other works, click for details.

**Mode B**: HTML code block + one line of usage notes.

## Must keep unchanged (absolutely do not modify)

- All JS (sphere projection / drag inertia / wheel zoom / hash routing / splash / time tick / mouse tilt)
- The CSS of `.work / .frame / .cell-head / .cell-foot / .num / .brand / .proj`
- The CSS and DOM structure of `.viewport / .sphere`
- `SPHERE_R = 1700 / STEP_DEG = 11 / ROW_HALF = 6` (core sphere-projection parameters; change R only for a stronger VR feel)
- The structure of `.overlay / .overlay-close / .info-pane / .info-section` (change text only, never classes)
- `mix-blend-mode: difference` on the topbar (core to the design language)

## Pitfalls checklist

- **Images**: `img` must be 1080×1080 square (the sphere cells are square); detail hero uses 1600×1000 landscape
- **Too few WORKS**: at least 8; if short, invent a few "independent work / experimental project" entries in the bio
- **Don't** write overlong `long` text for every work (300+ characters) — rhythm of white space matters more than information density
- **Don't** change the CJK serif stack like `font-family: "Noto Serif SC"` (it is the source of the atelier texture)
- **All three overlays (about / cv / contact) must be filled**: even if the user gave nothing, compose plausible content from the bio; never leave an overlay empty
- **filter overlay checkboxes** are decorative (no JS wired), but must derive from the actual WORKS categories and years
- **Personal portfolio** (not a studio): team lists one person; office addresses become "Independent · City of work"
