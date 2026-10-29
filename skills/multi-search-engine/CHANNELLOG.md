# Multi Search Engine

## Basic Information

- **Name**: multi-search-engine
- **Version**: v2.0.1
- **Description**: Integrates 17 search engines (8 domestic CN + 9 international), supports advanced search syntax
- **Release date**: 2026-02-06

## Search Engines

**Domestic (8)**: Baidu, Bing, 360, Sogou, WeChat, Toutiao, Jisilu
**International (9)**: Google, DuckDuckGo, Yahoo, Brave, Startpage, Ecosia, Qwant, WolframAlpha

## Core Features

- Advanced search operators (site:, filetype:, intitle:, etc.)
- DuckDuckGo Bangs shortcuts
- Time filters (hour/day/week/month/year)
- Privacy-preserving search
- WolframAlpha knowledge computation

## Update History

### v2.0.1 (2026-02-06)
- Streamlined documentation, optimized for release

### v2.0.0 (2026-02-06)
- Added 9 international search engines
- Strengthened deep search capabilities

### v1.0.0 (2026-02-04)
- Initial version: 8 domestic search engines

## Usage Examples

```javascript
// Google search
web_fetch({"url": "https://www.google.com/search?q=python"})

// Privacy search
web_fetch({"url": "https://duckduckgo.com/html/?q=privacy"})

// Site-restricted search
web_fetch({"url": "https://www.google.com/search?q=site:github.com+python"})
```

MIT License
