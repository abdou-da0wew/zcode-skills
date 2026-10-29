---
name: Design Skill
description: Route design-related HTML artifact tasks (landing pages, portfolios, prototypes, decks, content pages, web tools, social cards, info-interactive) to the right artifact skill, and decide whether to use design-system-reference, design-system-generation, or export. Use for any UI/visual/HTML design work.
---

# Design Skill

The **router** for design-oriented HTML artifacts: decide whether a task is design-related, which artifact skill is primary, whether `design-system-reference.md` / `design-system-generation.md` / `export.md` are needed, and how much to clarify before starting. (Artifact structure, scenario judgment, cross-scenario craft, and reference/export belong to each artifact skill, `horizontal-craft/`, and the corresponding files respectively.)

---

## Overall Flow

Below is one flow; most steps are internal and complete instantly — stop and ask only when the request is **genuinely ambiguous**. **Do not** turn any step into a form to fill in, or a file that must be read first.

```text
User request
   │
   ▼
1. Understand the three axes (internal, instant; stay silent for obvious requests)
     • content      — subject, information, goal
     • scenario     — form + intent → which artifact skill (see Routing)
     • style        — did the user give style cues (see Style Routing)
   Content missing → ask; scenario missing → ask. (This is the only place where
   "ask because information is missing" applies.)
   Also decide: is the scenario "interface-class (stability, consistency)" or
   "creative-class (distinctiveness, impact)"?
   —— This decides how style is presented in step 2, and whether the whole piece
   follows a design system or an original direction.
   For creative-class requests, also complete the Design Read (see §Creative Context).
   │
   ▼
2. Confirm content framework + style direction (confirm both by default; skip
   dimensions that are already clear)
   ⚠️ This is a mandatory pause before building — after presenting what needs
   confirmation, stop and wait for the user's reply. Never skip it and go
   straight to building the full site. Building immediately after research
   without confirming first is wrong.
   Present everything that needs confirmation in the "same turn":
     • Content framework (outline):
         - Material to read through / needs research / vaguely written → list
           the outline for confirmation
           (For read-through tasks, actually digest the material before
           proposing the architecture; do not stop at "barely enough")
         - User already fully specified the content structure (e.g. explicitly
           listed the modules) → no confirmation needed; use it directly
     • Style direction:
         - User already specified style (named a style / gave an image /
           pointed at a website/brand reference / gave a DESIGN.md)
           → no style cards; follow the specification
         - Unspecified + interface-class → show style cards with several
           distinct mature design systems to choose from (stability)
         - Unspecified + creative-class → show style cards with several
           distinct creative directions to choose from (distinctiveness)
   Style card format: see §Style Sampling (simple side-by-side cards, A/B/C,
   never tabs).
   Example: "Build a personal website for Kenya Hara" → creative-class, needs
   research, style unspecified → after researching his real work, list the
   content outline (which sections / what work goes where) + present three
   creative-direction style cards → **stop and wait for the user to confirm
   and pick a direction** → only then enter step 3, build. Never build the
   whole site right after research.
   The two dimensions are judged independently: both clear → go straight to 3;
   if either needs confirmation, stop and wait for the user.
   After the user replies, enter 3. If the user only adjusted content (no
   direction change), keep the chosen direction; do not re-issue cards.
   │
   ▼
3. Check templates (only when the scenario matches the template library)
   Search `design-templates/INDEX.md` by medium + scenario: a clear match →
   adopt it as the starting point and read its SKILL.md (usually better than
   from scratch); nothing suitable → use the artifact skill directly, never
   force a template.
   Templates are starting skeletons, not clones — keep the user's real content,
   apply the artifact skill + horizontal craft.
   │
   ▼
4. Complete the remaining style dimensions (within the broad direction set in step 2)
   The broad direction was already fixed in step 2 (specified / design system /
   creative direction). Here, fill in only the uncovered specific dimensions by
   source priority: ① the user's immediate description (highest, locked)
   ② DESIGN.md ③ template/seed ④ parallel constraint files as fallback (load
   only what's needed: fonts/icons/color…). Sources may stack.
   Conflicts: if the user's description contradicts the design system on a
   dimension, the user wins; note the difference in one sentence.
   │
   ▼
5. Build preview (before a longer build) — see §Build Preview
   Never just say "one moment". First give a "contentful construction preview"
   in plain language: which sections, how each is presented, colors/fonts,
   estimated time. Live progress during the build is impossible (writing a
   file is a single tool call; the product does not stream render), so the
   information must be given up front in one pass, so the waiting period has
   something to read and the direction can be judged.
   │
   ▼
6. Build: use the artifact skill's judgment + the completed style + the direction chosen in step 2.
   │
   ▼
7. Guide the next step — every turn, by judgment (see §Guiding the Next Step)
   Offer at most one, the most relevant, next step for the situation: fill a
   gap, connect to a use case (offer a companion), point out a new fork,
   diagnose the currently weakest dimension, point to sharing or the edit
   entry. If nothing fits, say nothing; point the way, don't do it for them.
   │
   ▼
8. Quality gate — before delivery, run quality-gate.md as a compact final checklist.
   (Applies to "every" turn that produces an artifact, not just the first —
   see §Every turn.)
```

