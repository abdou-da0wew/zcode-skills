# Text Typesetting Details

"The most fundamental aesthetics: easily ignored details and reading" — many layouts that look premium simply get all of these "small things" right.

> **This file covers**: font size / weight / tracking / line spacing / paragraphs / gray / Chinese-English mixing / widows and orphans / Ruby annotation.
> **Punctuation deep dive** (kinsoku / em dash / 4 styles / additive-subtractive models / squeeze-stretch priority): see `punctuation.md`.
> **Line-breaking deep dive** (title breaking / inseparable pairs): see `title-and-breaking.md`.

## 1. Type area: decides the reader's psychological pressure

The contrast between type-area position and margins is strong enough to "subtly shape the reader's taste".

- **Too full** (48 characters per line, 30 lines per page, small margins all around) → text "rushes at the reader", returning to the next line start is hard, fatiguing
- **Relaxed** (17–25 characters per line, margins increasing in proportion) → graceful, easy, pleasant

A layout with too many characters per line puts the reader under real psychological pressure: when wrapping, the eye struggles to find the next line's start, adding visual fatigue.

### Three laws of horizontal margins
1. **Tight inside, loose outside**: gutter (spine) < fore-edge (outer). Visual weight shifts outward.
2. **Tight top, loose bottom**: head < foot. Visual weight sits slightly high.
3. **Proportional increase**: commonly **2 : 3 : 5 : 8** or **3 : 5 : 8 : 13** (Fibonacci)

Most common ratio (horizontal books):
```
gutter : fore-edge : head : foot = 3 : 5 : 8 : 13
i.e. L3 + R5 + O8 + U13 (in characters)
```

### Web/H5 margin conversion
375px-wide H5 design canvas:
- Screen width 375; 20–24px left/right each; body type area 327–335px
- Top 24–32px, bottom 32–48px
- Module gaps use 16/24/32 (multiples of 4)

## 2. Letter spacing

**Core law: set body text solid; do not touch tracking.**

### Face ratio
How much of the em square the glyph actually fills. Modern fonts:
- HYXuanSong: 92%
- Founder YaSong: 94%
- HYShuSong: ~96%
- Founder ShuSong: 96%
- Source Han Sans: ~95%

A face ratio < 100% means **two glyphs set flush together already have natural spacing** — no extra tracking needed.

### Tracking rules
- **Body**: letter-spacing 0, solid
- **Titles** (≥ 24pt): may add 0.05–0.1em for composure
- **Display sizes** (≥ 40pt posters): may add 0.1–0.2em
- **Logos / single-glyph ornament**: tracking per design intent

### The 4 tracking modes (W3C terms)

| Mode | Tracking | Use |
|---|---|---|
| **Solid** | 0 | Default body |
| **Loose** | 1/4 em / 1/3 em / 1/2 em / 1 em | Balancing titles, balancing short captions, short poetry, children's books |
| **Evened** | Distributed by algorithm | Filling line length after kinsoku; uniform look for parallel list items |
| **Tight** | Negative | Magazine titles, ad copy with many characters squeezed into one line (**never for book titles or body**) |

CSS notes:
```css
/* Body area — don't touch */
.body { letter-spacing: 0; }

/* Large titles may add a little */
.headline { letter-spacing: 0.05em; }

/* Not like this */
.body-bad { letter-spacing: 1px; } /* breaks the size rhythm */
```

## 3. Line spacing

### Ratio ranges
| Ratio (size:spacing) | Feel | Use |
|---|---|---|
| 1 : 1.0 | Solid; metal-type-era standard | Dictionaries, newspapers (when lines are short) |
| 1 : 1.33 | Compact | Magazines, news |
| **1 : 1.5** | **Modern standard** | **Web body, business documents** |
| 1 : 1.7 | Comfortable | Long-form reading, technical documents |
| 1 : 2.0 | Airy | Literature, poetry, art-book captions |
| 1 : 2.5+ | Drifting; sections feel disconnected | Avoid |

