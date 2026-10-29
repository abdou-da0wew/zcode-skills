# Magazine Web PPT · Digital-Magazine-Style Web PPT Skill

> Other versions: [README.en.md](./README.en.md) (upstream English) · [README.pt-BR.md](./README.pt-BR.md) (Português)

An [agent skill](https://agentskills.io/) for the DiveeOI agent (OpenCode-based) that generates **single-file HTML horizontally paged PPT decks**. The visual foundation is "**digital magazine × e-ink**" — like *Monocle* pasted onto code.

> Distilled by [Guizang](https://x.com/op7418) from in-person talks such as "The One-Person Company: An Organization Folded by AI" and "A New Way to Work"; every pit stepped in along the way is recorded in `checklist.md`.

![Magazine Web PPT demo](https://github.com/user-attachments/assets/5dc316a2-401c-4e37-9123-ea081b6ae470)

## What you get

- 🖋 Three-level type system: **serif display headlines + sans body + monospace metadata**
- 🌊 **WebGL fluid / chromatic-aberration background**, visible on hero pages, restrained on body pages
- 📐 **Horizontal page flips**: keyboard ← → / wheel / touch swipe / bottom dots / ESC index
- 🎨 **5 preset theme palettes**: Ink Classic / Indigo Porcelain / Forest Ink / Kraft Paper / Dune
- 🧩 **10 page layouts**: opening cover, chapter divider, big-number stat, text-left/image-right, image grid, pipeline, suspense question, big quote, Before/After comparison, image-text mix
- 📄 **Single-file HTML**: no build, no server, opens directly in the browser

## Good fit / poor fit

**✅ Good fit**: in-person talks / industry briefings / private salons / AI product launches / demo days / presentations with a strong personal voice

**❌ Poor fit**: large data tables / training courseware (insufficient information density) / multi-user collaborative editing (static HTML)

## Installation

### Option 1: paste this message directly to your AI agent (recommended)

> Help me install the `guizang-ppt` skill for my DiveeOI agent (OpenCode-based). Follow these steps:
>
> 1. Make sure the agent's skills directory exists (create it if missing, e.g. `~/.opencode/skills/`)
> 2. Run `git clone https://github.com/op7418/guizang-ppt-skill.git <skills-dir>/magazine-web-ppt`
> 3. Verify: `ls <skills-dir>/magazine-web-ppt/` should show `SKILL.md`, `assets/` and `references/`
> 4. Tell me when it's installed; afterwards, when I say "make a magazine-style PPT" or similar, this skill should trigger

Paste that into the DiveeOI agent or any AI agent with shell access and it will complete the installation.

### Option 2: manual command line

```bash
git clone https://github.com/op7418/guizang-ppt-skill.git <skills-dir>/magazine-web-ppt
```

### Triggering

Once installed, the agent discovers and invokes the skill automatically in conversation. Trigger phrases:

- "make me a magazine-style PPT"
- "generate a horizontal swipe deck"
- "editorial magazine style presentation"
- "e-ink style talk slides"

## Usage flow

The skill is a structured 6-step workflow; the agent guides you through it:

1. **Requirement clarification** — 6-question checklist: audience, duration, source material, images, theme palette, hard constraints
2. **Copy the template** — `assets/template.html` → project directory, edit `<title>`, switch theme palette
3. **Fill in content** — pick from the 10 layout skeletons, paste, edit copy (run the class-name pre-flight + theme-rhythm planning first)
4. **Self-check** — against `references/checklist.md`; all P0 issues must pass
5. **Preview** — open directly in the browser
6. **Iterate** — inline style tweaks to font size / height / spacing

Full details in [`SKILL.md`](./SKILL.md).

## Directory structure

```
magazine-web-ppt/
├── SKILL.md              ← main skill file: workflow, principles, common mistakes
├── README.md             ← this file
├── assets/
│   └── template.html     ← complete runnable seed HTML (CSS + WebGL + page-flip JS preconfigured)
└── references/
    ├── components.md     ← component manual (fonts, colors, grids, icons, callouts, stats, pipeline)
    ├── layouts.md        ← 10 page-layout skeletons (paste-ready)
    ├── themes.md         ← 5 preset theme palettes (choose only, no customization)
    └── checklist.md      ← quality checklist (P0 / P1 / P2 / P3 graded)
```

## Theme palettes

Pick one from `references/themes.md` — **custom hex values are not allowed**; protecting the aesthetic matters more than offering freedom.

| Theme | Best for |
|------|---------|
| 🖋 Ink Classic | general default, commercial launches, when undecided |
| 🌊 Indigo Porcelain | tech / research / AI / technical launches |
| 🌿 Forest Ink | nature / sustainability / culture / non-fiction |
| 🍂 Kraft Paper | nostalgia / humanities / literary / indie magazines |
| 🌙 Dune | art / design / creative / galleries |

Switching themes only requires replacing the 6 variable lines inside `:root{}` at the top of `template.html`; all other CSS reads `var(--...)`.

## Core design principles

1. **Restraint over showing off** — the WebGL background only peeks through on hero pages
2. **Structure over decoration** — information is carried by type size + font contrast + grid whitespace, not shadows or floating cards
3. **Images are first-class citizens** — crop only the bottom; top and sides stay intact
4. **Rhythm comes from hero pages** — alternating hero / non-hero keeps eyes fresh
5. **Consistent terminology** — "Skills" stays "Skills"; no mixed translations

## Visual references

- Layout language of [*Monocle*](https://monocle.com) magazine
- YC's Garry Tan, "Thin Harness, Fat Skills"
- Guizang's in-person talk deck series

## Contributing

Bugs, typography issues, layout requests — open an Issue or PR. Preferred changes:

- Add classes in `template.html` rather than letting `layouts.md` use undefined classes
- Record new pitfalls in `checklist.md` at the matching P0 / P1 / P2 / P3 level
- Add new palettes to `themes.md` along with the scenarios they fit

## License

MIT © 2026 [op7418](https://github.com/op7418)
