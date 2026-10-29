# Style Preset Library

Each preset gives 8 `:root` CSS variables + 5 ASCII layer colors + the hero background gradient. Changing anything else requires corresponding follow-up changes (image filter, scrambler character colors, etc.).

> **Color principle**: the 5 ASCII layers must be **simultaneously readable on the background + harmonious with each other**. Keep the same warm/cool family with slight variation; don't assume "contrast = pretty".

---

## 1. Deep-space cyan (default · cosmic-cyan)

The most restrained space feel: gemstone blue-purple ground with cyan/pink/amber glowing layers. Fits local-first AI, note/writing tools, indie software, CLI tools.

```css
:root{
  --bg:#05060f;
  --fg:#e6e8ff;
  --dim:#7a7fa8;
  --accent:#8be9ff;     /* cyan */
  --accent2:#ff6ad5;    /* pink */
  --accent3:#c792ea;    /* purple */
  --line:#1a1d3a;
  --hl:#0d1024;
  --paper:#0a0c1f;
}
.hero{ background: radial-gradient(ellipse at 30% 20%, #1a0a2e 0%, #05060f 55%, #000 100%); }
#ascii-nebula  { color:#a87bd6; }   /* nebula */
#ascii-stars   { color:#cfe6ff; }   /* stars */
#ascii-planet  { color:#8be9ff; }   /* planet */
#ascii-asteroids{ color:#f5b971; }  /* asteroids */
#ascii-comets  { color:#ff8fd2; }   /* comets */
```
Image filter: `hue-rotate(200deg) saturate(.9) contrast(1.1) brightness(.6)`

---

## 2. Warm letterpress (letterpress-warm · the original Mozi palette)

Songti letterpress + beige background, vintage old-newspaper feel. Fits Chinese writing tools, indie publishing, design studios, niche magazines.

```css
:root{
  --bg:#F3E4D4;
  --fg:#1f1510;
  --dim:#8a7560;
  --accent:#660125;     /* wine red */
  --accent2:#a83344;
  --accent3:#7a4a1f;
  --line:#d8c4af;
  --hl:#ecd8ca;
  --paper:#ecd8ca;
}
.hero{ background: linear-gradient(180deg, #F3E4D4 0%, #e9d2b8 100%); }
#ascii-nebula  { color:#b88a6a; opacity:.5; mix-blend-mode:multiply; }
#ascii-stars   { color:#5a3a1e; opacity:.7; }
#ascii-planet  { color:#660125; }
#ascii-asteroids{ color:#7a4a1f; }
#ascii-comets  { color:#a83344; }
```
Image filter: `sepia(.3) contrast(1.05) saturate(.85) brightness(.95)`
Note: on warm backgrounds, change `mix-blend-mode: screen` to `multiply` so the ASCII reads as "pressed into the paper" instead of "glowing".

---

## 3. Cyber violet (cyber-violet)

Neon purple + electric pink, cyberpunk signage colors. Fits AI / Web3 / gaming peripherals / esports subscriptions.

```css
:root{
  --bg:#0a0118;
  --fg:#f0e6ff;
  --dim:#7e5cab;
  --accent:#ff00aa;     /* neon magenta */
  --accent2:#00ffe0;    /* electric cyan */
  --accent3:#b14aff;    /* purple */
  --line:#2a0d4a;
  --hl:#150327;
  --paper:#10021f;
}
.hero{ background: radial-gradient(ellipse at 70% 30%, #4a0e6e 0%, #0a0118 60%, #000 100%); }
#ascii-nebula  { color:#b14aff; opacity:.55; }
#ascii-stars   { color:#e0d4ff; }
#ascii-planet  { color:#00ffe0; }
#ascii-asteroids{ color:#ff00aa; }
#ascii-comets  { color:#ffd400; }   /* yellow electric comet */
```
Image filter: `hue-rotate(280deg) saturate(1.4) contrast(1.1) brightness(.65)`

---

## 4. Terminal green (terminal-green)

Black background with phosphor green, vintage CRT terminal flavor. Fits CLI tools, developer subscriptions, security products, retro games.

