# Font Selection & Pairing for Chinese

> This file is the scenario-driven reference for Chinese font selection, pairing, and loading. Do not read it by default in every Chinese typesetting task; read it only when fonts materially shape the visual direction, or when a named / loadable font must be tested.

This file is organized by the actual order of choosing a font: **§1 Choose fonts (the decision line — read top to bottom) → §2 Loading execution (needed only after choosing) → §3 Principle self-check (compare at the end)**.
Do not skim the font tables out of order; first locate a temperament match in §1, then take a loading method from §2.

## 1. Font selection (the decision line)

Do not browse every font table first, and do not pick an exciting-looking font name "because it's pretty". Classify the user's intent first, filter by medium / font role / loadability, and only then enter the matching library table.

### 1.1 User intent → scenario category

| User intent / keywords | Scenario category | Library table |
|---|---|---|
| SaaS / Dashboard / product page / tech / business / industrial / hard-edged / efficiency | Modern / industrial / tech / business | Table A |
| Literary / classical / cultural / neo-Chinese / emotional / editorial / publishing / magazine | Literary / classical / elegant / emotional | Table B |
| Classical texts / literary Chinese / poetry / quotes / dialogue / traditional culture / Kai temperament | Classical / literary Chinese / quotes / dialogue | Table C |
| Official documents / government notices / institutional files / red-header documents | Official / regulated (Mainland) | Table D |
| Taiwan official documents / Taiwan textbooks / Traditional formal / Kai education | Official / textbook (Taiwan) | Table E |
| Academic / papers / white papers / research reports / rigorous / trustworthy | Academic / rigorous / publishing | Table F |
| Xiaohongshu covers / posters / event pages / slogans / key visuals / display sizes | Titles / posters / display | Table G |

If one request hits several categories, choose the primary category by the artifact's main purpose:

- Product/UI usability first → Table A;
- Reading and publishing feel first → Table B / F;
- Fixed-image cover impact first → Table G;
- Formal regulation first → Table D / E.

### 1.2 Font filtering

Inside a library table, do not pick a font name directly. Filter by these 4 conditions.

| Filter | Question to ask | Selection principle |
|---|---|---|
| **Delivery medium** | Web/HTML, fixed image, long-form, dashboard, or official document? | Web prefers `A:CDN` / `B:OSS-slices`; fixed images allow stronger faces; long-form and dashboards prioritize readability; official documents follow the regulation. |
| **Font role** | Body, title, display, quote, numerals, or UI controls? | Body: readability; titles: temperament; display: short titles/slogans only; UI controls: stable screen fonts. |
| **Loadability** | Can the font actually load in HTML? | `A:CDN` usable directly; `B:OSS-slices` via `@font-face`; `C:reference-only` must never go into `font-family`. |
| **Content density** | Character-heavy/dense, or short titles/posters? | Dense content uses steady fonts; strong display fonts are only allowed for short titles. |

Quick filtering rules:

- **Web / HTML output**: prefer `A:CDN` or `B:OSS-slices`; never put `C:reference-only` into `font-family`.
- **Social images / posters / fixed-image output**: strong display faces allowed, but you still need a loadable plan, a user-provided font file, or an explicit statement that it is temperament reference only.
- **Long-form / reports / official-account articles**: body prefers highly readable fonts; strong display faces at most for titles, section names, quotes, or key numbers.
- **Dashboards / forms / admin / tool pages**: prefer system stacks and screen fonts (Source Han Sans, MiSans, etc.); never use strong display faces as UI body.
- **Official / formal materials**: user or institutional specs first; never use poster fonts to "boost design".

### 1.3 Library tables

Library tables hold only font facts: name, weights, usage hint, loading status. OSS/CDN/slice status lives here too — do not repeat it in scenario routing tables.

Meaning of the "Load" column:

- `A:CDN` = reachable via a public CDN; `<link>` directly (see §2.4).
- `B:OSS-slices` = woff2 slices exist (self-hosted); write `@font-face` per §1.2/§2.2.
- `C:reference-only` = no public loading path; temperament reference only. After fixing a direction, switch to an A/B font of the same temperament, or have the user provide the font file.
- `system` = system font (e.g. PingFang on macOS); no loading needed but no cross-platform guarantee.

Read a library table only when its scenario hits; never scan tables across scenarios.

### Table A: Modern / industrial / tech / business

**Keywords**: modern · industrial · tech · business · hard-edged · efficiency · neutral · minimal · UI · SaaS · Dashboard · product page

