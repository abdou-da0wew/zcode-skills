# International Search Engines Deep Search Guide

## 🔍 Google Deep Search

### 1.1 Basic Advanced Search Operators

| Operator | Function | Example | URL |
|--------|------|------|-----|
| `""` | Exact match | `"machine learning"` | `https://www.google.com/search?q=%22machine+learning%22` |
| `-` | Exclude keyword | `python -snake` | `https://www.google.com/search?q=python+-snake` |
| `OR` | Logical OR | `machine learning OR deep learning` | `https://www.google.com/search?q=machine+learning+OR+deep+learning` |
| `*` | Wildcard | `machine * algorithms` | `https://www.google.com/search?q=machine+*+algorithms` |
| `()` | Grouping | `(apple OR microsoft) phones` | `https://www.google.com/search?q=(apple+OR+microsoft)+phones` |
| `..` | Number range | `laptop $500..$1000` | `https://www.google.com/search?q=laptop+%24500..%241000` |

### 1.2 Site and File Search

| Operator | Function | Example |
|--------|------|------|
| `site:` | Site-restricted search | `site:github.com python projects` |
| `filetype:` | File type | `filetype:pdf annual report` |
| `inurl:` | URL contains | `inurl:login admin` |
| `intitle:` | Title contains | `intitle:"index of" mp3` |
| `intext:` | Body contains | `intext:password filetype:txt` |
| `cache:` | View cache | `cache:example.com` |
| `related:` | Related sites | `related:github.com` |
| `info:` | Site information | `info:example.com` |

### 1.3 Time Filter Parameters

| Parameter | Meaning | URL Example |
|------|------|---------|
| `tbs=qdr:h` | Past hour | `https://www.google.com/search?q=news&tbs=qdr:h` |
| `tbs=qdr:d` | Past 24 hours | `https://www.google.com/search?q=news&tbs=qdr:d` |
| `tbs=qdr:w` | Past week | `https://www.google.com/search?q=news&tbs=qdr:w` |
| `tbs=qdr:m` | Past month | `https://www.google.com/search?q=news&tbs=qdr:m` |
| `tbs=qdr:y` | Past year | `https://www.google.com/search?q=news&tbs=qdr:y` |
| `tbs=cdr:1,cd_min:1/1/2024,cd_max:12/31/2024` | Custom date range | Full year 2024 |

### 1.4 Language and Region Filters

| Parameter | Function | Example |
|------|------|------|
| `hl=en` | Interface language | `https://www.google.com/search?q=test&hl=en` |
| `lr=lang_zh-CN` | Result language | `https://www.google.com/search?q=test&lr=lang_zh-CN` |
| `cr=countryCN` | Country/region | `https://www.google.com/search?q=test&cr=countryCN` |
| `gl=us` | Geolocation | `https://www.google.com/search?q=test&gl=us` |

### 1.5 Special Search Types

| Type | URL | Description |
|------|-----|------|
| Image search | `https://www.google.com/search?q={keyword}&tbm=isch` | `tbm=isch` means images |
| News search | `https://www.google.com/search?q={keyword}&tbm=nws` | `tbm=nws` means news |
| Video search | `https://www.google.com/search?q={keyword}&tbm=vid` | `tbm=vid` means videos |
| Map search | `https://www.google.com/search?q={keyword}&tbm=map` | `tbm=map` means maps |
| Shopping search | `https://www.google.com/search?q={keyword}&tbm=shop` | `tbm=shop` means shopping |
| Book search | `https://www.google.com/search?q={keyword}&tbm=bks` | `tbm=bks` means books |
| Scholar search | `https://scholar.google.com/scholar?q={keyword}` | Google Scholar |

### 1.6 Google Deep Search Examples

