# onBeforeCompile GLSL Injection Pitfalls

## Scenario

When using the `transmission` feature of `MeshPhysicalMaterial` but needing to enhance the effect
(e.g. drei's MeshTransmissionMaterial), inject custom GLSL code via `material.onBeforeCompile`.

## Common Pitfalls

### 1. Function signature differences across versions

Different Three.js versions have different built-in function signatures:

```glsl
// r166 and earlier
vec4 getIBLVolumeRefraction(n, v, roughness, diffuseColor, specularColor, specularF90,
  pos, modelMatrix, viewMatrix, projectionMatrix, ior, thickness,
  attenuationColor, attenuationDistance)

// r167+ adds the dispersion parameter
vec4 getIBLVolumeRefraction(n, v, roughness, diffuseColor, specularColor, specularF90,
  pos, modelMatrix, viewMatrix, projectionMatrix, dispersion, ior, thickness,
  attenuationColor, attenuationDistance)
```

**You must check the actual signature in the target version**:
```bash
curl -s "https://cdn.jsdelivr.net/npm/three@0.167.0/src/renderers/shaders/ShaderChunk/transmission_pars_fragment.glsl.js" \
  | tr '\n' ' ' | grep -oE 'vec4 getIBLVolumeRefraction\([^)]+\)'
```

### 2. GLSL does not allow nested function definitions

```glsl
// Wrong! GLSL does not support defining a function inside a function
void main() {
  float myRand(vec2 co) { return fract(sin(...)); }  // compile error
}

// Correct: functions must be at global scope
float myRand(vec2 co) { return fract(sin(...)); }
void main() {
  float r = myRand(uv);
}
```

### 3. Conditional compilation macro guards

Some variables are only available under specific macros:
- `vWorldPosition` → requires `USE_TRANSMISSION` enabled
- `vTransmissionMapUv` → requires `USE_TRANSMISSIONMAP` enabled
- `roughnessFactor` → available only after `lights_physical_fragment`

```glsl
// When replacing #include <transmission_fragment>
// the original code carries #ifdef USE_TRANSMISSION; your replacement must include it too
#ifdef USE_TRANSMISSION
  // ... your code
#endif
```

### 4. Variable name collisions

Injected global functions/variables may collide with Three.js internals:
- Avoid generic names like `hash`, `random`, `noise`
- Prefix custom functions: `snoise` → OK, `random` → possible collision
- Prefix uniform names with `u`: `uDistortion`, `uNoiseTime`

## Recommended Patterns

### Safe injection: modify the normal instead of replacing the whole chunk

```javascript
material.onBeforeCompile = (shader) => {
  shader.uniforms.uDistortion = { value: 0 };
  shader.uniforms.uNoiseTime = { value: 0 };

  // Prepend uniform declarations + helper functions to the fragment shader
  shader.fragmentShader = `
    uniform float uDistortion;
    uniform float uNoiseTime;
    ${noiseGLSL}
  ` + shader.fragmentShader;

  // Insert the normal perturbation before transmission_fragment
  shader.fragmentShader = shader.fragmentShader.replace(
    '#include <transmission_fragment>',
    `
    #ifdef USE_TRANSMISSION
    {
      // Perturb the normal to affect the refraction direction
      if (uDistortion > 0.0) {
        normal = normalize(normal + uDistortion * vec3(
          snoiseFractal(vWorldPosition * 0.08 + vec3(uNoiseTime)),
          snoiseFractal(vWorldPosition.zxy * 0.08 - vec3(uNoiseTime)),
          snoiseFractal(vWorldPosition.yxz * 0.08)
        ));
      }
    }
    #endif
    #include <transmission_fragment>
    `
  );
};
```

### Full replacement: when randomized multi-sampling + chromatic aberration are needed

When you need MeshTransmissionMaterial's film-grain feel (randomly sampled noise) and chromatic aberration,
you must fully replace `#include <transmission_fragment>`. Key points:

1. Keep the `#ifdef USE_TRANSMISSION` / `#endif` wrapper
2. Keep the `#ifdef` blocks for transmissionMap and thicknessMap
3. Use the correct version of the `getIBLVolumeRefraction` signature
4. When handling chromatic aberration yourself, pass `dispersion = 0.0` and sample R/G/B with different IORs
5. Low sample count (6) + per-pixel random offsets → produces a visible film-grain feel

## Effect Source Quick Reference

| Effect | Source | Implementation |
|------|------|----------|
| Glass refraction | MeshPhysicalMaterial `transmission` | Three.js built-in |
| Chromatic aberration | Sampling R/G/B with different IORs | Replace transmission_fragment |
| Film grain | Low sample count + per-pixel random directions | Replace transmission_fragment |
| Organic distortion | Simplex noise perturbing the normal/refraction direction | onBeforeCompile injection |
| Color fringing | `dispersion` property (r167+) | MeshPhysicalMaterial built-in |