| Font | Weights | Use / hint | Load |
|---|---|---|---|
| Source Han Sans (SiYuan HeiTi) | 7 (ExtraLight–Heavy) | First choice for general screen use; body or titles | A:CDN |
| MiSans (Xiaomi MiLanTing) | 7 (Thin–Heavy) | Screen, mobile UI, dashboards; slightly open apertures | A:CDN |
| PingFang | 6 | macOS/iOS system first choice | system |
| HarmonyOS Sans | 9 | HarmonyOS ecosystem; among the richest weight sets; OSS slices loadable | B:OSS |
| Alibaba PuHuiTi | 5 | Business, Alibaba-flavored products; OSS slices loadable | B:OSS |
| OPPO Sans | 5 | Mobile, ColorOS ecosystem; OSS slices loadable | B:OSS |
| BIZ UD Gothic | 2 | Japanese temperament; ⚠ JIS-first — some Simplified characters fall back | A:CDN |
| Founder LantingHei (family) | 6+ | A classic publishing-typesetting choice | C:reference-only |
| HYQiHei | 12 | Richest weight set; commercial projects | C:reference-only |
| Chuangkit KingKong | 1 | Strong industrial display titles; OSS slices loadable | B:OSS |
| ZiTiChuanQi TeZhan Ti | 1 | Extreme industrial/sharp angles; titles only | B:OSS-slices |
| ZCOOL KuHei | 1 | Hard-edged titles | B:OSS-slices |
| BiaoXiaoZhi WuJie Hei | 1 | Modern / boundary-less display titles; OSS slices loadable | B:OSS |

**Hint**: industrial/tech does not mean uniformly ultra-black; in dense information, strong faces go only on main titles or key numbers. Glitch/TeZhan-style faces strongly change temperament — good for posters/launch pages, wrong for admin panels and long-form.

### Table B: Literary / classical / elegant / emotional

**Keywords**: literary · classical · elegant · emotional · cultural · neo-Chinese · mood · lyrical · editorial · publishing · magazine

| Font | Weights | Use / hint | Load |
|---|---|---|---|
| Source Han Serif (SiYuan SongTi) | 6 | Universal safe first choice; body or titles | A:CDN |
| BIZ UD Mincho | 2 | Modern mincho, highly readable; ⚠ JIS-first — some Simplified characters fall back | A:CDN |
| Founder ShuSong (FZShuSong) | many | Classic book Song, gentle | C:reference-only |
| Founder YaSong / ZhunYaSong | many | Representative modern Song | C:reference-only |
| HYXuanSong | 5 | Modern-leaning; small face ratio, generous whitespace | C:reference-only |
| HYShuSong | many | Classic book Song | C:reference-only |
| LXGW ZhiSong | 1 | Cultured display titles | B:OSS-slices |
| Feihua Song / I.Ming / JingHua LaoSong | 1 | Literary display titles; Feihua Song and I.Ming have OSS slices, JingHua LaoSong reference-only | B:OSS-slices / C:reference-only |
| JingZhi Glitch Mincho | 1 | Glitch-flavored literary titles | C:reference-only |
| XinYuGong CangSang Ti | 1 | Weathered/emotional literary titles; OSS slices loadable | B:OSS |
| ORADANO Mincho | 1 | Classical mincho display titles; OSS slices loadable | B:OSS |

**Hint**: these fonts establish qi and charm; they don't fit dense UI or data systems. Cultural feel can't come from the font alone — also control tracking, line height, and paragraph gray.

### Table C: Classical / literary Chinese / quotes / dialogue

**Keywords**: classical texts · literary Chinese · poetry · quotes · dialogue · scripts · bookish · traditional culture · Kai temperament

| Font | Weights | Use / hint | Load |
|---|---|---|---|
| LXGW WenKai | 3 | Modern bookish feel (Qing woodblock style); classical translations / literary Chinese / textbooks | A:CDN |
| ChillKai | 1 | Kai-style quotations | B:OSS-slices |
| Slide Chunfeng Kai | 1 | Decorative Kai display titles | B:OSS-slices |
| Early Summer Serif / GenRyuMin JP | many | Mincho literary titles/quotes | B:OSS-slices |
| RunZhiJia RuYinZouZhang Kai | 1 | Archaic display titles | C:reference-only |
| MengYuan Song | many | Modern Song alternative | C:reference-only |
| Jiangxi ZhuoKai | 1 | Rustic Kai | B:OSS-slices |
| Tsanger JinKai | many | Rigorous readable Kai; education/children | C:reference-only |
| Kaiti SC (macOS) | 1 | System Kai; titles, quotes | system |
| Founder KaiTi GBK | 1 | Common Mainland Kai; titles/quotes | C:reference-only |

**Hint**: Kai / mincho / FangSong families create literary air, but never default to them for long screen body text. In dialogue, first guarantee clear names, colons, quotes, and line spacing. In classical/literary scenarios also check punctuation, line breaking, vertical/horizontal, and tracking.

### Table D: Official / regulated (Mainland)

**Keywords**: official documents · government · notices · institutional files · formal regulation · red-header documents

| Font | Weights | Use / hint | Load |
|---|---|---|---|
| Founder XiaoBiaoSong (Simplified) | 1 | Level-1 document titles | C:reference-only |
| FangSong GB2312 | 1 | Document body (16pt) | C:reference-only |
| HeiTi (system/Founder) | many | Document subheads (16pt) | system / C |
| KaiTi GB2312 | 1 | Issuance notes (16pt) | C:reference-only |