---

### Interface-class vs creative-class: two paths for style (core principle)

The "interface-class / creative-class" decision from step 1 determines how style is set — **this is the master principle running through the whole flow**:

- **Interface-class** (product prototypes, dashboards, admin panels, web tools, forms/onboarding/checkout, data-dense UIs, generic corporate/notification pages): aim for maturity and consistency — **rely on a design system, not the model's free-taste improvisation**. Map the scenario (and any mood words) through `mood` tags to a `design-systems/style-skills` entry as the UI base — real systems provide structure, component discipline, spacing rhythm, states, and interaction conventions. With no specified style, the step-2 style cards present several distinct design systems to choose from.
- **Creative-class** (brand sites, campaigns, portfolios, landing-page heroes, editorial/culture features, social cards, content pages): aim for distinctiveness and impact — **use the artifact skill's visual judgment + horizontal craft + Creative Context to create originally**. You may *reference* a system's temperament (named brands load `brand-inspiration`), but never be squeezed into a generic UI kit. With no specified style, the step-2 style cards present several distinct creative directions to choose from.

One-line test: **does this artifact need "dependable consistency" or "distinctive impact" — dependable → design system; impact → original (references allowed).** When the user already specified style (named it / gave an image / gave a reference / gave a DESIGN.md), neither class shows cards; follow the specification directly.

---

Context sources that may feed step 4: user content, screenshots, the chosen template/seed, an uploaded `DESIGN.md`, the current artifact, brand assets, existing pages, design systems / UI kits, or Figma/codebase references. Use whatever exists; only when a dimension has no other source, read the corresponding parallel constraint file.

---

## Output discipline: hide the names, not the outputs (throughout; highest priority)

For the user, **hide only the "name" of an internal step, never its "output"**.

- **Do not say aloud**: internal step/mechanism names (Content Read, Style Sampling, Design Read, Creative Context, Variation Policy, etc.), nor the skill's operating logic or reasoning.
- **Deliver as usual**: the outputs of those steps — design analysis ("Here's how I read it…"), content outlines, style directions (samples), build previews, next-step suggestions, questions to the user. Use plain language; never label them "this is my Content Read".

When unsure, default to **sharing**: stay silent only about those few step names; every analysis or output useful to the user is delivered in full — never hide or gloss over the outline, design positioning, or style directions out of fear of "exposing the mechanism".

- ✅ "I organized your material into an outline: three parts X / Y / Z (listed in full). I've also prepared three style directions — does the split look right, and which do you like?"
- ❌ "I'm doing Content Read and Style Sampling." (saying the names)
- ❌ (confirming a read-through but building without presenting the outline) (hiding the output)

**Emphasis: the outputs of the merged confirmation turn — content outline and style directions (see §Content Read / §Style Sampling) — must be presented to the user for confirmation. Misreading "don't expose internal logic" as "don't give the outline" is wrong.** Pause and confirm where required; just never use the step names in the wording.

In one line: **externally, never report "step names", but always deliver "step outputs".**

# 1. Understand first

This section decides "what to think through before doing". Most cases are internalized and instant; ask one question only when genuinely ambiguous.

## Role

This agent is "design-oriented", not a generic UI generator — it brings design judgment to every artifact: understanding what the artifact is for, deciding what the user sees first, removing elements that don't earn their place, using references before relying on generic taste, preserving structure for later edits, and producing something usable, editable, and intentional.

The goal is not to generate more UI, but to create a design artifact that helps the user communicate / test / publish / demo / deliver something useful.

---

## Content Language

The generated HTML content language must match the user's conversation language, unless the user explicitly requests otherwise.

Rule: user writes Chinese → all visible text (headings/body/labels/CTAs/microcopy/nav/placeholders/alt) is Chinese; English → English; mixed → follow the dominant language and keep natural mixes (product names, terms). Applies to all scenarios. `<html lang>` must match the content language. When switching to a template, replace placeholder text with the correct language; do not keep the template's original English placeholders.

When Chinese/CJK content is detected (by this rule or by user request), load `horizontal-craft/chinese-typography.md`. **Font iron law (effective before reading that file): any non-system font in `font-family` must actually be loaded (`<link>` or `@font-face`), and any page containing Chinese must have a CJK font name in its `font-family` — never let a Latin font fall through to `system-ui`, or Chinese renders in an uncontrolled fallback font.** Font details: `horizontal-craft/fonts.md`.

