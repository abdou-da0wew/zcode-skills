# Framework Identification Signatures

## Three.js

**Un-obfuscated**: `THREE.`, `WebGLRenderer`, `ShaderMaterial`, `BufferGeometry`

**Obfuscated** (inferred from constructor arguments):

| Call pattern | Original class |
|---------|--------|
| `new X({canvas, antialias, alpha})` | `WebGLRenderer` |
| `new X(fov, aspect, near, far)` — 4 numbers | `PerspectiveCamera` |
| `new X(-1, 1, 1, -1, 0, 1)` — 6 args | `OrthographicCamera` |
| `new X(w, h, {wrapS, minFilter})` | `WebGLRenderTarget` |
| `new X(data, w, h, format, type)` — Float32Array | `DataTexture` |
| `new X(2, 2)` used as geometry | `PlaneGeometry` |
| `new X({uniforms, vertexShader, fragmentShader})` | `ShaderMaterial` |
| `X.getElapsedTime()` | `Clock` |

**Constants**: `ClampToEdgeWrapping`, `NearestFilter`, `RGBAFormat`, `FloatType`, `DoubleSide`

## 2D Canvas

When `dataEngine: null`, distinguish using the presence of `getContext('2d')` vs `createShader`/`shaderSource`:
- Has `getContext('2d')`, no WebGL calls → pure 2D Canvas
- Has WebGL calls → Raw WebGL / PixiJS

## Raw WebGL

```javascript
gl.createShader / gl.shaderSource / gl.compileShader / gl.createProgram
gl.bindBuffer / gl.bindFramebuffer / gl.drawArrays
```

## PixiJS

`PIXI.Application`, `PIXI.Filter`, `new PIXI.Filter(vertSrc, fragSrc, uniforms)`

## Babylon.js

`BABYLON.Engine`, `BABYLON.ShaderMaterial`, `BABYLON.Effect.ShadersStore`

## GPGPU Pattern

Two `WebGLRenderTarget`s (ping-pong) + `OrthographicCamera(-1,1,1,-1,0,1)` + `PlaneGeometry(2,2)` + `DataTexture` initial positions + a `setRenderTarget` loop

## Common Noise

| Function | Type |
|------|------|
| `snoise` | Simplex noise (Ashima) |
| `cnoise` | Classic Perlin |
| `cellular` | Worley/Voronoi |
| `fbm` | Fractal Brownian Motion |