**Hint**: in official-document scenarios do not improvise; the user's or institution's format spec governs. Never migrate official-document font schemes to ordinary web pages, posters, or product UI.

### Table E: Official / textbook (Taiwan)

**Keywords**: Taiwan official documents · Taiwan textbooks · Traditional formal · Kai education

| Font | Weights | Use / hint | Load |
|---|---|---|---|
| TW-Kai (government standard Kai) | 1 | Taiwan official/textbook standard | C:reference-only |
| DynaFont Kai | many | Taiwan official/textbook | C:reference-only |
| Arphic Kai | many | Same as above | C:reference-only |
| Arphic PMingLiU | 1 | Traditional classic body | system |

**Hint**: Taiwan official/textbook work must not borrow the Mainland FangSong scheme. For bilingual material, coordinate line height, baseline, and size between Chinese Kai and the Western face (e.g. Times New Roman).

### Table F: Academic / rigorous / publishing

**Keywords**: academic · rigorous · papers · white papers · research reports · publishing · formal · trustworthy

**Universal safe pairing**: Source Han Serif (body) + Source Han Sans (titles), or Founder ShuSong + Founder LantingHei.

| Font | Weights | Use / hint | Load |
|---|---|---|---|
| Source Han Serif | 6 | Body first choice | A:CDN |
| Source Han Sans | 7 | Title first choice | A:CDN |
| Swei Spring CJK TC | many | Academic, rigorous publishing titles; Traditional/Song temperament | B:OSS-slices |
| CorpSrcWinSong Slim | 1 | Academic report titles; OSS slices loadable | B:OSS |
| Zhuque Fangsong | 1 | FangSong body (specific contexts) | B:OSS-slices |
| XinYi JiXiang Song | 1 | Rigorous Song | B:OSS-slices |

**Hint**: rigorous scenarios prioritize readability and credibility; no strong decorative faces. FangSong suits official/institutional/formal-text temperament; do not misuse it as modern product-page body.

### Table G: Titles / posters / display sizes

**Keywords**: titles · posters · covers · key visuals · slogans · Xiaohongshu covers · event pages · display sizes · eye-catching

| Font | Weights | Use / hint | Load |
|---|---|---|---|
| Smiley Sans | 1 | Oblique modern display titles | A:CDN |
| DingTalk JinBuTi | 1 | Modern brand titles | A:CDN / B:OSS-slices |
| Douyin Sans (DouyinMeiHaoTi) | 1 | Douyin ecosystem, lively modern; OSS slices loadable | B:OSS |
| Alimama ShuHeiTi | 1 | Marketing titles, strong impact | B:OSS-slices |
| Source Han Sans Heavy | 1 | Universal safe heavy titles | A:CDN |
| PangMenZhengDao Title | 1 | Slogans, taglines; OSS slices loadable | B:OSS |
| WenYue Classic Mincho | 1 | Archaic/retro titles | C:reference-only |
| HY ZhuZi ShangHei / YueYuan | many | Modern brand | C:reference-only |
| YouShe Title Black | 1 | Universal display titles | B:OSS-slices |
| Zhuiguang Douyu Ti / YiPin QiHang Ti / Kuaikan Shijie Ti | 1 | Strong-temperament titles; YiPin QiHang Ti and Kuaikan Shijie Ti have OSS slices, Zhuiguang Douyu Ti reference-only | B:OSS-slices / C:reference-only |
| ZiHun BianTao Ti / Cangji Gaode Guomiao Hei / Leefont MengHei | 1 | Decorative titles; all have OSS slices | B:OSS-slices |
| Taobao Maicai Ti / TangXianBin Song / JingNan JunJunTi | 1 | Strong-temperament titles; JingNan JunJunTi has OSS slices, Taobao Maicai Ti / TangXianBin Song reference-only | B:OSS-slices / C:reference-only |

**Hint**: title/poster fonts may be stronger, but must serve the theme — never "just to be loud". Fine for Xiaohongshu, posters, event pages; use cautiously in B2B SaaS, admin panels, research reports. When a title is long, fix line breaking and hierarchy before deciding on a strong display face.

### 1.4 Family pairing paradigms (after picking a temperament font, decide body + title pairing)

### Paradigm A: one family, many weights (minimalist; recommended starting point)
- Source Han Sans Light (body)
- Source Han Sans Medium (subheads)
- Source Han Sans Bold (display titles)

### Paradigm B: Song + Hei classic pairing
- Source Han Serif Regular (body)
- Source Han Sans Medium (titles, captions, CTA buttons)

### Paradigm C: large Song titles + Hei body (publishing style)
- Founder ZhunYaSong Bold (display titles)
- Founder LantingHei Light (body)