W3C rule: **line spacing (inter-line gap) = 50%–100% of font size**; corresponding line height (including the glyph) = 1.5–2× the size. Beyond 100% adds no readability.

Beautiful metal-type-era layouts (e.g. periodical body around 1918) ran a size:spacing ratio between **1:1 and 4:3** — classic graceful examples.

### Practical values
- Print body 9pt → line spacing 12–18pt (default 18pt = 1:2, stately)
- Print body 10.5pt → line spacing 14–18pt
- Screen 16px → line-height 1.5–1.7 (= 24–27px)
- Screen 14px → line-height 1.6–1.8

**All line spacing must be an integer multiple of the modulus.** Otherwise lines cannot align across languages or sizes.

### Interline punctuation spacing bonus (W3C)
- When proper-name wavy marks (U+FE4F), style-A book-title wavy marks, or emphasis dots sit between lines:
  - **Single-sided binding: line spacing ≥ 1/2 font size**
  - **Double-sided binding: line spacing ≥ 5/8 font size**
- Vertical text with ruby: line spacing ≥ 1.5 × base glyph

## 4. Weight and size

### Weight vs contrast
- Weight shapes the contrast between text and its carrier (paper/screen)
- **Small text + heavier weight** > small text + light weight (small text needs contrast more)
- **Large text + light weight** can look elegant; large type can afford light weights

Example: on thin, translucent paper, set body text in a heavier Song weight — the black of the glyphs against the white of the paper forms an easy-reading contrast, and the heavier weight conversely highlights the paper's translucency.

### Weight selection matrix
| Size | Screen | Print | Recommended weight |
|---|---|---|---|
| Tiny | < 12px | < 6pt | Medium / Bold (55S–65S) |
| Small | 12–14px | 6–7.5pt | Regular / Medium (45S–55S) |
| Medium | 14–18px | 8–10pt | Regular (45S–55S) |
| Large | 18–24px | 10–14pt | Regular / Light (35S–45S) |
| Huge | > 24px | > 14pt | Light / Thin optional (25S–45S) |

### Hierarchy via weight, not typeface changes
Different sizes × different weights often form fields of near-identical gray, which then pull apart the spatial relation to other elements. Example: large body text in a lighter weight, small auxiliary text in a medium weight — their grays are close, yet hierarchy emerges naturally through size.

Hierarchy priority: **size > weight > color > typeface**. Only reach for the latter two when the former two can't resolve it.

## 5. Paragraphs and conventions

### Paragraph organization: do not treat 2-character indent as a universal default
- Books, classical texts, official documents, long formal print: first-line indent is fine, commonly 2 characters; short columns may reduce it to 1
- Web, H5, Xiaohongshu, dashboards, PPT, cards: usually no first-line indent; organize with paragraph spacing, grouping, and heading levels instead
- Quotes may use block indent or rule/background/card treatment; don't mechanically apply a 4-character indent
- List items need no first-line indent
- One work uses one paragraph convention; never stack "first-line indent + large paragraph gaps" together

### The 4 paragraph indent modes (W3C CLReq §6.2.1)

| Mode | Method | Applies to |
|---|---|---|
| **1. Indent every paragraph's first line** | All paragraphs start 2 characters in | Books, classical texts, official documents, formal print |
| **2. No indent on the first paragraph; indent the rest** | First paragraph flush, others 2 characters in | Long-form articles, EN→ZH translations, cross-cultural projects |
| **3. No indents anywhere + paragraph spacing** | Flush starts, blank line between paragraphs | Modern web, technical docs, H5, PPT, cards, Markdown rendering |
| **4. No indent when a sentence continues** | When a paragraph breaks mid-thought, the next paragraph stays flush | Essays, poetry, scripts |

### Hanging indent
First line flush, following lines indented. Used for:
- Script dialogue
- Q&A
- Legal clauses
- Dictionary entries
- Name rosters

