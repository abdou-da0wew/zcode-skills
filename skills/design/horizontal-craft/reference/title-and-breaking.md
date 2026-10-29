# Title Line Breaking & Word Wrapping

The most easily ignored rule set in Chinese typesetting. **Body-text wrapping and title wrapping follow completely opposite logics** — body breaks by character, titles break by word. Not knowing this, you will hard-split "our foreign ministry strongly condemns Iraq" and "the embassy bombing incident" across two title lines.

## 1. Core principles

| Text type | Breaking logic | Reason |
|---|---|---|
| **Body** | Break by character, not by word | ~60% of Mandarin words are disyllabic; word-based breaking creates a zigzag right edge — square glyphs are too large to form the Latin "wavy" edge |
| **Titles** | Must break by word | Few characters, large visual share; a split word creates ambiguity and reading blockage |
| **Poetry** | Break by line (each verse on its own line, or aligned) | Rhythm first |
| **TOCs, lists** | Break by entry (wrap with a hanging indent when needed) | Hanging keeps scannability |

## 2. Title line-breaking rules

### 1. Never break inside a word

"Word units" that must never be split:
- **Proper nouns**: personal names (e.g. statesmen, athletes), place names (Beijing / Harbin / Shanghai Pudong), institutions (Ministry of Foreign Affairs, CCTV), brands (Huawei / ByteDance)
- **Terms**: artificial intelligence, deep learning, quantum entanglement, COVID-19
- **Number + unit**: 3 kg, 5 million, chapter 5
- **Number strings**: 2024, 100 yuan
- **Book / film / song titles**: "Quiet Night Thoughts", "The Wandering Earth 2"
- **Idioms / set phrases**: 4-character idioms are never split (e.g. "waiting by the stump for rabbits", "the sea accepts a hundred rivers")

### 2. Function-word position taboos

| Word (pinyin) | Forbidden position | Reason |
|---|---|---|
| **de / di / de / zhi / suo** (particle-like modifiers) | **Never at line start** | The modification relation is severed |
| **he / yu / ji / huo / gen / tong** (and / with / or) | **Never at line end** | The parallel relation dangles |
| **shi / wei / nai** (copulas) | Not at line start | A copula needs its subject |
| **zai / yu / dui / xiang / cong** (prepositions) | Not at line end | A preposition needs its object |
| **le / zhe / guo** (aspect particles) | Not at line start | They attach to the preceding character |
| **ma / ne / ba / a / o** (mood particles) | Not at line start (usually) | Same as above |

### 3. Title counter-examples and fixes

❌ **Counter-example 1** (ambiguous):
```
wo waijiaobu qianglie qianze Yilake
dashiguan bei zha shijian
```
The reader may misparse this as "the Iraqi embassy was bombed".

✅ **Fixed**:
```
wo waijiaobu qianglie qianze
Yilake dashiguan bei zha shijian
```

❌ **Counter-example 2** (mid-word break):
```
pingguo fabu quanxin rengongzhi
neng xinpian M5
```

✅ **Fixed**:
```
pingguo fabu quanxin
rengong zhineng xinpian M5
```

❌ **Counter-example 3** (function-word position):
```
zhongguodui zhansheng le Meiguo dui he
Riben dui
```

✅ **Fixed** ("he"/and never ends a line):
```
zhongguodui zhansheng le
Meiguo dui he Riben dui
```

### 4. Title line-occupation rules (metal-type experience values)

A title must occupy an integer multiple of the body line height, or columns stop aligning.

| Title level | Lines occupied (including whitespace) | Typical size (with 9pt body) |
|---|---|---|
| Major title (chapter opener) | 4–5 | 18–24pt |
| Medium title (section opener) | 2–3 | 12–15pt |
| Minor title | 1–2 | 10–12pt |
| Two-part title (main + sub) | 3 | Main 12pt + sub 9pt |
| Run-in title (subsection head) | 1 line (continues into body) | 9pt bold |

**Key principle**: title size + surrounding whitespace = body line height × N. **Otherwise every following line of body text misses the baseline**.

### 5. Title position on the page

- **Major titles (chapter openers)**: must appear on the **front page**
  - Horizontal, left-turning book → right page (odd pages)
  - Vertical, right-turning book → left page (odd pages)
  - If the previous chapter's last page already ends on a front page → leave the verso blank (the "double blank page" is necessary; don't break it to save paper)
- **New page vs front-page start**:
  - New page: start from the next page regardless of parity (medium/minor titles)
  - Front-page start: must begin on a front page (major titles)
- **Medium/minor-title widow handling**: if a title lands at a page bottom with no room for its following body, **move the whole title to the top of the next page**

### 6. Title alignment

