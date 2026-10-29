# Config Parameter Extraction

Config values must be extracted from the source site — never guessed. (Example of guessing wrong: colors off by 60x, completely different patterns.)

## Sources (by priority)

### 1. Public REST API

```bash
# Search for API endpoints in the JS bundle
grep -oE 'api/(presets|shaders|collections)[^"]*' /tmp/*.js
# Call directly
curl -s -L --compressed 'https://example.com/api/collections/slug/uuid'
```

The API response may be encoded → see `encoded-definitions.md`

### 2. Nuxt.js Payload

```bash
grep -oE '_payload\.json[^"]*' /tmp/page.html          # payload URL
grep -oE 'public:\{[^}]*\}' /tmp/page.html             # runtime config (may contain keys)
```

### 3. Next.js

```bash
# App Router (RSC)
grep -oE '"(scene|glass|postProcessing)":\{' /tmp/page.html
# Pages Router
grep -o '<script id="__NEXT_DATA__"[^>]*>[^<]*' /tmp/page.html | sed 's/.*>//'
```

### 4. Inline JSON / window globals

```bash
grep -oE 'window\.__CONFIG__\s*=\s*\{[^;]+' /tmp/page.html
```

### 5. JS Bundle Defaults (last resort)

```bash
grep -oE '(config|options|settings)\s*=\s*\{' /tmp/entry-chunk.js
```

## Validation

- Color range: 0-1 or 0-255?
- resolution: pixel values or a scale factor?
- Booleans: does `false` skip an entire render pass?
