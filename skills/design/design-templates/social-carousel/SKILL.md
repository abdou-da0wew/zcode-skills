---
name: social-carousel
description: >-
  Xiaohongshu anthology / horizontal-scroll social template — 8 portrait cards in a continuous auto-scroll snap loop, each with a geometric crop mask (arch / oval / half-dome / diagonal) + Songti title + one ornamental SVG mark + corner volume metadata. For photography series / art direction / mood reels / brand moment collections (6-10 frames). Triggers: "make an anthology / horizontal scrolling gallery / mood reel / photography series / volume 0X cover set". NOT tutorials (use digital-eguide), NOT series shorter than 4 cards, NOT text-dense cards (scroll speed hides text).
visibility: public
mode: template
carrier: fixed-image
scenario: social-content
pattern_source: scroll-gallery.html
source_priority: skill-first
triggers:
  - "make an anthology selection"
  - "horizontal scrolling gallery"
  - "mood reel"
  - "photography series show"
  - "volume 0X cover set"
  - "auto-scroll card set"
related_patterns: social-card-image-led, digital-eguide
---

# Social Carousel Template

Use this template when the artifact is a **curated multi-card anthology** — 6–10 images that share an editorial identity and want to be experienced in rhythm, not as a list.

Distinct from `digital-eguide/social-carousel.html` (12-frame field-notes guide with 50/50 photo + metadata). This one is **gallery-paced**, no per-card metadata table, sculptural geometric masks.

## Use When

- The user wants to publish a **series / anthology / collection** — photography, art direction, branding moments, mood reel.
- Each card carries one image + a short serif title + a volume number (Volume 0X).
- The viewing context is browsing / pause / browse — not step-by-step instruction.
- The output is a fixed-image set (HTML-to-image) or an embedded auto-scrolling strip.

## Avoid When

- The content is a tutorial or numbered steps — use `digital-eguide/social-carousel.html` (it has progress + per-step metadata) or `social-card-swiss/`.
- The series is < 4 entries — make individual cards instead.
- The content is text-heavy (quotes, body copy) — gallery rhythm hides text.
- The platform expects discrete swipeable posts (XHS multi-image post) — this is one scrolling strip, not 9 separate posts.

## Required Reading

Read this `SKILL.md` first. Do **not** read `scroll-gallery.html` by default.

Read `scroll-gallery.html` only when you need: the geometric-mask shapes (arch / oval / half-dome / diagonal), the auto-scroll easing values, the seamless-loop double-render trick, or the hover-slowdown behavior. Extract patterns; do not copy the placeholder Songti titles, photo URLs, or class names wholesale.

## Design Strategy

Commit to the anthology spine before designing cards:

- one cover frame role per card (full-bleed, arched, oval, diagonal, masked half-dome)
- a single rotating ornamental SVG mark style (don't mix flower + grid + arrow)
- consistent corner metadata (volume + tag + year, picked once)
- one title font (Songti SC), one meta font (PingFang SC), no third voice

If the cards don't share a visual system, the auto-scroll exposes the inconsistency.

## Layout Bias

Prefer:

- 2:3 or 7:9 portrait per card; mix sparingly, never randomly
- restrained warm palette (creams / terracottas / sage) over white or near-black
- one geometric mask per card, rotated through the set
- ornamental marks small and consistent, in a single accent ink
- continuous slow auto-scroll, pause on hover, infinite loop

Avoid:

- emoji or 3D plastic stickers in corner metadata
- mixing portrait + landscape card aspects randomly
- adding step numbers (this is not a tutorial)
- decorative gradients behind images — the mask is the decoration
- black-gold / neon palettes — the template's identity is editorial / warm

## Platform / Size

A horizontal strip of vertical cards (~ 360×540 each). Designed for embedding on a long page or capturing as a wide image. If the user wants discrete XHS posts, export each card individually.
