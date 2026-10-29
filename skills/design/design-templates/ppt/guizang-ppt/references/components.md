# Component Reference · Components

This is the component manual for the `magazine-web-ppt` skill. template.html already defines all styles; this document only describes what each component looks like and how to use it.

## Contents

- [Basic Slide Shell](#basic-slide-shell)
- [Typography](#typography)
- [Chrome & Foot](#chrome--foot)
- [Callout Quote Box](#callout-quote-box)
- [Stat Number Matrix](#stat-number-matrix)
- [Platform Card](#platform-card)
- [Rowline Table Row](#rowline-table-row)
- [Pillar Card](#pillar-card)
- [Tag & Kicker](#tag--kicker)
- [Figure Image Frame](#figure-image-frame)
- [Icons](#icons)
- [Ghost Giant Background Word](#ghost-giant-background-word)
- [Highlight Marker](#highlight-marker)

---

## Basic Slide Shell

Every page is a `<section class="slide ...">`. It must carry the `data-theme` attribute (`light` or `dark`); the JS page-flip uses it to switch backgrounds.

```html
<section class="slide light" data-theme="light">   <!-- light page -->
<section class="slide dark" data-theme="dark">     <!-- dark page -->
<section class="slide light hero" data-theme="light">  <!-- hero page: light + thin overlay revealing WebGL -->
<section class="slide dark hero" data-theme="dark">    <!-- hero page: dark + thin overlay -->
```

**light vs dark usage: alternate them** — switch theme every 2-3 pages, never 3+ consecutive pages of the same color. The WebGL background transitions smoothly between the two shaders on flip.

**hero class usage**: only on visually dominant pages (cover, big-quote page, chapter transitions, closing). With `hero`, the overlay drops to 12-16% and the WebGL background shows through strongly, so don't put too much text on hero pages.

---

## Typography

The type-role split is this template's most important rule; mixing roles is forbidden.

| Class | Purpose | Font |
|---|---|---|
| `.display` | Oversized Latin display (hero pages) | Playfair Display 700, 11vw |
| `.display-zh` | Oversized CJK headline | CJK serif (e.g. Noto Serif SC) 700, 7.8vw |
| `.h1-zh` | Page main title | CJK serif 700, 4.6vw |
| `.h2-zh` | Subtitle | CJK serif 600, 3.2vw |
| `.h3-zh` | Pipeline step title | CJK serif 500, 1.9vw |
| `.lead` | Lead paragraph (larger than body) | CJK serif 400, 1.9vw |
| `.body-zh` | **Body/description (sans)** | CJK sans (e.g. Noto Sans SC) 400, 1.22vw |
| `.body-serif` | Body (serif) | CJK serif 400, 1.3vw |
| `.kicker` | Section hint (above the title) | IBM Plex Mono, 12px uppercase |
| `.meta` | Metadata label | IBM Plex Mono, 0.88vw uppercase |
| `.big-num` | Giant number | Playfair Display 800, 10vw |
| `.mid-num` | Medium number | Playfair Display 700, 5.5vw |

**Core rules**:
- **Serif** (`serif-zh` / `serif-en`): headlines, key quotes, numbers — used for "visual accent"
- **Sans** (`sans-zh`): body descriptions, long reading passages — used for "information density"
- **Mono** (`mono`): kicker, meta, foot English labels — used for "decorative rhythm"

**Emphasis tricks**:
- `<em class="en">English word</em>` — renders the English word in Playfair Display italic (looks great)
- `<em style="opacity:.65">phrase</em>` — fades the second half of a headline to create rhythm

---

## Chrome & Foot

The metadata bars at the top and bottom of every page. Almost every page should have them.

```html
<div class="chrome">
  <div class="left">
    <span>Act I · Hard Numbers</span>
    <span class="sep"></span>
    <span>Act I</span>
  </div>
  <div class="right"><span>02 / 27</span></div>
</div>

<!-- ... page body ... -->

<div class="foot">
  <div class="title">Project Name · CodePilot | github.com/codepilot</div>
  <div>Act I · Dev Numbers</div>
</div>
```

**Rules**:
- `chrome.right` always holds the page number `NN / TOTAL` (TOTAL = total page count)
- `foot.title` carries the localized project line, `foot.right` the English act label
- chrome + foot together form the magazine-style "header/footer"

---

## Callout Quote Box

Displays punchlines / key viewpoints / quotes from others.

```html
<div class="callout" style="max-width:80vw">
  <div class="q-big">"Three years ago this<br>would have taken a ten-person team a year."</div>
  <span class="cite">— one observer's judgment</span>
</div>
```

Variants:
- Without cite: just drop `<span class="cite">`
- With an English quote: `<em class="en">"Thin Harness, Fat Skills."</em>`
- On hero pages: wrap with `style="position:relative;z-index:2"` (so the background overlay doesn't cover it)

---

## Stat Number Matrix

Displays metrics, usually paired with `.grid-6` / `.grid-4`.

```html
<div class="grid-6">
  <div class="stat">
    <span class="m">Duration</span>
    <span class="n">64<em style="font-size:.4em;opacity:.5;font-style:normal"> days</em></span>
    <span class="l">from zero to now</span>
  </div>
  <!-- ... more stats ... -->
</div>
```

Three-part structure: `.m` small mono label → `.n` giant number → `.l` description. Units after the number use `<em>` shrunk to 0.4em, opacity 0.5.

**Common layout containers**:
- `.grid-6` — 3×2 grid (most common, 6 stats)
- `.grid-4` — 2×2 grid (4 stats)
- `.grid-3` — single row of 3 (3 stats / pillars)

---

## Platform Card

Displays a social platform / channel + follower count.

```html
<div class="plat">
  <div class="sub">Weibo</div>
  <div class="name">Weibo</div>
  <div class="nb">289K</div>
</div>
```

Optional fourth line (supplementary note):
```html
<div class="body-zh" style="font-size:max(11px,.8vw);opacity:.5;margin-top:.6vh">
  includes Xiaolvshu sync
</div>
```

**"Also On" variant** (supplementary platforms):
```html
<div class="plat" style="border-top-style:dashed;opacity:.72">
  <div class="sub">Also On</div>
  <div class="body-zh" style="font-weight:600;margin-top:.8vh">
    Bilibili · Zhihu
  </div>
</div>
```

---

## Rowline Table Row

List-style content, one item per row.

```html
<div class="rowline">
  <div class="k">CLAUDE.md</div>
  <div class="v">How you should work — behavior rules + work preferences + prohibitions</div>
  <div class="m">EMPLOYEE · HANDBOOK</div>
</div>
```

Three columns: `.k` serif keyword · `.v` body description · `.m` mono label (right-aligned). The first and last rowlines automatically get top/bottom borders.

**Variant: 2 columns**: `style="grid-template-columns:1fr 3fr"` and drop the `.m` column.

---

## Pillar Card

Three-pillar structure, common on "parallel concepts" pages.

```html
<div class="grid-3">
  <div class="pillar">
    <div class="ic">01</div>
    <div class="t">Three-layer<br>doc system</div>
    <div class="d">CLAUDE.md<br>+ project knowledge base<br>+ guardrail file</div>
  </div>
  <!-- ... more pillars ... -->
</div>
```

**Pillar with icon (for emphasis pages)**:
```html
<div class="pillar" style="padding:4vh 2vw;border:1px solid currentColor;border-color:rgba(10,10,11,.2)">
  <div class="ic"><i data-lucide="compass" class="ico-lg"></i></div>
  <div class="t">Judgment</div>
  <div class="d">The authority on decisions and direction.<br>Trade-offs, taste, sense of direction.</div>
</div>
```

`.ic` can be a serial (`01 / 02 / 03` or `A. / B. / C.`) or a Lucide icon.

---

## Tag & Kicker

**Kicker** is the small hint text above the title (mono, all caps, small size):
```html
<div class="kicker">Last 64 days · build log</div>
<div class="h1-zh">One person. What got built.</div>
```

**Tag** is a standalone pill label (bordered):
```html
<div style="display:flex;gap:1.6vw;flex-wrap:wrap">
  <div class="tag">Wake at 10am</div>
  <div class="tag">Gym Tue / Thu afternoons</div>
  <div class="tag">Still watches shows · plays games at night</div>
</div>
```

---

## Figure Image Frame

**This is the most pitfall-prone component in the template — follow the rules below.**

### Basic structure

```html
<figure class="tile">
  <div class="frame-img" style="height:26vh">
    <img src="images/xxx.png" alt="description">
  </div>
  <figcaption class="frame-cap">
    <span class="pf">Twitter</span>
    <span class="nb">137K</span>
  </figcaption>
</figure>
```

### Key constraints (hard-won lessons — don't violate)

1. **Always fix height with `height:Nvh`, never `aspect-ratio`.**
   - Reason: aspect-ratio inside a grid overflows the parent and stacks images on top of each other.
   - Recommended sizes: `height:18vh` (compact strip) / `22vh` (standard grid) / `26vh` (featured) / `28vh` (large image).

2. **`object-position:top center` (already set in CSS)** — only the bottom may be cropped.
   - Never crop left/right or top — that's where a screenshot's identity lives.

3. **For multiple images in a grid, use an inline grid rather than `grid-3`**:
   ```html
   <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1vh 1.2vw">
     <figure class="tile">...</figure>
     <figure class="tile">...</figure>
     <figure class="tile">...</figure>
   </div>
   ```

4. **Align the figure with the rest of the layout**: give the figure `align-self:end` only to bottom-align a column; never on images inside `frame-img` (see SKILL.md Step 3.2).

### Frame Caption Variants

```html
<!-- Standard: figure name left, number right -->
<figcaption class="frame-cap">
  <span class="pf">Twitter</span>
  <span class="nb">137K</span>
</figcaption>

<!-- Numbered -->
<figcaption class="frame-cap">
  <span class="idx">01</span>
  <span class="pf">AI polish</span>
  <span>Polish</span>
</figcaption>
```

### Image placeholder (design-phase stand-in)

When images aren't ready yet, use a dashed placeholder frame:
```html
<div class="img-slot r-4x3">  <!-- r-4x3 / r-16x9(default) / r-3x2 / r-1x1 -->
  <span class="plus">+</span>
  <span class="label">GitHub screenshot goes here</span>
</div>
```

---

## Icons

**Emoji is strictly forbidden.** Use Lucide via CDN (already imported by template.html).

```html
<i data-lucide="compass" class="ico-lg"></i>     <!-- large icon (pillars) -->
<i data-lucide="target" class="ico-md"></i>      <!-- medium icon (list items) -->
<i data-lucide="check-circle" class="ico-sm"></i>  <!-- small icon (inline) -->
```

**Common Lucide icon names** (grouped by meaning):

- Judgment: `compass`, `target`, `crosshair`, `search-check`
- Relations: `share-2`, `users`, `network`, `link`, `handshake`
- Brand: `crown`, `gem`, `award`, `star`, `badge-check`
- Process: `workflow`, `route`, `arrow-right-left`, `repeat`
- Data: `grid-2x2`, `bar-chart-3`, `trending-up`, `activity`
- Aesthetic: `palette`, `brush`, `eye`, `sparkles`
- Right/wrong: `check-circle`, `x-circle`, `check`, `x`
- Direction: `arrow-right`, `arrow-up-right`, `corner-down-right`

**Inline icon + text combo**:
```html
<div class="h3-zh" style="display:flex;align-items:center;gap:.8em">
  <i data-lucide="target" class="ico-md"></i>
  Judgment — what is worth writing
</div>
```

---

## Ghost Giant Background Word

A "decorative background word" at very low opacity for the magazine feel.

```html
<div class="ghost" style="right:-6vw;top:-8vh">BUT</div>
<div class="ghost" style="left:-8vw;bottom:-18vh;font-style:italic">Harness</div>
```

- Font size 34vw, opacity 0.06
- Common positions: `right:-6vw;top:-8vh` (overscanning top-right) / `left:-8vw;bottom:-18vh` (overscanning bottom-left)
- Content: an English word or number (chapter numbers 01/02/03, keywords BUT/NOW/HERE)

**Note**: on pages using ghost, give other content `position:relative;z-index:2` so it isn't pressed underneath.

---

## Highlight Marker

The "highlighter pen" effect for inline phrases:

```html
<span class="hi">not</span>
<span class="hi">a one-off burst</span>
```

Draws a translucent highlight bar under the text. Light bar on dark themes, dark bar on light themes (CSS handles both).

**When to use**: only on the 1-3 key words, never across large areas.
