# Style presets — switch by changing the 8 `:root` CSS variables

Each preset is 8 lines of CSS. To switch styles, replace the corresponding lines of the `:root` block in `template.html`.
Do not touch the fonts (unless the user explicitly asks for a font change); keep the industrial / museum texture.

---

## 1. default — cold steel blue (default / the original "Restrained Objects")

```css
:root{
  --bg:        #e6e9ee;
  --bg-soft:   #f1f3f6;
  --paper:     #c9cfd6;
  --ink:       #0c0f14;
  --ink-soft:  #535963;
  --line:      #aab0b8;
  --line-soft: #c4c9d0;
  --steel:     #3a4a5a;
}
```
Fits: Nordic industrial, machine collections, gray metal, instruments, cast-iron objects
Trigger words: restrained / Nordic / industrial / steel / gray

---

## 2. warm-leather — warm brown vintage

```css
:root{
  --bg:        #ece4d6;
  --bg-soft:   #f4eee2;
  --paper:     #d8cdb8;
  --ink:       #1c160e;
  --ink-soft:  #6e5e44;
  --line:      #b6a787;
  --line-soft: #cdc1a5;
  --steel:     #8a5a2e;   /* bronze brown */
}
```
Fits: leather, woodcraft, pipes, cameras, old watches, vintage furniture
Trigger words: warm / vintage / brown / leather / nostalgic / old pieces

---

## 3. night-iron — night iron

```css
:root{
  --bg:        #14161a;
  --bg-soft:   #1c1f24;
  --paper:     #2a2e35;
  --ink:       #e8eaee;     /* inverted: dark ground, light text */
  --ink-soft:  #9aa0a8;
  --line:      #3a3f46;
  --line-soft: #2a2e34;
  --steel:     #c9a35a;   /* dark gold */
}
```
Fits: high-end audio, mechanical keyboards, fireworks, dark-toned products, lighting
Trigger words: dark / deep / night / dark gold / black

Note: with this preset also darken the two radial colors of the body `background-image`; suggested:
```css
body{
  background-image:
    radial-gradient(at 20% 22%, rgba(58,74,90,0.18) 0px, transparent 50%),
    radial-gradient(at 78% 80%, rgba(201,163,90,0.05) 0px, transparent 55%);
}
```

---

## 4. paper-press — paper & print

```css
:root{
  --bg:        #f3eee2;
  --bg-soft:   #faf5e8;
  --paper:     #e2d9c1;
  --ink:       #181410;
  --ink-soft:  #5a4f3e;
  --line:      #b9ac8e;
  --line-soft: #cec3a6;
  --steel:     #9a3324;   /* lead red */
}
```
Fits: books, stationery, printed matter, handmade notes, news
Trigger words: paper / print / report / stationery / press / publishing

---

## 5. navy-blueprint — navy blueprint

```css
:root{
  --bg:        #1f2a3a;
  --bg-soft:   #263244;
  --paper:     #324154;
  --ink:       #f4f6fa;
  --ink-soft:  #aab6c8;
  --line:      #4a5568;
  --line-soft: #2e3a4d;
  --steel:     #ffffff;     /* white linework */
}
```
Fits: maritime instruments, aviation, navigation, ship parts, dark gauges
Trigger words: navy / blueprint / nautical / ship

Note: also change the marquee `.ticker` background to `var(--bg-soft)` and its text to `var(--ink)`, otherwise light-on-light is unreadable.

---

## 6. ceramic-clay — ceramic clay

```css
:root{
  --bg:        #e7d8c4;
  --bg-soft:   #f1e6d5;
  --paper:     #d3bfa3;
  --ink:       #2a1c12;
  --ink-soft:  #6b4f38;
  --line:      #b39472;
  --line-soft: #c8ad8c;
  --steel:     #5e3a1f;   /* kiln-fire brown */
}
```
Fits: pottery, porcelain, Anatolian objects, East Asian antiques, earthy crafts
Trigger words: ceramic / porcelain / earth / kiln / clay

---

## 7. mint-laboratory — laboratory mint

```css
:root{
  --bg:        #e8efea;
  --bg-soft:   #f1f5f2;
  --paper:     #c8d4ce;
  --ink:       #102018;
  --ink-soft:  #4f655a;
  --line:      #99ada3;
  --line-soft: #b9c7bf;
  --steel:     #2a6e5a;   /* moss green */
}
```
Fits: medical devices, glassware, lab instruments, botanicals, neutral clinical
Trigger words: lab / medical / glass / moss / green

---

## How to choose

If the user gives no style, pick automatically by category:

| Category | Default style |
|---|---|
| Cast iron, steel, machinery, Nordic objects | default |
| Woodcraft, leather, vintage, cameras | warm-leather |
| Audio, lighting, dark high-end | night-iron |
| Stationery, paper goods, books | paper-press |
| Maritime, aviation, navigation | navy-blueprint |
| Ceramics, East Asian objects | ceramic-clay |
| Lab instruments, medical, glass | mint-laboratory |
| Unsure | default (safest) |
