---
name: image-search
version: 1.0.0
description: |
  Pluggable web image search for agents. Retrieve real images from the web for
  any text query against an env-configurable metasearch backend (SearXNG JSON
  API convention, DuckDuckGo-style), with optional short captions, and get back
  direct image URLs ready to embed. Designed for the DiveeOI agent
  (OpenCode-based). Use when the user wants to find, fetch, illustrate, or
  embed images — e.g. "search for images of X", "find a picture of Y",
  "I need cover art for Z", "give me reference photos of W", "find an
  illustration", "get me a picture".
license: MIT
---

# image-search (pluggable, self-hostable)

Searches public web images for a natural-language query using a
**pluggable search backend** and (optionally) attaches a short caption. This
skills collection ships no proprietary search service — you point the skill at
any self-hostable or public search endpoint of your choice.

## Pluggable backends (env-configured)

| Variable | Default | Description |
|----------|---------|-------------|
| `SEARCH_BASE_URL` | `http://localhost:8080` | Base URL of a metasearch server. The default convention is the **SearXNG JSON API** (`GET {SEARCH_BASE_URL}/search?q=...&format=json`), the most common self-hosted search convention. |
| `SEARCH_API_KEY` | (empty) | Optional API key sent as `Authorization: Bearer <key>` for gateways that require one |
| `SEARCH_REGION` | `us` | Region/localization code passed to the backend (`gl`/`region` param, e.g. `us`, `cn`, `jp`, `de`) |
| `SEARCH_CAPTIONS` | `on` | `on`/`off` — captioning is performed by a vision LLM via `LLM_BASE_URL`/`LLM_MODEL` when the backend has no native captions |

Any backend that returns `{"results": [{"url": ..., "img_src": ..., "title": ...}, ...]}` (SearXNG shape) works out of the box. DuckDuckGo-style HTML endpoints can be adapted with a thin proxy; keep the output shape below.

## When to activate

Trigger this skill when the user wants to:

- Find images for an article, slide deck, PPT, blog post, or report.
- Get reference photos / inspiration for a topic.
- Embed pictures into generated documents with stable URLs.
- Caption a set of images in English or another language.

Do **not** use this skill for:

- Generating new images from scratch — use the `image-generation` skill.
- Reverse image search ("what is this image of?").
- Searching images inside a private corpus — this hits public web sources.

## Prerequisites

- A reachable image-capable search backend (a self-hosted **SearXNG** instance
  with `format=json` enabled is the recommended default; any SearXNG public
  instance or compatible aggregator also works)
- Optional: an OpenAI-compatible LLM endpoint (`LLM_BASE_URL`, `LLM_API_KEY`,
  `LLM_MODEL`) when you want local captions generated for the results

```bash
# Example: run your own backend with docker
docker run -d -p 8080:8080 searxng/searxng
# then: export SEARCH_BASE_URL=http://localhost:8080
```

## Invocation

```bash
curl -s "${SEARCH_BASE_URL}/search?q=<url-encoded query>&format=json&categories=images&region=${SEARCH_REGION}" \
  ${SEARCH_API_KEY:+-H "Authorization: Bearer $SEARCH_API_KEY"}
```

The call prints the JSON response to stdout, or you can write it to a file with
`-o <path>` / shell redirection. Wrap the raw backend response in the
normalized output shape below (a small helper script or jq one-liner is
enough — keep the same shape so downstream prompts stay stable).

### Parameters

| Parameter            | Default | Notes |
|----------------------|---------|-------|
| `q` (query)          | —       | Required. Natural-language sentence describing what should be in the image. Prefer one coherent concept; avoid mixing unrelated keywords. |
| `count`              | 5       | Number of images to return. Range 1–20 (slice the backend results). |
| `region`             | `us`    | Region code for localization. Common: `us`, `cn`, `jp`, `de`. Mapped to the backend's region/`gl` parameter. |
| `captions`           | `on`    | Disable for a faster, caption-less response (mapped to `SEARCH_CAPTIONS`). |
| `output`             | —       | Optional: write the full JSON response to this path. |

