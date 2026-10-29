# Quality Checklist

This checklist comes from the real iteration process of the "one-person company" talk deck. Every item summarizes a pit that was actually stepped in, ordered by importance.

Read it through before generating a PPT; after generating, self-check item by item.

---

## 🔴 P0 · Mistakes you must never make

### 0. Class-name validation before generating (most important)

**Symptom**: pasting a layouts.md skeleton straight into fresh HTML loses all styling — headlines render sans, big-number stats shrink to body size, pipeline pages smear into a blob, images pile at the browser bottom.

**Root cause**: if `template.html`'s `<style>` doesn't define these classes, the browser falls back to default styles.

**Fix**:
- **Before generating a PPT, you must `Read` `assets/template.html`** and confirm every class used in layouts.md is defined
- Most commonly missed classes: `h-hero / h-xl / h-sub / h-md / lead / meta-row / stat-card / stat-label / stat-nb / stat-unit / stat-note / pipeline-section / pipeline-label / pipeline / step / step-nb / step-title / step-desc / grid-2-7-5 / grid-2-6-6 / grid-2-8-4 / grid-3-3 / frame / img-cap / callout-src`
- If a class is genuinely missing, **add it to template.html's `<style>`**; don't inline-redefine per page
- After generating, if you see "headlines are sans" or "pipeline steps crammed into one line", it's almost 100% this problem

### 1. Never use emoji as icons

**Symptom**: emoji (🎯 💡 ✅) inside the magazine aesthetic instantly destroys the tone.

**Fix**: use the Lucide icon library via CDN:

```html
<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
...
<i data-lucide="target" class="ico-md"></i>
...
<script>lucide.createIcons();</script>
```

Common icon names: `target / palette / search-check / compass / share-2 / crown / check-circle / x-circle / plus / arrow-right / grid-2x2 / network`

### 2. Images may only be cropped at the bottom; never cut left/right or top

