---
name: dot-matrix-xhs
description: >-
  Bayer-dithered black-and-white dot-matrix covers for Rednote — magazine-feel posters / indie
  zine cover template. Black ground + real Canvas Bayer 8x8 ordered dithering that turns any
  photo into a pure black-and-white dot matrix, plus a top-and-bottom vignette, magazine-column
  four-corner text (issue number / column / wordmark / credit), an oversized heavy CJK display
  title set with Noto Sans JP Black in a 2x2 grid, and a center bracketed issue number. 4 layout
  skeletons (single-image cover / image-top text-bottom / series triptych / long-form inner
  page); container-query (cqh) units keep the type crisp at any size. Triggers: "dot-matrix
  feel / dither / 1-bit / black-and-white grain / Rednote cover / Vol issue poster / indie zine
  / newsprint feel". NOT multi-section product pages, NOT color posters.
visibility: public
mode: template
carrier: fixed-image
scenario: social-content
pattern_source: dot-matrix.html
source_priority: skill-first
triggers:
  - "make a dot-matrix Rednote cover"
  - "black-and-white grain cover"
  - "1-bit poster"
  - "Vol issue cover"
  - "indie zine cover"
  - "newsprint-feel cover"
  - "dither"
related_patterns: social-card-editorial
---

# dot-matrix-xhs — Bayer-dithered black-and-white dot-matrix covers

Take any photo and run a real-time Bayer 8x8 ordered dither on it, turning it into a "newsprint dot matrix", then layer it under magazine-style four-corner text and the CJK 2x2 display-title skeleton. **The container ratio is fixed at 1280x1644 (Rednote portrait cover)**, but layout uses container-query (cqh) units, so it stays crisp when scaled to any size.

## How to use this skill

1. **Get the feel first**: Read `dot-matrix.html` (the "A Fire at Midnight" example) and study the Bayer dithering grain density, vignette strength, and the hierarchy of the four corner columns. **This step only exists to learn what "right" looks like.**
2. **Pick a skeleton**: choose one of the 4 layout skeletons below (single-image cover / image-top text-bottom / series triptych / long-form inner page). **Do not clone "A Fire at Midnight" wholesale** (the same 2x2 + center brackets + bottom wordmark appearing together is a face-clone).
3. **Copy the building blocks**: the Canvas Bayer function, container-query typography, and four-corner text layout can be taken as-is.
4. **Check the red lines**: after writing, self-check against the "Must / Must not" list.

## Visual DNA — none of this can be dropped

Drop any one item and it is no longer dot-matrix magazine feel:

1. **Black ground + real Canvas Bayer dither**: the base layer is always an image that has been Bayer 8x8 dithered — **not CSS noise, not an SVG filter, not a pre-rendered PNG; it must run live on Canvas**. Any image (portrait, landscape, object) only becomes correct after `adjustBrightness(-20~-30) + adjustLevels(60~80, 190~210) + bayerDither`.
2. **Hard-edged pixel rendering**: the canvas must have `image-rendering:pixelated`; the dot matrix keeps hard edges when scaled and never turns blurry or grey.
3. **Top-and-bottom vignette**: `linear-gradient(180deg, rgba(0,0,0,.55) 0%, transparent 18%, transparent 70%, rgba(0,0,0,.45) 100%)`, which gives the top issue number and bottom wordmark their footing; **no four-corner vignette** (a circular falloff instantly reads as a phone-camera lens).
4. **Magazine-column four corners**: top-left = issue number (`No 04 / 2026`), top-right = column in English + small CJK, bottom-left = main wordmark, bottom-right = year + credit. **Fill at least 3 corners** — this is the indie-zine signature; fewer than 3 is just an image with captions.
5. **Oversized heavy CJK display title**: `Noto Sans JP Black` with `PingFang SC` fallback, `font-weight:900`, `line-height:1.1`, `letter-spacing:0` (dense CJK setting adds no tracking). **No light weights / kaiti / lishu / rounded faces**.
6. **White text with a light text-shadow**: every piece of text over the dot-matrix image gets `text-shadow:0 0 .8cqh rgba(0,0,0,.85)` so white type stays readable even over light dither areas.

