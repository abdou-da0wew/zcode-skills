# Unicorn Studio Extraction Workflow

Unicorn Studio (unicorn.studio) is a no-code WebGL design tool that uses curtains.js as its rendering engine and Firebase/Firestore as its backend.

## Recognition Signatures

- URL patterns: `unicorn.studio/remix/{remixId}` or `unicorn.studio/edit/{designId}`
- Meta tag: `<meta name="ai:technical-stack" content="Vue 3, curtains.js, Firebase, JavaScript SDK">`
- Embedded SDK: `unicornStudio-*.js` (~84KB embed version)
- Main app bundle: `index-*.js` (~2.1MB, contains the shader templates)

## Data Fetching Paths

### Path 1: Firestore REST API (recommended; works for remixes)

```bash
# Firebase config (extracted from the unicorn.studio frontend JS bundle, fetched fresh on every extraction)
# How to get it: curl -s https://www.unicorn.studio/ | grep -oP 'apiKey:"[^"]+"' | head -1
API_KEY="<extracted dynamically from the site bundle>"
PROJECT="unicorn-studio"

# Step 1: fetch the remix metadata (versionId, designId, creator info)
curl -s "https://firestore.googleapis.com/v1/projects/$PROJECT/databases/(default)/documents/remixes/{REMIX_ID}?key=$API_KEY"

# Step 2: fetch the version data (all layer definitions, parameters, texture references)
# versionId comes from Step 1's fields.versionId.stringValue
curl -s "https://firestore.googleapis.com/v1/projects/$PROJECT/databases/(default)/documents/versions/{VERSION_ID}?key=$API_KEY"
```

### Path 2: GCS/CDN Embed Data (for published embeds)

```bash
# Non-Pro users
curl -s "https://storage.googleapis.com/unicornstudio-production/embeds/{DESIGN_ID}"

# Pro users
curl -s "https://assets.unicorn.studio/embeds/{DESIGN_ID}"
```

Embed JSON format: `{ options: {...}, layers/history: [...], modules: [...] }`
Includes `compiledFragmentShaders[]` and `compiledVertexShaders[]` (compiled GLSL).

### Path 3: Extract from inline page JSON

Unicorn Studio embeds use the `data-us-project` or `data-us-project-src` HTML attributes;
the SDK's `init()` scans for these attributes and loads the corresponding projects.

## Identify the Data Shape First

Unicorn Studio has at least two common data shapes:

### 1. embed/export scene

- Usually the final scene JSON handed to `addScene()`
- Often already carries `compiledFragmentShaders[]` / `compiledVertexShaders[]`
- This format can be fed directly to the embed runtime

### 2. editor/version history

- Usually comes from the `history` of Firestore `versions/{id}`
- This is the editor's raw layer data and **cannot** be fed to `addScene()` directly

If you mistakenly treat `history` as an embed scene, typical symptoms are:

- `Plane: No fragment shader provided, will use a default one`
- `Plane: No vertex shader provided, will use a default one`
- `No composite shader data for element`
- The canvas is created, but the picture is all black or only the default layer remains

## Firestore Collection Structure

| Collection | Purpose | Key fields |
|---|---|---|
| `designs` | design metadata | creatorId, name, versionId, hasEmbed |
| `versions` | version data (core) | history[], options |
| `remixes` | remixable designs | designId, versionId, creatorId, thumbnail |

## Version Data Structure

Firestore REST responses wrap values as `{stringValue, integerValue, arrayValue, mapValue, ...}`, which need recursive parsing.

Each element of the `history` array is a layer:

```
layerType: "effect" | "text" | "image" | "model" | "shape"
type:      effect type (gradient, noiseFill, sdf_shape, glyphDither, bloomFast, ...)
```

### Layer parameters (common)

- `pos`, `scale`, `speed`, `opacity`, `blendMode`
- `trackMouse`, `trackAxes`, `mouseMomentum`
- `parentLayer`: UUID or false (links to the parent element)
- `breakpoints[]`: responsive breakpoint configuration
- `states`: appear/scroll/hover/mousemove animations
- `customFragmentShaders[]`, `customVertexShaders[]` (usually empty when using built-in effects)

## Correct Initialization Strategy

If what you have is the Firestore `version/history`, prefer imitating the site's own initialization chain; do not force-fit the embed API.

Typical call order:

1. `unpackageHistory()` or `unpackVersion()`
2. `createFontScript()`
3. `createCurtains()`
4. `handleItemPlanes()`
5. `fullRedraw()`

If the page bundle has a dedicated Remix/Preview component, follow it; don't rely only on the public UMD/SDK docs.

### Localizing assets