```javascript
// 1. Search GitHub for Python machine learning projects
web_fetch({"url": "https://www.google.com/search?q=site:github.com+python+machine+learning"})

// 2. Search for machine learning tutorials in PDF format from 2024
web_fetch({"url": "https://www.google.com/search?q=machine+learning+tutorial+filetype:pdf&tbs=cdr:1,cd_min:1/1/2024"})

// 3. Search for Python pages whose title contains "tutorial"
web_fetch({"url": "https://www.google.com/search?q=intitle:tutorial+python"})

// 4. Search news from the past week
web_fetch({"url": "https://www.google.com/search?q=AI+breakthrough&tbs=qdr:w&tbm=nws"})

// 5. Search for Chinese content (English interface, Chinese results)
web_fetch({"url": "https://www.google.com/search?q=artificial+intelligence&lr=lang_zh-CN&hl=en"})

// 6. Search for laptops in a specific price range
web_fetch({"url": "https://www.google.com/search?q=laptop+%241000..%242000+best+rating"})

// 7. Search while excluding Wikipedia
web_fetch({"url": "https://www.google.com/search?q=python+programming+-wikipedia"})

// 8. Search academic literature
web_fetch({"url": "https://scholar.google.com/scholar?q=deep+learning+optimization"})

// 9. Search cached pages (view deleted content)
web_fetch({"url": "https://webcache.googleusercontent.com/search?q=cache:example.com"})

// 10. Search for related sites
web_fetch({"url": "https://www.google.com/search?q=related:stackoverflow.com"})
```

---

## 🦆 DuckDuckGo Deep Search

### 2.1 DuckDuckGo Special Features

| Feature | Syntax | Example |
|------|------|------|
| **Bangs shortcuts** | `!abbreviation` | `!g python` → Google search |
| **Password generator** | `password` | `https://duckduckgo.com/?q=password+20` |
| **Color conversion** | `color` | `https://duckduckgo.com/?q=+%23FF5733` |
| **Short links** | `shorten` | `https://duckduckgo.com/?q=shorten+example.com` |
| **QR code generator** | `qr` | `https://duckduckgo.com/?q=qr+hello+world` |
| **UUID generator** | `uuid` | `https://duckduckgo.com/?q=uuid` |
| **Base64 encode/decode** | `base64` | `https://duckduckgo.com/?q=base64+hello` |

### 2.2 Complete DuckDuckGo Bangs List

#### Search Engines

| Bang | Target | Example |
|------|---------|------|
| `!g` | Google | `!g python tutorial` |
| `!b` | Bing | `!b weather` |
| `!y` | Yahoo | `!y finance` |
| `!sp` | Startpage | `!sp privacy` |
| `!brave` | Brave Search | `!brave tech` |

#### Programming and Development

| Bang | Target | Example |
|------|---------|------|
| `!gh` | GitHub | `!gh tensorflow` |
| `!so` | Stack Overflow | `!so javascript error` |
| `!npm` | npmjs.com | `!npm express` |
| `!pypi` | PyPI | `!pypi requests` |
| `!mdn` | MDN Web Docs | `!mdn fetch api` |
| `!docs` | DevDocs | `!docs python` |
| `!docker` | Docker Hub | `!docker nginx` |

#### Knowledge and Encyclopedias

| Bang | Target | Example |
|------|---------|------|
| `!w` | Wikipedia | `!w machine learning` |
| `!wen` | Wikipedia (English) | `!wen artificial intelligence` |
| `!wt` | Wiktionary | `!wt serendipity` |
| `!imdb` | IMDb | `!imdb inception` |

#### Shopping and Prices

| Bang | Target | Example |
|------|---------|------|
| `!a` | Amazon | `!a wireless headphones` |
| `!e` | eBay | `!e vintage watch` |
| `!ali` | AliExpress | `!ali phone case` |

#### Maps and Locations

| Bang | Target | Example |
|------|---------|------|
| `!m` | Google Maps | `!m Beijing` |
| `!maps` | OpenStreetMap | `!maps Paris` |

### 2.3 DuckDuckGo Search Parameters