### Paradigm D: same family, many weights + shared modulus
- Founder LantingZhunHei GBK 12pt (subheads)
- Founder LantingXianHei GBK 9pt (body)
- Founder XiHeiYi GBK 6pt (captions)
- Under one modulus (1.5pt), three sizes coordinate through family weights

### Paradigm E: Song + Kai (classical / literary)
- Founder ShuSong Regular 10.5pt (body)
- LXGW WenKai Medium 14pt (titles, quotes)
- For: classical poetry collections, literary essays, traditional-culture projects

### Paradigm F: Mainland official-document scheme
- Founder XiaoBiaoSong (title candidate)
- FangSong GB2312 (16pt, body candidate)
- HeiTi (16pt, hierarchy/subhead candidate)
- KaiTi GB2312 (16pt, notes/issuance text candidate)
- For Mainland official documents, notices, and institutional files only; never migrate to ordinary web/poster/UI.

### Paradigm G: Taiwan official / textbook scheme
- TW-Kai (Chinese body/textbook candidate)
- Times New Roman (Western candidate)
- Coordinate baseline, line height, and size between Chinese Kai and the Western serif.

### 1.5 Chinese-English mixing

When mixing, the goal is not "which font comes first in font-family" but:
- Chinese punctuation, em dashes, and ellipses must not be taken over by the Western font;
- English words and digits may get a better Latin face;
- Line height, baseline, and visual weight must coordinate.

| Chinese font | Pairable Western font | Note |
|---|---|---|
| Source Han Sans | Source Sans Pro / Inter | Tech, SaaS, reports |
| PingFang | San Francisco | Native macOS / iOS match |
| MiSans | MiSans Latin | Same family; line heights match well |
| HarmonyOS Sans | HarmonyOS Sans Latin | Same family |
| Source Han Serif | Source Serif Pro | Reports, editorial, publishing feel |
| Founder ShuSong | Times / Georgia | Classic Song + classic serif |
| Microsoft YaHei | Segoe UI | Windows environments |
| LXGW WenKai | Crimson Pro | WenKai + modern serif |
| Founder FangSong | EB Garamond / Crimson | Official-document / classical feel |

#### Safe default: Chinese font first

For general Chinese pages, H5, cards, and report body, put the Chinese font first by default to protect Chinese punctuation:

```css
font-family: "PingFang SC", "HarmonyOS Sans SC", "Noto Sans CJK SC",
             "Microsoft YaHei UI", "Microsoft YaHei",
             system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
```

#### When Latin-first is needed, do not put Inter first on body unconditionally

If `Inter` or `Helvetica` sits first on body, shared-codepoint characters (em dashes, quotes, ellipses) may be claimed by the Western font, causing sinking, breaking, or visual inconsistency.

The sturdier approach:

```css
@font-face {
  font-family: "Inter Local";
  src: local("Inter");
  unicode-range: U+0000-007F;
}
body {
  font-family: "PingFang SC", "Noto Sans CJK SC", "Microsoft YaHei", sans-serif;
}
.latin {
  font-family: "Inter Local", Inter, system-ui, sans-serif;
}
```

You can also apply the Latin class only to English titles, digits, code, and labels — never let it take over Chinese body punctuation.

### 1.6 Variable fonts

Newer fonts support axis-based adjustment, great for screens:
- Source Han Sans Variable (GitHub)
- HarmonyOS Sans Variable
- **MiSans VF** (Xiaomi official site; weight axis)
- Inter Variable

CSS:
```css
font-family: "Source Han Sans VF";
font-variation-settings: "wght" 450;
```

Variable weights let design respond to screen size (bolder on small screens, lighter on large).

## 2. Loading execution (after a font is chosen)

### 2.1 Three loading situations — distinguish before writing

| Font type | Loading method | Examples |
|---|---|---|
| **A. Public CDN reachable** | `<link>` the CDN directly (Google Fonts / jsDelivr etc. ship their own subsetting; the browser downloads on demand) | Source Han Sans/Serif, Noto SC, LXGW WenKai, Smiley Sans, Source Sans 3, etc. |
| **B. OSS slices / self-hosted slices** | Generated CSS `@font-face` referencing woff2 slices + `unicode-range`; `ext` fallback last | Display fonts with existing self-hosted slices; fonts with no public CDN but available self-hosted slices |
| **C. No loading path at all** | Never put it in `font-family` — temperament reference only | Candidates in §2 without a `✓ loadable` mark and with no CDN/slices in §2.3/§2.4 |

### 2.2 Class B OSS slices: the standard scheme

OSS-sliced fonts use **high-frequency-first CSS**: load the high-frequency Han slice first, then punctuation and Latin, and finally let the extension slice catch the rest.

Reference CSS structure:

```text
@font-face common-hi  → high-frequency Han glyphs, exact unicode-range list
@font-face punct      → CJK symbols + general punctuation + fullwidth ASCII
@font-face latin      → Basic Latin + Latin-1 Supplement + common punctuation
@font-face ext        → fallback for the remaining characters, placed last
```

