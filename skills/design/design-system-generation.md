---
name: Design System Generation Skill
description: Import, extract, normalize, or persist a reusable DESIGN.md from an existing design system, HTML artifact, screenshot, template, style reference, or generated interface.
---

# Design System Generation Skill

Turn visual rules into a reusable `DESIGN.md`. Ordinary first-version page generation does **not** need this skill; use it only when the user wants to import, extract, normalize, persist, or reuse a design language. Core idea (borrowed from the DESIGN.md method): describe the visual system in natural language, keep precise values when available, and explain **why** each design choice exists, not just what it looks like. The output feeds `skills/design/design-system-reference.md` for reuse by future generations.

## Three modes

- **Import**: the user provided an existing `DESIGN.md`/design spec and wants it turned into a reusable reference. Behavior: read it, keep the user's own rules, check for missing sections, normalize structure only when useful, **do not rewrite to the model's own taste**, keep precise values, flag ambiguities where necessary. (e.g. "here is my DESIGN.md, follow it from now on", "check this for missing parts")
- **Extraction**: extract design rules from HTML/screenshots/templates/pages/CSS/style skills/brand references. Behavior: inspect the source, extract visible values and patterns, distinguish measured values from inferred ones, **describe both surface style and underlying intent**, do not mechanically copy every CSS rule, do not invent details that aren't there, separate reusable rules from one-off details. (e.g. "derive a DESIGN.md from this HTML", "summarize this screenshot into a design system")
- **Persistence**: distill the current approved artifact's style into a system reusable in the future. Behavior: inspect the current artifact, extract stable rules from the approved design, identify what should repeat vs what is one-off, **don't turn page-specific details into universal rules**. (e.g. "persist this page's style into a DESIGN.md", "future pages should follow this version")

When multiple modes apply, the user's explicit request wins.

## Do not use this skill when