## Must / Must not (self-check after writing)

**Must**:
- [ ] Canvas really performs Bayer dithering (not a CSS filter, not SVG noise, not a pre-rendered image)
- [ ] The container has a fixed `aspect-ratio` (1280/1644 for covers; posters may choose freely)
- [ ] The container sets `container-type:size` and layout units use `cqh` / `cqw`
- [ ] At least 3 of the 4 corners carry content (pick 3 of: issue number, column, wordmark, credit)
- [ ] Main title weight ≥ 800
- [ ] The CJK webfont loads with the "four-piece" setup (preconnect + preload + print-onload + noscript)
- [ ] The canvas carries all three `image-rendering:pixelated / -moz-crisp-edges / crisp-edges` lines

**Must not**:
- [ ] Do not reproduce the full "2x2 CJK character array + center brackets + bottom wordmark" combination — that is the "A Fire at Midnight" fingerprint
- [ ] Do not fake the dot matrix with SVG noise / `filter: contrast` / `background-image: radial-gradient(...dot)` — it reads fake instantly
- [ ] Do not let the dot matrix keep greys (Bayer output must be pure black 0 or pure white 255, binary, no in-between values)
- [ ] Do not add saturated color to the image (sunset filters, teal-blue casts, cream tones) — this aesthetic is 1-bit pure black and white
- [ ] No rounded corners — frames, buttons, cards are all square
- [ ] No emoji / 3D stickers / gradient color / glassmorphism / floating shadows
- [ ] No PingFang Regular / Source Han Sans Light for titles — Heavy / Black weight is required
- [ ] Do not copy "SHEN / YE / GOU / HUO + VOL IV / 2026 + Night Fire wordmark + Rednote ID 955873829" — that is the example's fingerprint

## The four layout skeletons (pick one; do not rebuild the "A Fire at Midnight" combo)

Each skeleton carries the dither + four-corner-text DNA, but **the structures are completely different**, so outputs do not look like clones.

### Skeleton A — Single-image cover ("A Fire at Midnight" prototype; reference with care)
```
[Base]    Full-bleed Bayer dithered image + top/bottom vignette
[Corners] Top-left issue no. / top-right column + small CJK / bottom-left wordmark / bottom-right credit
[Upper]   hr divider + 2x2 oversized CJK title + English italic subtitle
[Center]  Bracketed issue number or theme word
```
Good for: a single visually strong photo as the cover (portrait close-up, landscape, still life). 1280x1644.

### Skeleton B — Image on top, text below
```
[Top 60%]    Bayer dithered image + issue number + column
[Bottom 40%] Pure black zone; large title on the left (one or two lines), quote + attribution on the right
[Footer bar] Hairline + wordmark + issue number
```
Good for: long titles, or projects that need deck copy, quotes, and attributions (no forced 2x2 grid). 1280x1644 or 1080x1350.

### Skeleton C — Series triptych
```
[Split into 3 columns]  Each column is an independent Bayer dithered image (portrait / object / environment)
                        Each column bottom carries its own small title + number 01 / 02 / 03
[Top bar]               Shared issue number + column
[Bottom bar]            Shared wordmark + collection name
```
Good for: series reporting, group portraits, product lineups, travelogue covers. Landscape 1644x1280 or portrait 1280x1644.

### Skeleton D — Inner page / long-form text column
```
[Top bar]    Issue number + column + hr
[Left col]   Sticky large title + quote (40% width)
[Right col]  Long body copy (multi-paragraph p + inline quotes), with 1-2 small dithered images
[Bottom bar] Page number + wordmark
```
Good for: zine inner pages, long essays, interviews (not just a cover — actual reading content). 1280x1800+ or A4 ratio.

