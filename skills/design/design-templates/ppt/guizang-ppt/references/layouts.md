# Page Layout Library (Layouts)

This document collects the 10 most-used page-layout skeletons. Each is a complete paste-ready `<section class="slide ...">...</section>` code block — swap the copy/images and it works.

---

## ⚠️ Must-read before generating (Pre-flight)

### A. Class names must come from template.html

All classes used in layouts.md (`h-hero` / `h-xl` / `h-sub` / `h-md` / `lead` / `meta-row` / `stat-card` / `stat-label` / `stat-nb` / `stat-unit` / `stat-note` / `pipeline-section` / `pipeline-label` / `pipeline` / `step` / `step-nb` / `step-title` / `step-desc` / `grid-2-7-5` / `grid-2-6-6` / `grid-2-8-4` / `grid-3-3` / `grid-6` / `grid-3` / `grid-4` / `frame` / `frame-img` / `img-cap` / `callout` / `callout-src` / `kicker`) are predefined in the `<style>` block of `assets/template.html`.

**Don't invent new class names**. If you must customize, use inline `style="..."`. If unsure whether a class exists before generating, grep template.html to confirm.

### B. Image ratio rules (very important)

**Always use standard ratios**, never oddball originals like `aspect-ratio: 2592/1798`:

| Scenario | Recommended ratio | How |
|------|---------|------|
| Main image, text-left/image-right | 16:10 or 4:3 | `aspect-ratio:16/10; max-height:54vh` |
| Image grid (multi-image compare) | uniform | **fixed `height:26vh`, no aspect-ratio** |
| Small image left + text right | 1:1 or 3:2 | `aspect-ratio:1/1; max-width:40vw` |
| Full-screen hero visual | 16:9 | `aspect-ratio:16/9; max-height:64vh` |
| Small inline illustration | 3:2 | `aspect-ratio:3/2; max-width:30vw` |

Images must be wrapped in `<figure class="frame-img">`; the inner `<img>` automatically gets `object-fit:cover + object-position:top center` — bottom-crop only, never top/left/right.

### C. Image positioning rules (avoid images piling at the very bottom, clipped by browser toolbars)