```
Libai:  chuang qian ming yue guang,
        yi shi di shang shuang.
Dufu:   hao yu zhi shi jie,
        dang chun nai fa sheng.
```

CSS:
```css
.hanging {
  text-indent: -4em;       /* first line protrudes 4 characters left */
  padding-left: 4em;        /* whole block indented 4 characters */
}
```

### Block indent
Uniform indent on the line-start side; for quotes, poetry, subtitles. Same size as body; may change typeface or add paragraph spacing; the gap must be an integer multiple of the body line.

```css
blockquote {
  margin: 1em 4em 1em 4em;     /* 4 characters in on each side */
  font-style: normal;          /* never italicize Chinese */
}
```

### Subheading treatment
Classic demonstration: same typeface, same size; distinguish conventions with space alone.
- Quotes: no leading space; distinguish via block indent, side rule, background, or card; the indent amount is decided by the layout
- Subheads: push 6 characters in from the paragraph start, with no blank line to the body
- Body: per the chosen paragraph convention; books/official documents may indent first lines, web/cards/UI usually stay flush and group with spacing

This "space instead of size" treatment marks advanced typesetting — **information hierarchy without strong contrast; spatial order instead**.

### The 4 single-line alignments (W3C)
- **Centered**: titles, signatures, standalone elements
- **Line start**: list items (left-aligned to line start)
- **Line end**: dates, signatures, prices (right-aligned to line end)
- **Evened**: filling after kinsoku / consistent look for parallel list items; **never even the last line of a paragraph, or a one-line paragraph**

## 6. Even text gray

Typography's highest ideal: **text forms an extremely even gray inside the type area**, making the text's shape easy to sculpt.

Enemies of even gray:
1. Unsqueezed punctuation → local white blocks
2. No spacing in Chinese-English mixing → uneven glyph widths
3. Mixed weights → jumpy black-white contrast
4. Ragged line ends (left-aligned) → gray breaks on the right
5. Traditional characters mixed into Simplified → locally darker

Allies of even gray:
1. Justified alignment (justify)
2. Automatic spacing for Chinese-English mixing
3. Uniform weight within a paragraph
4. Punctuation squeezing + kinsoku
5. Stable line spacing

### CSS implementation
```css
.body {
  text-align: justify;
  text-justify: inter-character;   /* distribute spacing between Chinese characters */
  text-spacing-trim: space-all;
  line-break: strict;
}
```

## 7. Chinese-English mixing

- **Automatically add a 1/4-character gap between Chinese and English** (the "Pangu's space")
  - Web: keep a half space between `<span>...</span>` runs; or use `text-autospace` (old IE spec) / CSS Text Module Level 4's `text-spacing`
  - Markdown writing: type the space manually between Chinese and English
- Halfwidth Western punctuation also takes a space next to Chinese characters
- Digits adjacent to Chinese also take a space: "di 3 zhang" (chapter 3) with a space, never "di3zhang"
- Units stay tight to numbers: `30px`, `9pt`, never `30 px`

### Spacing per W3C

- Horizontal Western letters use proportional fonts; digits use proportional or monospace fonts
- Gap between Han glyphs and Western letters/digits **≤ 1/4 em** (default 1/4 em, minimum 1/8 em, maximum 1/2 em)
- **No extra whitespace** when Western text/digits sit at line start/end
- Around Chinese pause punctuation, and after opening / before closing interlinear marks, do **not** adjust tracking or add whitespace around adjacent Western text/digits

## 8. Widow & orphan relief

Typesetting's "last-page syndrome". See `title-and-breaking.md` §5.

### An orphan character must not form a line
A paragraph's last line holds only 1 character + 1 punctuation mark.

Relief order:
1. **Squeeze into the previous line** (first choice): punctuation width adjustment, compressed Chinese-Western gaps, evened tracking
2. **Delete a character back into the previous line**: agree with the author to cut 1–2 characters
3. **Add a character**: pad so the last line holds ≥ 3 characters
4. **Even out the last line** (second choice): only for poetry and couplets

