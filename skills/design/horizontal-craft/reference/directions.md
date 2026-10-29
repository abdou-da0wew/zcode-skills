# Text Direction: Horizontal / Vertical / Mixed

Chinese is one of the few scripts in the world that runs **two parallel typesetting systems, horizontal and vertical**. "Which direction?" is the first decision of any Chinese typesetting project, not a default to horizontal. This file gives the direction decision tree, a parameter comparison, CSS implementation, and regional style differences.

## 1. Direction decision tree

```
What are the content's dominant attributes?
│
├─ Classical texts / literary Chinese / poetry / calligraphy collections / inscriptions / couplets ────→ Vertical
├─ Invitations / ceremony documents / letters with a vintage feel ──────────────→ Vertical
├─ Museum catalogs / art books' "poem-title-painting-colophon" pages ────────────→ Vertical
├─ Magazines / newspapers / textbooks / academic papers / business documents ───────→ Horizontal
├─ Modern novels / essays / web pages / H5 / App ───────────────→ Horizontal
└─ Reference books / dictionaries ───────────────────────→ Horizontal (vertical editions mostly found in old Republican-era prints)

Is mixed writing needed?
│
├─ A 1-letter English word/abbreviation inside vertical text ────→ Upright setting (single glyph stays horizontal)
├─ 2–3 digit Arabic numerals inside vertical text ───→ Tate-chu-yoko (a small horizontal group)
├─ A whole Western word/phrase/paragraph inside vertical text ───────→ Rotate 90° clockwise
├─ A small vertical annotation inside vertical text ──────────→ Double-line interlinear note (two parallel note lines, half font size)
├─ A vertical title/plaque inside horizontal text ──────→ Local writing-mode: vertical-rl
└─ A short vertical poetry quote inside horizontal text ───→ Local vertical block ("transplant style")
```

## 2. Horizontal vs vertical parameter comparison

| Dimension | Horizontal | Vertical |
|---|---|---|
| Text direction | Left → right | Top → bottom |
| Line direction | Top → bottom | **Right → left** |
| Page-turn direction | Left to right (**bound on the left**) | Right to left (**bound on the right**) |
| Front-page position | Right page (odd pages) | Left page (odd pages) |
| Column split direction | Vertical cuts (left/middle/right columns) | Horizontal cuts (top/middle/bottom columns) |
| Figure/table caption position | Above / below | Left / right |
| Table header row position | Top | Right |
| Table header column position | Left | Top |
| Last-page multi-column line counts | Align columns; leftover space at the end of the last column | Let it end naturally; column line counts may be uneven |
| Line-length cap | ≤ 48 characters | ≤ 55 characters |
| Line-length floor | ≥ 10 characters | ≥ 10 characters |
| CSS writing-mode | `horizontal-tb` (default) | `vertical-rl` |

## 3. Punctuation differences in horizontal/vertical (Mainland GB/T 15834-2011)

**Key differences. Mismatches make a layout look instantly amateur.**

| Punctuation | Horizontal (Mainland) | Vertical (Mainland) | HK/TW |
|---|---|---|---|
| Full stop (U+3002) | Bottom-left of glyph face | Top-right of glyph face | Centered |
| Comma (U+FF0C) | Bottom-left of glyph face | Top-right of glyph face | Centered |
| Ideographic comma / dunhao (U+3001) | Bottom-left of glyph face | Top-right of glyph face | Centered |
| Colon (U+FF1A) | Bottom-left, upright | **Upright, shifted right** (not rotated 90°) | Centered, upright |
| Semicolon (U+FF1B) | Bottom-left, upright | **Upright, shifted right** (not rotated 90°) | Centered, upright |
| Question mark (U+FF1F) | Bottom-left, upright | **Upright** (not rotated 90°) | Centered, upright |
| Exclamation (U+FF01) | Bottom-left, upright | **Upright** (not rotated 90°) | Centered, upright |
| Double quotes | Curly quotes (U+201C/U+201D) | **Corner brackets (U+300C/U+300D)** | Corner brackets |
| Single quotes | Curly quotes (U+2018/U+2019) | Corner brackets (U+300E/U+300F) | Corner brackets |
| Book-title marks | U+300A/U+300B, U+3008/U+3009 | U+300A/U+300B (upright) | Style A wavy underline (Taiwan) / Style B U+300A/U+300B |
| Em dash | —— spans 2 cells, horizontally centered | **spans 2 cells, vertically centered** | Same |
| Ellipsis | …… spans 2 cells, 6 dots horizontal-centered | spans 2 cells, 6 dots **vertically centered** | Same |

**Counter-examples (avoid)**:
- Applying Japanese rules to Chinese vertical text: Japanese vertical colons/semicolons/question marks/exclamations rotate 90° and lie down; **in Chinese they must stay upright**. One macOS release once rendered Chinese like Japanese due to early Unicode UAX#50 immaturity — a documented mistake.
- Using curly quotes (U+201C/U+201D) in vertical body text (switch to corner brackets U+300C/U+300D).

