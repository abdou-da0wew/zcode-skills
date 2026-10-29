---
name: chinese-typography
description: Use when making Chinese typesetting decisions. Covers type area / margins / font size / weight / letter spacing / line spacing / line length / paragraph indent / punctuation spacing / grid systems / font selection and pairing / mixed horizontal-vertical writing / title line breaking / em dash / fullwidth vs halfwidth / kinsoku (line-start and line-end rules). Trigger scenarios: book typesetting, long-form/article pages, PDF reports, H5/posters, PPT/Keynote, web body text, catalogs, prospectuses, PRD/technical documents, classical Chinese texts, official documents, invitations, museum catalogs, or any "the Chinese reading experience feels off" diagnosis and fix.
---

# Chinese Typography

The "modulus → grid → type area (banxin) → text shaping" methodology. Core idea in one sentence: **tie every spatial element of a page (type area, margins, font size, line spacing, letter spacing) to a single common modulus (a gene)**, so that order exists visibly and invisibly.

> **The grid = the tool's rationality; the rhythm = the designer's use of the grid. Beauty matters more than mechanically obeying the grid.**

## When to activate this skill

- The user asks you to "lay out a page / make a document / tweak styles / design an H5 / write a formal PDF / do a classical-text style / set official documents", and the text is mainly Chinese
- The user says "this page looks messy / hard to read / unprofessional / not like a publication / too cramped / lines too long / titles break strangely"
- The user works on long-form Chinese styles in CSS / Tailwind / InDesign / Figma / PPT / Keynote / Word / Typst / LaTeX
- The user asks "what font size / what line spacing / how wide a column / how much whitespace / horizontal or vertical / how should titles wrap"
- The user wants a "most beautiful Chinese books" style, publishing-house style, museum-catalog style, academic style, business-report style, or classical/calligraphic design

## Before triggering, ask yourself 3 directional questions

1. **Horizontal or vertical?** Classical-text modern translations, literary Chinese, poetry, invitations, traditional calligraphy collections, some museum-catalog inner pages → consider vertical first; modern long-form, textbooks, business documents → horizontal.
2. **Mixed writing?** Vertical embedded in horizontal (titles/plaques, couplets, quotation shaping) and horizontal embedded in vertical (Western terms, numbers, figure captions) are standard techniques, not "breaking the rules" — they are basic grammar.
3. **Regional style?** Mainland Simplified (horizontal punctuation sits bottom-left, vertical top-right, Kaiming-style punctuation) / Hong Kong-Taiwan Traditional (centered punctuation, kinsoku may be relaxed) / Japanese (punctuation bottom-left/top-right, strict kinsoku). The differences are mainly punctuation placement and kinsoku strictness — never mix them.

See `reference/directions.md` for details.

## The nine most critical rules (by importance)

### 1. Decide writing direction first; every type-area decision follows
- **Vertical**: text top→bottom, lines right→left; pages turn right-to-left, bound on the right; figure/table captions to the sides; pause punctuation (ideographic comma, full stop, semicolon, colon) sits top-right; quotation marks use corner brackets (U+300C/U+300D, U+300E/U+300F)
- **Horizontal**: text left→right, lines top→bottom; pages turn left-to-right, bound on the left; figure/table captions above/below; Mainland pause punctuation sits bottom-left; quotation marks use curly quotes (U+201C/U+201D, U+2018/U+2019)
- **Mixed**: a 1-letter English word/abbreviation inside vertical text → **set upright**; 2–3 digit numbers → **tate-chu-yoko** (horizontal-in-vertical); whole Western paragraphs → **rotate 90° clockwise**
- Do not apply Japanese punctuation rules to Chinese (e.g. a colon rotating 90° to lie down is a Japanese convention; in Chinese it stays upright)

### 2. Break titles by word, not by character count
**The most common user-facing pitfall.**
- Body text: break by character by default, not by word; ~60% of Mandarin words are disyllabic, and word-based breaking makes ragged zigzag lines.
- **Titles: must break by word**, otherwise ambiguity appears (classic bad example: "Foreign ministry strongly condemns the Iraq / embassy bombing incident" — the break makes it read as "Iraq embassy").
- Function-word taboos: the possessive particle *de* must not start a line; conjunctions meaning "and / or" must not end a line; place names, personal names, book titles, and terms must never be split.
- A title's line count must be an integer multiple of the body line height: level 1 takes 4–5 lines, level 2 takes 2–3 lines, level 3 takes 1–2 lines, a two-part title takes 3 lines.
- A major title must appear on an odd page (horizontal left-turning book = right page / vertical right-turning book = left page).
- In HTML, add `<wbr>` or `<br>` manually to control break points; for characters CSS must not break between, use `&#8288;` (U+2060 WJ).