## Copy-paste code blocks

### Bayer 8x8 dither (core; do not simplify)
```js
function bayerDither(ctx, W, H){
  const d = ctx.getImageData(0,0,W,H), px = d.data;
  const m = [
    [ 0,32, 8,40, 2,34,10,42],[48,16,56,24,50,18,58,26],
    [12,44, 4,36,14,46, 6,38],[60,28,52,20,62,30,54,22],
    [ 3,35,11,43, 1,33, 9,41],[51,19,59,27,49,17,57,25],
    [15,47, 7,39,13,45, 5,37],[63,31,55,23,61,29,53,21]
  ];
  for (let y=0; y<H; y++) for (let x=0; x<W; x++){
    const i=(y*W+x)*4;
    const luma = (0.299*px[i] + 0.587*px[i+1] + 0.114*px[i+2]) / 255;
    const t = (m[y%8][x%8] + 0.5) / 64;
    const v = luma > t ? 255 : 0;
    px[i]=px[i+1]=px[i+2]=v; px[i+3]=255;
  }
  ctx.putImageData(d,0,0);
}
```
**Key point**: do not swap the 8x8 matrix for 4x4 (grain too coarse) and do not swap it for Floyd-Steinberg (error diffusion is a different flavor; the grain "flows"). Dot density = the canvas internal resolution: W=600 H=771 is the cover default; go 900x1158 for finer grain or 400x514 for coarser.

### Preprocessing: darken + stretch contrast (so Bayer produces a crisp black/white matrix)
```js
function adjustBrightness(ctx, W, H, delta){
  const d = ctx.getImageData(0,0,W,H), px = d.data;
  for (let i=0; i<px.length; i+=4)
    for (let c=0; c<3; c++){ let v=px[i+c]+delta; px[i+c]=v<0?0:v>255?255:v; }
  ctx.putImageData(d,0,0);
}
function adjustLevels(ctx, W, H, lo, hi){
  const d = ctx.getImageData(0,0,W,H), px = d.data, scale = 255 / (hi - lo);
  for (let i=0; i<px.length; i+=4)
    for (let c=0; c<3; c++){ let v=(px[i+c]-lo)*scale; px[i+c]=v<0?0:v>255?255:v; }
  ctx.putImageData(d,0,0);
}
```
**Call order is fixed**: `drawImage → adjustBrightness(-25) → adjustLevels(70, 195) → bayerDither`. **Never dither first and adjust contrast after** — the dither output is already binarized, so later contrast adjustments do nothing.

### Canvas element setup
```html
<canvas class="bg" id="bg" width="600" height="771"></canvas>
<img class="src" id="src" src="YOUR_IMG_URL" crossorigin="anonymous" alt="">
```
```css
canvas.bg{
  position:absolute; inset:0;
  width:100%; height:100%;
  image-rendering:pixelated;
  image-rendering:-moz-crisp-edges;
  image-rendering:crisp-edges;
  z-index:0; display:block;
}
img.src{ display:none }
```
The source `<img>` exists only to feed canvas `drawImage` and is never displayed. `crossorigin="anonymous"` is required — otherwise getImageData throws a cross-origin error.

### Complete Canvas processing pipeline
```js
(async function(){
  if (document.fonts && document.fonts.ready){ try { await document.fonts.ready; } catch(e){} }
  const img = document.getElementById('src');
  const canvas = document.getElementById('bg');
  const ctx = canvas.getContext('2d');
  const W = canvas.width, H = canvas.height;

  const ready = (img.complete && img.naturalWidth > 0)
    ? Promise.resolve()
    : new Promise((res, rej) => { img.onload = res; img.onerror = rej; });
  try { await ready; } catch(e){ console.warn('img failed', e); return; }

  const ratio = Math.max(W / img.naturalWidth, H / img.naturalHeight);
  const dw = img.naturalWidth * ratio, dh = img.naturalHeight * ratio;
  ctx.drawImage(img, (W - dw) / 2, (H - dh) / 2, dw, dh);

  adjustBrightness(ctx, W, H, -25);
  adjustLevels(ctx, W, H, 70, 195);
  bayerDither(ctx, W, H);
})();
```

