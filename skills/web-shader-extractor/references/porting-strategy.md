# Porting Strategy

## Framework Choice

```
Pure 2D Canvas (getContext('2d'), no WebGL)?
├─ YES → Vanilla JS (zero dependencies, see § 2D Canvas below)
└─ NO  → pure 2D fullscreen shader / post-processing?
         ├─ YES → native WebGL2 (zero dependencies)
         └─ NO  → involves 3D / PBR / GPGPU / onBeforeCompile?
                  ├─ YES → keep the original framework (CDN importmap)
                  └─ unsure → start with the original framework, re-evaluate in Phase 6
```

## Native WebGL Project Structure

```
<name>/
├── index.html        # <canvas>
├── js/
│   ├── main.js       # WebGL2 initialization + multi-pass render loop
│   └── shaders/      # .glsl.js (export const fragmentShader)
└── README.md
```

- `canvas.getContext('webgl2')` + `#version 300 es` (`in`/`out`, `texture()`)
- Multi-pass via framebuffer + texture attachment
- Driven by `requestAnimationFrame`

## Three.js Project Structure

```
<name>/
├── index.html        # importmap CDN
├── js/
│   ├── main.js       # scene/camera/renderer + RTT pipeline
│   └── shaders/      # .glsl.js
└── README.md
```

- `RawShaderMaterial` + `glslVersion: THREE.GLSL3`
- `WebGLRenderTarget` for multi-pass
- CDN importmap, zero installation

CDN template:
```html
<script type="importmap">
{ "imports": { "three": "https://cdn.jsdelivr.net/npm/three@0.183.0/build/three.module.js" } }
</script>
```

Verify: `curl -sI '<url>' | head -3`

## Porting Notes for Multi-Layer Composite Scenes

Scenes extracted from no-code tools like Unicorn Studio / curtains.js usually have complex FBO chains. Below are the common pitfalls and the correct approach:

### 1. Understanding the parentLayer / effects parent-child relationship

In Unicorn Studio:
- The `effects[]` array of an **Element layer** (shape/text/image) stores the UUIDs of its child effects
- An **Effect layer's** `parentLayer` field points at the parent element's UUID
- Child effects render in `effects` array order, each pass reading the previous pass's FBO

When porting, you must reproduce this chained FBO structure; do not naively merge everything into one pass.

### 2. Transparent background with showBg=0

`showBg=0` means the shader outputs `vec4(0)` (fully transparent) where geometry is not hit.
This is not "black" — it is **transparent**; during compositing the layer underneath shows through.

```glsl
// Correct: showBg=0 → transparent
if (hit < 0.5) { fragColor = vec4(0.0); return; }

// Wrong: outputting black (would cover the layer below)
if (hit < 0.5) { fragColor = vec4(0.0, 0.0, 0.0, 1.0); return; }
```

When porting, you must use an alpha composite pass (`fg + bg * (1 - fg.a)`) to layer the result over the layer beneath.

### 3. How text/image elements are composited

Element layers (text/image) need to be rendered with Canvas 2D and uploaded to WebGL as textures.
**The compositing method determines the visual result**:

```glsl
// Wrong: alpha-over overlay (loses the background texture)
fragColor = mix(bg, vec4(txt.rgb, 1.0), txt.a);

// Wrong: additive (saturates to white, loses color variation)
fragColor = vec4(bg.rgb + txt.rgb * txt.a, 1.0);

// Correct: brightness amplification (preserves the background noise's color-texture variation)
fragColor = vec4(bg.rgb * mix(1.0, amplifyFactor, txt.a), 1.0);
```

**Why**: in the original scene, the text element is layered over a noise field; after the glyph dither pass,
each character's color comes from the pixel color at its position. If the text region is flat monochrome,
the ASCII characters are monochrome too. With brightness amplification, the noise's hue proportions are
fully preserved (purple:cyan:dark all scaled by the same factor), so the dithered characters carry the
noise texture's color variation.

### 4. Repeated effect instances

The same effect (e.g. noiseFill) can appear multiple times in a scene: once as an independent background layer
and once as a child effect of a shape group. The parameters may be identical but the pipeline position differs;
the child effect's output gets processed by later effects (e.g. SDF refraction), producing different visuals.

### 5. Glyph Atlas Compatibility

A base64-embedded PNG glyph atlas can throw `INVALID_VALUE: bad image data` from `texImage2D` in some
browser/WebGL environments. Generating it dynamically with Canvas 2D is recommended.

### 6. Color Space Consistency (the most common source of visual drift)

Three.js / shaders.com and similar tools work in **linear space** throughout. When porting to native WebGL:

```
Wrong (independent gamma per pass):
  Pass1: output pow(linear, 1/2.2)    ← sRGB
  Pass2: reads sRGB + computes highlights (linear) + outputs pow(result, 1/2.2)  ← chaos!

Correct (linear throughout, one final gamma):
  Pass1~N: all outputs linear
  Final:   pow(linear, 1/2.2)        ← the single sRGB encoding
```

hex color definition → `pow(srgb, 2.2)` to linear → compute in linear throughout → final `pow(linear, 1/2.2)` output.

### 7. Exact Parameter Alignment Principle

**Manually tweaking parameters to "compensate" for visual differences is absolutely forbidden.** All formula multipliers must match the original code exactly.
If the effect looks wrong, debug the root cause — color space, noise implementation, time base — instead of changing multipliers.
Manual tweaking may look better under the current config but will break under other parameter combinations.

## 2D Canvas

One file per effect, exporting `create<Name>Effect(container)` → `{ destroy }`. Multiple effects are managed by a `main.js` that handles switching.

### Performance Requirements

- `IntersectionObserver` + `visibilitychange` — stop the RAF when invisible
- DPR cap at `Math.min(devicePixelRatio, 2)`
- Cache post-processing in offscreen canvases; rebuild static content only on resize
- Use `Float32Array` for large particle datasets

## General Standards

- ES Modules (`import`/`export`)
- Replace minified variable names with meaningful ones
- README includes effect description, technical principles, and tunable parameters

## Phase 6: Simplification Evaluation

**Trigger**: after porting, verify the result is correct yourself. **Propose, don't auto-execute** — this is the only step in the whole flow that requires a user decision.

```
Only RawShaderMaterial + WebGLRenderTarget + fullscreen quad used?
├─ → can be simplified to native WebGL2 (saves ~600KB)
PBR / onBeforeCompile / 3D scene involved?
├─ → do not simplify
Unsure?
└─ → do not propose
```
