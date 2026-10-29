---
name: riso-product
description: Risograph-print-flavored product page / brand page / landing page template — cream paper ground + halftone dot texture + two-to-three color overprint + lishu / brush-style display title with offset color shadows + neobrutalism hard-shadow buttons and cards. 7 color presets (pink+blue / mint+coral / lemon+violet / olive+rose / night+neon / sky blue+mustard / terracotta+duck blue) × 4 layout skeletons (single-page long-scroll landing / home + one detail page / magazine standalone issue / poster-style single screen). Trigger: the user wants a "printed / riso / vintage screen-print / cream paper / print-zine" brand site, product landing, limited-drop page, or indie zine page. Do NOT use it when the user just says "make a product page" with no clear style.
visibility: public
mode: template
carrier: web-page
scenario: brand-landing
pattern_source: reference.html
source_priority: skill-first
triggers:
  - "make a riso-style product page"
  - "print-flavored brand page"
  - "cream paper landing"
  - "vintage screen-print product page"
  - "print-zine brand page"
  - "limited-drop page"
  - "indie zine page"
related_patterns: saas-landing
---

# riso-product — risograph-print-flavored pages

Translate the risograph machine's "two-to-three color overprint + halftone dots + cream paper" into a web page. The skeleton comes from the design prototype of the NOIRLAB acoustics home brand (see `reference.html`), but **this skill gives you temperament and building blocks, not a template**.

## How to use this skill

