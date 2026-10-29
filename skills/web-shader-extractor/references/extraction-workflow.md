# Shader Code Extraction: Agent Prompt & De-obfuscation

## Agent Deep-Extraction Prompt Template

Launch an agent (subagent_type: general-purpose) to analyze the bundle:

```
Analyze the file /tmp/main.js (a minified JS bundle of roughly X MB) and extract all visual-effect-related code.

What to extract:

1. **GLSL shader source**: search for strings containing "precision", "uniform", "void main",
   "gl_FragColor", "gl_Position". Extract the complete vertex/fragment shaders.

2. **Rendering-related JS classes**: canvas/renderer creation, particle/geometry management,
   the requestAnimationFrame animation loop, and mouse interaction code.

3. **Symbol mapping table**: minified variable names → original meanings
   (THREE.Vector2, THREE.Color, THREE.Scene, etc.)

4. **Configs and parameters**: tunable parameters like default colors, sizes, density

Save all extracted code to /tmp/extracted-effects.txt, segmented and labeled by function.
```

**Key point**: the agent can see the whole file; a 1MB+ bundle does not fit in the main context.

## Identifying Minified Symbols

Infer from constructor arguments and method calls:

```javascript
new ??(40, w/h, 0.1, 1000)       → PerspectiveCamera(fov, aspect, near, far)
new ??(-1, 1, 1, -1, 0, 1)      → OrthographicCamera
new ??({canvas, antialias, ...}) → WebGLRenderer
new ??(2, 2)                     → PlaneGeometry(w, h)
new ??(data, w, h, fmt, type)    → DataTexture
new ??(w, h, {minFilter, ...})   → WebGLRenderTarget

??.setRenderTarget()  → renderer
??.getElapsedTime()   → clock
??.setAttribute()     → bufferGeometry
```

## Framework Unwrapping (React / Vue etc. → Vanilla JS)

Canvas effects are often wrapped by frameworks like React/Vue. Unwrapping approach:

1. **Find the side-effect entry**: the Canvas initialization code inside `useEffect`/`onMounted` is the core logic
2. **Collect the cleanup**: aggregate all teardown operations (`removeEventListener`, `cancelAnimationFrame`, `observer.disconnect()`) into a `destroy()` function
3. **Drop the reactive wrappers**: Canvas state (particle positions, frame counters, etc.) is only read/written inside the RAF loop; plain `let` variables work — no `useState`/`ref` reactive containers needed

Native APIs (`IntersectionObserver`, `ResizeObserver`, `matchMedia`, etc.) are framework-agnostic and stay as-is.

## De-obfuscation Rules

1. **Class names**: infer from constructor arguments and method calls
2. **Variable names**: name by purpose (`ringPos`, `particleScale`, `simMaterial`)
3. **Shader variables**: uniform/varying names are usually not minified (`uTime`, `vPosition`)
4. **Keep the original GLSL**: shader code is usually a complete string; extract it directly
5. **String injection**: `${someVar.noise}` means a noise library was injected into the shader
