# Han Glyph Grid System, Explained

The complete unfolding of the "modulus → grid → type area" methodology for Chinese publications.

## 1. Core concepts

### Modulus (multiplier / coefficient)
One value of which every layout element is an integer multiple. It brings all spatial elements of the page into one proportional system.

- **Default recommendation: 1.5pt** (a 9pt body system)
  - Body 9pt = 6 × 1.5pt
  - Captions 6pt = 4 × 1.5pt
  - Subheads 12pt = 8 × 1.5pt
  - Line spacing 18pt = 12 × 1.5pt
  - Margins measured in 9pt = 1 character units
- **Academic / rigorous: 1pt** (finer steps)
- **Classical hardcover / multi-template alignment: 0.5pt** (extremely fine)
- **Never use 1.618pt / the φ ratio as the modulus** — Han glyphs are fixed-width squares; decimal fractions make cell widths impossible to reconcile

Modulus selection principle: **the body font size must divide evenly by the modulus**, and the modulus must produce a sufficient size gradient (no more than 12 levels).

### Font-size system
All sizes in a project come from one table. A typical 9pt / 1.5pt-modulus system:

| Use | Size (pt) | Modulus multiple |
|---|---|---|
| Main title / chapter opener | 18–24 | 12–16× |
| Chapter title | 15 | 10× |
| Section title | 12 | 8× |
| Body | 9 | 6× |
| Quote / secondary text | 7.5 | 5× |
| Footnote / caption | 6 | 4× |
| Running head / page number | 6 | 4× |

The "jump" between sizes should be at least 1.5× (below that, the difference is visually indistinguishable).

### Traditional Chinese type-size names (hao / pt / mm correspondence)

| Hao | pt | mm | Use |
|---|---|---|---|
| Chu (initial) | 42 | 14.8 | Chapter-opener display, big titles |
| No. 1 | 27.5–28 | 9.7–9.9 | Poster display titles |
| Small 1 | 24 | 8.5 | Display titles |
| No. 2 | 21–22 | 7.4–7.8 | Titles |
| Small 2 | 18 | 6.3 | Medium titles |
| No. 3 | 15.75–16 | 5.6 | **Official document body (GB/T 9704-2012: No. 3 FangSong)** |
| No. 4 | 13.75–14 | 4.9 | Subtitles |
| Small 4 | 12 | 4.2 | Secondary text |
| **No. 5** | **10.5** | **3.7** | **Book body (most common)** |
| Small 5 | 9 | 3.2 | Newspaper/periodical body ("new small 5") |
| No. 6 | 7.875 | 2.8 | Captions / **body-size floor** |
| No. 7 | 5.25 | 1.9 | Tiny auxiliary text |

### Page and type area

**Core formula: page format = body font size × integers**

- Example: 60 chars wide × 90 chars high × 9pt = **540 × 810pt = 190.5 × 285.75mm**
- Aspect ratio = 2:3 (a graceful Fibonacci ratio)
- Print/trim allowance: +6pt on width each side, +9pt on height top and bottom → trimmed size 552 × 828pt

Other common ratios: 1:1 / 2:3 / 3:5 / 5:8 / 8:13 (Fibonacci)

## 2. Type-area notation

This notation lets any typesetting scheme be described precisely in one line. **Learning it lets you think about layout like an architect.**

### Horizontal type area

```
L3 + [ W(9pt × 56) ] + R1 / O2 + { H(9pt × 83) } + U5
```

Meaning:
| Symbol | Meaning | Unit |
|---|---|---|
| **L** | Gutter (inner) margin | in 9pt characters |
| **R** | Fore-edge (outer) margin | in 9pt characters |
| **O** | Head (top) margin | in 9pt characters |
| **U** | Foot (bottom) margin | in 9pt characters |
| **W( )** | Type-area width, wrapped in square brackets `[ ]` | pt × characters |
| **H{ }** | Type-area height, wrapped in braces `{ }` | pt × characters |

Reading: gutter 3 characters, fore-edge 1, head 2, foot 5; type area is 9pt × 56 characters wide and 9pt × 83 lines high.

### Vertical type area (notation differs slightly)

In vertical writing, "width" = line count × font size and "height" = characters per line × font size; the gutter is on the **right** (left side on left pages).

```
O5 + { H(10.5pt × 40) } + U8 / R3 + [ W(10.5pt × 25) ] + L13
                                  ↑                       ↑
                            gutter (right of right page)     fore-edge (left)
```

Note: in vertical writing the L/R roles swap sides — **L still means gutter** (left side of left pages, right side of right pages), **R still means fore-edge**.

### Representative type-area schemes (6 selected examples)

All pages 540×810pt (60×90 characters).