### Container-query typography (crisp at any size)
```css
.frame{
  position:relative;
  height:min(94vh, 1644px);
  aspect-ratio: 1280 / 1644;
  container-type:size;
  background:#000; color:#fff;
  overflow:hidden;
}
.title{ font-size:12cqh; }
.credit{ font-size:.85cqh; letter-spacing:.28em; }
```
**Why cqh instead of vh**: vh tracks the viewport, so text does not follow when the container resizes. cqh tracks the `.frame` container, so the cover keeps its proportions even scaled to half size.

### Top-and-bottom vignette
```css
.vignette{
  position:absolute; inset:0; z-index:1; pointer-events:none;
  background: linear-gradient(180deg,
    rgba(0,0,0,.55) 0%, rgba(0,0,0,0) 18%,
    rgba(0,0,0,0) 70%, rgba(0,0,0,.45) 100%);
}
```
The top is a bit heavier (.55 vs .45) because the issue number is set smaller than the credit and needs more contrast protection.

### Four-corner column layout
```css
.layer{
  position:absolute; inset:0; z-index:2;
  padding:3.6cqh 4.4cqh;
  display:flex; flex-direction:column;
  pointer-events:none;
}
.layer *{ text-shadow:0 0 .8cqh rgba(0,0,0,.85) }
.top{
  display:flex; justify-content:space-between; align-items:center;
  font-size:.95cqh; letter-spacing:.32em; text-transform:uppercase; font-weight:500;
}
.bottom{
  margin-top:auto;
  display:flex; justify-content:space-between; align-items:flex-end;
}
```
`margin-top:auto` pins the footer to the bottom no matter how much content sits above it.

### CJK 2x2 title (skeleton A only)
```html
<div class="title-grid">
  <div class="col"><span class="sm">SHEN</span><span class="sm">GOU</span></div>
  <div class="col"><span class="lg">YE</span><span class="lg">HUO</span></div>
</div>
```
```css
.title-grid{
  display:inline-flex; align-items:flex-start; gap:0;
  font-family:'Noto Sans JP','PingFang SC','Heiti SC',sans-serif;
  font-weight:900; line-height:1.1; letter-spacing:0;
}
.title-grid .col{ display:flex; flex-direction:column }
.title-grid .sm, .title-grid .lg{ font-size:12cqh }
```
**Constraint**: it must be a 4-character CJK word split into two columns by position — characters 1 & 3 in one column, 2 & 4 in the other (romanized here as SHEN/GOU + YE/HUO, i.e. the example phrase "shen-ye-gou-huo", a bonfire at midnight) — reading down each column, not in linear reading order. Do not use this skeleton for 3, 5, or 6 characters.

### Bracketed issue-number ornament
```css
.brackets{
  position:relative; padding:1cqh 2.6cqh;
  font-weight:500; font-size:1.1cqh; letter-spacing:.36em;
  text-transform:uppercase;
}
.brackets::before, .brackets::after{
  content:''; position:absolute;
  width:1.3cqh; height:1.3cqh; border:1px solid #fff;
}
.brackets::before{ top:0; left:0; border-right:none; border-bottom:none }
.brackets::after{ bottom:0; right:0; border-left:none; border-top:none }
```
Two L corners (top-left + bottom-right) imitate a camera viewfinder / print crop marks.

## CJK webfont loading (required)

`Noto Sans JP` Heavy is a Japanese face with heavy weights (with CJK kanji fallback) and its files are large; CJK text prefers the local PingFang/Heiti stack. Use the "four-piece" setup:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" fetchpriority="high"
  href="https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,400;0,500;0,600;1,400&family=Noto+Sans+JP:wght@900&display=swap">
