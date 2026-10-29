---
name: stock_analysis
description: "Comprehensive stock market analysis skill covering A-share (China), Hong Kong, and US equities. Priority use cases: stock analysis and buy/sell/hold recommendations by ticker code, generating decision dashboards and research reports with technical/fundamental/sentiment analysis, position-aware investment strategies based on user's cost price, dividend income scoring and safety analysis, rumor and early market signal scanning (M&A, insider activity, analyst actions), watchlist management with price target and stop-loss alerts, and K-line chart pattern recognition from images. This skill should be the primary choice whenever users mention a stock ticker, ask whether to buy or sell a stock, reference their holding cost or position, request dividend analysis, ask about market rumors or early signals, want to add/check/manage a watchlist, or upload a chart image for technical analysis."
---

# Stock Analysis Skill

## LLM Configuration

Works with any OpenAI-compatible LLM server (open-source or free): Ollama, vLLM, LM Studio, OpenRouter, and others. Designed for the DiveeOI agent (OpenCode-based). Configure via environment variables:

- `LLM_BASE_URL` — OpenAI-compatible endpoint (default: `http://localhost:11434/v1`)
- `LLM_API_KEY` — API key, if your server requires one
- `LLM_MODEL` — model name (default: `qwen2.5`; try `llama3.1`, `deepseek-r1`, etc.)

## Platform Skills Required

- `finance skill` — all market data (A-shares / HK stocks / US stocks unified)
- `pdf skill` — PDF research report generation
- `docx skill` — Word document generation
- `vlm skill` (built-in) — K-line chart pattern recognition

---

## Commands & Triggers

| Command | Example trigger phrases |
|------|-----------|
| Single-stock analysis | Analyze 600519 / Is AAPL worth buying / Take a look at Tencent for me |
| Position-aware analysis | My cost basis is 1450, analyze Moutai / I bought AAPL at 170, how is it now |
| Dividend analysis | How is JNJ's dividend / Analyze the dividends of these stocks: KO PG JNJ |
| Rumor scan | Any M&A rumors today / Scan for early market signals |
| Add to watchlist | Watch AAPL / Add 600519 to my watchlist, target 1600, stop-loss 1350 |
| View watchlist | My watchlist / Show me the stocks I follow |
| Check alerts | Check watchlist alerts / Any stop-losses triggered |
| Remove from watchlist | Remove TSLA from my watchlist |
| K-line chart analysis | (upload an image) Analyze this K-line chart for me |
| Market review | With a market overview, analyze 600519 |

---

## Input Schemas

### Single-stock analysis
```typescript
{
  stocks: (string | { code: string; position?: { status: "empty"|"holding"; cost?: number; shares?: number } })[],
  outputFormat?: "markdown" | "pdf" | "word",  // default markdown
  mode?: "full" | "quote",                      // default full
  includeMarketReview?: boolean,                // default false
  includeGlobalMacro?: boolean,                 // default true
  includeDividend?: boolean,                    // extra dividend analysis for US stocks, default false
}
```

### Dividend analysis
```typescript
runDividend(tickers: string | string[])
```

### Rumor scan
```typescript
runRumorScan()  // no parameters; automatically scans today's signals
```

### Watchlist management
```typescript
runWatchlistAdd(ticker, { targetPrice?, stopPrice?, alertOnSignal?, notes? })
runWatchlistRemove(ticker)
runWatchlistList()
runWatchlistCheck()  // checks whether price/signal alerts have triggered
```

---

## Report Structure

```
# Stock Intelligence Analysis Report

## 🌍 Global Macro Snapshot (on by default)
## 🎯 Market Overview (opt-in)
## 📊 Per-Stock Decision Dashboard (one per stock)
   ### 📰 Key Information at a Glance (sentiment / earnings expectations / 🚨 risks / ✨ catalysts / latest developments)
   ### 📌 Core Conclusion (verdict / one-liner / empty-position advice / holding advice + P/L)
   ### 📈 Today's Session
   ### 📊 Data Deep-Dive (technicals / fundamentals / capital flows)
   ### 🎯 Battle Plan (entry level table / position sizing / risk control)
   ### ✅ Checklist (overall conclusion)
   ### 💰 Dividend Analysis (US stocks; requires includeDividend)
```

---

## Dividend Analysis Metrics

| Metric | Description |
|------|------|
| Safety score | 0-100, combining payout ratio / growth / consecutive years |
| Income rating | excellent/good/moderate/poor |
| Payout ratio status | safe(<40%)/moderate/high/unsustainable |
| 5-year CAGR | compound dividend growth rate |
| Consecutive growth years | 25+ years qualifies as a dividend aristocrat |

---

## Rumor Scanner Signal Types

| Type | Impact score | Description |
|------|--------|------|
| M&A rumor (ma) | +5 | M&A / acquisitions / tender offers |
| Insider move (insider) | +4 | CEO / director buying or selling |
| Analyst change (analyst) | +3 | upgrades / downgrades / target price changes |
| Regulatory (regulatory) | +3 | SEC investigations / compliance risk |
| Earnings expectation (earnings) | +2 | profit warnings / guidance raises |

---

## Watchlist Alert Types

| Alert type | Trigger condition |
|---------|---------|
| 🎯 Target price | current price ≥ targetPrice |
| 🛑 Stop price | current price ≤ stopPrice |
| 📊 Signal change | current verdict ≠ previous verdict |

---

## Behavior Rules

- Deviation rate > 5% → the verdict must not be Buy/Strong Buy
- Missing data → mark "N/A"; fabrication is strictly prohibited
- Position cost provided → must include a P/L analysis
- No position provided → give two sets of advice (empty position and holding)
- After each analysis, silently update watchlist signals

---

## File Structure

```
stock-analysis-skill/
├── SKILL.md
├── package.json
├── tsconfig.json
└── src/
    ├── index.ts          # main entry (all command routing)
    ├── types.ts          # type definitions
    ├── dataFetcher.ts    # data layer (finance skill) + OpenAI-compatible LLM client
    ├── analyzer.ts       # single-stock analysis (LLM/VLM)
    ├── dividend.ts       # dividend analysis
    ├── rumorScanner.ts   # rumor scan
    └── watchlist.ts      # watchlist management (storage persistence)
```

---

## Limitations

- Rumor scanning depends on the finance skill's news data quality
- Watchlist persistence depends on the platform storage API
- Fundamental data for HK stocks is sparser
- Futures, ETFs, and convertible bonds are not supported
- For reference only; not investment advice