See `reference/title-and-breaking.md` for details.

### 3. Fix the modulus first, then everything else
All font sizes, line spacing, margins, and type-area dimensions must be integer multiples of one modulus (typically 1.5pt or 0.5pt). The modulus runs through the whole document like a gene.
- Beginner default: **modulus = 1.5pt**, body 9pt (= 6×1.5pt), captions 6pt, subheads 12pt
- Never use a decimal "golden ratio" modulus like 1.618pt — Han glyphs are fixed-width squares; multi-digit decimals make cell widths impossible to reconcile
- For 1–5pt sizes use 0.5pt steps; for 6–12pt use 1pt steps (divisibility inherited from the metal-type era)

### 4. Line length must be an integer multiple of font size
**This is an explicit requirement of the W3C "Requirements for Chinese Text Layout" §2.3.5, not a suggestion.**
- Formula: `line length = font size × character count`; a non-integer multiple causes abnormal letter spacing on justified last lines (a mis-set signal).
- **Horizontal body text: 17–40 characters is best, hard cap ≤48; vertical body text ≤55; minimum line length ≥10 characters** (below 10, wrapping is too frequent and fatiguing).
- In CSS: `max-width: 30em` is the most reliable guardrail for Chinese (Latin is 65–75 characters ≈ 35em).
- To widen the page, add columns — never stretch the line indefinitely.
- Frame height formula: `height = (line count − 1) × line height + font size`; the last line only occupies the font-size height; do not round the height to whole mm.

### 5. Line spacing = 50%–100% of font size (i.e. 1.5–2× line height)
- W3C standard: line spacing (inter-line gap) = 50%–100% of font size, **corresponding to a line height (including the glyph itself) of 1.5–2×**.
- Comfortable on modern screens: `line-height: 1.5`; long-form/literary: 1.7–2.0; dense tables: 1.33.
- **Above 100% of font size adds no readability** (i.e. line-height beyond 2); too narrow (< 1.2) feels dense; too wide (> 2.2) breaks section cohesion.
- For vertical text with ruby annotation, **line spacing ≥ 1.5× base glyphs**.
- When proper-name marks / emphasis dots / book-title marks (style A) sit between lines, single-sided binding needs spacing ≥ 1/2 font size, double-sided ≥ 5/8 font size.

### 6. Type area sits slightly high; tight inside, loose outside; tight top, loose bottom
- Horizontal books: move the type area **slightly upward** for the best visual position
- Facing pages (book/PDF): **gutter (inner) < fore-edge (outer) < head (top) < foot (bottom)** (typical ratios 3:5:8:13 or 2:3:5:8)
- Vertical facing pages invert head/foot: head < foot (same as horizontal), but gutter (right side of the right page / left side of the left page) < fore-edge
- Margins too small make text "rush at the reader" and feel oppressive; the type area is the negative shape whose whitespace decides elegance
- **Fix the type area first, then the whitespace** (the Chinese method) — not the Western "reserve margins first, and the type area is what's left"

### 7. Letter spacing: leave it alone by default (solid setting)
- Modern Chinese fonts have face ratios of 92%–96%; space between characters is already built in; **do not add letter-spacing to body text**
- CSS: `letter-spacing: 0` (do not set "delicate-looking" values like `0.05em`; it breaks the size rhythm)
- Add tracking deliberately only for titles, logos, or emotional spatial expression
- Legitimate loose-setting scenarios: balancing titles, balancing captions, short poetry, children's books; common values 1/4 em, 1/3 em, 1/2 em, 1 em

### 8. Choose weight and size together; control paper/screen contrast
- Small text (6–7.5pt print / < 14px screen): medium weight (Regular / 55S) is most legible; avoid ultra-thin weights
- Large text (≥ 9pt print / ≥ 16px screen): Light / 45S can achieve elegance
- Screen dark-on-white needs ≥ 4.5:1 contrast (WCAG AA); on paper, ask "does the ink outweigh the paper"
- Within one text block use different weights of a single family — never mix 4 typefaces
- **Minimum body size floor**: W3C specifies size 6 = 7.875pt (≈ 2.8mm); below that Han glyph structure becomes hard to discern

