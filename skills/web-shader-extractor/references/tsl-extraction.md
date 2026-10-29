# Three.js TSL Identification & Reconstruction

Three.js r170+'s TSL (Three Shading Language) composes shader node graphs through JS function call chains, compiled to GLSL at runtime.

## Recognition Signals

1. The bundle has many `uniform`/`shader` references but almost no `precision`/`gl_FragColor`
2. The canvas `data-engine` shows r170+
3. Chained calls like `.mul()`/`.add()`/`.toVar()`/`.assign()` exist

## TSL → GLSL Mapping

| TSL | GLSL |
|-----|------|
| `screenUV` | `gl_FragCoord.xy / resolution` |
| `viewportSize` | `uniform vec2 resolution` |
| `float()`/`vec2()`/`vec3()`/`vec4()` | same names (but they are JS functions in TSL) |
| `.mul()`/`.add()`/`.sub()`/`.div()` | `*`/`+`/`-`/`/` |
| `sin()`/`cos()`/`mix()`/`smoothstep()` | same names |
| `clamp()`/`abs()`/`fract()`/`floor()` | same names |
| `pow()`/`exp()`/`sqrt()`/`dot()`/`length()` | same names |
| `Fn()` | shader function wrapper (inlined into GLSL) |
| `uniform()` | `uniform <type> name` |
| `convertToTexture()` | RTT (multi-pass rendering) |
| `.sample(uv)` | `texture(sampler, uv)` |
| `.toVar()`/`.assign()` | declare/assign mutable variables |
| `.oneMinus()` | `1.0 - x` |

## Reconstruction Steps

1. **Locate**: search for the `fragmentNode` property near component names
2. **Mapping table**: infer the minified → TSL function names from the import statements at the top of the bundle
   ```javascript
   import { A as screenUV, W as sin, ... } from "three-module"
   ```
3. **Translate**: chained calls → GLSL expressions
   ```javascript
   // TSL: screenUV.x.sub(center.x).mul(aspect)
   // GLSL: (uv.x - center.x) * aspect
   ```
4. **RTT**: `convertToTexture(childNode)` → render the child into a separate FBO pass and sample it with `texture()` in the main shader