### A widow line must not open a page
The page starts with the previous paragraph's final line.

Relief order:
1. **Return the widow to the previous page**: let the type area take 1 more line to join the previous paragraph
2. **Take 1 line from the previous page's last paragraph**: revise the previous paragraph to end earlier
3. **Delete characters**: trim this paragraph's opening so the widow isn't alone
4. **Add characters**: pad a full line's worth

CSS:
```css
p {
  orphans: 2;       /* keep at least 2 lines at a paragraph's end */
  widows: 2;        /* keep at least 2 lines at a paragraph's start */
}
```

## 9. Ruby annotation / pinyin (W3C CLReq §5.5)

### Bopomofo (Taiwan)
- Placed to the **right** of the base glyph in both horizontal and vertical, in principle
- Annotation size : base glyph = **3 : 10**
- Tone marks share the annotation size; neutral-tone mark = 1 : 15
- Tone positions:
  - Level/rising/departing/entering tones: to the **upper right** of the last symbol
  - Entering tone: lower right
  - Neutral tone: in front
- In vertical writing it returns half a symbol position upward; in horizontal it protrudes half a position rightward

### Hanyu Pinyin
- **Horizontal only**
- Usually above the base glyph (below in some contexts)
- Annotation size = **1/2** of the base glyph size
- Gap between adjacent annotations ≥ Western word space ≈ 1/4 character width
- Letterforms: single-story a / g, sans-serif with thick-lower/thin-upper second-tone strokes (publishing/education convention; no national standard)

**Two usages**:
1. **Per-glyph annotation**: annotation always above, wide tracking between glyphs, all lowercase
2. **Word-grouped annotation**: annotation usually below, ~1/2-character gaps between words, capitalized sentence starts/proper nouns, punctuation follows the left annotation

### HTML5 Ruby

```html
<!-- per-glyph annotation (base tokens are placeholders; put your Han glyphs in production) -->
<ruby>
  han<rt>hàn</rt>yu<rt>yǔ</rt>pin<rt>pīn</rt>yin<rt>yīn</rt>
</ruby>

<!-- whole-word annotation -->
<ruby>
  hanyu pinyin<rt>Hànyǔ Pīnyīn</rt>
</ruby>

<!-- with parenthesized fallback -->
<ruby>
  han<rp>(</rp><rt>hàn</rt><rp>)</rp>
</ruby>
```

CSS:
```css
ruby {
  ruby-position: over;            /* annotation above */
  /* ruby-position: under;        // annotation below (word-grouped style) */
}

rt {
  font-size: 0.5em;               /* pinyin = 1/2 of the base glyph */
  font-family: "Source Sans Pro", "Inter", sans-serif;
  line-height: 1;
}
```

### Note: CSS Ruby support differs across browsers; Apple Books has the most complete font choices. The stable web approach is simulating with manual `<sup>`.

## 10. Checklist (must pass before finalizing)

- [ ] Body line length 17–40 characters (max 48 horizontal / 55 vertical)?
- [ ] Line spacing 1.5–2× font size?
- [ ] Line spacing an integer multiple of the modulus?
- [ ] All font sizes within the modulus system?
- [ ] Margins ordered inner < outer < top < bottom?
- [ ] Body letter-spacing is 0?
- [ ] Does paragraph treatment match the medium (web/cards don't mechanically indent; books/official documents indent per template)?
- [ ] Uniform weight within each paragraph?
- [ ] A 1/4-character gap between Chinese and English?
- [ ] Any "orphan character + punctuation" at a paragraph end?
- [ ] Any widow line at a page top?
- [ ] Does the page hold up to even gray when viewed from a distance?
- [ ] Is one of the 4 indent modes chosen and carried through the whole document?

If any item fails, fix that item before talking about "aesthetics".