### Examples

```bash
# Default search (5 images, us region, captions on).
search_images "a cute orange tabby kitten playing with yarn" --count 5

# US region, no captioning (faster).
search_images "vintage red sports car on a mountain road" --count 5 --region us --captions off

# Non-English query — captions come back in the query language.
search_images "traditional Chinese ink landscape painting" --count 5 -o results.json
```

## Choosing parameters

- **`q` (query)**: use a descriptive sentence, not a keyword list. The backend
  is tuned for natural language and returns more on-topic results that way.
  Match the language to the audience: queries in a language tend to produce
  results and captions in that language.
- **`count`**: default to `5` for most asset-gathering tasks. Drop to
  `1`–`3` when the user only needs one finalist; raise toward `10`–`20`
  when building a moodboard or browsing options. Stay within `1`–`20`.
- **`captions: off`**: turn captions off for moodboards or when latency matters;
  leave them on when the user will pick images by reading the captions.
- **One concept per call**: for two unrelated subjects, fire two separate
  invocations rather than concatenating keywords.

## Response shape

```json
{
  "success": true,
  "query": "cute orange tabby kitten",
  "count": 5,
  "ranked": true,
  "results": [
    {
      "original_url": "https://example.com/images/<hash>.png",
      "caption": "A cute orange tabby kitten playing with yarn on a rug.",
      "source": "Unsplash",
      "original_width": "750px",
      "original_height": "500px"
    }
  ]
}
```

Failure response (HTTP may still be 200; check `success`):

```json
{
  "success": false,
  "query": "...",
  "count": 0,
  "ranked": true,
  "results": [],
  "error": "<human-readable reason>"
}
```

### Field reference

| Field                       | Type    | Notes |
|-----------------------------|---------|-------|
| `success`                   | boolean | Always check this before reading `results`. |
| `query`                     | string  | Echo of the input query. |
| `count`                     | integer | Number of images actually returned. |
| `ranked`                    | boolean | Whether captioning was applied. |
| `results[].original_url`    | string  | Direct image URL from the source. Use it directly for embedding; if you need guaranteed uptime, mirror the file to your own storage first. |
| `results[].caption`         | string  | Short caption. Present only when `ranked` is `true`. |
| `results[].source`          | string  | Original source site (e.g. `Unsplash`, `Pinterest`). |
| `results[].original_width`  | string  | Image width as `"NNNpx"`. |
| `results[].original_height` | string  | Image height as `"NNNpx"`. |
| `error`                     | string  | Present only on failure. |

## Operating tips

1. **Prefer the direct `original_url`, and verify it loads.** Source pages may
   be paywalled, geo-blocked, or deleted; the image URL is more stable, but for
   long-lived documents consider downloading and re-hosting the file yourself.
2. **Skip captioning for speed.** Turning captions off typically cuts response
   time by more than half. Use it when you'll caption results yourself.
3. **Be patient with timeouts.** A full call can take a while when captioning
   (image reachability probes + optional LLM captioning). Use a client-side
   timeout of at least 120 seconds.
4. **Region matters.** `region=cn` biases toward Chinese-language sources;
   `region=us` toward English. Pick the one that matches the user's audience.

## Error handling

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| Connection refused to `SEARCH_BASE_URL` | Backend not running | Start your SearXNG instance or fix `SEARCH_BASE_URL`. |
| `format=json` disabled (403) | SearXNG instance disallows the JSON API | Enable `formats: [html, json]` in the instance `settings.yml`. |
| `API request failed with status 401` / `403` | Auth issue at the gateway | Check `SEARCH_API_KEY`; credentials are managed outside this skill. |
| `API request failed with status 502` | Upstream service unreachable | Retry; if it persists the backend or its upstream engines are down. |
| Empty `results` but `success: true` | Query too narrow or backend filtered everything | Broaden the query, raise `count`, or change `region`. |