| Parameter | Function | Example |
|------|------|------|
| `kp=1` | Strict safe search | `https://duckduckgo.com/html/?q=test&kp=1` |
| `kp=-1` | Safe search off | `https://duckduckgo.com/html/?q=test&kp=-1` |
| `kl=cn` | China region | `https://duckduckgo.com/html/?q=news&kl=cn` |
| `kl=us-en` | US English | `https://duckduckgo.com/html/?q=news&kl=us-en` |
| `ia=web` | Web results | `https://duckduckgo.com/?q=test&ia=web` |
| `ia=images` | Image results | `https://duckduckgo.com/?q=test&ia=images` |
| `ia=news` | News results | `https://duckduckgo.com/?q=test&ia=news` |
| `ia=videos` | Video results | `https://duckduckgo.com/?q=test&ia=videos` |

### 2.4 DuckDuckGo Deep Search Examples

```javascript
// 1. Use a Bang to jump to Google search
web_fetch({"url": "https://duckduckgo.com/html/?q=!g+machine+learning"})

// 2. Search GitHub projects directly
web_fetch({"url": "https://duckduckgo.com/html/?q=!gh+react"})

// 3. Find Stack Overflow answers
web_fetch({"url": "https://duckduckgo.com/html/?q=!so+python+list+comprehension"})

// 4. Generate a password
web_fetch({"url": "https://duckduckgo.com/?q=password+16"})

// 5. Base64 encoding
web_fetch({"url": "https://duckduckgo.com/?q=base64+hello+world"})

// 6. Color code conversion
web_fetch({"url": "https://duckduckgo.com/?q=%23FF5733"})

// 7. Search YouTube videos
web_fetch({"url": "https://duckduckgo.com/html/?q=!yt+python+tutorial"})

// 8. Look up Wikipedia
web_fetch({"url": "https://duckduckgo.com/html/?q=!w+artificial+intelligence"})

// 9. Amazon product search
web_fetch({"url": "https://duckduckgo.com/html/?q=!a+laptop"})

// 10. Generate a QR code
web_fetch({"url": "https://duckduckgo.com/?q=qr+https://github.com"})
```

---

## 🔎 Brave Search Deep Search

### 3.1 Brave Search Special Features

| Feature | Parameter | Example |
|------|------|------|
| **Independent index** | No reliance on Google/Bing | Own crawler index |
| **Goggles** | Custom search rules | Create personalized filters |
| **Discussions** | Forum discussion search | Aggregates Reddit and other forums |
| **News** | News aggregation | Independent news index |

### 3.2 Brave Search Parameters

| Parameter | Function | Example |
|------|------|------|
| `tf=pw` | Past week | `https://search.brave.com/search?q=news&tf=pw` |
| `tf=pm` | Past month | `https://search.brave.com/search?q=tech&tf=pm` |
| `tf=py` | Past year | `https://search.brave.com/search?q=AI&tf=py` |
| `safesearch=strict` | Strict safe search | `https://search.brave.com/search?q=test&safesearch=strict` |
| `source=web` | Web search | Default |
| `source=news` | News search | `https://search.brave.com/search?q=tech&source=news` |
| `source=images` | Image search | `https://search.brave.com/search?q=cat&source=images` |
| `source=videos` | Video search | `https://search.brave.com/search?q=music&source=videos` |

### 3.3 Brave Search Goggles (Custom Filters)

Goggles allow you to create custom search rules:

```
$discard  // Discard everything
$boost,site=stackoverflow.com  // Boost Stack Overflow
$boost,site=github.com  // Boost GitHub
$boost,site=docs.python.org  // Boost Python documentation
```

### 3.4 Brave Search Deep Search Examples

```javascript
// 1. Tech news from this week
web_fetch({"url": "https://search.brave.com/search?q=technology&tf=pw&source=news"})

// 2. AI developments this month
web_fetch({"url": "https://search.brave.com/search?q=artificial+intelligence&tf=pm"})

// 3. Image search
web_fetch({"url": "https://search.brave.com/search?q=machine+learning&source=images"})

// 4. Video tutorials
web_fetch({"url": "https://search.brave.com/search?q=python+tutorial&source=videos"})

// 5. Search with the independent index
web_fetch({"url": "https://search.brave.com/search?q=privacy+tools"})
```