## 4. Three methods for Western text inside vertical (W3C CLReq §2.1.3)

When vertical text meets Western words/numbers, choose by length:

### Method 1: Upright
- For: **single letters, initialisms** (e.g. GDP, CPU, A)
- Method: use a monospaced-for-Han font or fullwidth characters; set letter by letter in the same direction as the Han glyphs
- CSS: `text-orientation: upright`
- Example: `one G D P growth…` (G, D, P each occupy one cell, same direction as the Han glyphs)

### Method 2: Rotated 90° clockwise
- For: **ordinary words / sentences / numbers of 4+ digits** (e.g. "JavaScript", "2024", "the quick brown fox")
- Method: proportional font; rotate the whole word or sentence
- Gap between Han and Western text **≤ 1/4 Han width**; when Western text sits at line start/end, **add no extra whitespace**
- CSS: `text-orientation: sideways` (the default behavior)

### Method 3: Tate-chu-yoko (horizontal-in-vertical)
- For: **2–3 digit Arabic numerals, short abbreviations** (e.g. "3.0", "A+", "2B", "21", "AM", "99")
- Method: proportional font kept in normal horizontal orientation; width ≈ one line pitch or slightly wider
- In the metal-type era it strictly never exceeded 1 Han width; today it may protrude slightly into the line gap
- CSS: `text-combine-upright: all`
- Example: age `21`, a `3.0`-liter engine, temperature `25` °C

### Mixed-writing spacing rules (vertical same as horizontal)
- Vertical text **normally avoids curly quotes** (use corner brackets instead)
- If quoting Western text with curly quotes, the quotes rotate with the quoted text
- In vertical text, Arabic numerals must not split across lines; em dashes/ellipses must not split

## 5. Vertical embedded in horizontal

Scenarios where modern horizontal documents embed small vertical blocks:

- Titles / plaques / calligraphic inscriptions
- Classical poetry quotes (a full quatrain set vertically to strengthen the classical feel)
- Couplets (two vertical strips shown in parallel)
- Seals, leisure seals, colophons
- Magazine feature "interleaved" pages

**CSS implementation**:
```css
.vertical-quote {
  writing-mode: vertical-rl;       /* vertical: lines run right to left */
  text-orientation: mixed;          /* Han glyphs upright, Western rotated */
  height: 20em;
  margin: 0 1em;
}
```

**Notes**:
- A vertical block inside horizontal text must be "given a container" — set an explicit height; don't let it stretch freely
- Vertical punctuation must switch to the top-right forms; never reuse the horizontal forms directly
- Embed at "semantic pauses" — between sentences, not between words

## 6. Binding and page-turn direction

Binding direction directly affects type-area position and reading experience; never get it backwards.

| Direction | Binding side | Page turn | First page (front) position | Used for |
|---|---|---|---|---|
| **Horizontal, left-turning** | Left | Left to right | **Right page** (odd pages) | Modern Chinese books, textbooks, reports, all English books |
| **Vertical, right-turning** | Right | Right to left | **Left page** (odd pages) | Classical texts, literary Chinese, poetry collections, traditional calligraphy collections |
| **Vertical, left-turning (wrong)** | Left | Left to right | — | Used in none of China/Japan/Korea |

**Key checks**:
- Major titles must open on the **front page** (right page for horizontal / left page for vertical), never on a verso
- When a chapter's final page leaves whitespace, the whitespace direction matches reading direction (below for both horizontal and vertical)
- Cross-spread images: horizontal left page extends rightward; vertical right page extends leftward

## 7. Complete CSS writing-mode guide

```css
/* Horizontal (default) */
.horizontal {
  writing-mode: horizontal-tb;     /* horizontal, top-to-bottom */
}

/* Vertical (Chinese, Japanese, traditional Mongolian) */
.vertical {
  writing-mode: vertical-rl;       /* vertical, right-to-left lines */
  text-orientation: mixed;          /* Han upright, halfwidth Western rotated 90° */
}

/* Vertical but lines run left-to-right (rare; some new Mongolian) */
.vertical-lr {
  writing-mode: vertical-lr;
}

/* Force single characters upright inside vertical (abbreviations, single letters) */
.upright {
  text-orientation: upright;
}

/* Tate-chu-yoko (small number groups stay horizontal) */
.tcy {
  text-combine-upright: all;
}
```