| Direction | Major title | Minor title |
|---|---|---|
| Horizontal | Mostly centered | Mostly left-aligned / indented from paragraph start |
| Vertical | Aligned to the first line (flush top) / dropped start (commonly 2 cells down) | Same |

**Vertical titles' "2-cell drop"**: vertical titles start 2 cells below the head margin, avoiding the oppression of a flush-top start.

### 7. Run-in titles

Subsection heads that don't break; body continues on the same line. Treatment:

```
4. Chapter summary  In this chapter we discussed…
       ↑
   1-character gap
```

- One character of space between the head and the body
- If the head's size is not an integer multiple, adjust the gap so the body's first and last lines align

## 3. CSS / HTML implementation of title breaking

### Method 1: manual `<br>` to control break points (most reliable)
```html
<h1>
  wo waijiaobu qianglie qianze<br>
  Yilake dashiguan bei zha shijian
</h1>
```

### Method 2: `<wbr>` to hint break points (may wrap here)
```html
<h1>pingguo fabu quanxin<wbr>rengong zhineng xinpian M5</h1>
```

### Method 3: U+2060 WORD JOINER (forbid a break here)
```html
<h1>di&#8288;5&#8288;zhang&nbsp;shendu xuexi</h1>
```
Note: do **not** use `&#8205;` (U+200D ZERO WIDTH JOINER) — that is for Arabic/Devanagari joining; it has no effect on Chinese line breaking.

### Method 4: CSS `text-wrap: balance` (modern browsers)
```css
h1, h2, h3 {
  text-wrap: balance;       /* balance the per-line character counts of multi-line titles */
}
```

### Method 5: responsive break points (different breakpoints per screen width)
```html
<h1>
  wo waijiaobu qianglie qianze<br class="md-only">
  <wbr>Yilake dashiguan bei zha shijian
</h1>
<style>
  @media (min-width: 768px) {
    .md-only { display: inline; }
  }
</style>
```

## 4. Body-text line-breaking rules

Body breaks by character, but 6 classes of positions **must not split** (the inseparable-pairs rules):

### 1. Never split inside Arabic numerals
- ❌ `100`<br>`0 yuan`
- ✅ Move the whole number to the next line

### 2. Never split number + unit
- Number + `%`, `‰`, `°`, `℃`, `℉` never split
- Number + signs like `±`, `+`, `−` never split
- Number + currency `¥`, `$`, `€`, `£` never split

### 3. Never split super/subscripts / annotation marks + their marked word
- ❌ `m`<br>`²`
- ❌ Apple<sup>1</sup> <br> Inc.
- ✅ The annotation superscript hugs the preceding character

### 4. Em dashes / ellipses must not split
- The em dash `——` (2 cells wide) must not break in the middle
- The ellipsis `……` (2 cells wide) must not break in the middle
- Multiple consecutive em dashes `————` may break between each pair

### 5. Western words break per hyphenation
- Western words inside horizontal text follow Western hyphenation rules at line ends
- Rotated Western words inside vertical text do not split except at hyphens

### 6. Special handling for URLs / email addresses
- Break at symbols like `@`, `/`, `?`
- **Never add a hyphen** (it would be misread as part of the URL)
- **Never change casing**
- CSS: `overflow-wrap: anywhere` (for long URLs)

### CSS implementation of the inseparable-pairs rules

```css
.body-text {
  word-break: keep-all;            /* never break inside words */
  overflow-wrap: break-word;        /* but allow long URLs to wrap */
  line-break: strict;               /* strict kinsoku */
  text-spacing-trim: space-all;     /* punctuation space squeezing */
  hanging-punctuation: allow-end;   /* hanging final-line punctuation */
}

/* Critical: do not write this */
.bad {
  word-break: break-all;            /* ❌ hard-breaks Chinese per character; kinsoku fully disabled */
}

/* Inseparable small groups: number+unit, super/subscripts */
.unit, .superscript-group {
  white-space: nowrap;              /* the whole group stays on one line */
}
```

### HTML markup for inseparable groups

```html
<!-- number + unit -->
temp <span class="unit">25 ℃</span>
price <span class="unit">¥ 999.99</span>

<!-- super/subscript -->
area <span class="superscript-group">10 m<sup>2</sup></span>

<!-- annotation mark -->
Apple Inc.<sup class="superscript-group">①</sup>

<!-- U+2060 works too -->
temp 25&#8288;℃
```

## 5. Widows & orphans

Typesetting's "last-page syndrome": a single character at a paragraph's end, a single line at a page's top. **Leaving them unfixed is a failure.**

### 1. An orphan character must not form a line

**Symptom**: the paragraph's last line holds only 1 character + 1 punctuation mark.

**3 reliefs** (by priority):

