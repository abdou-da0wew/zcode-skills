# Punctuation, the Complete Rules: Styles / Squeezing / Kinsoku / Em Dash

The "dark matter" of Chinese typesetting. It occupies 5%–15% of text area but decides 95% of the "professional feel". This file unfolds six topics: 4 punctuation styles, additive vs subtractive models, 4 kinsoku strictness levels, in-line squeeze/stretch priority, an em-dash deep dive, and a Unicode codepoint quick reference.

## 1. The four punctuation styles

Never mix. Lock one style per project.

### 1. Fullwidth style
- Every punctuation mark occupies 1 Han width
- Seen in: default web typesetting (engine doesn't adjust), older-school print publications
- Pros: strict horizontal/vertical alignment
- Cons: consecutive marks create "white holes" (a closing mark + full stop + opening mark ≈ 3 cells of blank)
- CSS: default behavior (no special handling)

### 2. Halfwidth style
- Every punctuation mark occupies 0.5 Han width
- Seen in: dictionaries (space saving), Apple's China website in 2018 (via the SF Pro SC webfont)
- Pros: compact; mixes naturally with Western text
- Cons: weak sentence-end pause; hurts reading rhythm
- CSS: `font-feature-settings: "halt" 1;` or switch to a halfwidth-capable font

### 3. Kaiming style (Mainland print mainstream)
- **Sentence-end punctuation fullwidth**: full stop, question mark, exclamation mark (U+3002, U+FF1F, U+FF01)
- **Within-sentence punctuation halfwidth**: comma, ideographic comma, semicolon, colon (U+FF0C, U+3001, U+FF1B, U+FF1A)
- Seen in: Mainland print media, Founder FIT default, most Mainland books
- **Recommended for modern Mainland horizontal body text**
- CSS: manual control or InDesign punctuation-squeezing presets

### 4. Centered style (HK/TW mainstream)
- All punctuation fullwidth + glyph face centered in the cell
- Works for both horizontal and vertical (punctuation position identical)
- Seen in: almost all HK/TW publications, traditional calligraphy collections
- Pros: direction-agnostic; friendly to horizontal/vertical alignment
- Cons: in horizontal text the full stop looks like it floats mid-cell
- CSS: HK/TW fonts (e.g. DynaFont, Arphic) carry this face distribution natively

### Selection decision table

| Project type | Recommended style | Note |
|---|---|---|
| Mainland modern books / magazines / periodicals | Kaiming | Mainstream choice |
| Mainland academic papers / prospectuses / official documents | Kaiming | Formal |
| HK/TW traditional books | Centered | Republican-era continuity |
| Dictionaries / reference books | Halfwidth | Space saving |
| Web body text (no engine support) | Fullwidth (forced) | `text-spacing-trim` improves it |
| Modern web / App (engine available) | Kaiming + `text-spacing-trim` | Recommended |
| Classical facsimiles / literary Chinese | Centered or fullwidth | Pairs with vertical writing |

## 2. Additive model vs subtractive model

**A minefield of misconceptions.**

### Additive model (the professional typesetting way)
- The punctuation glyph itself = **halfwidth**
- Gaps on one or both sides complete the fullwidth
- What you adjust = the gap (removable, halvable, stretchable)
- Used by: InDesign, QuarkXPress, JIS, all Adobe products
- When punctuation runs together: remove the adjacent gap

### Subtractive model (the popular mental model)
- The punctuation glyph itself = **fullwidth**
- "Squeezing" removes part of the width
- What you adjust = the glyph face itself
- Used by: Founder's own typesetting software, some Simplified-Chinese Word presets
- Problem: subtracting on an additive-model font computes wrong

### Practical judgment

**Using InDesign / Adobe systems**: additive model by default. Prefer fonts whose punctuation is face-shifted (Source Han, STFonts, Monotype); avoid many Founder body faces (Founder XinSong, FZ YouHei, Founder SongOne) — they center punctuation in the cell ("centered style"), which misaligns with Adobe's algorithm.

**Using Founder FIT**: subtractive model by default; internally consistent with Founder fonts, no problem.

**Web / CSS**: modern `text-spacing-trim: space-all` is an additive-model implementation.

### The 3 gap groups under the additive model

| Group | Punctuation | Gap |
|---|---|---|
| **Group 1**: default solid, no gap added | Emphasis dots, separator slash, short hyphen, Japanese question/exclamation | 0 |
| **Group 2**: half-cell gap on one side (Mainland + most Japanese) | Mainland question/exclamation/colon/semicolon/comma/ideographic comma/full stop; curly quotes (U+201C/D, U+2018/9); parentheses; book-title marks (U+300A/B) | halfwidth + half gap = fullwidth |
| **Group 3**: quarter-cell gap on both sides (most HK/TW + Japanese middle dot) | HK/TW question/exclamation/colon; Japanese middle dot (U+30FB) | halfwidth + 1/4 left + 1/4 right = fullwidth |

## 3. End-of-line halfwidth principle (GB/T 15834-2011 §5.1.10)

**Mandatory rule**: when a fullwidth punctuation mark lands at the end of a line, it **should occupy only halfwidth width**. I.e. "end-of-line punctuation → halfwidth".

- A hard rule in Mainland China and most Chinese publishing houses
- Visual effect: line ends align (no visual protrusion from a fullwidth final mark)
- Implementation: InDesign "punctuation squeeze" → halve at line end (automatic); CSS `hanging-punctuation: allow-end` lets punctuation hang outside the type area

## 4. Kinsoku: 4 strictness levels (W3C CLReq §6.1.1)

**One strictness level per document.**

### Level 0: none
- No kinsoku processing
- Found in some HK/TW newspapers (centered punctuation never looks abrupt)
- Not recommended for Mainland work

### Level 1: basic (minimum standard)
- **Never at line start**: full stop (U+3002), comma (U+FF0C), ideographic comma (U+3001), semicolon (U+FF1B), colon (U+FF1A), exclamation (U+FF01), question (U+FF1F), ellipsis (U+2026), em dash (U+2014), middle dot (U+00B7), all "closing" brackets and quotes (U+FF09, U+3011, U+300B, U+300D, U+300F, U+FF5D, U+3009), closing curly quotes (U+2019, U+201D), en dash (U+2013), slash (U+002F)
- **Never at line end**: all "opening" brackets and quotes (U+FF08, U+3010, U+300A, U+300C, U+300E, U+201C, U+2018)

### Level 2: GB method (Mainland national standard; recommended for formal publishing)
- All basic rules
- **Plus**: the slash (U+002F) may not end a line either
- This is the default level of the Mainland book industry

### Level 3: strict (recommended for hardcover/formal publishing)
- All GB rules
- **Plus**: the em dash (U+2014 pair) may not start a line
- **Plus**: the ellipsis (U+2026 pair) may not start a line
- InDesign's "Simplified Chinese kinsoku" defaults to this level

### Complete character reference

#### Never at line start
```
U+3002 full stop
U+FF0C comma            U+3001 ideographic comma
U+FF1B semicolon        U+FF1A colon
U+FF1F question mark    U+FF01 exclamation
U+2026 ellipsis         U+2014 em dash
U+00B7 middle dot       U+2013 en dash
All closing brackets/braces: U+FF09 U+3011 U+3017 U+3011 U+3009 U+300B U+300D U+300F U+3019 U+3017 U+FF60
All closing quotes: U+2019 U+201D
Trailing symbols: U+0025 % U+2030 per-mille U+2031 per-ten-thousand U+2103 deg-C U+2109 deg-F U+00B0 degree U+2032 prime U+2033 double-prime
Separator slash: U+002F U+FF0F U+2027 hyphenation point
```

#### Never at line end
```
All opening brackets/braces: U+FF08 U+3010 U+3016 U+3014 U+3008 U+300A U+300C U+300E U+3018 U+3016 U+FF5F
All opening quotes: U+2018 U+201C
Currency symbols: U+0024 $ U+00A5 ¥ U+20AC € U+00A3 £ U+00A2 ¢ U+20A9 ₩ U+20AB ₫
```

#### Inseparable (never split in the middle)
```
U+2014 ×2   em dash (the 2-cell pair is one unit)
U+2026 ×2   ellipsis (the 2-cell pair is one unit)
123456      inside Arabic numerals and the decimal point
50%         number + percent / per-mille / degree signs
20℃         number + unit (e.g. U+2103)
±5          sign + number
m²          marked word + super/subscript (U+00B2)
①②         annotation marks + annotated word (U+2460…)
word        Western words (per hyphenation rules)
```

### Processing order: "squeeze in first, push out second"

An explicit W3C rule.

1. **Step 1**: check whether the punctuation can be squeezed back into the previous line's end via "width squeezing"
   - End-of-line fullwidth punctuation → halfwidth
   - Consecutive punctuation → remove the adjacent gap
   - Chinese-Western gap 1/4 em → 1/8 em
2. **Step 2**: still doesn't fit — push the previous line's last character to the next line
3. **Step 3**: distribute the previous line's extra space by stretch priority
4. **Step 4**: only then increase letter spacing evenly

**Mnemonic**: **squeezing in only needs to free half a character width; pushing out moves at least a full character width; body typesetting should adjust as little as possible.**

### Relief after pushing: justify within

When in-line adjustment cannot make the line even, distribute space by stretch priority. See the next section.

## 5. In-line squeeze / stretch priority (W3C CLReq §6.2.2)

**This is the engine's internal algorithm table; knowing it tells you why InDesign adjusts what it does.**

### Squeeze priority (high to low)

| Priority | Target | Squeeze amount |
|---|---|---|
| a | **End-of-line punctuation** | Fixed half character width (GB/T 15834-2011 §5.1.10) |
| b | In-line Western word spacing | Minimum **1/4 em**, equal amounts at multiple sites |
| c | Middle dot (U+00B7) | Squeeze equally from both sides, minimum to 0 (result: half width) |
| d | Interlinear marks (brackets) | Before opening / after closing brackets, minimum to half width |
| e | Comma / ideographic comma / semicolon | Squeeze the trailing side or both sides equally, minimum to half width |
| f | Chinese-Western gap | Minimum **1/8 em** (some styles fix 1/4 em and forbid adjustment) |
| g | Full stop / question / exclamation | Squeeze to half width if space allows (some styles forbid it — the sentence-end pause is large) |

### Stretch priority (high to low)

| Priority | Target | Stretch amount |
|---|---|---|
| a | Western word spacing | Maximum **1/2 em**, equal amounts at multiple sites |
| b | Chinese-Western gap | From the 1/4 em default up to maximum **1/2 em** (in practice most styles stop at 1/3 em) |
| c (last resort) | Letter spacing | Stretch equally, but **never stretch spacing adjacent to kinsoku-restricted characters**; avoid stretching around en dashes and slashes |

### Key values quick reference

| Gap | Minimum | Default | Maximum |
|---|---|---|---|
| Western word spacing | 1/4 em | 1/3 em | 1/2 em |
| Chinese-Western gap | 1/8 em | 1/4 em | 1/2 em |
| Around middle dot | 0 | 1/4 em | 1/4 em |
| End-of-line punctuation | Half width | Half width | Half width (fixed) |
| Consecutive punctuation totaling 2 cells | 1 cell | 1.5 cells | 2 cells |

## 6. Consecutive punctuation (W3C CLReq §6.3.2)

**The most common disaster scene**: consecutive punctuation forms "white holes".

Untreated (schematic — each fullwidth mark occupies one cell):
```
(Note) Author, "Book Title" comment on the two lines, "the verse
was recited by every child, yet the words alone suffice". (Source) Editor
                              ↑↑↑
          closing quote + full stop + opening paren = 3 full cells of blank
```

Treated (schematic):
```
(Note) Author, "Book Title" comment on the two lines, "the verse was recited by
every child, yet the words alone suffice". (Source) Editor's comment
                       ↑↑
          the trio squeezed to about 1.5 cells
```

### Rules
- When any two adjacent punctuation marks together occupy 2 cells, **shrink to 1.5 cells**
- May shrink further to 1 cell (but usually don't — readers may misread two marks as one)
- Squeeze direction: opening/closing brackets hug the content they enclose

### Implementation
- InDesign: Paragraph → Chinese Typography Settings → "Punctuation Squeeze" → choose "Simplified Chinese default" or custom
- CSS: `text-spacing-trim: space-all` (handles it automatically)

## 7. Em dash deep dive

**The single most error-prone symbol.**

### 1. Codepoint priority
1. **U+2E3A** TWO-EM DASH `⸺` — the proper codepoint; 2 cells as one glyph, **first choice**
2. **U+2014** EM DASH `—` × 2 — the de facto standard; Source Han fonts substitute a continuous long bar via `ccmp`, **primary use**
3. ❌ U+2015 HORIZONTAL BAR `―` — most Simplified-Chinese fonts break it
4. ❌ U+2500 BOX DRAWINGS LIGHT HORIZONTAL `─` — semantically wrong (a table-drawing character)
5. ❌ U+30FC KATAKANA-HIRAGANA PROLONGED SOUND MARK — a Japanese long-vowel mark
6. ❌ U+FF0D FULLWIDTH HYPHEN-MINUS — a halfwidth connector
7. ❌ U+002D HYPHEN-MINUS `-` — the ASCII hyphen

### 2. Font recommendations (correct em-dash implementation)

**Recommended**:
- Source Han Sans / Source Han Serif (via OpenType `ccmp` replaces two consecutive U+2014 with one continuous bar; `locl` switches to a cell-centered glyph under CJK languages)
- PingFang
- HarmonyOS Sans / MiSans

**Minefields** (dash breaks / rides the cell edge / sinks):
- ZhongYi Song / ZhongYi FangSong ("will not connect no matter what")
- Old versions of Microsoft YaHei (dash sinks and the pair exceeds 2 cells)
- STHeiti (dash rides the edge, not centered)
- LanTingHei (dash rides the edge and is not centered)

### 3. Font-stack trap (CSS)

❌ **Wrong**:
```css
font-family: "Helvetica", "PingFang SC";   /* Latin font first */
```
Two consecutive `—` glyphs take Helvetica's shapes, causing sinking, breaking, and a gap between the two bars.

✅ **Correct (option A)**: drop the Latin font, use system Chinese fonts
```css
font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
```

✅ **Correct (option B)**: split `@font-face` with `unicode-range`
```css
@font-face {
  font-family: "Helvetica Local";
  src: local("Helvetica");
  unicode-range: U+0000-007F;       /* ASCII only */
}
body {
  font-family: "Helvetica Local", "PingFang SC", sans-serif;
}
```

✅ **Correct (option C)**: declare `lang` to activate `locl`
```html
<html lang="zh-CN">
```

### 4. Preventing a break between the two em dashes

**InDesign**:
1. Paragraph panel → check "No Hyphenation" (on by default)
2. Kinsoku rule set → "characters that must not be separated" → add U+2014, U+2015, U+2500
3. Don't just tick "no line break" (that's only a local manual fix)

**Word**:
- The `―` in the Simplified edition's "trailing punctuation" list is actually U+2015, not U+2014
- To give U+2014 kinsoku treatment, add it manually to "custom trailing punctuation"
- Last-resort trick: select a single `—`, Format → Font → Character Spacing → Scale 200%, forcing one em dash to occupy two cells (from the Typesetting and Proofreading Standards)

**CSS**:
```html
<!-- forbid a line break between the two em dashes -->
He said—&#8288;—I'm not going.
```

### 5. National-standard basis
- GB/T 15834-2011 §4.10 / §5.1.4: the em dash occupies two cells, vertically centered, **must not break in the middle**

## 8. Unicode codepoint quick reference (W3C CLReq recommendations)

| Mark | Unicode | Recommended | Not recommended alternatives |
|---|---|---|---|
| Full stop | U+3002 | ✅ | U+FF0E / U+002E |
| Comma | U+FF0C | ✅ | U+002C |
| Ideographic comma (dunhao) | U+3001 | ✅ | — |
| Semicolon | U+FF1B | ✅ | U+003B |
| Colon | U+FF1A | ✅ | U+003A |
| Question mark | U+FF1F | ✅ | U+003F |
| Exclamation | U+FF01 | ✅ | U+0021 |
| Opening curly double quote | U+201C | ✅ (horizontal) | — |
| Closing curly double quote | U+201D | ✅ (horizontal) | — |
| Opening corner quote | U+300C | ✅ (vertical) | — |
| Closing corner quote | U+300D | ✅ (vertical) | — |
| Opening double corner quote | U+300E | ✅ (vertical) | — |
| Closing double corner quote | U+300F | ✅ (vertical) | — |
| Opening parenthesis | U+FF08 | ✅ | U+0028 |
| Closing parenthesis | U+FF09 | ✅ | U+0029 |
| Opening book-title mark | U+300A | ✅ | — |
| Closing book-title mark | U+300B | ✅ | — |
| Opening single book-title mark | U+3008 | ✅ | — |
| Closing single book-title mark | U+3009 | ✅ | — |
| Em dash | U+2E3A `⸺` / U+2014 × 2 `——` | ✅ | U+2015 / U+2500 / U+30FC |
| Ellipsis | U+2026 × 2 | ✅ | U+22EF (auto-centered alternative for horizontal and vertical) |
| En dash | U+2013 | ✅ | — |
| One-cell dash | U+2014 | ✅ | — |
| Wavy dash | U+FF5E | ✅ | U+007E |
| Middle dot | U+00B7 | ✅ | U+30FB / U+2027 / U+2022 |
| Separator slash | U+002F or U+FF0F | ✅ | — |
| Emphasis dot | U+25CF or U+2022 | ✅ | — |

## 9. Complete CSS implementation (modern browsers, 2024+)

```css
.body-text {
  /* Letter spacing: solid setting */
  letter-spacing: 0;

  /* Punctuation space squeezing (additive-model implementation) */
  text-spacing-trim: space-all;

  /* Punctuation hangs outside the type area (aligns end-of-line punctuation visually) */
  hanging-punctuation: allow-end;

  /* Strict kinsoku */
  line-break: strict;

  /* Never break inside words */
  word-break: keep-all;

  /* Allow overlong URLs to wrap */
  overflow-wrap: break-word;

  /* Justify both edges */
  text-align: justify;

  /* Distribute spacing between Chinese characters */
  text-justify: inter-character;

  /* Punctuation width optimization (OpenType) */
  font-feature-settings:
    "halt" 1,         /* halfwidth spacing */
    "palt" 1;         /* proportional setting (for titles) */
}

/* Titles: no halt; titles set solid */
h1, h2, h3 {
  font-feature-settings: "palt" 1;  /* proportional only */
}

/* Web / H5 / card body: usually no first-line indent */
p {
  text-indent: 0;
  margin: 0 0 1em 0;
}

/* Books / official documents / classical long-form: indent only when the corresponding template specifies it */
.book-copy p,
.official-doc p,
.classical-copy p {
  text-indent: 2em;
  margin: 0;
}

/* Quote blocks: never italic; indent/rule/background decided by the layout */
blockquote {
  font-style: normal;
}
```

Legacy-browser fallback: use `<wbr>` for manual line breaking; use a script (e.g. `kerning.js`).

## 10. Checklist (punctuation-related)

Must pass before finalizing:

- [ ] Is the punctuation style (fullwidth / halfwidth / Kaiming / centered) consistent throughout?
- [ ] Is end-of-line fullwidth punctuation converted to halfwidth?
- [ ] Is a kinsoku level (basic / GB / strict) chosen and enabled?
- [ ] Is consecutive punctuation squeezed to within 1.5 cells?
- [ ] Does the em dash use U+2014 × 2 (not four hyphens)?
- [ ] Is the dash rendered by Source Han / PingFang rather than ZhongYi / old YaHei?
- [ ] Is the em dash added to the "must not separate" set?
- [ ] Are quotes curly (U+201C/D) in horizontal text and corner brackets (U+300C/D, U+300E/F) in vertical text?
- [ ] Does CSS `font-family` put the Chinese font before the Latin font?
- [ ] Does the HTML declare `lang="zh-CN"` or `lang="zh-TW"`?
- [ ] Does paragraph treatment match the medium: web/cards don't mechanically indent first lines; books/official documents/classical long-form indent per template?
- [ ] Does Chinese-English mixing carry a 1/4-cell gap?