Slice notes:

| Slice | Recommended form | Coverage |
|---|---|---|
| `common-hi` | Use the exact high-frequency Han `unicode-range` from the generated CSS; never simplify to the whole `U+4E00-9FFF` | High-frequency/common Chinese; used first for titles, covers, and common body text |
| `punct` | `U+3000-303F, U+2000-206F, U+FF00-FFEF` | CJK symbols/punctuation, general punctuation, fullwidth ASCII |
| `latin` | `U+0020-007E, U+00A0-00FF, U+2010-2027` | Basic Latin, Latin-1 Supplement, common punctuation |
| `ext` | `U+0-10FFFF`, must be last | Fallback for everything else, including low-frequency Han and rare glyphs |

Why `common-hi` must not just say `U+4E00-9FFF`:

- `U+4E00-9FFF` would make the common slice carry the entire CJK Unified Ideographs block, defeating "high-frequency first".
- The generated `common-hi` compresses the ~2,500 most common Han glyphs into precise ranges; the browser downloads the high-frequency slice only when those glyphs appear.
- Low-frequency glyphs fall to the final `ext` slice, preventing the first paint from forcing a huge full-Chinese download.

**Slice hosting**: slice woff2 files are self-hosted (your own bucket/CDN). Substitute your own asset base — `{FONT_ASSET_BASE}` below — for each slice URL. Do not hotlink third-party private hosts.

**Paste-ready `@font-face` template** (fill the 4 slice URLs for your chosen font/weight; copy the `common-hi` `unicode-range` from the corresponding generated CSS):

```css
/* High-frequency Han glyphs: do not simplify to U+4E00-9FFF; copy the exact ranges from the generated CSS */
@font-face {
  font-family: "{Font display name}";
  src: url("{FONT_ASSET_BASE}/{font-family}/{weight}/common-hi.woff2") format("woff2");
  unicode-range:
    /* paste generated common-hi unicode-range here */;
  font-display: swap;
}

/* CJK symbols + general punctuation + fullwidth ASCII */
@font-face {
  font-family: "{Font display name}";
  src: url("{FONT_ASSET_BASE}/{font-family}/{weight}/punct.woff2") format("woff2");
  unicode-range: U+3000-303F, U+2000-206F, U+FF00-FFEF;
  font-display: swap;
}

/* Basic Latin + Latin-1 Supplement + common punctuation */
@font-face {
  font-family: "{Font display name}";
  src: url("{FONT_ASSET_BASE}/{font-family}/{weight}/latin.woff2") format("woff2");
  unicode-range: U+0020-007E, U+00A0-00FF, U+2010-2027;
  font-display: swap;
}

/* Fallback: remaining characters. Must be last */
@font-face {
  font-family: "{Font display name}";
  src: url("{FONT_ASSET_BASE}/{font-family}/{weight}/ext.woff2") format("woff2");
  unicode-range: U+0-10FFFF;
  font-display: swap;
}
```

Usage notes:

- Keep the `common-hi` / `punct` / `latin` / `ext` order; `ext` must be last.
- If no generated CSS exists for the font, quick previews may use simplified ranges, but never treat that as the formal loading scheme.
- For short titles/social cards, usually only `common-hi`, `punct`, and some `latin` are hit; long-form and rare glyphs trigger `ext`.
- In production, still verify licensing, caching, CORS, file sizes, and the actually-hit glyphs.

**Mechanism**: the browser matches page characters against `unicode-range` and downloads slices accordingly. High-frequency Han glyphs hit `common-hi` first, punctuation hits `punct`, English/digits hit `latin`, and everything else falls to the final `ext`.

### 2.3 Slice inventory (fonts with self-hostable 4-slice sets)

This section is the loading lookup table, kept inside `fonts.md` so runtime does not jump to a third file.

Order of use:

1. First complete "user intent → scenario category → font filtering" per §1.
2. If a `B:OSS-slices` font was selected, come back here for its `css_family`, `font_weight`, and slice availability.
3. Fill the URLs into the §2.2 `@font-face` template, self-hosting the woff2 files under your `{FONT_ASSET_BASE}`.
4. Multi-weight families must declare `font-weight`; never declare every slice as `normal`.
5. The exact `common-hi` `unicode-range` should be copied from the corresponding generated CSS; without generated CSS, testing only.

Never pick a font from this section. It only answers "how does the already-chosen font load".

> **Where do the slice files come from?** The historical slices were hosted on a private CDN that is not part of this open-source release. Regenerate the 4 slices per font with a subsetting tool (e.g. `cn-font-split`) from the upstream font files, upload them to your own bucket/CDN, and fill `{FONT_ASSET_BASE}` accordingly. All fonts listed below are free/open-source or otherwise redistributable per their licenses — check each license before redistribution.

#### Font family summary

