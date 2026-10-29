---
name: "multi-search-engine"
description: "Multi search engine integration with 8 domestic (CN) search engines plus pluggable international backends. Supports advanced search operators, time filters, site search, and WeChat article search. No API keys required."
---

# Multi Search Engine v2.0.1

Integration of 8 domestic Chinese search engines for web crawling without API keys, plus a documented pluggable pattern for adding any international/self-hosted backend.

This skill uses direct URL fetching (no proprietary SDK). Any agent tool that fetches a URL (e.g. `web_fetch`) can drive it.

## Search Engines (Domestic - CN Only)

- **Baidu**: `https://www.baidu.com/s?wd={keyword}`
- **Bing CN**: `https://cn.bing.com/search?q={keyword}&ensearch=0`
- **Bing INT**: `https://cn.bing.com/search?q={keyword}&ensearch=1`
- **360**: `https://www.so.com/s?q={keyword}`
- **Sogou**: `https://sogou.com/web?query={keyword}`
- **WeChat**: `https://wx.sogou.com/weixin?type=2&query={keyword}`
- **Toutiao**: `https://so.toutiao.com/search?keyword={keyword}`
- **Jisilu**: `https://www.jisilu.cn/explore/?keyword={keyword}`

## Quick Examples

```javascript
// Basic search (Baidu)
web_fetch({"url": "https://www.baidu.com/s?wd=python+tutorial"})

// Site-specific (Bing CN)
web_fetch({"url": "https://cn.bing.com/search?q=site:github.com+react&ensearch=0"})

// File type (Baidu)
web_fetch({"url": "https://www.baidu.com/s?wd=machine+learning+filetype:pdf"})

// WeChat article search
web_fetch({"url": "https://wx.sogou.com/weixin?type=2&query=AI+latest+developments"})

// Toutiao search
web_fetch({"url": "https://so.toutiao.com/search?keyword=renewable+energy+policy"})

// Jisilu financial data
web_fetch({"url": "https://www.jisilu.cn/explore/?keyword=REITs"})
```

## Pluggable International Backends

Beyond the built-in CN engines, any search backend can be plugged in via
environment configuration while keeping the same calling pattern:

- **SearXNG (self-hosted, recommended)**: set `SEARCH_BASE_URL` to your
  instance and query its JSON API —
  `GET {SEARCH_BASE_URL}/search?q={keyword}&format=json`
  (returns `{"results": [{title, url, content}, ...]}`).
- **DuckDuckGo-style**: `https://duckduckgo.com/html/?q={keyword}` (HTML
  results; parse or use a proxy).
- **Google/Bing/Brave etc.**: use the URL patterns documented in
  `references/international-search.md`.
- Optional auth: pass `SEARCH_API_KEY` as a Bearer token when the backend
  requires one.

The output shape across backends is normalized to
`{results: [{name, url, snippet}, ...]}` so downstream prompts stay stable.

## Advanced Operators

| Operator | Example | Description |
|----------|---------|-------------|
| `site:` | `site:github.com python` | Search within site |
| `filetype:` | `filetype:pdf report` | Specific file type |
| `""` | `"machine learning"` | Exact match |
| `-` | `python -snake` | Exclude term |
| `OR` | `cat OR dog` | Either term |

## Time Filters

| Parameter | Description |
|-----------|-------------|
| `tbs=qdr:h` | Past hour |
| `tbs=qdr:d` | Past day |
| `tbs=qdr:w` | Past week |
| `tbs=qdr:m` | Past month |
| `tbs=qdr:y` | Past year |

## Search Engine Notes

- **WeChat Search**: Best for searching WeChat public articles and content
- **Toutiao**: Good for trending topics and news aggregation
- **Jisilu**: Focused on financial and investment data
- **Bing INT**: International search results via Bing interface
- **Bing CN**: Localized Chinese search results

## Documentation

- `references/international-search.md` - Archived international search guide (for reference)
- `CHANGELOG.md` - Version history

## License

MIT
