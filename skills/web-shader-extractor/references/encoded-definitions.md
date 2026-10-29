# Encoded Config Decoding

## Recognition Signals

1. The API response carries an `_encoded: true` flag
2. The `definition` field is a Base64 string rather than JSON
3. The JS contains `atob()`/`btoa()` + `TextEncoder`/`TextDecoder` + XOR
4. The runtime config contains `obfuscationKey`

```bash
grep -oE '(atob|btoa|obfuscation|_encoded)' /tmp/*.js | sort | uniq -c
grep -oE 'obfuscationKey:"[^"]*"' /tmp/page.html
```

## Common Schemes

### Base64 + XOR

```python
import base64, json

def decode(encoded, key):
    raw = base64.b64decode(encoded)
    key_bytes = key.encode('utf-8')
    decrypted = bytes([raw[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(raw))])
    return json.loads(decrypted.decode('utf-8'))
```

### Short-code mapping (abbreviated component/prop names)

The config uses `C74`/`p29` in place of `StudioBackground`/`color`.

```bash
grep -oE '(codeToComponent|codeToProp)' /tmp/bundle.js
```

The mapping table is usually generated dynamically — all names are sorted alphabetically and assigned `C{nn}`/`p{nn}` numbers.

## Key Sources

| Framework | Location |
|------|------|
| Nuxt.js | `public:{obfuscationKey:"..."}` in the HTML |
| Next.js | `runtimeConfig` inside `__NEXT_DATA__` |
| SPA | bundle constant or `window.__CONFIG__` |

## Finding the Decode Function

```bash
grep -l '_encoded' /tmp/*.js
grep -A3 '_encoded' /tmp/bundle.js
# Pattern: if (t._encoded) { return decode(t.definition, key) }
```