| font_examples | css_family | font_weights | scene | slices |
| --- | --- | --- | --- | --- |
| ChillKai | `"ChillKai"` | 400 | Classical / literary Chinese / quotes / dialogue | 4 (common-hi/punct/latin/ext) |
| Slide Chunfeng Kai | `"Slide Chunfeng Kai"` | 400 | Classical / literary Chinese / quotes / dialogue, Kai titles | 4 |
| Jiangxi ZhuoKai | `"Jiangxi ZhuoKai"` | 400 | Classical / literary Chinese / rustic Kai | 4 |
| Zhuque Fangsong | `"Zhuque Fangsong"` | 400 | Academic / rigorous / FangSong contexts | 4 |
| CorpSrcWinSong Slim | `"CorpSrcWinSong Slim"` | 400 | Academic / rigorous / publishing titles | 4 |
| Alibaba PuHuiTi 3.0 | `"Alibaba PuHuiTi 3.0"` | 400 | Modern / business | 4 |
| Douyin Sans | `"Douyin Sans"` | 400 | Titles / posters / lively modern | 4 |
| HarmonyOS Sans SC (Thin) | `"HarmonyOS Sans SC"` | 100 | Modern / industrial / tech | 4 |
| HarmonyOS Sans SC (Light) | `"HarmonyOS Sans SC"` | 300 | Modern / industrial / tech | 4 |
| HarmonyOS Sans SC (Regular) | `"HarmonyOS Sans SC"` | 400 | Modern / industrial / tech | 4 |
| HarmonyOS Sans SC (Medium) | `"HarmonyOS Sans SC"` | 500 | Modern / industrial / tech | 4 |
| HarmonyOS Sans SC (Bold) | `"HarmonyOS Sans SC"` | 700 | Modern / industrial / tech | 4 |
| HarmonyOS Sans SC (Black) | `"HarmonyOS Sans SC"` | 900 | Modern / industrial / tech | 4 |
| OPPO Sans (Regular) | `"OPPO Sans"` | 400 | Modern / mobile / ColorOS | 4 |
| OPPO Sans (Medium) | `"OPPO Sans"` | 500 | Modern / mobile / ColorOS | 4 |
| OPPO Sans (Bold) | `"OPPO Sans"` | 700 | Modern / mobile / ColorOS | 4 |
| Swei Spring CJK TC (Black/Bold/ExtraLight) | `"Swei Spring CJK TC"` | 200, 700, 900 | Academic / rigorous / publishing, Traditional/Song titles | 4 per weight |
| XinYi JiXiang Song | `"XinYi JiXiang Song"` | 400 | Academic / rigorous / Song titles | 4 |
| Early Summer Serif (all weights) | `"Early Summer Serif"` | 200–900 (7) | Literary / classical / elegant, mincho titles/short text | 4 per weight |
| Swei Spring Sugar CJK TC (all weights) | `"Swei Spring Sugar CJK TC"` | 200, 300, 400, 500 | Literary / classical / elegant, soft Song | 4 per weight |
| GenRyuMin JP (all weights) | `"GenRyuMin JP"` | 200–900 (7) | Literary / classical / quotes, mincho; Japanese/traditional temperament | 4 per weight |
| ORADANO Mincho | `"ORADANO Mincho"` | 400 | Literary / classical / emotional titles | 4 |
| XinYuGong CangSang Ti | `"XinYuGong CangSang Ti"` | 400 | Literary / classical / emotional titles | 4 |
| LXGW ZhiSong | `"LXGW ZhiSong"` | 400 | Literary / classical / emotional titles | 4 |
| Feihua Song | `"Feihua Song"` | 400 | Literary / classical / emotional titles | 4 |
| I.Ming | `"I.Ming"` | 400 | Literary / classical / mincho titles | 4 |
| RunZhiJia KangXi | `"RunZhiJia KangXi"` | 400 | Literary / classical / traditional titles | 4 |
| RunZhiJia KangXi Slim | `"RunZhiJia KangXi Slim"` | 400 | Literary / classical / traditional titles | 4 |
| YiPin QiHang Ti | `"YiPin QiHang Ti"` | 400 | Titles / posters | 4 |
| Kuaikan Shijie Ti | `"Kuaikan Shijie Ti"` | 400 | Titles / posters / youth content | 4 |
| Leefont MengHei | `"Leefont MengHei"` | 400 | Titles / posters / strong-temperament titles | 4 |
| Cangji Gaode Guomiao Hei | `"Cangji Gaode Guomiao Hei"` | 400 | Titles / posters / strong-temperament titles | 4 |
| JingNan JunJunTi | `"JingNan JunJunTi"` | 400 | Titles / posters / strong-temperament titles | 4 |
| PangMenZhengDao Title | `"PangMenZhengDao Title"` | 400 | Titles / posters / slogans | 4 |
| DingTalk JinBuTi | `"DingTalk JinBuTi"` | 400 | Titles / posters / modern brand | 4 |
| Alimama ShuHeiTi | `"Alimama ShuHeiTi"` | 400 | Titles / posters / marketing / launches | 4 |
| ZiHun BianTao Ti | `"ZiHun BianTao Ti"` | 400 | Titles / posters / decorative titles | 4 |
| YouShe Title Black | `"YouShe Title Black"` | 400 | Titles / posters / universal heavy titles | 4 |
| ZiTiChuanQi TeZhan Ti | `"ZiTiChuanQi TeZhan Ti"` | 400 | Modern / industrial / sharp display titles | 4 |
| Blix (all weights) | `"Blix"` | 100–700 (7) | Modern / industrial / tech / business, multi-weight titles/UI tests | 4 per weight |
| Blix Text | `"Blix Text"` | 400 | Modern / industrial / tech / business, multi-weight body/title tests | 4 |
| XiangLiFang HeiTi | `"XiangLiFang HeiTi"` | 400 | Modern / industrial / tech titles | 4 |
| Chuangkit KingKong | `"Chuangkit KingKong"` | 400 | Modern / industrial / tech titles | 4 |
| Dela Gothic One | `"Dela Gothic One"` | 400 | Modern / industrial / tech titles | 4 |
| BiaoXiaoZhi WuJie Hei | `"BiaoXiaoZhi WuJie Hei"` | 400 | Modern / industrial / tech titles | 4 |
| ZCOOL KuHei | `"ZCOOL KuHei"` | 400 | Modern / industrial / tech titles | 4 |
| Plix (all weights) | `"Plix"` | 100–700 (7) | Modern / industrial / tech, multi-weight titles/launches | 4 per weight |
| Plix Text | `"Plix Text"` | 400 | Modern / industrial / tech, multi-weight body/title tests | 4 |
| Lushuai Zhengrui Hei | `"Lushuai Zhengrui Hei"` | 400 | Modern / industrial / sharp titles | 4 |