<link rel="stylesheet" media="print" onload="this.media='all'"
  href="https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,400;0,500;0,600;1,400&family=Noto+Sans+JP:wght@900&display=swap">
<noscript><link rel="stylesheet"
  href="https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,400;0,500;0,600;1,400&family=Noto+Sans+JP:wght@900&display=swap"></noscript>
```
The font stack must always include the `'PingFang SC','Heiti SC'` fallback; use Inter for small English text (italic reserved for subtitles).

## Input checklist

Get all of this from the user before starting:
1. **A base image** (required) — URL or local path. Faces / landscapes / still life all work, but **contrast must be strong**; a washed-out image turns to mush after dithering. Check it in an image editor first — as long as the subject separates from the background, it is fine.
2. **Issue number + column** (required) — `No 04 / 2026` + column in English (CAMPING / TRAVEL / FOOD...) + 2-4 CJK characters as small text.
3. **Title** (required) — skeleton A: 4 characters + an English italic subtitle; skeletons B/C/D: free length.
4. **Wordmark + credit** (required) — main brand in large type, 2-4 characters + year / Rednote ID / author name / source.
5. **Ratio** (optional) — default 1280/1644; may specify 1080/1350, 1644/1280, or 1x1.
6. **Dither grain density** (optional) — "fine / medium / coarse" maps to canvas internal widths 900 / 600 / 400.

## Anti-pattern quick reference (if you see these, go back and fix)

| Symptom | What went wrong | Fix |
|---|---|---|
| Dot matrix is mush, original unrecognizable | No adjustLevels contrast stretch | Add `adjustLevels(70, 195)`; without it there is no dot-matrix feel |
| Matrix all black or all white | brightness/levels pushed too far | brightness ∈ [-30, -10], levels lo<80 hi>180 |
| Text floats unreadably over the image | Missing text-shadow / vignette | `text-shadow:0 0 .8cqh rgba(0,0,0,.85)` + top/bottom gradients |
| Matrix blurs when scaled | Missing `image-rendering:pixelated` | Add all three image-rendering lines on the canvas |
| Type does not follow the container when scaled | Used vh instead of cqh | Container sets `container-type:size`; all font sizes use cqh |
| Title looks thin and soft | Used PingFang Regular / Light | Switch to Noto Sans JP 900 + PingFang Heavy fallback |
| CJK title tracking looks like a shop sign | Added letter-spacing | Dense CJK setting: `letter-spacing:0` |
| Corner text fills only 1-2 corners | Magazine feel collapses into "image with captions" | Fill at least 3 corners (pick 3 of issue no. / column / wordmark / credit) |
| Emoji / rounded corners / color used | Violates the 1-bit black-and-white aesthetic | Remove them; return to pure black-and-white + square corners |
| Matrix looks like CSS noise | Real Canvas Bayer never ran | Must run `bayerDither` on Canvas; no SVG/CSS simulation |
| Output is a dead ringer for "A Fire at Midnight" | Another skeleton was not chosen | Force one of B/C/D |

## About dot-matrix.html

It sits in the same directory as this skill and is the complete "A Fire at Midnight" example (a skeleton A implementation). **Study only the Bayer call order, the cqh layout structure, and the four-corner hierarchy** — do not carry "SHEN / YE / GOU / HUO + VOL IV / 2026 + Night Fire wordmark + Rednote ID 955873829" verbatim into a new project — that is the example's fingerprint.

## Output requirements

- Single-file HTML (HTML + CSS + Canvas processing JS)
- Container queries + fixed `aspect-ratio`; crisp when scaled
- CJK webfont loaded with the four-piece setup
- All three canvas `image-rendering` lines present
- No comments explaining what Bayer is — a correct call order is enough