| Ex. | Notation | Use |
|---|---|---|
| V_1 | `L3+[W(9×56)]+R1 / O2+{H(9×83)}+U5` | Maximum fill; reference books/dictionaries |
| V_12 | `L2+[W(9×53)]+R5 / O3+{H(9×79)}+U8` | Literary fiction |
| V_22 | `L5+[W(9×42)]+R13 / O8+{H(9×61)}+U21` | Wide fore-edge for annotation (textbooks/note-taking books) |
| V_26 | `L5+[W(9×50)]+R5 / O13+{H(9×69)}+U8` | Full-bleed top / symmetric; art books |
| V_31 | `L3+[W(9×54)]+R3 / O5+{H(9×77)}+U8` | General academic; the most common |
| V_32 | `L3+[W(9×54)]+R3 / O5+{H(9×77)}+U8` | Same as above, for multi-template alignment |

**Patterns**:
- Nearly always L < R, or L+R smaller than O+U (visual center of gravity slightly high)
- Margin values are neighboring Fibonacci numbers (1, 2, 3, 5, 8, 13, 21)

## 3. Columns

The type area can be subdivided into columns. Column width and column gap are both modulus multiples.

- 1 column: literature, essays
- 2 columns: magazines, academic papers, textbooks
- 3+ columns: dictionaries, catalogs, news, data handbooks
- Column gap: **2 characters wide** (e.g. 9pt × 2 = 18pt) is most common; 1 character also works

Characters per column:
- 1-column page: 17–40 characters (W3C recommends 17–40, hard cap 48)
- 2-column page: 15–22 characters
- 3-column page: 12–18 characters

## 4. Converting the modulus across media

### Screen / web
- Body 16px → modulus 4px (16/4=4; use 2px if too coarse)
- Size gradient: 12 / 14 / 16 / 20 / 24 / 32 / 48 / 64 px (all multiples of 4 + even-number harmony)
- max-width: `30em` ≈ 480px @ 16px
- line-height: 1.5–1.7

### PowerPoint / Keynote
- 4:3 canvas 1024×768 → 64px modulus, 16×12 grid
- 16:9 canvas 1920×1080 → 60px modulus, 32×18 grid
- Titles 40–60pt, body 24–32pt, notes 14–18pt

### H5 / mobile (375pt design canvas)
- Modulus 4pt, body 14–16pt
- Line length ≤ 18 characters recommended (375pt minus margins ≈ 311pt / 18pt glyph width = 17 characters)

### Printed books
- 32mo (140×210mm) → body 9–10pt
- 16mo (185×260mm) → body 9.5–11pt
- 8mo / art books → body may go 10–12pt (longer viewing distance)

## 5. The seven essentials of the grid

The most condensed summary of the methodology:

1. **Where to start?** Start from one character — more precisely, from the modulus that composes it. "One Han glyph = one cell"; 1:1 is the first term of the Fibonacci golden sequence.
2. **Page size = integer multiple of body font size.** E.g. 60 × 90 characters.
3. **Page size = integer multiple of the modulus size.** Under a 1.5pt modulus, 540×810pt = 194,400 cells.
4. **From 1 to ∞**: 5,400 cells can be grouped into 1-char, 2-char, or N-char combinations for margins and type area; head/gutter/foot/fore-edge can follow Fibonacci ratios (1:2:3:5) freely.
5. **Feel is the core of design**: the grid, as a tool, cannot supply feel. "Beauty matters more than strictly obeying the grid."
6. **Design different sizes with the same modulus**: the proportional relations between sizes come from the shared modulus.
7. **Design line spacing with the modulus**: line spacing must be a modulus multiple. Under one modulus, text with different sizes and line spacings can still align line to line (multilingual or multi-template facing).

## 6. Practical grid rules (specific to Chinese)

A Chinese grid is not just "a frame around text" — it must go down to in-line character cells; express every dimension in `em`/`rem`, not px/mm.

### 6.1 Workflow: fix the type area from font size first, then derive margins

The Chinese workflow is "type area first, margins after", **not the Western "margins first, type area is what's left"**:

```
1. Fix the font size (e.g. 9pt)
2. Fix characters per line (e.g. 30)
3. Line length = font size × characters (9 × 30 = 270pt)
4. Fix lines per page (e.g. 28)
5. Fix line spacing (e.g. 18pt)
6. Type-area height = (28-1) × 18 + 9 = 495pt
7. Page size − type area = whitespace
8. Allocate L/R/O/U by 3:5:8:13 (left/right/outer/inner)
```

### 6.2 Measure everything in "characters occupied / lines occupied"

| Element | Measurement |
|---|---|
| First-line indent (books/official documents/classical long-form) | `text-indent: 2em` |
| Web/card/UI paragraphs | Usually no first-line indent; flush left |
| Column gap | 2 characters wide |
| Level-1 title line occupation | 4–5 lines (multiples of body line height) |
| Level-2 title | 2–3 lines |
| Level-3 title | 1–2 lines |
| Two-part title | 3 lines |
| Name lists | Each name takes 3 cells; 2-character names get 1 trailing blank cell |