### 2.4 Reference: CDN / system font loading

> Key rule: if you name a font in `font-family`, you must also load it (via a CDN `<link>`, or self-hosted `@font-face`).
> A name without loading = useless; the browser falls back to the default font. When unsure, prefer Class A fonts with a public CDN.

#### Chinese fonts

| Font | Class | Loading |
|---|---|---|
| Source Han Sans SC | Hei | A: `https://cdn.jsdelivr.net/npm/cn-fontsource-source-han-sans-sc-vf/font.css`; or self-hosted slices → see §2 |
| Source Han Serif SC | Song | A: `https://cdn.jsdelivr.net/npm/cn-fontsource-source-han-serif-sc-vf/font.css`; or self-hosted slices → see §2 |
| Noto Sans SC | Hei | A: same source as Source Han Sans (`Noto+Sans+SC` on Google Fonts) |
| Noto Serif SC | Song | A: same source as Source Han Serif (`Noto+Serif+SC` on Google Fonts) |
| LXGW WenKai | Kai | A: `https://cdn.jsdelivr.net/npm/cn-fontsource-lxgw-wen-kai-screen-r/font.css` (Google Fonts: `LXGW+WenKai`) |
| Smiley Sans | Title/Hei | A: `https://cdn.jsdelivr.net/npm/cn-fontsource-smiley-sans-oblique-regular/font.css` |
| DingTalk JinBuTi | Title/Hei | A: `https://cdn.jsdelivr.net/npm/cn-fontsource-ding-talk-jin-bu-ti-regular/font.css`; B: OSS slices → see §2.3 |
| BIZ UDGothic / UDMincho | Hei/Song (Japanese-first; some Simplified characters fall back) | A: `https://fonts.googleapis.com/css2?family=BIZ+UDGothic` (or `BIZ+UDMincho`) — edge fonts, use as needed |
| MiSans | Hei | A: `https://cdn.jsdelivr.net/npm/misans@4.1.0/lib/Normal/MiSans-Regular.min.css` (swap Medium/Bold per weight) |
| HarmonyOS Sans | Hei | B:OSS; slices per §2.3 (Thin–Black, all weights) |
| Alibaba PuHuiTi | Hei | B:OSS; slices per §2.3 |
| OPPO Sans | Hei | B:OSS; slices per §2.3 (Regular/Medium/Bold) |
| Douyin Sans | Title/Hei | B:OSS; slices per §2.3 |
| Alimama ShuHeiTi | Title/Hei | B: OSS slices → see §2.3 |
| Other inventory test fonts | Title/Song/Kai/FangSong | See §2.3; for titles, covers, posters, social cards, or specific tests only — never default body |

#### Latin / Western fonts (for the Latin part of mixed text; more character than system defaults)

> None of these are system fonts; they must be loaded. **Do not default to Inter** (an overused AI tell — see `anti-ai-slop.md`); prefer the list below.