- Download image/font/texture assets locally where possible
- Rewrite `src` and `fontCSS.src` in `history` to local paths
- Some object fields may be maps with numeric keys; normalize them into arrays before persisting

### Effect-specific parameters

| Effect | Key parameters |
|---|---|
| gradient | fill[], stops[], gradientType, gradientAngle, wrap |
| noiseFill | noiseType, turbulence, color1, color2, colorPhase, chroma, direction |
| sdf_shape | shape(0-22), refraction, extrude, smoothing, axis, animationDirection, lightPosition |
| glyphDither | characters, glyphSet, scale, gamma, monochrome, texture (sprite atlas) |
| bloomFast | amount, intensity, exposure, tint |

## Shader Code Extraction

**Key finding**: the Embed SDK (~84KB) contains no GLSL shader code. The shader templates live in the main app bundle (~2.1MB) and are stored into the embed JSON after a 7-step compilation pipeline.

### Where shaders live in the app bundle

Shader templates are string literals identified by variable names:

```
Effect name        → variable name
glyphDither     → X$ (fragment)
noiseFill       → WY (fragment)
sdf_shape       → XY (fragment)
gradient        → eX (fragment)
bloomFast       → Hj (fragment)
Generic vertex   → ye (vertex)
Gradient vertex  → ko (vertex)
Composite fragment → Uz (composite fragment)
Composite vertex   → Nz (composite vertex)
```

Note: variable names change between builds; locate them by searching for key signatures.

### Template variables

Shader templates contain `${variable}` placeholders, replaced at compile time:

| Variable | Content |
|---|---|
| `${fe}` | mask-related uniform declarations |
| `${Vt}` | layer blending helpers (applyLayerMix, applyLayerMixAlpha, applyLayerMixClip) |
| `${gt}` | PCG hash / random functions (pcg2d, randFibo) |
| `${ht}` | blend mode functions (17 modes: Normal, Add, Multiply, Screen, Overlay, ...) |
| `${pe("var")}` | mask application + fragColor output |
| `${wf}` | BCC noise derivatives (OpenSimplex2S) |
| `${Aa}` | Perlin noise function |
| `${yr}` | deband dithering function |
| `${cm}` | gradient color/stop uniform declarations |
| `${xz}` | Gaussian weight function (bloom blur) |

### Compilation pipeline

```
1. Fz(): replace uniform values with constants
2. Dz(): handle gradient color counts (switch-case trimming)
3. Mz(): evaluate constant switches (dead-code elimination)
4. Rz(): process #ifelseopen/#ifelseclose blocks (conditional compilation)
5. Iz(): remove unused functions
6. Cz(): remove unused uniform declarations
7. Bp(): strip comments, normalize whitespace
```

## Render Pipeline (core; must be reproduced correctly when porting)

```
curtains.js WebGL2 renderer
├─ Each effect layer = one Plane + an independent FBO
├─ Layers render in a linear chain by renderOrder; each plane reads the previous FBO as uTexture
├─ An Element (shape/text/image) + child effects form a render group:
│   1. The Element's own plane renders first → FBO_elem
│   2. Child effects render in effects array order → FBO_child1, FBO_child2, ...
│   3. The composite plane renders last: alpha-blends the child effect output onto the background scene
├─ Standalone post-processing effects (parentLayer=false) process the global scene
└─ The last plane outputs directly to the canvas (no FBO)
```

### The Element + child-effect FBO chain (critical)

```
Take a shape group (sdf + noise) as an example:

FBO_before ─────────────────────────────────────────┐
                                                     │
Shape's own plane → FBO_shape (renders the base geometry) │
    ↓                                                 │
Child noiseFill → FBO_noise (uBgTexture = FBO_shape)  │
    ↓                                                 │
Child sdf_shape → FBO_sdf (uTexture = FBO_noise)      │
    ↓ (showBg=0: outside the shape = vec4(0) transparent) │
    ↓                                                 │
Composite plane → FBO_result                          │
    uTexture = FBO_sdf (last child effect output)       │
    uBgTexture = FBO_before (scene before the element) ←───┘
    output = alpha_blend(fg, bg) = fg + bg * (1 - fg.a)
```

### Child-effect linkage mechanism

```js
// The Element's effects array → list of child-effect parentLayer UUIDs
shape.effects = ["e270a7cd-...", "fb591190-..."]

// Each child effect references its parent element's UUID
noiseFill.parentLayer = "e270a7cd-..."   // effects[0]
sdf_shape.parentLayer = "fb591190-..."   // effects[1]

// Finding child effects in the embed SDK:
getChildEffectItems() {
    return this.effects.map(uuid =>
        state.layers.find(l => l.parentLayer === uuid)
    ).filter(Boolean)
}
```

