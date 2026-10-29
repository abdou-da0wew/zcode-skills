# shaders.com Extraction Workflow

shaders.com is a shader design tool built on Nuxt.js + Three.js r183 TSL + Supabase.

## Recognition Signatures

- URL: `shaders.com/collection/{slug}/{presetId}` or `shaders.com/preset/{id}`
- Canvas: `data-renderer="shaders"` + `data-engine="three.js r183"`
- Nuxt.js (`_nuxt/` paths)
- Clerk authentication
- Supabase storage (`data.shaders.com/storage/v1/`)

## Key Architectural Differences

Completely different from Unicorn Studio:
- **No GLSL** — uses the Three.js TSL (Three Shading Language) node system
- **87 component types** — each with its own TSL `fragmentNode` function
- **Definition data is XOR + base64 encoded**
- **Components can nest** — tree structure (Glass's children are its inner effects)

## Data Fetching

### API endpoints

```bash
# Collection variant (with encoded definitions) — public, no auth needed
curl -s "https://shaders.com/api/collections/{slug}/{variantId}"

# Preview API (encoded definitions + watermark injection)
curl -s "https://shaders.com/api/preview/preset/{presetId}"

# Nuxt payload (metadata only, no shader definitions)
curl -s "https://shaders.com/collection/{slug}/{id}/_payload.json"
```

### Definition decoding

Definitions are XOR + base64 encoded, with two key sets:

1. **Website API** (`/api/collections/`):
   - Obfuscation key: `a5e7244ad0973f07e10285bfa75ddbe4` (from the Nuxt runtime config)
   - Component/prop names use short codes (`C52`=Plasma, `p06`=angle, etc.)
   - Decode: `JSON.parse(XOR(base64decode(encoded), keyBytes))`
   - Then you need the code→name mapping table to restore readable names

2. **Preview API** (`/api/preview/`):
   - Key: `shaders-preview-key`
   - Uses human-readable prop names (no mapping needed)
   - Note: it injects a watermark `ImageTexture` component

### Code mapping table

The 87 components are numbered `C00-C86` alphabetically; the 233 props are numbered `p00-p232` alphabetically.
The mapping table can be extracted from the JS bundle.

## Known Pitfalls

### Y-axis flip (recurring!)

**SDF textures and UV coordinates are systematically Y-flipped** — confirmed across multiple extractions:

shaders.com's SDF binaries (`.bin`) use an **image coordinate system** (Y=0 at the top),
while WebGL texture coordinates put Y=0 at the bottom. Loading directly flips shapes upside down.

```glsl
// Wrong: sampling the SDF with shapeUV directly
float sdf = texture(tSDF, shapeUV).r;

// Correct: flip Y
vec2 sdfUV = vec2(shapeUV.x, 1.0 - shapeUV.y);
float sdf = texture(tSDF, sdfUV).r;

// Note: the gradient's Y component must be negated too
float dSdy = -(texture(tSDF, sdfUV - vec2(0, eps)).r - sdf) / eps;
```

Likewise, `center.y` in component definitions uses DOM coordinates (Y=0 at the top),
and must be flipped in the Glass shader: `center.y = 1.0 - center.y`.

### SDF binary format

- Format: 512×512 Float32 single channel (1,048,576 bytes = 512² × 4)
- Value range: signed distance, negative = inside, positive = outside (e.g. [-0.065, 0.486])
- **No remapping needed** (don't do `*2-1`); use the raw values
- Requires the `OES_texture_float_linear` extension for linear filtering
- WebGL2 upload: `gl.texImage2D(gl.TEXTURE_2D, 0, gl.R32F, 512, 512, 0, gl.RED, gl.FLOAT, data)`

## Component Type Quick Reference

| Category | Components | Complexity |
|------|------|--------|
| Texture | Plasma, Godrays, SimplexNoise, LinearGradient, RadialGradient | Medium |
| Shape | Glass, Blob, Circle, Ring, Star, RoundedRect, Polygon | High (Glass is the most complex) |
| Distortion | WaveDistortion, ChromaticAberration, Liquify, Twirl, Bulge | Low-medium |
| Stylization | FilmGrain, Halftone, Ascii, Dither, Glow, Bloom | Low-medium |
| Post-processing | Blur, ProgressiveBlur, BrightnessContrast, HueShift | Low |

## Render Pipeline

```
Three.js r183 TSL renderer
├─ Prefers WebGPU, falls back to WebGL
├─ Orthographic camera + a single fullscreen quad
├─ Component tree composites bottom-up
├─ Components with children use RTT (render-to-texture) to capture child content
├─ Blend modes use custom blend functions
└─ The Glass component is the most complex: SDF evaluation → gradient normals → refraction → chromatic aberration → blur → shading → highlights → Fresnel → composite
```

## Porting Strategy

1. **TSL cannot be copied directly** — it must be translated to GLSL
2. **Extract the TSL `fragmentNode` from the JS bundle** → de-obfuscate → translate to GLSL
3. **Component tree → multi-pass FBO pipeline**
4. **SDF textures need a Y-flip** (see pitfalls above)
5. **Glass has many parameters** (20+); every value must be matched exactly

## Color Space Handling (critical)

shaders.com's Three.js renderer works in **linear space** throughout:
- hex colors in component definitions (e.g. `#2c2c42`) are **sRGB** values
- TSL's `color()` function converts sRGB→linear automatically
- All intermediate FBOs store linear values
- The renderer performs the final linear→sRGB output encoding

When porting:
```glsl
// 1. When defining colors: sRGB hex → linear
vec3 colorA = pow(vec3(0.173, 0.173, 0.259), vec3(2.2));  // #2c2c42

// 2. Intermediate passes: compute entirely in linear space; no gamma
// 3. Final output pass (only once): linear → sRGB
fragColor = vec4(pow(color.rgb, vec3(1.0/2.2)), color.a);
```

**Common mistake**: applying gamma correction in intermediate passes, causing later passes to accumulate highlights/Fresnel in the wrong space.

## Exact Parameter Alignment Principle

**Manual parameter tweaking is absolutely forbidden.** Every parameter must strictly match the formulas and multipliers of the TSL translation:

```
TSL original multiplier             → value GLSL must use
aberration * 0.06           → do not change to 0.12
fresnelSoftness * 0.06      → do not change to 0.12
fresnel (0.17)              → do not change to 0.4
SDF gradient eps = 0.01     → do not change to 0.005
```

If the visuals don't match, check:
1. Whether the color space is correct (sRGB/linear confusion is the most common cause)
2. Differences in noise function implementations (Perlin implementations vs `mx_noise_float`)
3. Whether the time base is correct
4. Whether the FBO pipeline order matches the component tree

**Do not** "compensate" for visual differences by changing multipliers — it will break under other parameter configurations.

## TSL Time Conventions

`timerLocal(speed)` = increments by `speed` units per second. When porting: `uTime = seconds * speed`.

The shader then applies its own internal multipliers:

| Component | speed parameter | shader-internal multiplier | actual rate per second |
|------|-----------|----------------|------------|
| Plasma | 2 | × 0.125 | 0.25 |
| Godrays | 0.7 | × 0.2 | 0.14 |
| WaveDistortion | 0.8 | × 0.5 | 0.4 |
| FilmGrain | — | no time (static) | 0 |

## TSL→GLSL Identifier Mapping (SPCVwBqR.js)

Common mappings (they change between builds; extract them dynamically):

| Local name | TSL function | GLSL |
|--------|---------|------|
| C / z | vec4() | vec4 |
| x / D | vec2() | vec2 |
| q / N | vec3() | vec3 |
| P / J | resolution | u_resolution |
| A / $ | uv | vUv |
| se / Oe | sin() | sin() |
| W / I | cos() | cos() |
| ne | mix() | mix() |
| D | smoothstep() | smoothstep() |
| fe | clamp() | clamp() |
| ar | mx_noise_float() | perlinNoise3D() |
| dr / Gt | timerLocal() | u_time × speed |
| Me / wt | rtt() | FBO pass |
| Ce | renderOutput() | fragColor |
