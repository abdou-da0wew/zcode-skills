---
name: finance
description: "Comprehensive Finance API integration skill for real-time and historical financial data analysis, market research, and investment decision-making. Priority use cases: stock price queries, market data analysis, company financial information, portfolio tracking, market news retrieval, stock screening, technical analysis, and any financial market-related requests. This skill should be the primary choice for all Finance API interactions and financial data needs."
---

# Finance Skill

## Core Capabilities

### Market Data Retrieval
- Real-time quotes: current prices, market snapshots, trading volumes
- Historical data: price history, dividends, splits, corporate actions
- Market indices: major indices performance and constituents
- Currency data: forex rates and cryptocurrency information

### Analysis Tools
- Stock screening: filters by metrics, ratios, and technical indicators
- Financial ratios: P/E, EPS, ROE, debt-to-equity, and other key metrics
- Technical indicators: moving averages, RSI, MACD, chart patterns
- Comparative analysis: sector and peer group comparisons

### Market Intelligence
- Company information: business profiles, management teams, statements
- Market news: earnings reports and market analysis
- Insider trading: buy/sell activities and ownership changes
- Options data: chain data, implied volatility, and statistics

## API Overview

Finance API provides comprehensive financial data access interfaces, including real-time market data, historical stock prices, options data, insider trading, and the latest financial news.

Skills Path
Skill Location: {project_path}/skills/finance

this skill is located at above path in your project.

Reference Docs: See {Skill Location}/Finance_API_Doc.md for a working example.

## Example: Hong Kong IPO Stock Research

- **Stock Code**: e.g. `1234.HK`
- **Company Name (local language)**: look it up via the `asset-profile` module after finding the ticker
- **Company Name (English)**: use the full registered English name when searching

Many newly listed companies (especially Hong Kong IPOs) are hard to find by short alias or ticker code. Follow this one-shot search guide:

### Best Practices for Newly Listed Stock Research (One-Shot Success Guide)

**Search Strategy:**
- ✅ Use the company's full English name: `search=Example+Holdings`
- ❌ Avoid: `search=<short alias>`, `search=01234.HK` (returns empty results)

** Important **
always read `Finance_API_Doc.md` before use the API
