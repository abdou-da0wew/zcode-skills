# Theme Presets

Five carefully tuned color palettes that keep the "digital magazine × e-ink" aesthetic intact. **Do not let the user pick custom colors — a bad color pairing ruins the frame instantly.** Choose only from the presets below.

---

## Usage

1. Ask the user which theme to use (or recommend one based on the content)
2. Open the `<style>` block in `assets/template.html`
3. Locate the `:root{` block at the top
4. **Replace as a whole** the lines flagged with the theme-colors comment: `--ink` / `--ink-rgb` / `--paper` / `--paper-rgb` / `--paper-tint` / `--ink-tint`
5. All other CSS goes through `var(--...)` — no other changes needed

---

## 🖋 Ink Classic (Monocle default)

**Best for**: general sharing, business launches, tech products — the safe default for any occasion.
**Tone**: pure ink black + warm off-white; the most magazine-like, in the vein of Monocle / Apricot / A Book Apart.

```css
--ink:#0a0a0b;
--ink-rgb:10,10,11;
--paper:#f1efea;
--paper-rgb:241,239,234;
--paper-tint:#e8e5de;
--ink-tint:#18181a;
```

---

## 🌊 Indigo Porcelain

**Best for**: tech / research / data sharing, engineering culture, deep-dive content, technical launches.
**Tone**: deep indigo + porcelain white — calm, rational, deep, like an academic journal or blue-and-white porcelain.

```css
--ink:#0a1f3d;
--ink-rgb:10,31,61;
--paper:#f1f3f5;
--paper-rgb:241,243,245;
--paper-tint:#e4e8ec;
--ink-tint:#152a4a;
```

---

## 🌿 Forest Ink

**Best for**: nature / sustainability / culture / non-fiction content, outdoor brands, environmental themes.
**Tone**: deep forest green + ivory — grounded and breathable, like a vintage National Geographic.

```css
--ink:#1a2e1f;
--ink-rgb:26,46,31;
--paper:#f5f1e8;
--paper-rgb:245,241,232;
--paper-tint:#ece7da;
--ink-tint:#253d2c;
```

---

## 🍂 Kraft Paper

**Best for**: nostalgia / humanities / reading / history / literary sharing, indie magazines, craft brands.
**Tone**: deep brown + warm beige, like a kraft envelope or an old notebook — warm, with a sense of age.

```css
--ink:#2a1e13;
--ink-rgb:42,30,19;
--paper:#eedfc7;
--paper-rgb:238,223,199;
--paper-tint:#e0d0b6;
--ink-tint:#3a2a1d;
```

---

## 🌙 Dune

**Best for**: art / design / creative / fashion sharing, gallery brochures, aesthetics-first salons.
**Tone**: charcoal + sand — restrained, refined, neutral, like a desert dusk or an architecture monograph.

```css
--ink:#1f1a14;
--ink-rgb:31,26,20;
--paper:#f0e6d2;
--paper-rgb:240,230,210;
--paper-tint:#e3d7bf;
--ink-tint:#2d2620;
```

---

## Picking Guide

| If the content is... | Recommended theme |
|---|---|
| Unsure / first time | 🖋 Ink Classic |
| AI / tech / product launch | 🌊 Indigo Porcelain |
| Content / industry notes / culture | 🌿 Forest Ink |
| Book reviews / lifestyle / humanities | 🍂 Kraft Paper |
| Design / art / brand | 🌙 Dune |

---

## Switching Rules

- **One deck, one theme** — never switch colors midway
- The WebGL shader’s default accent colors (titanium-gold dispersion / silver flow) work with all 5 presets (tested and acceptable)
- Borders / icons driven by `currentColor` automatically follow each section’s text color — no extra adjustments needed
- After picking a theme, the `<title>` text and `chrome` copy can reinforce its semantics (e.g. "Vol.03 · Autumn" pairs well with Kraft Paper)

## ❌ Don’ts

- ❌ **No mixing and matching** (e.g. ink from Ink Classic with paper from Dune) — it will clash completely
- ❌ **Don’t accept an arbitrary hex value from the user** — politely decline and offer the 5 presets to choose from
- ❌ **Don’t edit colors elsewhere in template.html** — every scattered rgba goes through var, so changing `:root` once is enough

After the theme is chosen, tell the user in the skill conversation: "Using 🖋 Ink Classic / 🌊 Indigo Porcelain …" and note it in the deck project record so later iterations stay consistent.