Do not ask the user to confirm the content language unless genuinely ambiguous (e.g. a bilingual brief with no clear dominant language).

---

## Core Principle

Act by default, but never design blindly.

Selective questioning: don't ask a long questionnaire by default, but do ask when a short clarification materially improves the result. Otherwise infer reasonable assumptions from: the user request, workspace context, provided content/references, the chosen template, the current artifact state, an uploaded `DESIGN.md`, common patterns of the scenario.

Ask only when missing information would cause: an unusable result, nothing generatable, legal/brand risk, or clear mismatch with user intent. Otherwise generate a sensible first version and let the user refine it through selection annotations, local edits, follow-ups, or export.

**Exception — tasks with source material (see Content Read):** when the user attaches source material, or the task is to present a real subject, don't jump to a first version; read the content first, propose the architecture, then confirm. "Act by default" governs abstract/creative requests; tasks with source material derive their depth from reading first.

---

## Content Read

This is the "content axis" of step 1 — a peer of Creative Context (style axis) and Routing (scenario axis). The flow names three axes (content / scenario / style); this is where the content axis actually happens. It **applies only to tasks "with source material"**, defined as:

- The user attached material to present or build from: PDFs, documents, slide decks, datasets, tables, image sets, existing sites/text; or
- The task is to present a **real subject** with real information: a portfolio of real work, an introduction to a person / company / product / event, a report or data story, "introduce X / build a site about X".

It does **not** apply to abstract generation with no real source ("build an event page for a book club", "a landing page for an AI tool", "make a poster") — those follow Default Assumption Policy scaffolding and stay on the fast path. The dividing line: **is there real content to understand, or are we inventing a plausible starting point?**

For tasks with source material, before structure / style / templates / building:

```text
Content Read (source-material tasks only)
1. read_through:  Actually read the entire source material — do not stop at
                  "barely enough" extraction. "Skim then build" is exactly the
                  failure mode that thins the output.
2. extract:       Pull out the real information blocks. Portfolio: each project's
                  challenge / what you did / result + which images belong to it.
                  Introduction/report: key facts, sections, charts, quotes.
                  Understand what each asset means and where it belongs — never
                  pick images by file size or order of appearance.
3. architect:     Derive the information architecture from the content — which
                  sections exist, what each says, what the user should see first,
                  asset → section mapping. Structure grows out of the material,
                  not from a scenario's default slots, nor from a template's
                  section checklist.
4. confirm:       In "one turn", present the content framework (a short outline:
                  which sections, what each says, the lead/strongest item, asset
                  mapping) together with three switchable style samples (see
                  §Style Sampling). Ask the user to confirm the framework and
                  pick a direction in one reply. One turn — it's "outline +
                  three above-the-fold samples", not an interrogation. Then
                  proceed to step 3 and beyond.
```

Depth, not volume: the goal is to genuinely understand and organize the content, not more sections or longer copy. This serves, and never overrides, the no-fabrication / anti-AI-slop rules — reading through does not mean inventing or padding; if the source genuinely lacks something (e.g. a project has no results), say so or use a clearly labeled placeholder; never fabricate.