---

## 📊 WolframAlpha Knowledge Computation Search

### 4.1 WolframAlpha Data Types

| Type | Example Query | URL |
|------|---------|-----|
| **Math computation** | `integrate x^2 dx` | `https://www.wolframalpha.com/input?i=integrate+x%5E2+dx` |
| **Unit conversion** | `100 miles to km` | `https://www.wolframalpha.com/input?i=100+miles+to+km` |
| **Currency conversion** | `100 USD to CNY` | `https://www.wolframalpha.com/input?i=100+USD+to+CNY` |
| **Stock data** | `AAPL stock` | `https://www.wolframalpha.com/input?i=AAPL+stock` |
| **Weather query** | `weather in Beijing` | `https://www.wolframalpha.com/input?i=weather+in+Beijing` |
| **Population data** | `population of China` | `https://www.wolframalpha.com/input?i=population+of+China` |
| **Chemical elements** | `properties of gold` | `https://www.wolframalpha.com/input?i=properties+of+gold` |
| **Nutrition facts** | `nutrition of apple` | `https://www.wolframalpha.com/input?i=nutrition+of+apple` |
| **Date computation** | `days between Jan 1 2020 and Dec 31 2024` | Date interval calculation |
| **Time zone conversion** | `10am Beijing to New York` | Time zone conversion |
| **IP address** | `8.8.8.8` | IP information lookup |
| **Barcode** | `scan barcode 123456789` | Barcode information |
| **Flights** | `flight AA123` | Flight information |

### 4.2 WolframAlpha Deep Search Examples

```javascript
// 1. Compute an integral
web_fetch({"url": "https://www.wolframalpha.com/input?i=integrate+sin%28x%29+from+0+to+pi"})

// 2. Solve an equation
web_fetch({"url": "https://www.wolframalpha.com/input?i=solve+x%5E2-5x%2B6%3D0"})

// 3. Real-time currency exchange rates
web_fetch({"url": "https://www.wolframalpha.com/input?i=100+USD+to+CNY"})

// 4. Real-time stock data
web_fetch({"url": "https://www.wolframalpha.com/input?i=Apple+stock+price"})

// 5. City weather
web_fetch({"url": "https://www.wolframalpha.com/input?i=weather+in+Shanghai+tomorrow"})

// 6. Country statistics
web_fetch({"url": "https://www.wolframalpha.com/input?i=GDP+of+China+vs+USA"})

// 7. Chemistry computation
web_fetch({"url": "https://www.wolframalpha.com/input?i=molar+mass+of+H2SO4"})

// 8. Physical constants
web_fetch({"url": "https://www.wolframalpha.com/input?i=speed+of+light"})

// 9. Nutrition information
web_fetch({"url": "https://www.wolframalpha.com/input?i=calories+in+banana"})

// 10. Historical dates
web_fetch({"url": "https://www.wolframalpha.com/input?i=events+on+July+20+1969"})
```

---

## 🔧 Startpage Privacy Search

### 5.1 Startpage Special Features

| Feature | Description | URL |
|------|------|-----|
| **Proxy browsing** | Anonymous access to search results | Click "Anonymous View" |
| **No tracking** | No search history recorded | On by default |
| **EU servers** | Protected by EU privacy law | Data stays in Europe |
| **Proxy images** | Images loaded via proxy | Hides your IP |

### 5.2 Startpage Parameters