### 9. Punctuation width must follow the "additive model", with strict kinsoku
**The biggest overlooked problem in horizontal Chinese.** Mainland defaults to Kaiming style (fullwidth at sentence end, halfwidth within sentences); Hong Kong/Taiwan default to centered; end-of-line punctuation is always halfwidth (GB/T 15834-2011 §5.1.10).
- Pick one punctuation style for the whole document: **fullwidth / halfwidth / Kaiming / centered** (see `reference/punctuation.md`)
- Additive model: punctuation = halfwidth glyph + added gap; what you adjust is the gap, not the glyph face. InDesign / QuarkXPress / JIS all work this way.
- Kinsoku is mandatory: **basic level = the minimum** (line-start: no pause commas, full stops, colons, semicolons, exclamation/question marks, or closing quotes/brackets/book-title marks; line-end: no opening quotes/brackets/book-title marks); formal Chinese publishing uses **GB level / strict level**
- Line-start forbidden: ideographic comma (U+3001), fullwidth full stop (U+3002), fullwidth semicolon/colon/question/exclamation (U+FF1B U+FF1A U+FF1F U+FF01), ellipsis (U+2026), em dash (U+2014), closing paren/bracket (U+FF09), closing corner quotes (U+300D U+300F), etc.; line-end forbidden: opening paren (U+FF08), opening angle book-title mark (U+300A), opening corner quotes (U+300C U+300E), open double quote (U+201C)
- Indent the first line of paragraphs 2 characters (`text-indent: 2em`); no blank line between paragraphs; block quotes indent 4 characters
- Inseparable pairs: em dash / ellipsis / digits within a number / number + unit / super-subscript + annotated word / Western words must never be split by a line break

See `reference/punctuation.md` for details.

## Expressive techniques (beyond rigor: give Chinese layouts highlights and rhythm, not flatness)

The nine rules above guarantee "**set rigorously, professionally, without amateur tells**". But rigor is not brilliance — a compliant yet flat long-form page, with body + titles + paragraphs laid out in an even wash, no visual hammer, no rhythm, is exactly the familiar "Chinese typesetting is boring" result. For **long-form / editorial pages / posters / catalogs / official-account layouts / any Chinese page that wants design presence**, while keeping the nine rules, deliberately use the techniques below to create highlights (pick 1–3 by content; do not pile them all on):

- **Extreme title-size contrast.** Pull body and main title 3–5× apart (body 16px → main title clamped to 48–96px+), making the title the visual hammer rather than "slightly bigger body text". Han square glyphs have enormous tension at large sizes — dare to scale up.
- **Weight contrast creates focus.** Within one screen use three tiers — "ultra-bold display + regular body + light auxiliary info" — for hierarchy; avoid stacking many weights in Chinese, 2–3 tiers is enough, but dare to contrast.
- **Drop caps / opening ornament.** Open an article or chapter with a drop cap (2–3 lines tall) or an enlarged opening sentence, giving reading a clear "entrance ritual".
- **Horizontal-vertical mixing as shape.** Embed a vertical title/quote/chapter name inside horizontal body text (see rule 1) — a shaping grammar unique to Chinese. A vertical title hugging the margin, or a vertical short quote as a side rail, instantly reads as "Chinese design" rather than a "translated webpage".
- **Quote / golden-sentence shaping blocks.** Pull a key sentence out and enlarge it into an independent shaped block (large size, whitespace, or punctuation ornament), serving as the rhythm pause and memory point of long-form — not buried inside a paragraph.
- **Large type / numbers as the layout's subject.** Posters, chapter pages, and data pages can let one line of huge type or one big number occupy most of the viewport, with body text demoted to support — the text itself is the picture.
- **Rhythm: alternate fast and slow.** Title/quote/plate zones are "slow, heavy, large"; body zones are "fast, light, dense"; use alternation of size and whitespace to create page-turning rhythm instead of one density throughout.

The floor: **these techniques serve content and readability, not showing off**. Expressiveness builds on the nine rigorous rules — set it right first, then make it shine; size contrast and mixed-direction shaping must never break kinsoku, line-length modulus, or type-area order. Scenes that need restraint (official documents, formal report body) stay quiet; scenes that should shine (editorial long-form, posters, brand content) use these actively.

## Design philosophy to read before using