1. **Read the temperament**: first Read `reference.html` to understand the color blending, shadow direction, type hierarchy, and halftone density. **This step is only to "know what right looks like".**
2. **Pick a palette**: choose one of the 7 presets below (or mix freely from the user's description); **do not default to the reference's pink+blue**.
3. **Pick a skeleton**: choose one of the 4 layout archetypes below (or mix); **cloning the reference's home + 4 detail pages + story page structure wholesale is forbidden**.
4. **Borrow blocks**: the CSS fragments (halftone, paper, neobrutalism shadow, riso shade, offset title shadow) may be used directly.
5. **Check the red lines**: when done, self-check against the "must / must-not" list.

## Visual DNA — none of these may be lost

Drop any one and it is no longer riso:

1. **Cream paper ground**: the background must be neither pure white nor cold gray; it must carry a warm beige/oat/linen tone (lightness 88–94, saturation 8–18)
2. **Halftone overprint**: a global `body::after` using `radial-gradient(circle at 1px 1px, ...)`, 5–8px grid, `mix-blend-mode: multiply`, opacity 30–55%. On large color fields, add another coarser layer in a different color (8–12px)
3. **Two-to-three color overprint hero**: hero / big color blocks use 2-3 `radial-gradient` ellipses in different positions and colors (pink + blue + yellow is the classic trio, but all may be swapped), `mix-blend-mode: multiply`, letting colors naturally produce a third color where they overlap
4. **Lishu/brush display titles** + **offset color shadows**: `text-shadow: 4px 4px 0 var(--accent-a), 8px 8px 0 var(--accent-b)`, mimicking the physical misregistration of screen printing
5. **Neobrutalism hard shadows**: buttons/cards use `box-shadow: Npx Npx 0 var(--ink)` (N=4–8); on hover the shadow collapses to 0 and the element shifts `translate(Npx, Npx)`; 2px solid borders

## Must / must-not (self-check when done)

**Must**:
- [ ] At least 1 text element carries the offset color shadow
- [ ] A visible but non-muddy halftone paper texture globally
- [ ] At least 1 hero / big color block built from 2+ multiply-blended radial gradients
- [ ] At least 1 button/card set with hard shadow + hover collapse
- [ ] The title face is lishu/brush or kai (see the `--hanli` stack), **not PingFang / Source Han Sans**
- [ ] Colors saturated but not harsh; the paper ground softens any strong color's plastic feel

**Must-not**:
- [ ] Do not copy reference.html's `<section>` structure wholesale (announce bar → header → hero → 4-column USP → feature → cat-grid → material → process → gallery → counters → testi → faq → news → footer + 4 detail pages + 1 story page)
- [ ] Do not default to pink #FF3F8E + blue #2240FF — that is NOIRLAB's fingerprint
- [ ] No black-gold / glassmorphism / deep-space gradients / emoji / 3D plastic stickers
- [ ] Do not put a heavy gray overlay on images (halftone stays light, ink stays transparent)
- [ ] Halftone dots must not be same-color same-size — that reads as CSS noise; use at least two layers with different grain and color
- [ ] Do not copy NOIRLAB-owned copy: the brand name, Lin Jian'an, Tongji, 28dB, etc.

## The 7 color presets (pick one; defaulting is forbidden)

Each satisfies "low-saturation cream ground + two strong colors + one support (optional)". Copy into `:root`.

```css
/* 1. Hot pink + federal blue (NOIRLAB original — use with care, it's a dead ringer) */
--paper:#F1EBDA; --ink:#1B1A18;  --a:#FF3F8E; --b:#2240FF; --c:#FFD23A;

/* 2. Mint + coral — fresh, feminine, skincare / tea drinks / subscription boxes */
--paper:#EFEEE5; --ink:#1F2A28;  --a:#FF6B5A; --b:#2BB7A1; --c:#FFC857;

/* 3. Lemon + violet — high-impact, streetwear, sneakers / electronics / young brands */
--paper:#F4EFE4; --ink:#16151A;  --a:#F4E04D; --b:#6A2EE8; --c:#FF4D8D;

/* 4. Olive + rose — composed, inward, tea / wine / home goods / indie zines */
--paper:#EFE9D8; --ink:#1E1C18;  --a:#C24A6C; --b:#5C6E2C; --c:#D9A24A;

/* 5. Night + neon — dark-ground riso, the inverted move */
--paper:#1B1A18; --ink:#F1EBDA;  --a:#FF3F8E; --b:#4DE0C7; --c:#FFD23A;
/* Note: on dark grounds halftone dots must be light-colored with screen blending */

/* 6. Sky blue + mustard — outdoors, coffee, slow living, stationery */
--paper:#EDE8D8; --ink:#1B1B1B;  --a:#3D89C7; --b:#D6A92E; --c:#E0625E;

/* 7. Terracotta + duck blue — craft / handmade / ceramics / folk craft */
--paper:#F0E7D5; --ink:#1F1A16;  --a:#C25538; --b:#2F6B7D; --c:#E4B83B;
```

Substitution rule: replace `var(--pink)` in reference.html with your chosen `var(--a)`, `var(--blue)` with `var(--b)`, `var(--yellow)` with `var(--c)`. **Replace the whole set consistently** — never pink here and red there.

## The 4 layout skeletons (pick one; no more "home + 4 detail pages + story page")

Each comes with riso visuals but a **structurally distinct** shape, so outputs don't look alike.

### Skeleton A — single-page long-scroll landing
```
[announce marquee] → [hero w/ offset title] → [3-column USP] → [product overview grid 3-6 cards]
→ [big single-product spotlight w/ half-body image + spec table] → [founder quote + number counters]
→ [community/real reviews 3 cards] → [FAQ 5–7 accordion] → [subscribe bar] → [footer]
```
**No detail pages**. All products/details fold open on the same page. Fits narrow brands with 1–4 SKUs.

### Skeleton B — two pages: home + single detail (no hash routing)
```
home: [fullscreen hero + offset title] → [4-card product grid] → [brand story 2-column long read] → [footer]
detail: separate detail.html → [big hero + price capsule] → [long read left + sticky spec table right]
        → [3 detail images dgallery] → [other series 3 cards] → [back to home]
```
Fits brands with 1 hero product + a few secondary SKUs (e.g. 1 perfume + 3 accessories).

### Skeleton C — magazine / indie zine layout
```
[cover page: one big word + full-screen riso noise + issue no./date in mono]
[contents: numbered left rail, right column with title + author + section per piece]
[inner pages: asymmetric two-column, long read 6:4 / pull quote 7:3 / big image 1:1 / mixed]
[spine footer: mono small type — section name + page number]
```
Fits brand content sites / brand magazines / cultural brands / publishing projects. May have no CTA buttons at all.

### Skeleton D — poster-style single screen (fold-only)
```
The whole first screen is one page:
  top: announce + brand
  middle: huge offset title (60% of screen height) + one-line subtitle
  bottom: single CTA + one detail thumbnail (opens a lightbox)
No scrolling needed. Fits waitlist / drop / limited release / event.
```

## Copy-ready CSS blocks

### Global paper texture + halftone (required)
```css
body{
  background: var(--paper);
  color: var(--ink);
  position: relative;
}
/* Grain noise (paper-fiber feel) */
body::before{
  content:""; position:fixed; inset:0; pointer-events:none; z-index:9000;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='320' height='320'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .12 0 0 0 0 .10 0 0 0 0 .08 0 0 0 .35 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");
  opacity:.45; mix-blend-mode:multiply;
}
/* Halftone dots */
body::after{
  content:""; position:fixed; inset:0; pointer-events:none; z-index:8990;
  background-image: radial-gradient(circle at 1px 1px, rgba(27,26,24,.08) 1px, transparent 1.4px);
  background-size: 5px 5px;
  mix-blend-mode: multiply; opacity:.55;
}
```

### Offset color title shadow
```css
.headline-riso{
  font-family: var(--hanli);  /* see the font stack below */
  text-shadow: 4px 4px 0 var(--a), 8px 8px 0 var(--b);
  letter-spacing: .04em;
}
/* Inverted version: dark ground */
.headline-riso--invert{
  color: var(--paper);
  text-shadow: 3px 3px 0 var(--a), 6px 6px 0 var(--c);
}
```

### Lishu/brush font stack (for CJK display titles)
```css
:root{
  --hanli: "HakushuReisho", "Yuji Mai", "Yuji Boku",
           "ZCOOL XiaoWei", "STLiti", "LiSu", "SimLi", Georgia, serif;
}
/* CDN fallback if needed */
/* <link href="https://fonts.googleapis.com/css2?family=Yuji+Mai&family=ZCOOL+XiaoWei&display=swap" rel="stylesheet"> */
/* Detect a locally installed Hakushu lishu with local() */
@font-face{
  font-family:"HakushuReisho"; font-display:swap;
  src: local("HOT-ReishoR-K"), local("Hakushu Reisho R"), local("HakushuReisho");
}
```
**Forbidden**: PingFang / Source Han Sans / Microsoft YaHei for titles — the riso flavor dies instantly. Body text may use Inter / system sans.

### Riso three-color overprint (for big blocks / hero)
```css
.riso-shade{
  position: absolute; inset: 0; pointer-events: none;
  background:
    radial-gradient(ellipse 55% 65% at 18% 25%, rgba(255,63,142,.55) 0%, transparent 60%),
    radial-gradient(ellipse 50% 55% at 82% 75%, rgba(34,64,255,.50) 0%, transparent 60%),
    radial-gradient(ellipse 30% 35% at 65% 18%, rgba(255,210,58,.40) 0%, transparent 70%);
  mix-blend-mode: multiply;
}
```
**Key**: the 3 ellipses must be **staggered in position** (top-left / bottom-right / mid-right) for the misregistration feel. Three colors centered on the same point = failure.

### Neobrutalism button
```css
.btn-riso{
  display:inline-flex; align-items:center; gap:14px;
  padding:16px 28px; font-weight:600; letter-spacing:.05em;
  border:2px solid var(--ink); border-radius:999px;
  background: var(--ink); color: var(--paper);
  box-shadow: 5px 5px 0 var(--a);
  transition: all .25s cubic-bezier(.2,.8,.2,1);
}
.btn-riso:hover{
  background: var(--a); color: var(--paper);
  box-shadow: 0 0 0 var(--a);
  transform: translate(5px, 5px);
}
```
4 variants: `--ink` (solid dark) / `--paper` (light ground, colored shadow) / `--ghost` (transparent + ink border) / `--accent` (strong color ground). **Hover collapsing the shadow to 0 + translate** is the heart of this shadow system: on hover the shadow "disappears" rather than "deepens".

### Neobrutalism card
```css
.card-riso{
  border: 2px solid var(--ink);
  box-shadow: 6px 6px 0 var(--ink);
  background: var(--paper-2);
  transition: transform .3s, box-shadow .3s;
}
.card-riso:hover{
  transform: translate(-3px, -3px);
  box-shadow: 9px 9px 0 var(--a);  /* shadow turns color + deepens */
}
```

### Image halftone overlay (without muddying the image)
```css
.img-riso{
  position: relative; overflow: hidden;
  border: 2px solid var(--ink); box-shadow: 5px 5px 0 var(--a);
}
.img-riso > img,
.img-riso > .img{
  width:100%; height:100%; object-fit: cover;
  filter: contrast(1.05) saturate(.9);  /* slightly desaturate, closer to ink */
}
.img-riso::after{
  content:""; position:absolute; inset:0; pointer-events:none;
  background-image: radial-gradient(circle at 1px 1px, rgba(34,64,255,.18) 1px, transparent 1.4px);
  background-size: 5px 5px;
  mix-blend-mode: multiply;
}
```
**Core**: halftone dots sit above the image at only 18% opacity; the image itself stays crisp; `filter: contrast(1.05) saturate(.9)` pulls the digital feel back toward ink.

### Marquee announce bar (optional)
```css
.announce{
  background: var(--a); color: var(--paper);
  border-bottom: 2px solid var(--ink); text-shadow: 1.5px 1.5px 0 var(--b);
  height:40px; display:flex; align-items:center; overflow:hidden;
}
.announce__track{ display:flex; gap:64px; white-space:nowrap; animation: marquee 38s linear infinite; }
@keyframes marquee{ from{transform:translateX(0)} to{transform:translateX(-50%)} }
```

## CJK webfont loading (required)

Google's Yuji Mai / ZCOOL XiaoWei are CJK webfonts and the files are large. Load with the "four-piece" pattern:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" fetchpriority="high"
  href="https://fonts.googleapis.com/css2?family=Yuji+Mai&family=ZCOOL+XiaoWei&display=swap">
<link rel="stylesheet"
  href="https://fonts.googleapis.com/css2?family=Yuji+Mai&family=ZCOOL+XiaoWei&display=swap"
  media="print" onload="this.media='all'">
<noscript><link rel="stylesheet"
  href="https://fonts.googleapis.com/css2?family=Yuji+Mai&family=ZCOOL+XiaoWei&display=swap"></noscript>
```
Then `font-display: swap` + a system lishu fallback (already written into `--hanli`).

## Anti-pattern quick check (if you see these, go back and fix)

| Symptom | What's wrong | Fix |
|---|---|---|
| Title is bold PingFang | no brush/lishu face | switch to `var(--hanli)` |
| Title has no shadow / shadow is black | no offset color shadow | `text-shadow:4px 4px 0 var(--a),8px 8px 0 var(--b)` |
| Background is #FFFFFF / cold gray | wrong paper ground | switch to warm cream #F1EBDA / #EFE9D8 |
| Halftone missing or a muddy blur | wrong opacity, grain too big or too dense | 5–8px grid, opacity 30–55% |
| Images gray and unreadable | heavy overlay added | only halftone at 18% + `filter: contrast(1.05) saturate(.9)` |
| Button hover shadow grows | direction reversed | hover shadow should collapse to 0 + element translate |
| Used NOIRLAB pink+blue throughout | dead ringer | switch to one of the 7 presets |
| Wrote 4 hash-routed detail pages | cloned the reference structure | use skeleton A/B/C/D |

## About reference.html

It sits in this skill's directory with **all images inlined as base64** (deduplicated via CSS `:root` variables `--img-01..06`) — a single ~2.6MB file; double-click to open and see the full effect. **Read the temperament only; never copy the structure**. If you just want to know "what right roughly looks like", look at it; if you want to know "how should I build my new project", use skeletons A/B/C/D and the blocks above.

## Input checklist

Collect these from the user before starting:
1. Brand name + one-line positioning
2. 1–6 products / 1 hero product / a single event (affects skeleton choice)
3. Palette preference (preset name or description)
4. Images: user-provided or picsum placeholders
5. Any "must not resemble NOIRLAB" red lines in the style description (if the user wants "low-key and restrained" → avoid skeleton A's fullscreen marquee)

## Output requirements

- Single-file HTML (hash routing optional; skeletons A/D don't need it, B/C may)
- Responsive on mobile (≥1024 / 900 / 520 breakpoints — implement at least two)
- CJK webfont loaded with the four-piece pattern above
- No comments explaining what the CSS is; the CSS speaks for itself
