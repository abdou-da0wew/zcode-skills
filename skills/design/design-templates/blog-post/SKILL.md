---
name: blog-post
description: Long-form article / blog-post template — two voices: a wildstay-style lifestyle launch piece with editorial grid + oversized display type, and a WeChat-official-account-style serif beauty/longform with measured prose and quiet hairlines.
visibility: public
mode: template
carrier: long-form-article
scenario: editorial-content
pattern_source: qiye-wildstay.html, skin-barrier-rereading.html
source_priority: skill-first
triggers:
  - "make a long-form article page"
  - "official-account long-form post"
  - "wildstay lifestyle big-title page"
  - "beauty feature long-read"
  - "editorial blog post"
  - "editorial long read"
---

# Blog Post Template

Use this template for **single-page long-form articles** — brand stories, lifestyle features, beauty / wellness deep-reads, cultural essays, WeChat-official-account-style long posts rendered as standalone web pages.

This template ships two variants. Pick before building.

## Variants

### `qiye-wildstay.html` — Lifestyle / brand-launch editorial

- Voice: aspirational, energetic, image-led, asymmetric.
- Use for: outdoor / travel / camping / lifestyle product launches, brand-launch features, brand stories with strong photography.
- Distinctive moves: oversized display numerals (date as poster), Helvetica + PingFang stack, grid-scattered title characters, rotated accent bars, pill CTAs.

### `skin-barrier-rereading.html` — Serif long-read

- Voice: introspective, scholarly, text-first.
- Use for: beauty / skincare / health / science / culture deep-dives, WeChat-official-account-style serialized columns.
- Distinctive moves: Songti SC display title + Cormorant Garamond italic English subtitle, blue-grey accent rules, justified body, restrained metadata header.

## Use When

- The artifact is a **scrolling web article**, not a fixed-image card.
- Content is paragraph-led with images, pull-quotes, possibly a few module breaks.
- The user wants an official-account / magazine-feature / brand-long-read feel — not a SaaS landing, not a social card.

## Avoid When

- The piece is < 200 words — use a social card instead.
- The content is operational (KPIs, dashboards, schedules, OKRs).
- The output is meant to be exported as one image (use social-card-editorial).
- The user wants a deck (use a `ppt/` template).

## Required Reading

Read this `SKILL.md` first. Then read **only the chosen variant** in full to lift typographic rhythm and section transitions.

Do not mix the two voices in one piece. They embody different reading contracts.

## Design Strategy

Pick the variant from voice, not topic:

- Energy + photography forward → **wildstay**
- Quiet + reasoned + paragraphs → **skin-barrier-rereading**

Then decide the spine:

- masthead / metadata strip (issue, date, author, kicker)
- title block (display + sub + dek)
- hero image or hero quote (not both)
- 3–6 body sections with clear hierarchy
- inline images with captions (numbered if many)
- closing / colophon

## Layout Bias

Prefer:

- generous line-height for CJK body text (≥ 1.75) when the target language is Chinese
- one display font + one body font, not three
- hairline rules over decorative dividers
- justified or natural ragged-right body — never centered
- captions and metadata in small caps / mono / Latin to break the body-text rhythm

Avoid:

- emoji decorations inside body copy
- generic blog-card grids ("related posts" tiles)
- background gradients behind body copy
- multi-column body on desktop unless variant explicitly supports it