**Symptom**: stretching images with `aspect-ratio` stacks them or cuts key information (like a screenshot's title bar) when the parent is too small.

**Fix**: the image container uses **fixed height + overflow hidden**; the image uses `object-fit:cover + object-position:top`:

```html
<figure class="frame-img" style="height:26vh">
  <img src="screenshot.png">
</figure>
```

CSS already presets `.frame-img img` to `object-position:top` — bottom-crop only.

**Never write this** (overflows the container inside grids):

```html
<!-- bad example -->
<figure class="frame-img" style="aspect-ratio: 16/9">...</figure>
```

**Exception**: a single hero visual (outside grids) may use `aspect-ratio + max-height`, because the parent provides a fallback.

### 2b. Light pages with a dark WebGL = muddy grey (theme switching not working)

**Symptom**: every light page's background looks veiled in grey; even hero light is grey.

**Root cause**: JS switches the two canvases' opacity based on the slide's theme. If the deck opens with hero dark and nothing switches the bg to light, the body never gets the `light-bg` class and `canvas#bg-dark` stays on top.

**Fix**:
- The template's `go()` function infers the theme from `classList` (`light` / `dark`), so **every slide must explicitly carry a `light` or `dark` class**. Don't omit it and don't invent custom theme names
- Hero pages use `hero light` / `hero dark`; body pages use `light` / `dark`. A bare `hero` without a theme color is broken
- A deck must contain at least one **non-hero light page** so the body gets a chance to add `light-bg`

### 2b-2. All-light deck, no rhythm

**Symptom**: except the `hero dark` cover, every page defaults to `light` — visually flat, no breathing room, a wash of white.

**Root cause**: layouts.md skeletons default to `light`; pasting them without adjusting themes produces an all-light deck.

**Fix**:
- **Draw the "theme rhythm table" before generating**: mark each page as one of `hero dark` / `hero light` / `light` / `dark`, align on it, then code
- **Hard rules**: 3+ consecutive same-theme pages = not allowed; decks of 8+ pages need ≥1 `hero dark` + ≥1 `hero light`; an all-`light` body is not allowed — you need `dark` body pages
- **Pick theme by layout** (see "theme rhythm planning" at the top of layouts.md):
  - Text+image (Layout 4), big quote (Layout 8), image-text mix (Layout 10) → **alternate `light` / `dark`**
  - Big-number stats, image grids, pipelines, comparison pages → `light` (screenshots/numbers/flows need a bright ground)
  - Cover, question pages → `hero dark`
  - Chapter dividers → alternate `hero dark` and `hero light`
- **Self-check after generating**: `grep 'class="slide' index.html`, visually confirm the rhythm alternates

### 2c. Don't let chrome and kicker say the same thing

**Symptom**: top-left `.chrome` reads "Design First · design leads the way" and the same page's `.kicker` reads "Phase 01 · design stage" — translated duplicates, heavy AI flavor.

**Fix**:
- **chrome = magazine header / nav label**: may repeat across pages (e.g. "Act II · Workflow", "Data · Result", "lukew.com · 2026.04")
- **kicker = this page's unique lead-in**: short, hooky, a "mini-prefix" of the headline (e.g. "BUT", "One person. What got built.", "The Question")
- One describes the column/act, the other describes this page — never translate each other

### 3. Headline size must fit the screen width / character count

**Symptom**: a CJK headline set too large (e.g. 13vw) fits one character per line — the forced wrapping is hideous.

**Fix**:
- `h-hero` (largest): 10vw, **and headline length ≤ 5 characters**
- `h-xl` (next): 6vw-7vw
- Break long titles manually with `<br>`; don't rely on auto-wrap
- Add `white-space:nowrap` when needed

**Example**: "I am not a programmer." uses `h-xl` at 7.2vw + nowrap, fits on one line.

### 4. Font roles: serif headlines, sans body

**Fix**:
- Headlines, key quotes, big numbers → **serif** (Noto Serif SC + Playfair Display + Source Serif)
- Body, descriptions, pipeline step names → **sans** (Noto Sans SC + Inter)
- Metadata, code, labels → **mono** (IBM Plex Mono + JetBrains Mono)

All fonts load via Google Fonts CDN, preconfigured in the template.

### 4b. Don't bottom-align images with `align-self:end`

**Symptom**: in text-left/image-right layouts, adding `align-self:end` on `<figure>` to align the right column image with the left column callout bottom. Results:
- If the parent isn't a grid (e.g. the class is undefined), `align-self` does nothing and the image drops to the document flow bottom, clipped by the browser toolbar
- Even in a grid, the image hugs the cell bottom and on short screens is still covered by `.foot` and the `#nav` dots

**Fix**:
- Image-text mixes **must use `.frame.grid-2-7-5`** (or `.grid-2-6-6`/`.grid-2-8-4`)
- The right column `<figure class="frame-img">` uses a **standard ratio 16/10 or 4/3 + max-height:56vh** and naturally hugs the top
- To make the left column callout look "bottom-anchored", give the **left column** flex column + `justify-content:space-between`; don't touch the right column

### 4c. Don't use oddball original image ratios

**Symptom**: ratios copied from the original image like `aspect-ratio: 2592/1798` produce strange whitespace or overflow at different screen sizes.

**Fix**: whatever the original ratio, the frame always uses a standard ratio **16/10 / 4/3 / 3/2 / 1/1 / 16/9**. Images auto-fit with `object-fit:cover + object-position:top`: top preserved, a small bottom crop is harmless.

### 5. No heavy borders / shadows on images

**Symptom**: strong shadows or black frames added for a "premium" feel instantly turn it into a business PPT.

**Fix**: at most a 1-4px small radius + **extremely faint grain** (already in the template). No `box-shadow`, no `border` (unless a 1px very light grey).

---

## 🟡 P1 · Layout rhythm

### 6. Alternate hero and non-hero pages

**Recommended rhythm** (25-30 pages):
```
Hero Cover → Act Divider (hero) → 3-4 pages non-hero → Act Divider (hero)
→ 4-5 pages non-hero → Hero Question → ... → Hero Close
```

2+ consecutive hero pages tire people; 4+ consecutive non-hero pages kill the rhythm.

### 7. Alternate big-number pages and dense pages

Big-number pages (stats / hero questions) and dense pages (pipelines / image grids) should alternate so the audience's eyes don't tire.

### 8. Keep terminology for the same concept consistent

**Symptom**: one moment "Skills", the next "Competence", then "thin harness, fat skills" — inconsistent across the deck.

**Fix**:
- Prefer the **English term** (Skills / Harness / Pipeline / Workflow) — these are familiar to the audience
- **Don't force-translate**; forced translations read stiff
- One spelling per term across the whole deck

### 9. Footer chrome page numbers must be consistent

Use the `XX / total` format (e.g. `05 / 27`). **Don't add a dynamic page counter in the top-right** (it duplicates `.chrome`).

---

## 🟢 P2 · Visual polish

### 10. WebGL background overlay opacity

**dark hero**: overlay 12-15% (WebGL clearly visible)
**light hero**: overlay 16-20% (WebGL subtly visible, not fighting text)
**ordinary light/dark pages**: overlay 92-95% (barely visible)

If a page has very little text (hero question), the overlay can be thinner; if body text is dense, thicken the overlay to guarantee readability.

### 11. Light hero shader must not have a strong center point

**Symptom**: Spiral Vortex or radial ripples are too conspicuous on the light theme — like a Windows 98 screensaver.

**Fix**: light heroes use center-less FBM domain-warped flow, with the base color kept silver/paper (near #F0F0F0 / #FBF8F3) and subtle chromatic offset (below 0.05).

### 12. Dark heroes allow more visual impact

Dark heroes can use shaders with central structure like Holographic Dispersion (titanium-gold aberration), because a black ground holds more visual information.

### 13. Text-left/image-right alignment

- Left column text group `justify-content:space-between`: title hugs top, quote box hugs bottom
- Right column image `align-self:end`: aligns with the left column's bottom element
- The grid overall uses `align-items:start` (not `center` / `end`)

### 14. Subtle image corner radius

All `.frame-img` and `.frame-img img` get `border-radius:4px` — visually "soft" but not soggy. **Never exceed 8px**, or it looks like consumer-app UI.

---

## 🔵 P3 · Operational details

### 15. Use relative image paths

Images live under `images/`; HTML references them relatively as `images/xxx.png`, never absolute paths.

### 16. Page numbers are hard-coded in `.chrome`

JS dynamically computes the total and extends the bottom flip dots, but `XX / N` inside `.chrome` is hard-coded. Update N by hand when adding/removing pages.

### 17. Keep the flip navigation

The template supports by default: ← → / wheel / touch swipe / bottom dots / Home·End. Don't delete the navigation logic in JS.

### 18. Don't hard-set `height:100vh`; use `min-height:80vh`

`100vh` makes content exactly fill the screen, but browser toolbars/tab bars eat into the height and content overflows. `min-height:80vh + align-content:center` is more robust.

---

## 🧪 Final self-check

After generating the PPT, walk this checklist item by item:

```
Pre-flight (before generating)
  □ Read template.html's <style>; confirmed all needed classes exist
  □ Decided the Layout (1-10) for every page
  □ Drew the "theme rhythm table": every page marked hero dark / hero light / light / dark
  □ Rhythm table meets hard rules: no 3 consecutive same-theme pages / ≥1 hero dark + ≥1 hero light (8+ pages) / at least 1 dark body page
  □ `<title>` changed to the actual deck title (grep "[REQUIRED]" should return nothing)

Content
  □ Per-act page-count proportions are sensible (not top-heavy)
  □ No emoji used as icons
  □ Terms like Skills / Harness used consistently
  □ Every page has a clear kicker + headline + body hierarchy

Typography
  □ No headline wraps one character per line
  □ Image grids use height:Nvh, not aspect-ratio
  □ Images cropped only at the bottom; top and sides intact
  □ Serif/sans font roles match the template
  □ Multiple pipeline groups have clear separation

Visual
  □ Hero and non-hero pages alternate
  □ WebGL background visible on hero pages
  □ Images have subtle corner radius
  □ No heavy shadows or borders

Interaction
  □ ← → page flips work
  □ Bottom dot count matches total pages
  □ chrome page numbers match actual page numbers
  □ ESC triggers the index view (if kept)
```

Only when every box is checked is the PPT qualified.