### uTime time base (critical trap)

In the Embed SDK, `uTime` is **not seconds** — it accumulates per frame:
```js
// inside setEffectPlaneUniforms():
t.uniforms.time.value += speed * 60 / this.fps;
```

At 60fps: `uTime += speed` every frame. After 1 second, `uTime = speed × 60`.

| Effect layer | speed | uTime after 1 second |
|--------|-------|-------------|
| noiseFill | 0.25 | 15 |
| sdf_shape | 0.5 | 30 |
| gradient | 0.25 | 15 |

**When porting you must multiply by `speed × 60`**, otherwise the animation runs 15-60x too slow:
```js
// Correct:
uni1f(prog, 'uTime', elapsedSeconds * speed * 60);
// Wrong:
uni1f(prog, 'uTime', elapsedSeconds);
```

### The critical role of the showBg parameter

- `showBg=0`: when a ray misses the geometry, output `vec4(0)` — **transparent** (not black!)
- `showBg=1`: when a ray misses, sample `uTexture/uBgTexture` (show the background content)

**showBg=0 is the most common porting trap**: if you wrongly output opaque black `vec4(0,0,0,1)`,
the composite alpha blend will paint over the layers below instead of showing through. Make sure alpha=0.

## Porting Strategy

1. **Pure 2D post-processing effects** (glyphDither, bloomFast): native WebGL2 fullscreen quad
2. **Generative effects** (noiseFill, gradient): native WebGL2
3. **3D SDF** (sdf_shape): native WebGL2 raymarching
4. **Complex scenes** (multi-layer composites): requires a multi-pass FBO pipeline
5. **Text layers**: render the text with Canvas 2D → upload to WebGL as a texture

## Playwright Verification

Playwright's default headless environment may have no usable WebGL. When you see the symptoms below, suspect the environment first — not your extraction logic:

- `Renderer: WebGL context could not be created`
- `0 canvas(es) found`
- `Error creating Curtains instance`
- Pure black screenshots

In that case, switch to `swiftshader` and verify again:

```bash
--use-angle=swiftshader
--use-gl=angle
--enable-unsafe-swiftshader
--ignore-gpu-blocklist
```

Suggested verification order:

1. Check whether the console shows shader/runtime errors or a WebGL context creation failure
2. Check whether a `canvas` was actually generated in the DOM
3. Take a screenshot with `swiftshader`
4. Compare composition against the original site's thumbnail or above-the-fold screenshot

### Glyph Atlas Generation

The original glyph atlas is a base64 PNG (with cross-browser compatibility issues).
Generating it dynamically with Canvas 2D is recommended:

```js
function createGlyphAtlas(chars, size = 40) {
  const canvas = document.createElement('canvas');
  canvas.width = size * chars.length;
  canvas.height = size;
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = '#000';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = '#fff';
  ctx.font = `bold ${size * 0.8}px monospace`;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  for (let i = 0; i < chars.length; i++) {
    ctx.fillText(chars[i], size * i + size / 2, size / 2);
  }
  return canvas; // → gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, canvas)
}
```

## Cloud Functions Endpoints

All located at `https://us-central1-unicorn-studio.cloudfunctions.net/`:
- `publishEmbedTest` — publish/update an embed (auth required)
- `getUserIdByUsername` — username→userId
- `handleVideos/handleModels/handleImages` — asset processing
- `generateImprovedMSDF` — MSDF text rendering
- `generateDepthMap` — depth map generation
- `copyRemixAssets` — remix asset copying

## Example: Complete Extraction Flow

```bash
# 1. Extract the remix ID from the URL
REMIX_ID="QZxhNFb1X1OaUqaJLT9S"

# 2. Fetch the remix metadata
curl -s "https://firestore.googleapis.com/v1/projects/unicorn-studio/databases/(default)/documents/remixes/$REMIX_ID?key=$API_KEY" > remix.json

# 3. Extract the versionId
VERSION_ID=$(python3 -c "import json; print(json.load(open('remix.json'))['fields']['versionId']['stringValue'])")

# 4. Fetch the version data
curl -s "https://firestore.googleapis.com/v1/projects/unicorn-studio/databases/(default)/documents/versions/$VERSION_ID?key=$API_KEY" > version.json

# 5. Parse the layers and parameters in the version data → recursively parse the Firestore REST format with Python/Node

# 6. Extract the shader templates for the relevant effect types from the app bundle
curl -s "https://www.unicorn.studio/assets/index-*.js" > app-bundle.js
# Search for the effect type names to locate the shader code

# 7. Combine parameters + shader templates → build the standalone WebGL2 project
```