#### Relief A: squeeze into the previous line (first choice)
- Punctuation width adjustment: convert all of the previous line's punctuation from fullwidth to halfwidth to free space
- Chinese-Western gap adjustment: compress the 1/4 em mixing gap to 1/8 em
- Tracking even-out: compress the previous line's tracking by 1/24 em

#### Relief B: delete a character to pull the orphan back
- Agree with the author to cut 1–2 characters
- Rework the syntax (e.g. "feichang" → "hen")

#### Relief C: add a character so the last line holds ≥ 3
- Agree with the author to pad 1 character so the last line is no longer "lonely"
- Add filler particles (le / de / ze)

#### Relief D (second choice): even out the last line
- Distribute the single last-line character across the whole type-area width
- Applies to poetry and couplets, **not to modern prose** (looks wrong)

### 2. A widow line must not open a page

**Symptom**: the page opens with the previous paragraph's final line (1 line + paragraph gap).

**4 reliefs** (by priority):

#### Relief A: return the widow to the previous page (extend the type area)
- Let the widow exceed the foot of the type area by 1 line, joining the previous paragraph
- Temporarily shrink this page's foot by 1 line (permitted in non-strict contexts)

#### Relief B: take 1 line from the previous page's last paragraph
- Revise the previous paragraph so it ends on a natural pause at the last line
- Let the new paragraph start on this page (most natural)

#### Relief C: delete characters
- Cut one line's worth from this paragraph's opening so the widow isn't alone

#### Relief D: add characters
- Pad one line's worth into the previous paragraph

### 3. CSS implementation

```css
p {
  orphans: 2;       /* keep at least 2 lines at a paragraph's end (no lone character) */
  widows: 2;        /* keep at least 2 lines at a paragraph's start (no lone line) */
}

/* Keep paragraphs from being cut by page breaks */
h1, h2, h3 {
  page-break-after: avoid;       /* no page break after a title */
  break-after: avoid-page;        /* same, modern syntax */
}

img, figure {
  page-break-inside: avoid;       /* images are never cut */
  break-inside: avoid;
}
```

## 6. Line-break control tools summary

| Tool | Granularity | Usage | Platforms |
|---|---|---|---|
| `<br>` | Forced break | HTML | All |
| `<wbr>` | Soft break point (may wrap here) | HTML5 | Modern browsers |
| `&#8288;` (U+2060 WJ) | Forbid a break here | HTML entity | Modern browsers |
| `&nbsp;` | Non-breaking space | HTML entity | All |
| `white-space: nowrap` | No wrapping for the whole element | CSS | All |
| `word-break: keep-all` | Never break inside words (never `break-all`) | CSS | All modern |
| `overflow-wrap: break-word` | Allow overlong words to wrap | CSS | Modern browsers |
| `line-break: strict` | Strict kinsoku | CSS | Modern browsers |
| `text-wrap: balance` | Balanced multi-line | CSS | Modern browsers (2024+) |
| `hyphens: auto` | Automatic Western hyphenation | CSS | Modern browsers |

## 7. Line-breaking settings in InDesign / Word

### InDesign
1. **Turn off "digit linking"** (on by default, it misreads things like the "wan yi" inside "in case of emergency" as digits):
   - With no document open → Paragraph panel options → turn off "digit linking" → affects all new documents
2. **Use the Adobe CJK single-line composer** (not the paragraph composer)
   - The paragraph composer pollutes neighboring lines with single-line spacing adjustments
3. **Kinsoku settings**: choose "Simplified Chinese kinsoku"; for the in-kinsoku handling type choose "push in first" or "fixed adjustment priority"
4. **Paragraph panel "No Hyphenation"** checked (on by default) so em dashes don't split

### Word
1. Paragraph dialog → Asian Typography
2. Check "Allow punctuation to overflow the boundary"
3. Check "Control first/last characters per Chinese conventions"
4. Set "first/last characters" to "Standard" or "Strict"
5. **Note**: Word's default Chinese "trailing punctuation" list does not include U+2014; add the em dash to "custom trailing punctuation" manually

## 8. Checklist (line-breaking-related)

Must pass before finalizing:

- [ ] Do all titles break by word, never hard-split mid-word?
- [ ] Does the particle *de* start a title line? Do "and/with" words end a title line?
- [ ] Is each title's line occupation an integer multiple of the body line height?
- [ ] Are major titles on the front page (right page horizontal / left page vertical)?
- [ ] Do number + unit groups stay unsplit? (use `<span class="unit">` or `&#8288;`)
- [ ] Are em dashes and ellipses never split in the middle?
- [ ] Do annotation superscripts hug their marked word?
- [ ] Any "orphan character + punctuation" at a paragraph end?
- [ ] Any widow line at a page top?
- [ ] Do URLs/emails break at sensible positions (no added hyphens)?
- [ ] Does CSS use `word-break: keep-all` instead of `break-all`?
