---
name: social-card-quote
description: Quote-driven social card — a thesis / pull-quote / principle / key question / one-line insight fills the whole text block, backed by source / section label / marginal note / three anchors. Must break lines semantically (no auto-wrap reliance) and include at least one anchor to prevent floating. Triggers: "make a quote card / thesis card / punchline card / principle card / hero question card". NOT long paragraphs disguised as quotes, NOT empty motivational slogans, NOT centered text with no anchoring structure.
visibility: public
mode: template
carrier: fixed-image
scenario: social-content
pattern_source: pattern.html
source_priority: skill-first
triggers:
  - "make a quote card"
  - "thesis card"
  - "punchline card"
  - "principle card"
  - "hero question card"
  - "one-liner card"
  - "book excerpt card"
related_patterns: social-card-editorial
---

# Social Card Quote / Thesis Template

Use when the page should carry one strong sentence, question, principle, or conclusion.

## Core Rule

The quote is the page. Do not bury it under decorations or explainers.

## Structure Options

- thesis sentence + source/context row
- hero question + short prompt
- quote + marginal note
- one-line principle + 3 tiny anchors
- section divider with large title

## Must Do

- Break lines semantically, not by random wrapping.
- Provide at least one anchor: date, section label, source, note, or footer marker.
- Keep whitespace intentional.
- Use `reference/title-and-breaking.md` for semantic line breaking.

## Avoid

- Long paragraphs disguised as quotes.
- Empty motivational slogans.
- Centered text with no anchoring structure.
- Overusing quote marks when the sentence is not a quote.

## Related Pattern

Use `social-card-editorial` as the closest pattern if a visual reference is needed.

## Pattern Source Rule

Read this `SKILL.md` first. Do **not** read `pattern.html` by default.

Read `pattern.html` only when you need concrete layout rhythm, spatial relationships, or interaction/annotation behavior that this markdown cannot fully specify. When read, extract patterns only; do not copy DOM, CSS classes, exact spacing, placeholder copy, or styling wholesale.