**Wrong approaches** (pits already stepped in — don't repeat):
- Using `align-self:end` outside a grid container: `align-self` has no effect outside flex/grid, so the image falls to the end of the document flow and piles at the bottom
- Pinning an image with `position:absolute + bottom:0`: it gets covered by the bottom `.foot` and `#nav` dots
- Setting only `height:N vh` without `max-height`: overflows the viewport on short screens

**Correct approaches**:
- Image-text mixes **must use the grid structure of `.frame.grid-2-7-5`** (or `.grid-2-6-6` / `.grid-2-8-4`)
- Grid containers default to `align-items:start` (preset in the template), so images naturally hug the cell top
- If you need "image bottom aligned with the left column callout": **make the left column a flex column with `justify-content:space-between`** (so the callout hugs the left column's bottom); **keep the right column figure on align-items:start** — do not add `align-self:end`
- Recommend adding inline `style="padding-top:6vh"` to every grid parent for breathing room around the title area

### D. Theme palette and theme rhythm

- Pick the palette from the 5 presets in `references/themes.md`; custom hex values are not allowed
- Theme rhythm (which of light / dark / hero light / hero dark each page uses) has hard rules in the "theme rhythm planning" section below — must-read before generating
- Decide both before picking layouts to avoid rework

---

## 0. Basic structure (identical for all slides)

```html
<section class="slide [light|dark|hero light|hero dark]">
  <div class="chrome">
    <div>Context label · sub-label</div>
    <div>ACT · page number / total</div>
  </div>
  <!-- main content -->
  <div class="foot">
    <div>Page description</div>
    <div>— · —</div>
  </div>
</section>
```

- Non-hero pages should carry a `light` or `dark` theme; hero pages carry `hero light` or `hero dark` (participates in the WebGL theme interpolation)
- `chrome` and `foot` are optional but recommended corner metadata
- **Hero pages are for chapter covers / openings / closings / transitions**; non-hero pages are for body content

### ⚠️ chrome and kicker must not repeat the same message

This is the most common content-duplication problem. The two live on completely different semantic axes:

| Slot | Role | Nature of content | Example |
|------|------|---------|------|
| `.chrome` top-left | **magazine header / nav metadata** | stable "column name" or "chapter category", may repeat across pages | "Act II · Workflow" / "Data · Result" / "lukew.com · 2026.04" |
| `.chrome` top-right | **page + act number** | fixed format | "Act II · 15 / 25" |
| `.kicker` | **this page's unique lead-in** | the headline's "mini-prefix", like the line above a magazine headline; should differ every page | "BUT" / "One person. What got built." / "Phase 01 · design stage" |

**Counter-example** (pit already stepped in): chrome says "Design First · design leads the way" while kicker says "Phase 01 · design stage" — duplicated meaning; readers instantly smell AI-generated content.

**Correct approach**: chrome is the **column label** (stable, reusable across pages); kicker is **this page's hook** (short, dramatic). They complement each other and never translate each other.

### ⚠️ Theme rhythm planning (must-read · mandatory before generating)

**Core mechanism**: every `<section>` must carry one of `light` / `dark` / `hero light` / `hero dark`. JS infers the theme from the class, decides whether the body gets `light-bg`, and thus which of the two WebGL canvases (dark/bright) sits on top. Missing theme or custom names = fallback errors.

#### Per-layout theme defaults

| Layout | Default theme | Reason |
|---|---|---|
| 1. Opening cover | `hero dark` | opening ceremony, strong impact on dark |
| 2. Chapter divider | `hero dark` and `hero light` **must alternate** | breathing rhythm |
| 3. Big-number stats | `light` | numbers need a paper-white ground; occasionally insert `dark` in long stat runs |
| 4. Text+image | **alternate `light` / `dark`** | the workhorse of body rhythm |
| 5. Image grid | `light` | screenshots need a bright ground |
| 6. Pipeline | `light` | flows need clarity |
| 7. Question page | `hero dark` | strong visual impact by default |
| 8. Big quote | **prefer `dark`**, occasionally `light` | the ceremony of a quote lives on dark |
| 9. Comparison | `light` | two columns need clarity |
| 10. Image-text mix | **alternate `light` / `dark`** | rhythm |

#### Hard rhythm rules (grep self-check after generating)

- ❌ **Forbidden**: 3+ consecutive pages of the same theme (both light stacking and dark stacking)
- ❌ **Forbidden**: decks of 8+ pages without at least 1 `hero dark` + 1 `hero light`
- ❌ **Forbidden**: a deck of only `light` body pages with no `dark` body pages — flat, no breathing room
- ✅ **Recommended**: insert 1 hero page (cover / divider / question / big quote) every 3-4 pages

#### 8-page rhythm template (use as-is)

| Page | Theme | Layout | Note |
|---|---|---|---|
| 1 | `hero dark` | cover | opening |
| 2 | `light` | big-number stats | data drop |
| 3 | `dark` | text+image | contrast / story |
| 4 | `light` | pipeline | flow |
| 5 | `hero light` | chapter divider | breath |
| 6 | `dark` | text+image or big quote | |
| 7 | `hero dark` | question page | suspense close |
| 8 | `light` | big quote / ending | closing |

**Draw this table and align on it before writing slides**. Skipping planning and pasting skeletons = an all-light deck.

---

## Layout 1: Opening Cover (Hero Cover)

```html
<section class="slide hero dark">
  <div class="chrome">
    <div>A Talk · 2026.04.22</div>
    <div>Vol.01</div>
  </div>
  <div class="frame" style="display:grid; gap:4vh; align-content:center; min-height:80vh">
    <div class="kicker">Private salon · Li Jigang</div>
    <h1 class="h-hero">One-Person Company</h1>
    <h2 class="h-sub">An organization folded by AI</h2>
    <p class="lead" style="max-width:60vw">
      An AI creator — 110K lines of code in 64 days, shipping continuously on 9 platforms, with almost no change to daily life.
    </p>
    <div class="meta-row">
      <span>Guizang</span><span>·</span><span>indie creator / CodePilot author</span>
    </div>
  </div>
  <div class="foot">
    <div>A talk about AI · organizations · individuals</div>
    <div>— 2026 —</div>
  </div>
</section>
```

**Key points**:
- Use `hero dark` so the WebGL background shows through most of the canvas
- `h-hero` is the largest size (10vw); here it is the title's main visual
- `min-height:80vh + align-content:center` vertically centers the content block
- No page number needed in `.chrome` — the cover stands alone

---

## Layout 2: Chapter Divider (Act Divider)

```html
<section class="slide hero light">
  <div class="chrome">
    <div>Act One · Hard Numbers</div>
    <div>Act I · 01 / 25</div>
  </div>
  <div class="frame" style="display:grid; gap:6vh; align-content:center; min-height:80vh">
    <div class="kicker">Act I</div>
    <h1 class="h-hero" style="font-size:8.5vw">Hard Numbers</h1>
    <p class="lead" style="max-width:55vw">
      Numbers first. Method later.
    </p>
  </div>
  <div class="foot">
    <div>Act One opener</div>
    <div>— · —</div>
  </div>
</section>
```

**Key points**:
- Minimal: kicker + big title + one lead line
- Alternate chapter covers between `hero light` / `hero dark` for rhythm
- `h-hero` can drop from 10vw to 8.5vw to fit longer titles

---

## Layout 3: Big-Number Stat Grid

```html
<section class="slide light">
  <div class="chrome">
    <div>Last 64 days · build log</div>
    <div>Act I / Dev · 02 / 25</div>
  </div>
  <div class="frame" style="padding-top:6vh">
    <div class="kicker">One person. What got built.</div>
    <h2 class="h-xl">The last 64 days</h2>
    <p class="lead" style="margin-bottom:5vh">From zero to open-source CodePilot.</p>

    <div class="grid-6" style="margin-top:6vh">
      <div class="stat-card">
        <div class="stat-label">Duration</div>
        <div class="stat-nb">64 <span class="stat-unit">days</span></div>
        <div class="stat-note">from zero to now</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Lines of Code</div>
        <div class="stat-nb">110K+</div>
        <div class="stat-note">written line by line</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">GitHub Stars</div>
        <div class="stat-nb">5,166</div>
        <div class="stat-note">one open-source repo</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Downloads</div>
        <div class="stat-nb">41K+</div>
        <div class="stat-note">installed on tens of thousands of machines</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">AI Providers</div>
        <div class="stat-nb">19</div>
        <div class="stat-note">cross-platform integrations</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Commits</div>
        <div class="stat-nb">608+</div>
        <div class="stat-note">no collaborators</div>
      </div>
    </div>
  </div>
  <div class="foot">
    <div>Project · CodePilot | github.com/codepilot</div>
    <div>Act I · Dev Numbers</div>
  </div>
</section>
```

**Key points**:
- 3×2 or 4×2 grids are the most stable (see `.grid-6`)
- Every `stat-card` has a fixed structure: label (small English) → nb (big number) → note (caption)
- Keep numbers to 2-3 characters (longer overflows); use K / M shorthand
- Leave ≥5vh of top buffer so the title area grabs the eye first

---

## Layout 4: Text Left, Image Right (Quote + Image)

```html
<section class="slide light">
  <div class="chrome">
    <div>Identity contrast · The Twist</div>
    <div>03 / 25</div>
  </div>
  <div class="frame grid-2-7-5" style="padding-top:6vh">
    <!-- Left column: title + body + callout; flex column lets the callout hug the column bottom -->
    <div style="display:flex; flex-direction:column; justify-content:space-between; gap:3vh">
      <div>
        <div class="kicker">BUT</div>
        <h2 class="h-xl" style="white-space:nowrap; font-size:7.2vw">
          I'm not a programmer.
        </h2>
        <p class="lead" style="margin-top:3vh">
          Never wrote a line of code after college. The last decade was UI design and AI VFX.
        </p>
      </div>
      <div class="callout">
        "Three years ago this<br>
        would have taken a ten-person team a year."
        <div class="callout-src">— one observer's judgment</div>
      </div>
    </div>
    <!-- Right column: standard 16/10 ratio + max-height; no align-self:end -->
    <figure class="frame-img" style="aspect-ratio:16/10; max-height:56vh">
      <img src="images/codepilot.png" alt="CodePilot product screenshot">
      <figcaption class="img-cap">CodePilot · product screenshot</figcaption>
    </figure>
  </div>
  <div class="foot">
    <div>Page 03 · I'm not a programmer</div>
    <div>— · —</div>
  </div>
</section>
```

**Key points**:
- Use `grid-2-7-5` (7 parts left, 5 right); `align-items:start` is preset in the template
- **Left column** uses flex column + `justify-content:space-between`: title hugs top, callout naturally hugs bottom
- **Right column image: do NOT add `align-self:end`**. It slides the image to the cell bottom where short screens let the browser toolbar cover it
- Images must use the **standard 16/10 or 4/3 ratio + `max-height:56vh`**, never oddball originals (`2592/1798` style)

---

## Layout 5: Image Grid (multi-image comparison)

```html
<section class="slide light">
  <div class="chrome">
    <div>Follower proof</div>
    <div>Act I / Ops · 05 / 27</div>
  </div>
  <div class="frame" style="padding-top:5vh">
    <div class="kicker">Proof · follower counts</div>
    <h2 class="h-xl">10 platforms · 6 screenshots</h2>

    <div class="grid-3-3" style="margin-top:4vh">
      <figure class="frame-img" style="height:26vh">
        <img src="images/weibo.png" alt="Weibo 289K">
        <figcaption class="img-cap">Weibo · 289K</figcaption>
      </figure>
      <figure class="frame-img" style="height:26vh">
        <img src="images/twitter.png" alt="Twitter 137K">
        <figcaption class="img-cap">Twitter · 137K</figcaption>
      </figure>
      <figure class="frame-img" style="height:26vh">
        <img src="images/wechat.png" alt="Official account 96K">
        <figcaption class="img-cap">Official account · 96K</figcaption>
      </figure>
      <figure class="frame-img" style="height:26vh">
        <img src="images/jike.png" alt="Jike 26K">
        <figcaption class="img-cap">Jike · 26K</figcaption>
      </figure>
      <figure class="frame-img" style="height:26vh">
        <img src="images/xhs.png" alt="XHS 19K">
        <figcaption class="img-cap">XHS · 19K</figcaption>
      </figure>
      <figure class="frame-img" style="height:26vh">
        <img src="images/douyin.png" alt="Douyin 10K">
        <figcaption class="img-cap">Douyin · 10K</figcaption>
      </figure>
    </div>
  </div>
  <div class="foot">
    <div>Screenshot date · 2026.04</div>
    <div>Page 05 · follower proof</div>
  </div>
</section>
```

**Key points**:
- Critical: every `frame-img` must hard-code `height:NNvh` (no `aspect-ratio`), or the grid overflows
- Images automatically `object-fit:cover + object-position:top` — bottom-crop only
- Carry them in `.grid-3-3` (3×2) or `.grid-3` (3×1)

---

## Layout 6: Two-Column Pipeline

```html
<section class="slide light">
  <div class="chrome">
    <div>My workflow · Workflow</div>
    <div>Act II · 15 / 27</div>
  </div>
  <div class="frame">
    <div class="kicker">Pipeline</div>
    <h2 class="h-xl">Two pipelines</h2>

    <!-- Group 1: text side -->
    <div class="pipeline-section">
      <div class="pipeline-label">Text side · Text Pipeline</div>
      <div class="pipeline">
        <div class="step">
          <div class="step-nb">01</div>
          <div class="step-title">Draft</div>
          <div class="step-desc">AI helps draft the first version</div>
        </div>
        <div class="step">
          <div class="step-nb">02</div>
          <div class="step-title">Polish</div>
          <div class="step-desc">AI polishes away the AI flavor</div>
        </div>
        <div class="step">
          <div class="step-nb">03</div>
          <div class="step-title">Morph</div>
          <div class="step-desc">AI reshapes it for Twitter / XHS</div>
        </div>
        <div class="step">
          <div class="step-nb">04</div>
          <div class="step-title">Illustrate</div>
          <div class="step-desc">AI generates infographics</div>
        </div>
        <div class="step">
          <div class="step-nb">05</div>
          <div class="step-title">Distribute</div>
          <div class="step-desc">one-click publish to 9 platforms</div>
        </div>
      </div>
    </div>

    <!-- Group 2: video side -->
    <div class="pipeline-section">
      <div class="pipeline-label">Visual · video side · Video Pipeline</div>
      <div class="pipeline">
        <div class="step">
          <div class="step-nb">06</div>
          <div class="step-title">Cut</div>
          <div class="step-desc">AI helps edit</div>
        </div>
        <div class="step">
          <div class="step-nb">07</div>
          <div class="step-title">Wrap</div>
          <div class="step-desc">AI helps package</div>
        </div>
        <div class="step">
          <div class="step-nb">08</div>
          <div class="step-title">Cover</div>
          <div class="step-desc">AI generates the cover</div>
        </div>
      </div>
    </div>
  </div>
  <div class="foot">
    <div>Page 15 · my content factory</div>
    <div>Workflow</div>
  </div>
</section>
```

**Key points**:
- Use `.pipeline-section` to group and `.pipeline-label` for group titles
- 3.6vh gap + a top hairline divider between groups (preset in CSS)
- Each step is a fixed nb → title → desc structure
- No step-count limit, but ≤5 steps per row is best; beyond that start a second pipeline

---

## Layout 7: Suspense Close / Question Page (Hero Question)

```html
<section class="slide hero dark">
  <div class="chrome">
    <div>A question left with you</div>
    <div>24 / 27</div>
  </div>
  <div class="frame" style="display:grid; gap:8vh; align-content:center; min-height:80vh">
    <div class="kicker">The Question</div>
    <h1 class="h-hero" style="font-size:7vw; line-height:1.15">
      In your company, which roles<br>
      were never meant<br>
      to be done by humans?
    </h1>
    <p class="lead" style="max-width:50vw">
      This is not a technology question. It is an architecture question.
    </p>
  </div>
  <div class="foot">
    <div>Page 24 · The Question</div>
    <div>— · —</div>
  </div>
</section>
```

**Key points**:
- The more whitespace on a hero page the better; only the question
- Adjust `h-hero` size to length (7vw suits 3 lines, 10vw suits 1 line)
- Break lines manually with `<br>`, making sure breaks fall at semantic points
- Optionally close with a `lead` line as the reveal

---

## Layout 8: Big Quote (serif pull-quote)

```html
<section class="slide light">
  <div class="chrome">
    <div>The Takeaway</div>
    <div>18 / 25</div>
  </div>
  <div class="frame" style="display:grid; gap:5vh; align-content:center; min-height:80vh">
    <div class="kicker">Quote</div>
    <blockquote style="font-family:var(--serif-zh); font-weight:700; font-size:5.8vw; line-height:1.2; letter-spacing:-.01em; max-width:72vw">
      "With no handoff,<br>everyone is building."
    </blockquote>
    <p class="lead" style="max-width:55vw; opacity:.65">
      Without the handoff, everyone builds.<br>
      And that makes all the difference.
    </p>
    <div class="meta-row">
      <span>— Luke Wroblewski</span><span>·</span><span>2026.04.16</span>
    </div>
  </div>
  <div class="foot">
    <div>Page 18 · quote</div>
    <div>— · —</div>
  </div>
</section>
```

**Key points**:
- Whole page is whitespace with just one big quote + source
- `<blockquote>` is enlarged with inline style (5-6vw); don't use `h-hero` (that name is reserved for page main titles)
- Follow with the translation/echo line (lead · opacity:.65) to create hierarchy
- Pair with `meta-row` for source · date

---

## Layout 9: Before / After Comparison (A vs B)

```html
<section class="slide light">
  <div class="chrome">
    <div>Old vs new · The Shift</div>
    <div>12 / 25</div>
  </div>
  <div class="frame" style="padding-top:5vh">
    <div class="kicker">Before / After · paradigm shift</div>
    <h2 class="h-xl" style="margin-bottom:4vh">From handoff to co-building</h2>

    <div class="grid-2-6-6" style="gap:5vw 4vh">
      <!-- Left column: before -->
      <div style="padding:3vh 2vw; border-left:3px solid currentColor; opacity:.55">
        <div class="kicker" style="opacity:.9">Before · the old way</div>
        <h3 class="h-md" style="margin-top:2vh">Design → build → handoff</h3>
        <ul style="margin-top:3vh; padding-left:1.2em; display:flex; flex-direction:column; gap:1.4vh; font-family:var(--sans-zh); font-size:max(14px,1.1vw); line-height:1.55">
          <li>Designers comp in Figma</li>
          <li>Developers eyeball files and translate pixels</li>
          <li>Endless PR loops to align</li>
          <li>Non-technical people can't touch code</li>
        </ul>
      </div>
      <!-- Right column: after -->
      <div style="padding:3vh 2vw; border-left:3px solid currentColor">
        <div class="kicker" style="opacity:.9">After · the new way</div>
        <h3 class="h-md" style="margin-top:2vh">Same tools · parallel · co-building</h3>
        <ul style="margin-top:3vh; padding-left:1.2em; display:flex; flex-direction:column; gap:1.4vh; font-family:var(--sans-zh); font-size:max(14px,1.1vw); line-height:1.55">
          <li>Three roles work simultaneously in Intent</li>
          <li>agents.md as the shared context</li>
          <li>Agents handle alignment / conflicts / animation</li>
          <li>Anyone can safely contribute code</li>
        </ul>
      </div>
    </div>
  </div>
  <div class="foot">
    <div>Page 12 · paradigm shift</div>
    <div>Before / After</div>
  </div>
</section>
```

**Key points**:
- Use `.grid-2-6-6` (1:1) to split left/right
- Left column `opacity:.55` visually demotes the "old"; right column full brightness highlights the "new"
- Both columns use `border-left:3px solid` + padding for a blockquote feel
- Identical column structure: `kicker` → `h-md` → `<ul>` bullets — rhythm stays even

---

## Layout 10: Image-Text Mix (Lead Image + Side Text)

```html
<section class="slide light">
  <div class="chrome">
    <div>Design First</div>
    <div>08 / 16</div>
  </div>
  <div class="frame grid-2-8-4" style="padding-top:6vh">
    <!-- Left column: long body + quote -->
    <div>
      <div class="kicker">Phase 01 · design stage</div>
      <h2 class="h-xl" style="margin-top:1vh; margin-bottom:3vh">Design first · 2 weeks</h2>

      <p class="lead" style="margin-bottom:3vh">
        Visual exploration and the design system completed in Figma — grid / typography / color variables / reusable components — several rounds of desktop and mobile feedback.
      </p>

      <p style="font-family:var(--sans-zh); font-size:max(14px,1.15vw); line-height:1.75; opacity:.78; margin-bottom:2.4vh">
        Within two weeks the visual style, rough structure, and directional content were all stable. This was a solid traditional design process — nothing novel here yet.
      </p>

      <div class="callout" style="margin-top:3vh">
        "This phase was pretty standard.<br>Just a solid Web design process."
        <div class="callout-src">— Luke Wroblewski</div>
      </div>
    </div>
    <!-- Right column: supporting image · portrait or square -->
    <figure class="frame-img" style="aspect-ratio:3/4; max-height:60vh">
      <img src="images/figma.png" alt="Figma design system">
      <figcaption class="img-cap">Figma · Design System</figcaption>
    </figure>
  </div>
  <div class="foot">
    <div>Page 08 · Design First</div>
    <div>about 2 weeks</div>
  </div>
</section>
```

**Key points**:
- `.grid-2-8-4` (8:4) lets the body dominate and the image support
- The left column stacks several information levels: kicker → big title → lead → body paragraph → callout (quote)
- The right column image uses **portrait 3:4** or square 1:1 to avoid competing with the left text for attention
- This layout suits **information-heavy pages** (unlike Layout 4, which carries a single punchline)

---

## Appendix: common grid templates

| Class | Ratio | Use |
|---|---|---|
| `.grid-2-6-6` | 6:6 (1:1) | even halves |
| `.grid-2-7-5` | 7:5 | text-dominant + supporting image |
| `.grid-2-8-4` | 8:4 (2:1) | long text + small image/data |
| `.grid-3` | 1:1:1 | 3 parallel items (cases/screenshots) |
| `.grid-3-3` | 3×2 | 6-image matrix |
| `.grid-6` | 3×2 | 6 data cards |

All grids reserve `gap: 3vw 4vh` (3vw horizontal, 4vh vertical); override individually as needed.

---

## Page-rhythm recommendation

For a 25-30 page talk, the recommended rhythm:

1. **Hero Cover** (page 1)
2. **Act Divider** (act-one opener, hero light or hero dark)
3. **Big Numbers** (drop hard data for impact)
4. **Quote + Image** (identity contrast / hook)
5. **Image Grid** (supporting evidence)
6. **Hero Question** (act close, leave suspense)
7. ... acts two and three repeat the same rhythm ...
8. **Hero Close** (final page, question or thanks)

Hero and non-hero pages should interleave at roughly **2-3 : 1**; never more than 3 consecutive non-hero pages, never more than 2 consecutive hero pages.