| Parameter | Function | Example |
|------|------|------|
| `cat=web` | Web search | Default |
| `cat=images` | Image search | `...&cat=images` |
| `cat=video` | Video search | `...&cat=video` |
| `cat=news` | News search | `...&cat=news` |
| `language=english` | English results | `...&language=english` |
| `time=day` | Past 24 hours | `...&time=day` |
| `time=week` | Past week | `...&time=week` |
| `time=month` | Past month | `...&time=month` |
| `time=year` | Past year | `...&time=year` |
| `nj=0` | Family filter off | `...&nj=0` |

### 5.3 Startpage Deep Search Examples

```javascript
// 1. Privacy search
web_fetch({"url": "https://www.startpage.com/sp/search?query=privacy+tools"})

// 2. Privacy image search
web_fetch({"url": "https://www.startpage.com/sp/search?query=nature&cat=images"})

// 3. This week's news (privacy mode)
web_fetch({"url": "https://www.startpage.com/sp/search?query=tech+news&time=week&cat=news"})

// 4. English results search
web_fetch({"url": "https://www.startpage.com/sp/search?query=machine+learning&language=english"})
```

---

## 🌍 Combined Search Strategies

### 6.1 Choosing an Engine by Search Goal

| Search Goal | First Choice | Alternatives | Reason |
|---------|---------|---------|------|
| **Academic research** | Google Scholar | Google, Brave | Academic resource indexing |
| **Programming and development** | Google | GitHub (DuckDuckGo bang) | Comprehensive technical documentation |
| **Privacy-sensitive** | DuckDuckGo | Startpage, Brave | Does not track users |
| **Real-time news** | Brave News | Google News | Independent news index |
| **Knowledge computation** | WolframAlpha | Google | Structured data |
| **Chinese content** | Google HK | Bing | Well optimized for Chinese |
| **European perspective** | Qwant | Startpage | EU compliant |
| **Eco-friendly** | Ecosia | DuckDuckGo | Searches fund tree planting |
| **Unfiltered** | Brave | Startpage | Unbiased results |

### 6.2 Cross-Validation with Multiple Engines

```javascript
// Strategy: search the same keyword on multiple engines and compare results
const keyword = "climate change 2024";

// Get different perspectives
const searches = [
  { engine: "Google", url: `https://www.google.com/search?q=${keyword}&tbs=qdr:m` },
  { engine: "Brave", url: `https://search.brave.com/search?q=${keyword}&tf=pm` },
  { engine: "DuckDuckGo", url: `https://duckduckgo.com/html/?q=${keyword}` },
  { engine: "Ecosia", url: `https://www.ecosia.org/search?q=${keyword}` }
];

// Analyze the differences between the engines' results
```

### 6.3 Time-Sensitive Search Strategies

| Timeliness Requirement | Engine Choice | Parameter Settings |
|-----------|---------|---------|
| **Real-time (hourly)** | Google News, Brave News | `tbs=qdr:h`, `tf=pw` |
| **Recent (daily)** | Google, Brave | `tbs=qdr:d`, `time=day` |
| **This week** | All engines | `tbs=qdr:w`, `tf=pw` |
| **This month** | All engines | `tbs=qdr:m`, `tf=pm` |
| **Historical** | Google Scholar | Academic archives |

### 6.4 Deep Search by Professional Domain

#### Technical Development

```javascript
// GitHub project search
web_fetch({"url": "https://duckduckgo.com/html/?q=!gh+tensorflow+stars:%3E1000"})

// Stack Overflow questions
web_fetch({"url": "https://duckduckgo.com/html/?q=!so+python+memory+leak"})

// MDN documentation
web_fetch({"url": "https://duckduckgo.com/html/?q=!mdn+javascript+async+await"})

// PyPI packages
web_fetch({"url": "https://duckduckgo.com/html/?q=!pypi+requests"})

// npm packages
web_fetch({"url": "https://duckduckgo.com/html/?q=!npm+express"})
```

#### Academic Research

```javascript
// Google Scholar papers
web_fetch({"url": "https://scholar.google.com/scholar?q=deep+learning+2024"})

// Search for PDF papers
web_fetch({"url": "https://www.google.com/search?q=machine+learning+filetype:pdf+2024"})