1. **The grid is a tool, not shackles**. The Swiss school's "constructive design that can be analyzed and understood" — a grid lets the most ordinary typesetting shop produce elegant pages, but **excellent work always "breaks the grid" at the right moment**
2. **Intuition is disguised memory** — only trained intuition works; beginners obey rules strictly, veterans then break them consciously
3. **Positive vs negative shape**: the type area is the positive shape; margins are the negative shape, and the negative shape can even take priority over the positive as the basis of aesthetic judgment. **Whitespace is not emptiness; it is design**
4. **One book, one universe**: grandeur comes from precise details. "Small things" like punctuation spacing and line-spacing values are the core of reading comfort
5. **The tension between rational architecture and spiritual poetry**: Chinese typesetting needs both the rationality of Euclidean geometry / Fibonacci sequences and the spirituality of "metrical beauty"
6. **Foundational concepts must not be violated, major principles should not be violated, multiple options are built into a self-consistent logic by priority** (the "Peacock Plan" ordering)
7. **Type design ≠ typography**. This skill covers the latter; do not get drawn into debating whether a typeface itself is good — manage "how it is used"

## Standard workflow (works for any medium)

Decide in this order; do not skip steps:

1. **Writing direction**: horizontal / vertical / mixed; regional style (Mainland / HK-TW / Japanese)
2. **Page format / canvas**: paper in millimeters, screen in px; common aspect ratios 2:3 / 3:4 / 16:9 / 5:8
3. **Body font size**: print 9pt / screen 16px / H5 depends on viewing distance
4. **Modulus**: usually body size ÷ 6 or ÷ 4 (body 9pt → modulus 1.5pt; body 16px → modulus 4px)
5. **Build the type area**: page = body size × integers (e.g. 60 chars wide × 90 chars high = 540×810pt). **Type area first, whitespace after**
6. **Set margins**: set left/right/outer/head as modulus multiples, respecting "tight inside, loose outside; tight top, loose bottom"
7. **Compute columns**: 17–40 characters per column (column gap also a modulus multiple, commonly 2 characters = 18pt)
8. **Set line spacing**: font size × 1.5–2, and a modulus multiple
9. **Define the size system**: title / subhead / body / caption / footnote / page number — all modulus multiples; title line count must be a body line-height multiple
10. **Choose fonts**: one family, multiple weights; pick serif/sans and Song/Hei/Kai/FangSong to match the content's temperament
11. **Set punctuation style**: fullwidth / halfwidth / Kaiming / centered, consistent throughout
12. **Set type + check punctuation spacing + check line wraps + check title breaks + check text gray evenness + check orphans and singles**


## Font-selection routing (do not pick fonts in this file)

This file owns the Chinese typesetting baseline: type area, line length, line spacing, paragraphs, punctuation, title breaking, reading gray. **Do not choose specific display fonts from this file.**

Font selection is handled in two tiers:

```text
Ordinary Chinese web / UI / H5 / prototype body text
→ use the safe system font stack; do not read `reference/fonts.md`

Fonts materially shape the visual direction, or a named / uploaded / OSS / CDN font is needed
→ you must read `reference/fonts.md`
```

When font selection is needed, read `reference/fonts.md`: §1 Choose fonts (temperament → font table) → §2 Loading execution (including §2.5 assembling font-family). Both choosing and loading happen in that file; do not split them into extra files.

### Safe default font stack

For ordinary Chinese web, UI, H5, form, dashboard, and tool-page body text, use the system Chinese font stack by default. The Chinese font must come before the Latin fonts, protecting Chinese punctuation, em dashes, ellipses, and fullwidth symbols.

```css
font-family: "PingFang SC", "HarmonyOS Sans SC", "Noto Sans CJK SC",
             "Microsoft YaHei UI", "Microsoft YaHei",
             system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
```

Do not use display, calligraphic, game, or strongly decorative fonts for body text. Titles may have more character, but must first go through the scenario filter in `reference/fonts.md`.

After choosing a specific font from `fonts.md` (especially when a separate Latin font is specified for English), assemble `font-family` strictly per `reference/fonts.md §2.5`: **on pages containing Chinese, an explicit CJK font name must appear in `font-family`, and a Latin font must never be followed directly by `system-ui`** (otherwise the Chinese fallback is uncontrolled).

### When you must read `reference/fonts.md`

If any of the following hold, do not pick fonts by feel in this file — read `reference/fonts.md`:

| Trigger | Why fonts.md is required |
|---|---|
| Covers, posters, Xiaohongshu, official-account header images, PPT covers, event pages, key visuals | The title font directly decides visual temperament |
| The user gives font-related style words: techy, industrial, literary, classical, academic, magazine, premium, formal, official-document, bookish, handcrafted | These are not typesetting baseline; they are font-scenario choices |
| The user explicitly mentions fonts, glyph shapes, type feel, Song, Hei, Kai, FangSong, title faces, display faces | This is now a font-selection task |
| A named font, uploaded font, OSS font, CDN font, `@font-face`, or self-hosted font is needed | You must confirm loadability and fallback |
| Long-form, reports, official accounts, white papers, publication-feel pages where the font affects reading temperament | You must choose among Song/Hei/Kai/FangSong and weigh face ratio |
| Brand pages, product launch pages, portfolios, content pages that need a visible font personality | The font is a style source; the system stack alone will not do |
| The current visual direction would visibly change with the font choice | Jumping from this file's default stack straight to a display font is not allowed |

### When not to read `reference/fonts.md`

The safe system font stack is enough when:

- ordinary product UI, dashboards, admin panels, forms, tool-page body text;
- the user has no font/style demand and fonts will not visibly change the visual direction;
- the design system or template already provides an explicit font scheme;
- the task is only local spacing, line height, line breaking, punctuation, or type-area adjustment.

### OSS / test font loading

Do not pick fonts directly by name or URL. First complete the scenario filter in `reference/fonts.md §1`; if the chosen font needs real loading, use the URL table and `@font-face` templates in `§2` of the same file, and assemble font-family per `§2.5`.

## Common errors and diagnosis

| Symptom | Cause | Fix |
|---|---|---|
| "Looks cramped, tiring" | Line length > 48 chars or line spacing < 1.3 | Narrow the type area / raise `line-height` to 1.5–1.7 |
| "Looks empty, loose" | Line spacing > 2.0 or size too small | Tighten line spacing, or step size up once |
| "White blocks / moth-eaten feel in the page" | Consecutive fullwidth punctuation not squeezed | Enable InDesign Chinese typesetting settings / CSS `text-spacing-trim` |
| "Too many sizes, chaotic" | Sizes not on one modulus | Rebuild the size system; every size = modulus × integer |
| "Hierarchy unclear" | Size ratio < 1.5× or weight gap too small | Increase size ratio or change weight; don't prop hierarchy with color |
| "Margins look wrong" | All four sides equal width | Change to increasing inner < outer < top < bottom |
| "Title breaks nonsensically" | Breaking by character count, tearing words apart | Manual `<wbr>` between words; never break before the particle *de* or after "and" |
| "Last-line spacing wildly large or small" | Line length not a size multiple + justification | Recompute `width = font size × character count` |
| "Em dash splits in two" | Two `—` glyphs without no-break set | InDesign: add to the "inseparable" set / CSS: add `&#8288;` |
| "A single character plus a period on the previous line" | An orphan character forms a line | Squeeze into the previous line / distribute the last line / rewrite to drop a character |
| "Page header is one line (last line of previous section)" | A widow line lands alone on a page | Adjust the previous page / delete or add characters |
| "Numbers lie sideways in vertical text" | tate-chu-yoko not used | 2–3 digit numbers use tate-chu-yoko; 4+ digits rotate as a whole |


## Reference files (read by condition; the 1–3 most relevant)

| Trigger | Read this file | What it covers |
|---|---|---|
| Manual line breaking needed for titles/covers/posters/PPT/Xiaohongshu titles | `reference/title-and-breaking.md` | Title breaking, line occupation, body line breaking, inseparable pairs, orphans and singles |
| Long-form/reports/official accounts/official documents/publications, punctuation-dense, em dash/ellipsis/quote/book-title-mark problems | `reference/punctuation.md` | Kinsoku, punctuation styles, additive/subtractive models, em dash, ellipsis, inline squeeze/stretch |
| Diagnosis of size/line spacing/tracking/paragraphs/text gray/screen reading comfort | `reference/text-detail.md` | Font size, weight, tracking, line spacing, paragraph indent, ruby annotation, text gray |
| Font selection, display fonts, brand fonts, title fonts, formal report fonts, loadable font testing | `reference/fonts.md` | §1 Choose fonts (temperament → table) → §2 Loading execution; do not pick fonts directly from this file |
| Complex layouts/long-form reports/PDF/catalogs/columns/type area/modulus/grids | `reference/grid-system.md` | Modulus, type area, grids, column widths, key CLReq values (web/H5/deck borrow only modulus and reading logic) |
| Vertical/mixed writing, poetry, classical texts, invitations, traditional Chinese, regional differences | `reference/directions.md` | Horizontal/vertical/mixed writing, binding direction, CSS writing-mode, regional style differences |