| Font | Style | Web loading |
|---|---|---|
| Source Sans 3 | Sans, neutral professional (Source Han Sans's Latin sibling) | `https://cdn.jsdelivr.net/npm/@fontsource/source-sans-3/index.css` |
| Source Serif 4 | Serif, editorial/publishing (pairs with Source Han Serif) | `https://cdn.jsdelivr.net/npm/@fontsource/source-serif-4/index.css` |
| Crimson Pro | Serif, literary/elegant | `https://cdn.jsdelivr.net/npm/@fontsource/crimson-pro/index.css` |
| EB Garamond | Serif, classical/bookish | `https://cdn.jsdelivr.net/npm/@fontsource/eb-garamond/index.css` |

### 2.5 Assembling the font-family stack (the last step between choosing and writing CSS; the easiest to get wrong)

The most common mistake after choosing fonts is **omitting the CJK link in `font-family`** — e.g. choosing "Inter for English + system Chinese" but writing
`font-family: 'Inter', system-ui, sans-serif`; Chinese jumps straight to system-ui with uncontrolled rendering.

**Hard rule: any page containing Chinese must have an explicit CJK font name in `font-family`. A Latin font must never be followed directly by `system-ui`.**

Two templates by whether Chinese and English share a font:

```css
/* Case A: same font for Chinese and English / no special Latin choice → CJK font first */
font-family: '{CJK font}', system-ui, sans-serif;
/* Example: */
font-family: 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', system-ui, sans-serif;

/* Case B: different fonts (a Latin display font was specified) → Latin first, but CJK must immediately follow */
font-family: '{Latin font}', '{CJK font}', 'PingFang SC', 'Microsoft YaHei', system-ui, sans-serif;
/* Example: */
font-family: 'Inter', 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', system-ui, sans-serif;
```

**Counter-examples (do not write these)**:
```css
font-family: 'Inter', system-ui, sans-serif;   /* ✗ Chinese falls back to system-ui, uncontrolled */
font-family: 'Helvetica', 'PingFang SC';        /* ✗ English-first steals Chinese punctuation (dashes/quotes sink) */
```

**Relation to the "Chinese before Latin" iron rule** (two strategies; never mix them):
- **Case A (same font)**: CJK first — this IS "Chinese before Latin", preventing the English font from stealing Chinese punctuation glyphs.
- **Case B (separate fonts)**: Latin first but CJK immediately after — the browser falls back per character; the Latin font renders only the Latin glyphs it has, and Chinese lands on the adjacent CJK font. If worried about punctuation being claimed in this case, restrict the Latin font to Latin codepoints with `unicode-range`:

```css
@font-face {
  font-family: "Inter Latin";
  src: local("Inter");
  unicode-range: U+0000-024F;   /* Latin only; punctuation/Chinese left to the CJK font */
}
body { font-family: "Inter Latin", "Noto Sans SC", "PingFang SC", system-ui, sans-serif; }
```

For sinking punctuation / em-dash issues see the em-dash deep dive in `punctuation.md`.

## 3. Principle self-check (compare after choosing fonts)

### 3.1 Face-ratio conclusions

- **Face ratio ≈ 95%** (Source Han Sans, Noto Sans CJK, HarmonyOS Sans, MiSans, Alibaba PuHuiTi, etc.): screen first choice — a large face ratio stays legible at small sizes.
- **Face ratio ≈ 85%** (Source Han Serif, LXGW WenKai, traditional Song/Kai): print, long-form reading, literary/classical temperament first choice — visually relaxed, comfortable for long sessions.
- **Never mix widely different face ratios** (e.g. 95% Hei + 85% Song) at the same title/body level; visual weight will break.

### 3.2 General pairing principles

- ≤ 2 font families per project; prefer one family with many weights, building hierarchy through weight and size.
- At most 1 strong display font per design; body returns to a highly readable face.
- Title/poster fonts may be strong but must serve the theme — never "just to be loud".
- The candidate lists' order is not a priority ranking; choose by content temperament, readability, and medium.

### 3.3 Absolute avoid

Forbidden for body/serious content:
- ❌ STCaiyun, STHupo, STXingkai
- ❌ Any "effects font" with shadows/3D/plastic texture
- ❌ Decorative brush fonts as body text (e.g. Makerfaire YueYuan-style faces)
- ❌ Game fonts (dark-fantasy, sci-fi etc.) for long-form
- ❌ Kai as modern long-form body (**exception: children's books / education**) — Kai's thin strokes fatigue
- ❌ FangSong for large blocks of modern body (**exception: official documents**) — same reason
- ⚠️ ZhongYi Song, ZhongYi FangSong, old Microsoft YaHei: dashes/ellipses may break or sink; test for web and long-form
- ⚠️ STHeiti and some LantingHei versions: punctuation may not be centered; test before publishing/brand use

Use cautiously in titles/posters:
- ⚠️ Cartoon fonts in business contexts
- ⚠️ Calligraphy fonts in tech contexts
- ⚠️ Serif (Song) fonts for sports/dynamic themes