Every title's line occupation **must be an integer multiple of the body line height** — this is the basic requirement of "lining up to lines".

### 6.3 Manage in-line character cells too

When an odd number of half-width punctuation marks leaves a half-cell remainder, two approaches (no absolute right or wrong, but know which compromise you chose):

- **Metal-type approach**: give the half-cell remainder to that punctuation mark → the mark becomes fullwidth, the line stays grid-aligned
- **Digital default**: distribute the half cell across the whole line's tracking → the mark is unchanged but the whole line drifts off the grid

### 6.4 "Breaking the grid" is allowed beyond the strict grid

Occasionally breaking the grid can lift work past its ceiling, but **establish the floor before discussing the ceiling**:

- One large image crossing out of the type area
- One title line reaching out of its column
- Deliberate local whitespace inside a paragraph
- Distinguishing templates with blank lines/indents at the same size (not via bold or font changes)

### 6.5 Priority: function first, formal alignment second

"Fullwidth everything + no kinsoku + fullwidth digits/letters" achieves absolute alignment both ways but sacrifices readability. **Do all of the following first; consider formal alignment after**:

- Punctuation width adjustment (see `punctuation.md`)
- Kinsoku (see `punctuation.md §4`)
- Line-break control (see `title-and-breaking.md`)
- Orthography choices (Chinese numerals vs Arabic numerals; Chinese-Western mixing strategy)

"Sacrificing function for form" is wrong.

## 7. W3C CLReq key-value quick reference

The hard numbers scattered through the W3C "Requirements for Chinese Text Layout", gathered for lookup.

### Font size / line length / line spacing

| Item | Minimum | Recommended | Maximum |
|---|---|---|---|
| Body font size | No. 6 (7.875pt ≈ 2.8mm) | No. 5 10.5pt / Small-5 9pt | — |
| Line length (characters per line) | ≥ 10 | 17–40 | Horizontal ≤ 48 / vertical ≤ 55 |
| Line spacing (as font-size ratio) | 50% of size | 50–100% | 100% (beyond adds no readability) |
| Line height (including the glyph) | 1.5 × size | 1.5–2 × size | 2 × size |
| First-line indent | — | Only when a template like books/official documents/classical long-form specifies it; commonly 2em, short columns 1em | — |
| Vertical line spacing with ruby | ≥ 1.5 × base glyph | — | — |
| Interline punctuation, single-sided binding | ≥ 1/2 font size | — | — |
| Interline punctuation, double-sided binding | ≥ 5/8 font size | — | — |

### Chinese-Western mixing spacing

| Spacing | Minimum | Default | Maximum |
|---|---|---|---|
| Between Chinese and Western | 1/8 em | 1/4 em | 1/2 em |
| Western word spacing | 1/4 em | 1/3 em | 1/2 em |
| End-of-line punctuation | Half character width | Half | Half (fixed) |

### Ruby/annotation size ratios

| Method | Annotation size | Line-spacing bonus |
|---|---|---|
| Bopomofo | 30% of base glyph | line spacing ≥ 1.5 × base glyph |
| Hanyu Pinyin | 50% of base glyph | Same as above |
| Neutral-tone mark (Bopomofo) | 1/15 of base glyph | — |

### Title line occupation

| Title level | Lines | Size (with 9pt body) |
|---|---|---|
| Major title (chapter opener) | 4–5 | 18–24pt |
| Medium title (section opener) | 2–3 | 12–15pt |
| Minor title | 1–2 | 10–12pt |
| Two-part title | 3 | Main 12pt + sub 9pt |
| Run-in title | 1 line (continues into body) | 9pt bold |

### Consecutive punctuation width

| State | Width |
|---|---|
| Any two adjacent punctuation marks together | 2 characters (unsqueezed) |
| Should shrink to | **1.5 characters** |
| Can further shrink to | 1 character |

## 8. Horizontal / vertical type-area orientation differences

Under different directions, the "row / column" meanings of the type area swap:

| Concept | Horizontal | Vertical |
|---|---|---|
| One line | A horizontal run of characters | A vertical run of characters |
| Line length | Horizontal width | Vertical height |
| Lines per page | How many lines stack vertically | How many lines array horizontally |
| Line spacing | Between two lines above/below | Between two lines left/right |
| Type-area width W | Horizontal dimension | Horizontal dimension (= line count × font size) |
| Type-area height H | Vertical dimension | Vertical dimension (= characters per line × font size) |
| Gutter L | Left (right page) / right (left page) | Right (right page) / left (left page) |
| Fore-edge R | Right (right page) / left (left page) | Left (right page) / right (left page) |

See `directions.md` for details.
