#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Batch exact-string replacements for guizang-ppt/assets/template.html (chunk3 localization)."""
import io, sys

path = "/home/z/my-project/skills/design/design-templates/ppt/guizang-ppt/assets/template.html"
s = io.open(path, encoding="utf-8").read()

pairs = [
(r'<html lang="zh-CN">', r'<html lang="en">'),
(r'<title>[必填] 替换为 PPT 标题 · Deck Title</title>', r'<title>[REQUIRED] replace with PPT title · Deck Title</title>'),
(r'''/* ============ 主题色(默认:🖋 墨水经典) ============
       切换主题:从 references/themes.md 复制对应的 :root 块
       整体替换这几行(--ink / --ink-rgb / --paper / --paper-rgb)
       其他地方散落的 rgba() 都走 var(--ink-rgb) / var(--paper-rgb),无需逐处改 */''',
 r'''/* ============ Theme palette (default: 🖋 Ink Classic) ============
       Switch theme: copy the matching :root block from references/themes.md
       and wholesale-replace these lines (--ink / --ink-rgb / --paper / --paper-rgb)
       All scattered rgba() elsewhere reads var(--ink-rgb) / var(--paper-rgb), so nothing else needs editing */'''),
(r'/* ============ 字体(跨主题固定) ============ */', r'/* ============ Fonts (fixed across themes) ============ */'),
(r'/* ============ WebGL 双背景 ============ */', r'/* ============ WebGL dual background ============ */'),
(r'/* ============ Deck 容器 + 翻页 ============ */', r'/* ============ Deck container + page flip ============ */'),
(r'/* width: NSLIDES * 100vw，会在 JS 里动态矫正 */', r'/* width: NSLIDES * 100vw; corrected dynamically in JS */'),
(r'/* 默认页：遮罩较厚，保证文字可读 */', r'/* Default page: thick overlay keeps text readable */'),
(r'/* Hero 页：遮罩大幅降低，让 WebGL 背景明显透出 */', r'/* Hero page: overlay drops sharply so the WebGL background shows through */'),
(r'/* Hero 页顶底微弱渐隐，保证 chrome/foot 区域可读 */', r'/* Hero page: faint top/bottom fade keeps chrome/foot readable */'),
(r'/* ============ Magazine chrome：顶部 meta + 底部 foot ============ */', r'/* ============ Magazine chrome: top meta + bottom foot ============ */'),
(r'''/* ============ 字体规则 ============
     · 衬线（Noto Serif SC / Playfair）：大标题、重点金句、数字
     · 非衬线（Noto Sans SC）：正文描述、body、补充说明
     · 等宽（IBM Plex Mono）：kicker、meta 小标签、foot 右侧
  */''',
 r'''/* ============ Font roles ============
     · Serif (Playfair / CJK serif such as Noto Serif SC): headlines, key quotes, numbers
     · Sans (Inter / CJK sans such as Noto Sans SC): body copy, descriptions, supplements
     · Mono (IBM Plex Mono): kicker, small meta labels, foot right side
  */'''),
(r'/* ============ 布局工具 ============ */', r'/* ============ Layout utilities ============ */'),
(r'/* ============ Stat（数字矩阵） ============ */', r'/* ============ Stat (number matrix) ============ */'),
(r'/* ============ Callout（引用框） ============ */', r'/* ============ Callout (quote box) ============ */'),
(r'/* ============ Platform（平台卡） ============ */', r'/* ============ Platform (platform card) ============ */'),
(r'/* ============ Rowline（表格行） ============ */', r'/* ============ Rowline (table row) ============ */'),
(r'/* ============ Pillar（支柱卡片） ============ */', r'/* ============ Pillar (pillar card) ============ */'),
(r'/* ============ Icons（Lucide via CDN） ============ */', r'/* ============ Icons (Lucide via CDN) ============ */'),
(r'/* ============ 图片占位（虚线框，提示设计师位置） ============ */', r'/* ============ Image placeholder (dashed frame marking the designer slot) ============ */'),
(r'''/* ============ 图片实填框（关键：固定高度 + 只裁底部） ============
     重要约束：高度用内联 height:Nvh 精确控制，不要用 aspect-ratio（会撑破布局）
     object-position:top center 保证严禁裁剪顶部和左右，只裁剪底部
  */''',
 r'''/* ============ Filled image frame (key: fixed height + bottom-crop only) ============
     Hard constraint: control height precisely with inline height:Nvh; never aspect-ratio (it breaks the layout)
     object-position:top center guarantees the top/left/right are never cropped — bottom only
  */'''),
(r'/* ============ 导航 ============ */', r'/* ============ Navigation ============ */'),
(r'''============ LAYOUTS API · 面向 agent 的类（v2）============
     所有 layouts.md 中的骨架都基于下面这套命名。
     如果你在 layouts.md 里看到某个类，它必须在下面有定义。''',
 r'''============ LAYOUTS API · agent-facing classes (v2) ============
     All skeletons in layouts.md are built on the naming below.
     If you see a class in layouts.md, it must be defined down there.'''),
(r'/* ---------- .frame：每页主内容容器 ---------- */', r'/* ---------- .frame: each page\u2019s main content container ---------- */'),
(r'/* 当 .frame 同时加了 grid 类时，grid 的 display:grid 覆盖 flex */', r'/* When .frame also carries a grid class, the grid display:grid overrides flex */'),
(r'/* ---------- 标题层级（API 名称，衬线为主） ---------- */', r'/* ---------- Heading hierarchy (API names, serif-led) ---------- */'),
(r'/* 英文标题专用（Playfair 衬线） */', r'/* English headlines only (Playfair serif) */'),
(r'/* ---------- lead 引语 ---------- */', r'/* ---------- lead quote paragraph ---------- */'),
(r'/* ---------- meta-row 底部元数据 ---------- */', r'/* ---------- meta-row bottom metadata ---------- */'),
(r'/* ---------- stat-card（数据大字报用） ---------- */', r'/* ---------- stat-card (big-number stats) ---------- */'),
(r'/* 当 stat-card 用于 grid-4（2x2），数字可以更大 */', r'/* When stat-card sits in grid-4 (2x2), numbers can go larger */'),
(r'/* 当只有 3 个，字也可以稍大 */', r'/* With only 3 items the type can be a bit larger too */'),
(r'/* ---------- pipeline（流水线） ---------- */', r'/* ---------- pipeline ---------- */'),
(r'/* ---------- 网格（layouts.md 所用） ---------- */', r'/* ---------- Grids (used by layouts.md) ---------- */'),
(r'/* 这些类独立挂到任何容器上都能生效，不依赖 .frame 复合选择器 */', r'/* These classes work on any container; they do not rely on the .frame compound selector */'),
(r'/* grid-6 已在旧样式里定义为 3x2，这里仅补 align */', r'/* grid-6 is already 3x2 in the legacy styles; only align is added here */'),
(r'/* ---------- 图片 frame-img（layouts.md 主命名） ---------- */', r'/* ---------- Image frame-img (layouts.md primary naming) ---------- */'),
(r'/* 在旧样式里已定义，这里补 img-cap 命名别名与增强 */', r'/* Already defined in legacy styles; img-cap naming alias and enhancements added here */'),
(r'/* callout src 命名别名 */', r'/* callout src naming alias */'),
(r'/* ---------- chrome & foot 补位（layouts.md 简单写法） ---------- */', r'/* ---------- chrome & foot slots (simple layouts.md style) ---------- */'),
(r'/* ---------- 响应式降级 ---------- */', r'/* ---------- Responsive degradation ---------- */'),
(r'<div id="hint">← → 翻页 · ESC 索引</div>', r'<div id="hint">← → flip · ESC index</div>'),
(r'''SLIDES 插入区 · 在此处填充所有 <section class="slide ..."> 页面
     每页模板参考 references/page-patterns.md
     页面组件参考 references/components.md''',
 r'''SLIDES insertion zone · fill all <section class="slide ..."> pages here
     Per-page templates: references/page-patterns.md
     Page components: references/components.md'''),
(r'''/* =============== WebGL 双背景 ===============
   深色页：Holographic Dispersion（全息色散 · 钛金暗流）—— 彩虹微扰、鼠标径向涟漪
   浅色页：Spiral Vortex（旋转涡流 · 银色珍珠）—— domain-warp 流动、无中心
   修改风格请参考 references/webgl-backgrounds.md
*/''',
 r'''/* =============== WebGL dual background ===============
   Dark pages: Holographic Dispersion (titanium-gold dark flow) — subtle rainbow perturbation, mouse ripples
   Light pages: Spiral Vortex (rotating vortex · silver pearl) — domain-warp flow, center-less
   To restyle, see references/webgl-backgrounds.md
*/'''),
(r'// =============== 导航（翻页 / 圆点 / 键盘 / 滚轮 / 触屏） ===============', r'// =============== Navigation (flip / dots / keyboard / wheel / touch) ==============='),
(r'// 关键：矫正 deck 宽度为 total * 100vw，否则翻页会错位', r'// Key: correct the deck width to total * 100vw, otherwise flips misalign'),
(r'/* 主题切换：优先读 data-theme，其次从 class（light/dark）推断 */', r'/* Theme switch: prefer data-theme, then infer from class (light/dark) */'),
(r'/* =============== ESC 索引视图 =============== */', r'/* =============== ESC index view =============== */'),
]

missed = []
for old, new in pairs:
    if old in s:
        s = s.replace(old, new, 1)
    else:
        missed.append(old[:70])

io.open(path, "w", encoding="utf-8").write(s)
print("REPLACED OK" if not missed else "MISSED:\n" + "\n".join(missed))