// arXiv papers
web_fetch({"url": "https://duckduckgo.com/html/?q=site:arxiv.org+quantum+computing"})
```

#### Finance and Investment

```javascript
// Real-time stock data
web_fetch({"url": "https://www.wolframalpha.com/input?i=AAPL+stock"})

// Exchange rate conversion
web_fetch({"url": "https://www.wolframalpha.com/input?i=EUR+to+USD"})

// Search earnings report PDFs
web_fetch({"url": "https://www.google.com/search?q=Apple+Q4+2024+earnings+filetype:pdf"})
```

#### News and Current Events

```javascript
// Google News
web_fetch({"url": "https://www.google.com/search?q=breaking+news&tbm=nws&tbs=qdr:h"})

// Brave News
web_fetch({"url": "https://search.brave.com/search?q=world+news&source=news"})

// DuckDuckGo News
web_fetch({"url": "https://duckduckgo.com/html/?q=tech+news&ia=news"})
```

---

## 🛠️ Advanced Search Techniques Summary

### URL Encoding Helper Function

```javascript
// URL-encode a keyword
function encodeKeyword(keyword) {
  return encodeURIComponent(keyword);
}

// Example
const keyword = "machine learning";
const encoded = encodeKeyword(keyword); // "machine%20learning"
```

### Batch Search Templates

```javascript
// Multi-engine batch search function
function generateSearchUrls(keyword) {
  const encoded = encodeURIComponent(keyword);
  return {
    google: `https://www.google.com/search?q=${encoded}`,
    google_hk: `https://www.google.com.hk/search?q=${encoded}`,
    duckduckgo: `https://duckduckgo.com/html/?q=${encoded}`,
    brave: `https://search.brave.com/search?q=${encoded}`,
    startpage: `https://www.startpage.com/sp/search?query=${encoded}`,
    bing_intl: `https://cn.bing.com/search?q=${encoded}&ensearch=1`,
    yahoo: `https://search.yahoo.com/search?p=${encoded}`,
    ecosia: `https://www.ecosia.org/search?q=${encoded}`,
    qwant: `https://www.qwant.com/?q=${encoded}`
  };
}

// Usage example
const urls = generateSearchUrls("artificial intelligence");
```

### Time Filter Shortcut Function

```javascript
// Google time filter URL generation
function googleTimeSearch(keyword, period) {
  const periods = {
    hour: 'qdr:h',
    day: 'qdr:d',
    week: 'qdr:w',
    month: 'qdr:m',
    year: 'qdr:y'
  };
  return `https://www.google.com/search?q=${encodeURIComponent(keyword)}&tbs=${periods[period]}`;
}

// Usage example
const recentNews = googleTimeSearch("AI breakthrough", "week");
```

---

## 📝 Complete Search Example Collection

```javascript
// ==================== Technical Development ====================

// 1. Search GitHub for high-star Python projects
web_fetch({"url": "https://www.google.com/search?q=site:github.com+python+stars:%3E1000"})

// 2. Best Stack Overflow answers
web_fetch({"url": "https://duckduckgo.com/html/?q=!so+best+way+to+learn+python"})

// 3. MDN documentation queries
web_fetch({"url": "https://duckduckgo.com/html/?q=!mdn+promises"})

// 4. Search npm packages
web_fetch({"url": "https://duckduckgo.com/html/?q=!npm+axios"})

// ==================== Academic Research ====================

// 5. Google Scholar papers
web_fetch({"url": "https://scholar.google.com/scholar?q=transformer+architecture"})

// 6. Search for PDF papers
web_fetch({"url": "https://www.google.com/search?q=attention+is+all+you+need+filetype:pdf"})

// 7. Latest arXiv papers
web_fetch({"url": "https://duckduckgo.com/html/?q=site:arxiv.org+abs+quantum"})

// ==================== News and Current Events ====================

// 8. Latest Google News (past hour)
web_fetch({"url": "https://www.google.com/search?q=breaking+news&tbs=qdr:h&tbm=nws"})

