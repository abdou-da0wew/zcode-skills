---
name: web-shader-extractor
description: |
  Extract WebGL/Canvas/Shader visual effect code from web pages, de-obfuscate it, and port it into a standalone native JS project.
  Trigger when the user provides a URL and asks to extract a shader, extract an effect, extract an animation, extract a canvas effect,
  replicate a website's visual effect, "rip this site's background effect", etc.
---

# Web Shader Extractor

Extract WebGL/Canvas/Shader effects from web pages, de-obfuscate them, and port them into standalone projects.

Core principles:
- **Replicate 1:1 first; only consider simplifying the framework after correctness is confirmed**
- **Run fully autonomously without interrupting the user** — extraction is a read-only operation with no safety risk. Except for the Phase 6 simplification proposal, all steps run automatically without asking the user for confirmation. When problems arise, judge the best path yourself and keep moving; only ask the user when a product decision is genuinely needed.

## Phase 0: Environment Check (auto-runs on first use)

Before starting extraction, check and automatically install the required dependencies. **Do not ask the user; install directly**.

```bash
# 1. Check Node.js
node --version 2>/dev/null || {
  echo "Node.js not found, installing..."
  # macOS
  brew install node 2>/dev/null || {
    # fallback: download LTS directly
    curl -fsSL https://nodejs.org/dist/v22.15.0/node-v22.15.0-darwin-arm64.tar.gz | tar xz -C /usr/local --strip-components=1
  }
}

# 2. Playwright and browser (fetch-rendered-dom.mjs auto-installs, but this precheck surfaces problems early)
RUNNER_DIR="$HOME/.cache/playwright-runner"
if [ ! -d "$RUNNER_DIR/node_modules/playwright" ]; then
  echo "Installing Playwright (one-time setup)..."
  mkdir -p "$RUNNER_DIR"
  echo '{"type":"module"}' > "$RUNNER_DIR/package.json"
  npm install playwright --prefix "$RUNNER_DIR"
  npx --prefix "$RUNNER_DIR" playwright install chromium
  echo "Playwright + Chromium installed."
fi
```

If installation hits permission or network problems, try these fallbacks:
- npm permission issues → install into the user directory with `--prefix`
- Network issues (slow Chromium download) → set `PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright` to use a mirror
- If Playwright truly cannot be installed → degrade to pure-curl mode (skip DOM rendering; analyze only static HTML + JS bundle) and note in Phase 2 that canvas-info may be missing

## Phase 1: Fetch the Source

**Run in parallel**: Playwright to fetch the rendered DOM + curl to fetch the static HTML.

```bash
# Playwright (canvas engine version, component tree, runtime network requests)
node ~/.claude/skills/web-shader-extractor/scripts/fetch-rendered-dom.mjs '<URL>'
# → /tmp/rendered/: dom.html, canvas-info.json, network.json, screenshot.png, console.log

# curl (raw HTML, for extracting inline configs and keys)
curl -s -L --compressed '<URL>' > /tmp/page.html
```

If the Playwright script fails (not installed / startup error), first attempt auto-repair (reinstall dependencies); if it still fails, degrade to pure-curl mode and keep working — do not stop to ask the user.

Cross-extract JS URLs from network.json and the HTML, and batch-download them into /tmp/.

### Phase 2: Tech Stack Identification

```
dataEngine field of canvas-info.json:
├─ "three.js rXXX" → Three.js (r170+ may be TSL → references/tsl-extraction.md)
├─ "Babylon.js vX.X" → Babylon.js
├─ null → distinguish further:
│   ├─ bundle contains createShader/shaderSource → Raw WebGL / PixiJS
│   └─ bundle contains getContext('2d') and no WebGL calls → 2D Canvas (→ references/porting-strategy.md § 2D Canvas)
└─ no canvas → CSS/SVG animation

URL or HTML signature matches a known platform → jump straight to the dedicated workflow (skip generic Phases 3-4):
├─ unicorn.studio → references/unicorn-studio.md (Firestore REST API to fetch config + shaders directly)
└─ shaders.com → references/shaders-com.md (Nuxt payload + XOR decoding + TSL→GLSL translation)

Scan to confirm: bash scripts/scan-bundle.sh /tmp/*.js
→ framework signature quick reference: references/tech-signatures.md
```

### Phase 3: Config Extraction

```
1. Look for public APIs → fetch config directly (the API response may be encoded → references/encoded-definitions.md)
2. Extract from Nuxt payload / __NEXT_DATA__ / inline HTML JSON
3. Extract default values from the JS bundle
→ details in references/config-extraction.md
```

### Phase 4: Shader Code Extraction

Use a **subagent** to analyze the JS bundle (1MB+ does not fit the main context).
→ agent prompt template and de-obfuscation rules in `references/extraction-workflow.md`

### Phase 5: Porting

```
Pure 2D fullscreen shader → native WebGL2 (zero dependencies)
3D / PBR / GPGPU → keep the original framework (CDN importmap)
Unsure → start with the original framework and re-evaluate in Phase 6
→ details in references/porting-strategy.md
```

### Phase 6: Simplification Evaluation

After porting, verify the result yourself (open the page and compare screenshots). If the result is correct and simplification is possible, **propose the simplification to the user** and let them decide whether to execute it.

### Phase 7: Extraction Report (ask the user whether to generate it)

After extraction, **ask the user** whether to generate `EXTRACTION-REPORT.md` (it costs extra tokens to review the conversation history).

Report structure:
```markdown
# Extraction Report: {project name}
**Source / author / platform / time**

## Target effect (one-sentence description)
## Extraction approach and timeline (each iteration's problem → fix)
## Scene structure (component tree / layer structure)
## Final render pipeline (pass list)
## Key resource files
## Key lessons learned (table: lesson / impact / where it was recorded)
## Remaining known differences
## Tech stack (original vs. ported)
```

The report goes inside the project directory (e.g. `ascii-glyph-dither/EXTRACTION-REPORT.md`).

## Reference Index

| When you need to | Read |
|--------|------|
| Identify the framework (Three.js/WebGL/PixiJS signatures) | `references/tech-signatures.md` |
| Agent extraction prompt + de-obfuscation rules | `references/extraction-workflow.md` |
| Fetch config parameters (API/payload/inline) | `references/config-extraction.md` |
| Rebuild Three.js TSL node shaders | `references/tsl-extraction.md` |
| Decode encoded/encrypted configs | `references/encoded-definitions.md` |
| onBeforeCompile GLSL injection pitfalls | `references/shader-injection.md` |
| Porting framework choice + project structure | `references/porting-strategy.md` |
| **Unicorn Studio** dedicated flow (curtains.js + Firestore) | `references/unicorn-studio.md` |
| **shaders.com** dedicated flow (TSL + XOR encoding + Y-flip trap) | `references/shaders-com.md` |