```css
:root{
  --bg:#000800;
  --fg:#a8ffb0;
  --dim:#5fa05f;
  --accent:#00ff66;     /* phosphor green */
  --accent2:#80ff80;
  --accent3:#ffaa44;
  --line:#0a3010;
  --hl:#001500;
  --paper:#001a05;
}
.hero{ background: radial-gradient(ellipse at center, #052010 0%, #000800 70%, #000 100%); }
#ascii-nebula  { color:#2a8a44; opacity:.45; }
#ascii-stars   { color:#a8ffb0; }
#ascii-planet  { color:#00ff66; }
#ascii-asteroids{ color:#ffaa44; }
#ascii-comets  { color:#80ffd4; }
```
Image filter: `grayscale(1) brightness(.6) sepia(1) hue-rotate(70deg) saturate(2)`
You can also add scanlines via `.hero::after`: `background: repeating-linear-gradient(0deg, transparent 0, transparent 2px, rgba(0,255,102,.05) 3px, rgba(0,255,102,.05) 4px);`

---

## 5. Aurora (aurora · a cool-toned variation of the default style)

Gray-cyan ice blue as the main color with a touch of pink and green, like the northern lights. Fits meditation / wellness / travel / Nordic-style products.

```css
:root{
  --bg:#0c1420;
  --fg:#dceaf0;
  --dim:#6b8499;
  --accent:#7fe3c4;     /* aurora green */
  --accent2:#b8a4ff;    /* pale violet */
  --accent3:#ffb3c1;    /* aurora pink */
  --line:#1a2638;
  --hl:#101a28;
  --paper:#0e1622;
}
.hero{ background: linear-gradient(160deg, #1a3548 0%, #0c1420 50%, #050810 100%); }
#ascii-nebula  { color:#b8a4ff; opacity:.5; }
#ascii-stars   { color:#dceaf0; }
#ascii-planet  { color:#7fe3c4; }
#ascii-asteroids{ color:#ffb3c1; }
#ascii-comets  { color:#88ddff; }
```
Image filter: `hue-rotate(180deg) saturate(.7) contrast(1.05) brightness(.7)`

---

## 6. Desert sunset (desert-sunset · warm ASCII family)

Orange-red earth + caramel + apricot, dune-at-dusk feel. Fits coffee / indie hardware / crafts / food subscriptions.

```css
:root{
  --bg:#1a0a05;
  --fg:#f5e6d0;
  --dim:#a8765a;
  --accent:#ff8b3d;     /* toasted orange */
  --accent2:#d94545;    /* burnt red */
  --accent3:#ffd47a;    /* apricot yellow */
  --line:#3a1a10;
  --hl:#1f0d06;
  --paper:#15080a;
}
.hero{ background: radial-gradient(ellipse at 50% 80%, #5a1f10 0%, #1a0a05 60%, #000 100%); }
#ascii-nebula  { color:#a8765a; opacity:.5; }
#ascii-stars   { color:#ffd47a; }
#ascii-planet  { color:#ff8b3d; }
#ascii-asteroids{ color:#d94545; }
#ascii-comets  { color:#ffe9c2; }
```
Image filter: `sepia(.5) saturate(1.3) contrast(1.1) brightness(.7) hue-rotate(-10deg)`

---

## How to design your own

If the user's style description doesn't match any of the 6 presets above, follow this process:

1. **Pick the color temperature**: cold (blue/purple/cyan) / warm (orange/red/yellow) / neutral (green/gray)
2. **Choose the darkest value for `--bg`** (e.g. `#05060f`) and the lightest for `--fg` (e.g. `#e6e8ff`)
3. **`--accent` / `--accent2` / `--accent3`** three colors: separate them by **hue**, not saturation; they appear in small areas and must "light each other up"
4. **The 5 ASCII layer colors**, ordered by principle:
   - `nebula` → translucent purple/gray, as the base
   - `stars` → high-lightness white/warm white, the brightest
   - `planet` → the main `--accent`
   - `asteroids` → a warm contrast color (add a warm accent even if the main scheme is cold)
   - `comets` → second-highest saturation, the visual anchor that "streams past"
5. **Image filter** must be adjusted in step, otherwise unsplash photos will "not blend into the environment"

> How to test: plug the 5 layer colors into a palette generator (Coolors / Realtime Colors) and confirm the minimum contrast between them is ≥ 2.0 and the maximum hue difference is ≥ 90°.