Full HTML example (pinyin transcription of Li Bai's "Quiet Night Thoughts" — substitute the real Chinese text in production):
```html
<article style="writing-mode: vertical-rl; height: 30em;">
  <p>
    chuang qian ming yue guang, yi shi di shang shuang.
    ju tou wang ming yue, di tou si gu gu-<span style="text-combine-upright: all;">21</span>-xiang.
  </p>
</article>
```

## 8. The three regional style systems

An index table of regional differences — lock one region per project and align each dimension below. Execution details live in the corresponding files: punctuation in `punctuation.md`, fonts in `fonts.md`, kinsoku in `punctuation.md §4`.

| Dimension | Mainland Simplified | HK/TW Traditional | Japanese |
|---|---|---|---|
| Punctuation position | **Horizontal: bottom-left; vertical: top-right** | **Centered** (same in both directions) | Horizontal bottom-left, vertical top-right (same as Mainland) |
| Kinsoku strictness | GB level / strict level | Usually relaxed (centered punctuation never looks abrupt) | Strict |
| Punctuation style | Mostly Kaiming style (fullwidth at sentence end, halfwidth within sentences) | Centered, widths mostly unadjusted | Kaiming style + strict squeezing |
| Vertical colon/semicolon | Upright, shifted right | Centered, upright | **Rotated 90°, lying down** |
| Quotation marks | Curly (horizontal) / corner brackets (vertical) | Corner brackets (single outside, double inside) | Corner brackets |
| Book-title marks | U+300A/U+300B, U+3008/U+3009 | Style A wavy underline + Style B U+300A/U+300B | Double corner brackets (U+300E/U+300F) |
| Middle dot · | **Half Han width** | **Full Han width** | Full Han width |
| Official-document font | **FangSong** | **Kai** | Mincho |

**Core discipline**: lock the regional style at project start; never mix Mainland/HK/TW/Japanese conventions.

## 9. When vertical? When horizontal?

### Must be vertical
- Facsimile editions of classical texts / modern translations that preserve the original look
- Literary-Chinese school textbooks (some Taiwan textbooks)
- Traditional medicine, Buddhist, Taoist scriptures
- Calligraphy collections, model-copybooks
- Traditional opera scripts (older editions)
- Vermilion-annotated memorials, replicated family letters

### Strongly recommend vertical
- Contemporary classical poetry collections
- Tea ceremony / incense / traditional painting books
- High-end art books' "poem-title-painting-colophon" pages
- Invitations / ceremony cards / thank-you cards (short passages)
- Some museum-catalog inner pages (mixed)
- Inscriptions / dedications / leisure seals

### Vertical optional (adds classical feel / ritual sense)
- Essay-collection covers
- Poster titles
- Tea packaging, baijiu packaging copy
- Wedding invitations
- Vintage-style cafe menus

### Do not use vertical
- Modern long-form (users are habituated to horizontal scanning)
- Table-dense documents (vertical tables are hard)
- Technical/academic content with heavy Chinese-English mixing
- Web body text (hard to write/read; poor ecosystem support)
- App / H5 (small screens strain vertical layouts)

## 10. Advanced mixed writing (horizontal-vertical crossover)

Never treat "mixed writing" as breaking the rules — it is basic Chinese typesetting grammar. Five common patterns:

### 1. Horizontal body + vertical quote
Body text horizontal; a quoted poem, couplet, or inscription set vertically as one block, forming a rhythm contrast with the body.

```html
<article class="horizontal-body">
  <p>Li Bai writes in "Quiet Night Thoughts":</p>
  <blockquote class="vertical-quote">
    chuang qian ming yue guang, yi shi di shang shuang.<br>
    ju tou wang ming yue, di tou si gu xiang.
  </blockquote>
  <p>This poem shows…</p>
</article>
```

### 2. Vertical body + horizontal data
Classical-text modern translations: body vertical, but chronologies, data tables, and map notes horizontal. Distinguished by paper/background color.

### 3. Spread "half horizontal, half vertical"
Left page vertical (the classical original), right page horizontal (the modern translation), compared page by page. Common in classical-text modern translations.

### 4. Vertical titles, horizontal body
Covers / chapter openers use vertical display titles for ceremony; inner-page body returns to horizontal for utility.

### 5. Double-line interlinear notes (small notes)
Inside vertical body text, insert interlinear notes: two note lines of equal height at half the body size, running in parallel. Standard equipment in classical editions.

```
TEXT│ Double-line note:
    │ upper note│ lower note
TEXT│ upper note│ lower note
    │
```

## 11. Checklist (direction-related)

Must pass before finalizing:

- [ ] Does the writing direction (horizontal / vertical / mixed) match the content's temperament?
- [ ] Does binding direction correspond to writing direction? (horizontal → left-turning; vertical → right-turning)
- [ ] Are major titles on the front page (right page for horizontal / left page for vertical)?
- [ ] Do numbers in vertical text use tate-chu-yoko?
- [ ] Do single English letters in vertical text use upright setting?
- [ ] Has vertical punctuation switched to the top-right forms?
- [ ] Do vertical colons/semicolons stay upright (not lying down Japanese-style)?
- [ ] Have vertical quotes switched to corner brackets (U+300C/U+300D)?
- [ ] Is the regional style consistent? (no mixing HK/TW centered punctuation with Mainland GB kinsoku)
- [ ] Do vertical blocks inside horizontal text have explicit heights?
- [ ] Do figure/table caption directions match the main writing direction?
- [ ] Are CSS `writing-mode` and `text-orientation` set as a pair?