// 9. Brave tech news this week
web_fetch({"url": "https://search.brave.com/search?q=technology&tf=pw&source=news"})

// 10. DuckDuckGo News
web_fetch({"url": "https://duckduckgo.com/html/?q=world+news&ia=news"})

// ==================== Finance and Investment ====================

// 11. Real-time stock data
web_fetch({"url": "https://www.wolframalpha.com/input?i=Tesla+stock"})

// 12. Currency exchange rates
web_fetch({"url": "https://www.wolframalpha.com/input?i=1+BTC+to+USD"})

// 13. Company earnings report PDFs
web_fetch({"url": "https://www.google.com/search?q=Microsoft+annual+report+2024+filetype:pdf"})

// ==================== Knowledge Computation ====================

// 14. Math computation
web_fetch({"url": "https://www.wolframalpha.com/input?i=derivative+of+x%5E3+sin%28x%29"})

// 15. Unit conversion
web_fetch({"url": "https://www.wolframalpha.com/input?i=convert+100+miles+to+kilometers"})

// 16. Nutrition information
web_fetch({"url": "https://www.wolframalpha.com/input?i=protein+in+chicken+breast"})

// ==================== Privacy-Preserving Search ====================

// 17. DuckDuckGo privacy search
web_fetch({"url": "https://duckduckgo.com/html/?q=privacy+tools"})

// 18. Startpage anonymous search
web_fetch({"url": "https://www.startpage.com/sp/search?query=secure+messaging"})

// 19. Brave no-tracking search
web_fetch({"url": "https://search.brave.com/search?q=encryption+software"})

// ==================== Advanced Combined Search ====================

// 20. Multi-condition exact Google search
web_fetch({"url": "https://www.google.com/search?q=%22machine+learning%22+site:github.com+filetype:pdf+2024"})

// 21. Search excluding specific sites
web_fetch({"url": "https://www.google.com/search?q=python+tutorial+-wikipedia+-w3schools"})

// 22. Price range search
web_fetch({"url": "https://www.google.com/search?q=laptop+%24800..%241200+best+review"})

// 23. Use Bangs for quick jumps
web_fetch({"url": "https://duckduckgo.com/html/?q=!g+site:medium.com+python"})

// 24. Image search (Google)
web_fetch({"url": "https://www.google.com/search?q=beautiful+landscape&tbm=isch"})

// 25. Academic citation search
web_fetch({"url": "https://scholar.google.com/scholar?q=author:%22Geoffrey+Hinton%22"})
```

---

## 🔐 Privacy Protection Best Practices

### Search Engine Privacy Levels

| Engine | Tracking Level | Data Retention | Encrypted | Recommended For |
|------|---------|---------|------|---------|
| **DuckDuckGo** | No tracking | No retention | Yes | Everyday privacy search |
| **Startpage** | No tracking | No retention | Yes | Google results with privacy |
| **Brave** | No tracking | No retention | Yes | Independent index, unbiased |
| **Qwant** | No tracking | No retention | Yes | EU compliance requirements |
| **Google** | Heavy tracking | Long retention | Yes | Personalized results |
| **Bing** | Moderate tracking | Long retention | Yes | Microsoft service integration |

### Privacy Search Recommendations

1. **Everyday use**: DuckDuckGo or Brave
2. **Google results with privacy**: Startpage
3. **Academic research**: Google Scholar (less tracking for academic use)
4. **Sensitive queries**: Use the Tor browser + DuckDuckGo onion service
5. **Cross-device sync**: Avoid logging into search engine accounts

---

## 📚 References

- [Complete list of Google search operators](https://support.google.com/websearch/answer/...)
- [Complete list of DuckDuckGo Bangs](https://duckduckgo.com/bang)
- [Brave Search documentation](https://search.brave.com/help/...)
- [WolframAlpha examples](https://www.wolframalpha.com/examples/)