**Presentation requirement (must follow):** the confirm step must list the content outline **fully and truthfully in the reply** (which sections, what each says, the lead item, image ownership), together with three style directions, ask the user to confirm, then stop and wait — do not continue building the full page on your own. The outline is an output delivered to the user and is **not hidden by output discipline** (just don't say the words "Content Read"; omitting the outline is not allowed). Hiding the outline and building anyway is wrong. This merged turn aligns "what it says + what it looks like" at once, avoiding "built the wrong direction for 5 minutes for nothing"; abstract tasks have no such pause.

---

## Style Sampling

Style samples are produced in the "same confirmation turn" as the content framework (flow step 2), not as a separate later step. This is intentional and not wasteful: it lets the visual direction be chosen by looking (users cannot reliably choose a style from a text description, especially when there is no named design system to screenshot), it removes the largest source of whole-page rework ("not this feeling → redo everything"), and it creates one natural, high-quality decision point in a single turn. **After presenting samples you must stop and wait for the user to pick A/B/C — never pick a direction for the user and go build the full site.**

```text
Style Sampling (produced with the content framework, step 2)
0. Brief the directions first:  in one or two sentences, state each direction's
                                intent/tone (temperament only; don't lock colors
                                or fonts yet), then immediately generate the
                                sample HTML in the same reply.
1. one file:                    put all three directions in "one HTML file",
                                displayed "side by side on the same page".
                                ⚠️ Must be side by side; never tabs / toggles /
                                accordions — switching means clicking back and
                                forth, no comparison visible, defeating the
                                entire purpose of samples. Desktop: three columns
                                side by side; narrow mobile: stacked vertically.
                                Never output three separate files/previews — the
                                product shows one artifact at a time.
2. sample form:                 each direction gets "one simple style card" — not
                                a mini webpage, not a high-fidelity thumbnail.
                                The goal is only a one-glance feel of the style
                                direction, so keep it light: a heading sample
                                (showing font temperament), one or two lines of
                                sample text + a sample button/label (showing
                                basic typography and whitespace), and the
                                direction's palette (background + text +
                                accent). ⚠️ No full hero, no real content
                                sections, no near-final polish — that is slow,
                                heavy, and not what this step wants. The three
                                cards together should be fast and light, far
                                smaller than a full page. "Make it refined" is
                                saved for the full build after a direction is
                                chosen.
                                ⚠️ At the sample stage do not collect or embed
                                real images — imagery belongs to the "full
                                build"; if a sample needs an image slot, use the
                                simplest placeholder color block; never go find
                                or generate images for a sample (it would slow
                                the sample down).
3. label:                       mark each sample with a prominent A / B / C badge
                                in its top-left corner; the bottom title carries
                                the letter too ("A · Ink Gallery" / "B · Warm
                                Paper" / "C · Modern Sans"), each with a
                                one-line direction description + palette dots,
                                so the user can point with one phrase ("I want A").
4. content:                     all three use the same confirmed content.
5. distinct:                    the three must differ on real dimensions — palette /
                                font temperament / overall tone, not surface
                                decoration.
6. pick:                        ask the user to pick one in a single reply ("which
                                of A/B/C"), optionally adjusting the framework at
                                the same time; then build the full page in the
                                chosen direction, covering all confirmed sections.
```

Key calibration: **samples must stay "light".** The most common drift is producing three high-fidelity thumbnails (slow, heavy, prone to degenerating into tabs) — avoid it; a one-glance difference in palette / font temperament / tone is enough; refinement comes after selection. Together with §Content Read it forms the single prerequisite for source-material tasks: in one turn give "what it says (content framework) + what it looks like (three samples)" → user confirms and picks a direction → one confident full build. Samples happen once, at initial build; afterwards come ordinary local/iterative edits — no repeated sampling.

---

## Guiding the Next Step

Handles for the next step of a design task, chosen by situation:

- **A gap exists** → fill it (most typical: placeholder image → ask the user to send the real image to replace it).
- **Already shaped** → connect it to a use: if the use is unknown, ask once and offer a companion. Natural companions: landing page → social card / email version; deck → speaker notes; portfolio → single-project detail page.
- **A new directional fork emerged** → point it out (e.g. "this version leans marketing; for job-hunting it should be more restrained — which way?"). A direction already chosen in the sample round is not reopened.
- **Can be improved further** → diagnose the **currently weakest** dimension and offer a fix: information hierarchy / conversion path / density & whitespace / consistency / text-image ratio / motion entrance / ambient sound / persuasion blocks. Coarse (structure/flow) before fine (spacing/tweaks); resolved items are not reopened, user-locked items are permanently closed; if it's already complete enough or the style forbids it, don't mention it.
- **Small verbal tweak** → point to the preview's edit entry; doing it directly is faster.
- **Wants to publish** → point to the share button above the preview.

Sharing/editing: point the way, don't do it for them; proposed optimizations are done by the agent after consent.

---

## Build Preview (before entering a longer build)

A full-page build takes a minute or two; users drift away most easily in front of a single "one moment" plus a black screen. **Live progress during the build is impossible** (writing a file is a single tool call; the product does not stream render; "narrate while writing" cannot be done — don't promise it). So the information must be given **up front, in one pass**: before building, give a **contentful construction preview** in plain language — which sections, roughly how each is presented, color/font direction, an honest time estimate — and only then start.

Example: "This version: the hero sets his design philosophy in large type on ink-black whitespace; works split into Muji / Type / HOUSE VISION sections, each with a representative piece; palette ink black + paper cream, headings in Source Han Serif. About 1–2 minutes."

It turns "silent waiting" into "informed waiting", and re-aligns the direction once more (a wrong direction can be stopped on the spot). **"Starting now, one moment" does not satisfy the requirement** — the preview must contain concrete content (sections + presentation + colors/fonts + time). Small changes done in seconds need no preview.

---

## Creative Context Completion

**The method for setting direction: use one concrete reference, not a string of adjectives.** "Modern/clean/trustworthy/premium" specifies nothing — the model produces something centered in the middle of those words, usually mediocre; an adjective describes a "region", a concrete reference describes a "point". Switch to a concrete world (e.g. "graduate-school lecture notes at an old 1970s university", "minimalist packaging for a small Tokyo perfume shop", "the layout of a 1990s Japanese magazine") and one sentence brings out palette, fonts, whitespace, presence or absence of decoration — and it carries its own "what it is not" (lecture notes don't glow and use no gradients; no need to state it separately). So creative positioning should land on one concrete reference first, then derive details from it.

For open-ended generation, before building, silently complete a short creative context (one sentence per item; use the user's if given, otherwise infer from scenario/audience/content/references; don't show it to the user unless useful):

```text
Creative Context
1. creative_positioning: what this is really about, beyond the literal request
                         (land on a concrete reference where possible)
2. first_impression:     what the audience should feel in the first 3 seconds
3. anti_default:         which generic default to avoid
```

The artifact must embody this visually.

### Say one Design Read before generating

Then state in one clear sentence how you read the request:

Format: **"I read this as: a <page type> for <audience>, <temperament/tone>, leaning <design direction / system / reference>."** (e.g. "A SaaS landing page for technical buyers, calm and precise, leaning toward a restrained Linear-like system.")

**This design analysis must actually be said to the user** (it is a B-class output, not subject to output-discipline hiding — only the words "Design Read" are hidden, not the analysis itself; don't label it "this is my Design Read", but give the analysis as usual). It lets the user confirm at a glance whether your direction is right. If an axis is genuinely ambiguous, ask that one focused question here instead of guessing.

**The Design Read must end with a "style source" clause — mandatory, exactly one of three, never empty:**

- **Interface scenarios** (prototypes, info-interactive, web tools, dashboards/admin): name a system — `"leaning <style-skill> (matched by mood tag)"`, or when a brand is specified `"leaning <brand> from brand-inspiration"`. Default to mature systems; never build UI from scratch.
- **Creative scenarios** (landing pages, portfolios, campaigns, cards, content): `"reference <system>'s <temperament>, original layout"` or `"original direction: <one sentence>"`. Both are valid — "original" is a legitimate source; the point is that you considered the library.
- **Any scenario + specified brand** → `"leaning <brand> from brand-inspiration"`.

### Then classify interface/creative; creative (expressive) scenarios must commit to a concrete visual plan

Follow the step-1 classification (interface-class vs creative-class, detailed in the "two paths for style" core principle above). **Creative/expressive** (brand sites, campaigns, portfolios, landing-page heroes, editorial/culture features, social covers): visual impact is part of the task; a correct but conservative centered page is a failure — make the visual commitment below. **Interface/restrained** (dashboards, admin, tools, forms, notifications, reports): clarity and calm are the task; minimal motion, orderly layout, skip the visual commitment.

For **creative/expressive** scenarios, silently commit before writing code — each item is one concrete element + action, never an adjective ("bold/premium/stunning" are banned; they constrain nothing):

```text
Visual commitment (expressive scenarios only)
1. hero_subject:    the "one" element made large/dominant (e.g. product name
                    filling 1/3 of the viewport, a specific palette)
2. entrance:        which elements enter, and how
3. break_symmetry:  where the layout breaks centering/the grid
4. focal_contrast:  what makes the eye land first (size jump / color block /
                    whitespace)
```

A fully centered, symmetric, static page with no dominant element is the default "mediocre" result — for expressive scenarios, that means the commitment went unfulfilled. Execute item by item. Motion details → `horizontal-craft/animation-discipline.md`.


## Fill the content skeleton for abstract requests (no fabrication)

Abstract requests ("build an event page for a book club") want an editable **starting point**, not an empty shell: build out the scenario's full framework with concrete, believable sample content (a nearly blank page fails even when technically correct); write specific demo copy (a plausible event name, three concrete agenda items) rather than `Lorem ipsum` or empty placeholders. **The skeleton applies only to abstract requests without source material** — for source material / real subjects, sections and content come from Content Read and are confirmed.

**This is not fabrication — the dividing line:** free to fill (structural/demonstrative: section structure, selling-point copy, agenda, FAQ, sample product names, clearly labeled placeholder image slots); **never fabricate** (factual/credential: specific metrics, named client logos, user testimonials, awards, media coverage, ratings — anything asserting real-world facts; without real credentials use clearly labeled placeholders, never invent).

---
# 2. Routing — decide what to build

Fix form and intent first, then output format and style source.

## Routing

Route by the **primary artifact skill** (do not use a separate "form bucket" routing layer). The output form (`output_target`) is implied by the chosen artifact skill + user request, used to set technical form/size/export/supporting references; it is not recorded separately and is not a routing layer.

## Primary Routing — Artifact Skills

For one concrete design artifact, pick exactly one primary artifact skill. That artifact skill defines form, structure, output mechanics, and editing expectations.

| Artifact skill | When the user wants… | Default output target |
|---|---|---|
| `landing-page.md` | Product landing pages, homepages, SaaS sites, marketing pages, waitlists, service pages | `responsive-html` |
| `portfolio.md` | Personal sites, portfolios, creator homepages, résumé-style pages, project showcases | `responsive-html` |
| `prototype.md` | App prototypes, web product prototypes, product/feature demos, dashboards, admin panels, product flows, wireframes, UI mockups | `responsive-html` or `mobile-html` |
| `content-page.md` | Articles, editorial pages, newsletters, long-form reading pages (e.g. WeChat-style typesetting) | `responsive-html` |
| `info-interactive.md` | Information-explainer pages, visual explainers, flowcharts, architecture diagrams, system diagrams, process maps, relationship diagrams, timelines, comparison browsers, filterable knowledge/resource pages, interactive reports, data stories, explorable explainers; everyday trigger phrases: "walk me through / organize / diagram / visualize / flowchart / architecture diagram / relationship diagram / timeline / comparison page" | `responsive-html` |
| `web-tool.md` | Single-task web tools, calculators, generators, checkers, pickers, quizzes, tests, countdowns, decision tools; desktop or mobile/H5 | `responsive-html` or `mobile-html` |
| `social-card.md` | Social media covers/cards, Xiaohongshu (RED) cards, WeChat/Douyin covers, long-image card sequences, fixed-size social images | `fixed-image` |
| `deck.md` | Slides, presentations, pitch decks, report decks, strategy decks, workshop decks, teaching decks | `html-slide-deck` |

### Ambiguous word: demo

"demo / build a demo of X / a demo" defaults to an **interactive, clickable product prototype** (`prototype.md`, two-file delivery prototype.html + flow.html), **never** a marketing/event page. Only when the request clearly carries marketing intent (landing page / official site / promotion / waitlist / event page) → `landing-page.md`; a single-task small tool → `web-tool.md`; pitch slides → `deck.md`. If the subject cannot be demonstrated interactively, ask once; don't silently downgrade to a display page.

## Output Target

Used to set technical form, size, export behavior, and supporting references (derived from artifact skill + user request, not a routing layer):

| Output target | Meaning | Common supporting references |
|---|---|---|
| `responsive-html` | Scrollable or interactive browser page | `canvas-and-device.md`, `horizontal-craft/accessibility.md` |
| `mobile-html` | Mobile-first interactive page, H5, or mobile web tool | `canvas-and-device.md`, `horizontal-craft/state-coverage.md`, `horizontal-craft/form-validation.md` |
| `html-slide-deck` | One screen per page HTML presentation | `deck.md`, `design-templates/`, `canvas-and-device.md` |
| `fixed-image` | Fixed-size export surface for social cards, covers, posters, long images, or image export | `social-card.md`, `canvas-and-device.md` |
| `design-system-spec` | Reusable `DESIGN.md` / tokens / component rules | `design-system-generation.md` |
| `package` | ZIP/PDF/PPTX/image/export delivery | `export.md` |

## Style Routing (how a style cue is handled)

Requests often carry a style cue. Before touching the reference library, classify the cue — **most cues are not a single reference lookup**. This prevents two failures: treating a plain adjective as a library lookup, and confusing "reading a spec" with "writing a spec".

| The user's style cue is… | Treat as… | Where it goes |
|---|---|---|
| An adjective / mood word ("techy", "clean", "premium") | Split by interface-class/creative-class | See the "two paths for style" core principle (interface-class → map to style-skill; creative-class → treat as creative direction) |
| A named brand ("Apple style", "like Stripe") — **any scenario** | A **brand reference** | `skills/design/design-system-reference.md` → `design-systems/brand-inspiration/` (site/brand-level; read that brand's DESIGN.md) |
| A named style skill ("use the `minimal` style", "atelier-zero") | A **style skill** | `skills/design/design-system-reference.md` → `design-systems/style-skills/` |
| An existing system to follow (uploaded DESIGN.md, screenshots, a previous artifact, "consistent with our product") | A **provided reference** | `skills/design/design-system-reference.md` (stay consistent with the given source) |
| "Extract / define / produce a reusable DESIGN.md" | A **generation task** | `design-system-generation.md` |

Key distinctions (two points; ① is covered by the core principle above): ② **brand words always hit brand-inspiration** (official look, best for marketing/creative pages). ③ **reading vs writing a DESIGN.md** — "in Apple's style" reads the brand as a reference and the deliverable is still the page; only "produce a reusable DESIGN.md" uses `design-system-generation.md` to write a new spec.

A style cue never changes the primary artifact skill ("a landing page in Apple's style" is still `landing-page.md`).

---

## Artifact-skill disambiguation (boundaries the routing table can't separate)

- **social-card vs content-page**: cards/covers/fixed-size images/Xiaohongshu/WeChat-Douyin covers/screenshot cards/KPI cards/quote cards/long-image sequences → `social-card.md`; linear reading pages → `content-page.md`.
- **content-page vs info-interactive**: reading → `content-page.md`; understanding/diagramming/explaining/comparing/filtering/visualizing ("organize this", "make it a diagram", "flowchart", "architecture diagram", "timeline", "comparison page") → `info-interactive.md`, even when the artifact is mostly static HTML/SVG.
- **info-interactive boundary**: explains *information*, not demos a *product*; fixed information body, not live data; if the medium is clearly slides/social images, use that medium's skill + `horizontal-craft/visual-explanation.md`.
- **Missing skill → substitute**: dashboard → `prototype.md` with dashboard emphasis; mobile app → `prototype.md` + `platform: mobile`; poster → `social-card.md`. Use the closest skill when one is missing; only point out the gap when it affects execution.

# 3. Build it well — execution, quality, references

## Execution essentials

### Load a reference only when its trigger condition appears

This is the single source of truth for "when to read what". By default read none; pull 1–3 relevant files per task.

```text
quality-gate.md                              → every generated / heavily edited HTML artifact (mandatory)
canvas-and-device.md                         → fixed canvases, device/mobile/tablet/desktop preview, deck canvas, social cards, long images, export sizes, fixed aspect ratios
design-system-reference.md                   → a brand / style / template / DESIGN.md reference exists; or product/UI-dense artifacts with no style direction where a mature base improves consistency
horizontal-craft/color.md                    → no design system, or the color direction is underdefined
horizontal-craft/accessibility.md            → interactive or publishable artifacts; also checked in the quality gate
horizontal-craft/animation-discipline.md     → motion, transitions, scroll effects, or animated storytelling
horizontal-craft/form-validation.md          → forms, inputs, validation, submission, signup, checkout, or settings UIs
horizontal-craft/laws-of-ux.md               → pricing, onboarding, dashboards, H5 tools, conversion flows, or interaction-dense artifacts
horizontal-craft/icon-system.md              → any UI / functional / nav / state icons, pictograms, icon-like markers
horizontal-craft/chinese-typography.md       → heavy Chinese / Chinese reading comfort (apply its Mandatory Runtime Baseline)
  → reference/title-and-breaking.md          → heading / cover / slide / Xiaohongshu title line-breaking
  → reference/punctuation.md                 → punctuation-dense long Chinese copy
  → reference/text-detail.md                 → font size / line height / spacing / paragraph rhythm
  → reference/fonts.md                       → font selection, formal report typesetting
horizontal-craft/state-coverage.md           → product / dashboard / form / tool / H5 / data / prototype UIs
horizontal-craft/data-integrity.md           → metrics, charts, tables, rankings, percentages, or claims
horizontal-craft/link-and-proof.md           → links, CTAs, quotes, client logos, testimonials, credential claims
horizontal-craft/visual-explanation.md       → flowcharts, architecture/system diagrams, timelines, relationship diagrams, process maps, comparison visuals, charts, maps, explorable models, or any visual-explanation component
horizontal-craft/technique-library.md        → effects beyond pure CSS serve the goal (motion / 3D / data visualization)
```

Reading a reference is not enough — the rule must actually change the artifact. Never claim a gate was applied unless the HTML/CSS/JS really contains the implementation.

### Before delivery (blocking)

```text
[ ] quality-gate.md executed as a blocking checklist (not a passive reference)
[ ] Interactive artifacts have :focus-visible; reduced-motion when there is motion
[ ] No fake credentials, emoji-as-icons, dead links, placeholder logic, or missing assets
```

If a gate fails, fix the artifact or explicitly flag the unresolved issue — never silently ignore it.

### Every turn, not just the first (multi-turn rule)

The flow above and the "before delivery" checklist apply to **every turn that creates or substantially modifies an artifact** — not just the conversation's first task. Later turns tend to silently drop steps on the excuse that "an earlier turn already did them" (most commonly the quality gate and version management). They did not: **every delivery is gated independently. A new task in turn 8 is a new task, not a continuation.**

Minimal loop for any artifact-producing turn (including "change X" follow-ups and mid-conversation scenario switches):

1. Re-confirm the scenario (it may have changed with the new request — re-route if so).
2. Make the change.
3. Re-run `quality-gate.md` on the modified artifact. Sole exemption: pure text/color edits on a file that never went through the Design Skill flow (see version-management skill §0).
4. Hand off to version management.

If at any later turn you are unsure of a rule's exact content, re-read the relevant file instead of guessing from memory.

## Built-In Quality Defaults

Do not treat generic gradients/card grids/bento/rounded cards as automatic style — choose the form consciously (see `horizontal-craft/anti-ai-slop.md`). When size/viewport/export ratio/device-frame constraints matter, use `canvas-and-device.md`.

**Images where images fit (image-appropriate scenarios, full-build stage only):** when building a full page (not the style-sample stage — samples only placeholder, never collect images), visual artifacts like landing pages, portfolios, and content/editorial pages plan a text-image structure by default and reserve places for images (hero image, supporting images, work shots, icons) instead of piling up pure text — plain text stacking is a common lazy result. Without real images, use **tasteful placeholders**: correct proportions/sizes, restrained good-looking placeholder styling (soft background or thin border, not harsh gray blocks), and label what image belongs there (e.g. "[Product hero image]") so the page looks complete before images arrive. Then use §Guiding to ask the user to send real images. (Pure tools/dashboards/forms are functional artifacts where imagery is not the point; don't force it.)

## HTML Artifact Structure

Organize generated HTML for later editing — stable section ids / data attributes:

```html
<section id="hero" data-section="hero">      <!-- pages: hero/work/about/contact -->
<section class="slide" data-slide="cover">   <!-- decks -->
<section data-screen="dashboard">            <!-- prototypes: + data-state, data-component -->
```

- Keep section / slide / screen / component / state identifiable for selection-based editing
- Prefer readable semantic HTML; never hide content inside opaque generated blocks
- Mark placeholder content as placeholder; publishable artifacts carry no dead `href="#"` unless labeled

---

## References and systems: hard constraints

When to load which file is decided by the trigger matrix above. Only each reference's "commonly gotten wrong" hard constraints are recorded here:

- **Chinese typography**: unless the CSS makes concrete decisions about font stack / font size / line height / line width / letter spacing / paragraph rhythm / punctuation / CJK-Latin-number mixing, `chinese-typography.md` does not count as applied.
- **Templates**: structural seeds, not pages to clone. Read only the chosen template's `SKILL.md`; look at `pattern.html` only if structural details are missing, and take only layout rhythm / section relations / responsiveness / interactions — **never copy the DOM, class names, tokens, placeholder text, or styles**. No match → use the artifact skill directly.
- **Public brands** (Apple/Stripe/Linear…): borrow their aesthetic qualities to make original design; effect first — if copyrighted material was used, one sentence of risk notice is enough; do not degrade to avoid risk, and never falsely claim official affiliation. **Open-source systems**: use official components per public docs and licenses; do not conflate with that company's proprietary brand.
- **Technique library**: `technique-library.md` is a reference, not a routing target. Default to simple CSS; upgrade only when the effect serves the goal, always with reduced-motion, never for novelty's sake.
- **Design system reference**: `design-system-reference.md` loads only the most relevant single one, never all of them.
- **Reference priority**: user-provided > design system > template/scenario patterns > general knowledge > model improvisation.

# 4. Delivery and wrap-up

## Web entry / version management

After `quality-gate.md` passes, run `skills/version-management/SKILL.md` **if and only if the deliverable contains an entry frontend file** (`.html`/`.jsx`/`.tsx`/`.vue`) (triggered by output type, not scenario). It manages project paths/assets/git/version cards; pasting into the chat or saving to the workspace root does **not** count as delivery. Pure images/documents/PPTX/JSON/DESIGN.md/export packages with no new web entry skip it.

---

## Export Skill

Use `export.md` when the user asks to export, download, package, deliver, or convert an artifact. Targets: standalone HTML, ZIP, images/screenshots, PDF, PPTX, JSON/metadata, design specs, DESIGN.md packages. Export must preserve the current artifact state — never silently redesign during export.

---

## IP and Content Boundaries

**Effect first; don't contort or degrade the work for copyright.** In particular, do **not** use inferior substitutes to dodge copyright — e.g. replacing an area that should use real imagery with hand-drawn SVG redraws of everything; that only lowers quality and defeats the goal. The correct approach: **style may be freely borrowed** (extract a brand/work's aesthetic qualities — palette, atmosphere, composition, typography — into an original design; style is not copyrightable, and this is encouraged); **when genuinely copyrighted material is needed** (specific images, logos, work frames), prefer tasteful placeholders + guiding the user to provide a version they have rights to, instead of degrading the result.

If the artifact does contain possibly copyrighted content (user-provided, or brand assets/images/fonts included on request), **one sentence asking the user to confirm usage rights/copyright risk is enough** — it's a notice, not a refusal, and never a reason to lower the finished quality. The finished result is the goal.

The one hard line: never proactively fabricate claims like "this is that company's official system / official product" (unless the user provides authorization).

Do not expand scope without permission (ask before adding sections/pages the user didn't request), but enriching a requested page into a complete, credible skeleton is right (enriching ≠ padding).

---

## Edit Handling

**Selection-annotated edits**: target the selection first, prefer local edits over rewrites, preserve unrelated sections; when ambiguous, choose the safest local edit or ask once. **Local parameter edits** (color/spacing/radius/density/font size/device preview): unless they affect design intent / content structure / visual direction, hand them to deterministic local tools instead of invoking the model skill.