Generating a single first-version page, only consuming an existing design system without changing it, local edits only, deterministic parameter changes only (color/spacing/radius/density), or ordinary design reference lookup (that's `design-system-reference.md`).

---

## Workflow

### 1. Determine the mode
Classify as Import / Extraction / Persistence; when several apply, the user's explicit request wins.

---

### 2. Extract design intent (don't just describe appearance)

Explain why the design uses each pattern, not just what it looks like.

Weak: `Blue buttons, rounded cards.`
Good: `Blue is reserved for primary actions and progress states, giving the interface one clear path; rounded corners soften an otherwise technical layout, making dense information more approachable.`

Cover: what each visual choice communicates, which parts are structural vs decorative, how it extends to future pages, which elements are the core of the style, and which must not be overused.

### 3. Separate stable rules from one-off choices

A good design system does not blindly preserve every detail. Sort decisions into: **core rules** (repeat in all future work), **optional motifs** (useful but not required everywhere), **one-off details** (belong to the current artifact only), **avoid** (should not repeat).

Example:
```text
Core rules: compact monospace metadata tags for project year/role/status.
Optional motif: when many projects, list rows show a hover preview image.
One-off detail: the oversized animated project number belongs to the homepage hero only.
Avoid: don't add random system tags to unrelated content pages.
```

### 4. Produce or update the DESIGN.md

The user provided an existing `DESIGN.md` → update/normalize rather than wholesale replace; extracting from an artifact → produce a new one; persisting the current design → produce one for reuse via `design-system-reference.md`. Concise but sufficient to guide future generation; don't build a sprawling design bible.

---

# DESIGN.md structure

Use the following 9-section structure by default. In each section write **practical rules + why** (not just values); keep precise values when available and clearly mark inferred ones.

**1. Visual Theme & Atmosphere** — overall temperament: mood, polish, density, visual temperature, personality, audience, the first-2-seconds feeling. **Anchor the theme with one concrete reference, not a string of adjectives** — "modern/clean/premium/trustworthy" specifies nothing; the model will only produce something mediocre centered in the middle of those words. Adjectives describe a "region"; a concrete reference (a class of objects/scenes/eras, e.g. "graduate-school lecture notes at an old 1970s university") describes a "point", and one sentence brings out palette/fonts/whitespace/presence of decoration — plus its own "what it is not". If adjectives are unavoidable, define their concrete meaning in this system.

**2. Color Palette & Roles** — record colors by **role**, not as a list: where each is used, which must not be overused, restrained accent. Don't invent values that aren't visible; mark inferred ones:
```md
### Core Palette
- Background `#F7F3EA` — warm editorial base color; page background.
- Text Primary `#171717` — high-contrast body copy and headings.
- Text Muted `#73706A` — metadata, captions, secondary details.
- Accent `#D94F30` — primary CTAs, active states, and one highlight per section only.
- Border `rgba(23,23,23,0.14)` — subtle structure without heavy boxes.
```

**3. Typography Rules** — font families + a **semantic hierarchy** (most systems have 9–15 levels, named semantically like headline/display/body/label/caption, each optionally split into small/medium/large), with size/weight/line-height per level, hierarchy span (restrained: headings ~1.9× body rather than 5×), and CJK-Latin-number mixing.

**4. Layout & Elevation** — grid/content width, spacing rhythm, whitespace strategy, content-area structure, alignment logic (structural, not decorative). **Also state "how hierarchy/depth is expressed"**: if shadows are used, define shadow rules; for flat design state the substitute (borders / color contrast / tonal layering, e.g. light background with pure-white cards for main content) — how hierarchy is conveyed is a core decision and must not be omitted.

**5. Component & Shape** — **shape language**: the overall shape personality (sharp / soft) and a unified radius strategy (e.g. all interactive elements at 4px, "restrained modernity"). **Component forms**: corner radius, borders, shadows, and padding rules for key components (cards/buttons/tags/inputs, etc.), **especially covering state variants** (primary/secondary, hover/pressed/active, empty/error/disabled) — state coverage is what makes a design system; don't just draw the default state.

**6. Interaction & Motion** — motion personality, entrance/hover/transition conventions, always with reduced-motion, core interactions distinguished from one-off effects.

**7. Responsive Behavior** — breakpoints, how mobile re-flows, touch friendliness, readability at each viewport.

**8. Do's and Don'ts** — write concrete rules. **Note: long, rambling Don'ts usually mean the theme description is too vague (a sufficiently concrete reference carries most negative constraints on its own); one concrete reference plus a deliberate Do/Don't list is the best combination.**
```text
Do: let the work be the main evidence; keep strong hierarchy; restrained consistent metadata tags; limit accent count; one memorable structural/interaction idea; reuse precise values when available.
Don't: fake testimonials/metrics/logos; generic section filler; copying brand assets/proprietary UI; purposeless decorative gradients/emoji; every section shouting equally loudly; dead links/broken clicks in publishable artifacts; treating a one-off hero effect as a universal rule.
```

**9. Agent Prompt Guide** — directly actionable generation instructions for a future agent:
```md
When generating a new page in this system: start from a work-first structure; use compact metadata tags for role/year/category; reserve accent for primary actions and active states; show real work early, don't open with a long bio; make one bold structural move and keep the rest quiet; avoid generic card grids unless the user asks for a simple version; keep responsive and touch-friendly behavior.
```


## Lightweight Tokens

If useful, include a compact token section.

Use only when values are available or can be responsibly inferred.

Example:

```json
{
  "color": {
    "background": "#F7F3EA",
    "surface": "#FFFFFF",
    "textPrimary": "#171717",
    "textMuted": "#73706A",
    "accent": "#D94F30",
    "border": "rgba(23, 23, 23, 0.14)"
  },
  "radius": {
    "sm": "6px",
    "md": "12px",
    "lg": "24px"
  },
  "spacing": {
    "base": "8px",
    "section": "96px"
  },
  "typography": {
    "bodySize": "16px",
    "bodyLineHeight": "1.5",
    "labelSize": "11px"
  }
}
```

Do not include fake precision. If values are inferred, state that they are inferred.

---

## Mode-specific pitfalls (avoid lists)

The core behavior of the three modes was given above under "Three modes". Each should avoid:
- **Extraction**: don't dump raw CSS into the DESIGN.md, don't invent values that aren't there, don't treat one-off details as system rules, don't omit responsive/interaction.
- **Persistence**: don't overfit the current page, don't treat placeholder content as design rules, don't harden temporary experiments into a permanent system, don't ignore style decisions the user already approved.
- **Import**: the output can be an updated version / normalized version / gap analysis + suggestions / compatibility notes; don't delete user rules unless they conflict or duplicate.

## Quality Rules

A good `DESIGN.md`: reusable, specific, rooted in the source material, concise but sufficient, clear about core vs optional, IP-safe, useful for future generation. **Avoid**: generic design boilerplate, empty "premium/modern/clean" wording, theory without actionable rules, copying proprietary brand systems, treating a single artifact's details as universal rules, inventing tokens the source doesn't support.

## IP and Brand Safety

When the source is public-brand inspiration: don't present the output as an official system, don't copy logos/assets/exact page structures/proprietary UI, describe only high-level visual qualities, and orient the output toward original, reusable rules. When the source is user-owned: what they explicitly provide is authoritative, keep precise values, and mark assumptions where information is incomplete.

## Chinese Typography Reference

When the artifact contains substantial Chinese/CJK text, Chinese editorial typesetting, WeChat-official-account layouts, Xiaohongshu cards, Chinese decks, Chinese UI labels, or print-style HTML, use `horizontal-craft/chinese-typography.md`; translate print methods into HTML structure: content width, grid, whitespace, heading groups, figure plates, margin notes, section rhythm, and punctuation.

## Quality Gate

Apply `quality-gate.md` before delivery; this scenario may add stricter checks but must not weaken the shared gate.

## Handoff

The generated/imported/normalized/updated `DESIGN.md` feeds `skills/design/design-system-reference.md` for reuse by future designs; it should be a reusable reference, not a one-time summary. When useful, record: the source artifact/template/screenshot, the chosen style skill/brand inspiration, date and version, assumptions, missing information.
