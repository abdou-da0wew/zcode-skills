/**
 * analyzer.ts — LLM/VLM analysis layer
 * Seven-section decision dashboard + optional dividend analysis for US stocks
 */

import { chatCompletions, validateStockData, MODEL } from "./dataFetcher";
import { StockData, AnalysisResult, OutputFormat, Market, Verdict, PositionInfo } from "./types";
import { analyzeDividend, formatDividendMarkdown } from "./dividend";

const MARKET_LABEL: Record<Market, string> = { CN: "A-share", HK: "HK stock", US: "US stock" };

// ── Dashboard prompt ──────────────────────────────────────

function buildDashboardPrompt(
  data: StockData,
  position: PositionInfo | undefined,
  warnings: string[]
): string {
  const warningBlock = warnings.length > 0
    ? `⚠️ Data warnings (must be reflected in the report):\n${warnings.map((w) => `- ${w}`).join("\n")}\n\n`
    : "";

  const positionBlock = position
    ? position.status === "holding"
      ? `User position: holding, cost basis ${position.cost ?? "unknown"}${position.shares ? `, ${position.shares} shares` : ""}. Provide a P/L analysis and targeted advice.`
      : `User position: currently no position.`
    : `User position: not provided (give two sets of advice — one for empty-position and one for holding readers).`;

  return `${warningBlock}${positionBlock}

Stock data:
\`\`\`json
${JSON.stringify(data, null, 2)}
\`\`\`

Output the complete decision dashboard in exactly the following format (strictly follow the structure; do not add or remove sections):

---

## Decision Dashboard · {name}({code}) · {market}

---

### 📰 Key Information at a Glance
**💭 Sentiment:** one sentence
**📊 Earnings expectations:** brief comment combining PE/ROE/industry; mark missing data as "N/A"
**🚨 Risk alerts:**
- Risk 1 (technical or macro)
- Risk 2 (fundamental or industry)
**✨ Positive catalysts:**
- Catalyst 1 (technical)
- Catalyst 2 (fundamental or industry)
**📢 Latest development:** one key piece of information with industry context

---

### 📌 Core Conclusion
**[emoji] Verdict: Strong Buy / Buy / Hold / Sell** (choose exactly one; deviation rate >5% must not be Buy)
**💬 One-line decision:** core logic
**⏰ Time sensitivity:** act now / within today / no rush

(based on position status)
- **🆕 Empty-position readers:** whether to enter, entry points, position size
- **💼 Holding readers:** hold / add / trim / stop-loss advice${position?.status === "holding" && position.cost ? ", including cost-basis P/L analysis" : ""}

---

### 📈 Today's Session
List: close, previous close, open, high, low, change %, change amount, amplitude, volume, turnover (mark missing as "N/A")

---

### 📊 Data Deep-Dive

**Technicals:**
Table (indicator | value | reading): MA5, MA10, MA20, deviation rate (BIAS20), RSI (if available), support, resistance
Conclusion: moving-average state + trend strength (xx/100)

**Fundamentals (state the reporting period):**
Table (indicator | value | industry comparison): ROE, gross margin, net margin, debt ratio, PE, PB
Mark missing data as "N/A"; never fabricate

**Capital flows:** (applies to A-shares/HK stocks; optional for US stocks)
- Main-capital net inflow: amount (share %), one-sentence reading
- Chips: profit-taking ratio | average cost | concentration

---

### 🎯 Battle Plan

| Level type | Price | Notes |
|---------|------|------|
| 🎯 Ideal buy | xxx | |
| 🔵 Second-best buy | xxx | |
| 🛑 Stop-loss | xxx | |
| 🎊 Target | xxx | |

**💰 Position advice:** x/10 of capital
**Entry strategy:** staggered entries
**Risk control:** stop-loss discipline

---

### ✅ Checklist
- ✅/⚠️/❌ Moving-average state
- ✅/⚠️/❌ Deviation rate safe (<5%)
- ✅/⚠️/❌ Volume confirmation
- ✅/⚠️/❌ Valuation reasonable
- ✅/⚠️/❌ Capital flow
- ✅/⚠️/❌ Chip health

**Overall conclusion:** one sentence summarizing the current state and recommendation.

---
*The analysis above is for reference only and does not constitute investment advice; act at your own risk.*`;
}

// ── Research report prompt (PDF/Word) ─────────────────────

function buildReportPrompt(data: StockData, position: PositionInfo | undefined): string {
  const positionBlock = position?.status === "holding"
    ? `User position cost: ${position.cost ?? "unknown"}`
    : "User currently has no position";

  return `${positionBlock}

Stock data:
\`\`\`json
${JSON.stringify(data, null, 2)}
\`\`\`

Generate a structured research report:

[Research Report] {name}({code}) · {market} · {date}

I. Investment conclusion (Buy/Strong Buy/Hold/Sell, with target price and stop-loss; two sets of advice — empty position and holding)
II. Key information at a glance (sentiment / earnings expectations / risks / catalysts / latest developments)
III. Data deep-dive (technicals / fundamentals / capital flows)
IV. Battle plan (level table / position / holding period)
V. Risk disclosures (2-3 items)

Disclaimer: this report is AI-assisted, for reference only, and does not constitute investment advice; act at your own risk.`;
}

// ── Verdict extraction ────────────────────────────────────

function extractVerdict(text: string): Verdict {
  const CANON: Record<string, Verdict> = {
    "strong buy": "Strong Buy",
    "buy": "Buy",
    "hold": "Hold",
    "sell": "Sell",
  };
  const patterns = [
    /verdict[:\s]*[💚🟢🟡🔴⚪]?\s*(Strong Buy|Buy|Hold|Sell)/i,
    /conclusion[:\s]*[💚🟢🟡🔴⚪]?\s*(Strong Buy|Buy|Hold|Sell)/i,
    /\*\*(Strong Buy|Buy|Hold|Sell)\*\*/i,
  ];
  for (const p of patterns) {
    const m = text.match(p);
    if (m) return CANON[m[1].toLowerCase()] ?? "Hold";
  }
  return "Hold";
}

// ── Core analysis ─────────────────────────────────────────

export async function analyzeStock(
  data: StockData,
  outputFormat: OutputFormat = "markdown",
  position?: PositionInfo,
  includeDividend = false
): Promise<AnalysisResult> {
  const { valid, warnings } = validateStockData(data);
  const name = data.name ?? data.code;

  if (!valid) {
    return {
      code: data.code, market: data.market, name,
      verdict: "Hold",
      analysis: `## ⚠️ Data Fetch Failed\n\nData for ${data.code} could not be retrieved (${data.error ?? "unknown error"}); verify manually.`,
      warnings, outputFormat,
      generatedAt: new Date().toISOString(),
    };
  }

  const userPrompt = outputFormat === "markdown"
    ? buildDashboardPrompt(data, position, warnings)
    : buildReportPrompt(data, position);

  let analysisText = "⚠️ The LLM returned no content; please retry.";
  try {
    const completion = await chatCompletions({
      model: MODEL,
      messages: [
        { role: "system", content: `You are a senior ${MARKET_LABEL[data.market]} stock analyst. Mark missing data as "N/A"; fabricating data is strictly prohibited. When the deviation rate is >5%, never recommend buying. The verdict must be exactly one of: Strong Buy / Buy / Hold / Sell. Output language: English.` },
        { role: "user", content: userPrompt },
      ],
    });
    analysisText = completion.choices[0]?.message?.content ?? analysisText;
  } catch (err: any) {
    analysisText = `## ⚠️ Analysis Failed\n\nLLM call error: ${err.message}`;
  }

  // Optional dividend analysis for US stocks
  if (includeDividend && data.market === "US" && outputFormat === "markdown") {
    try {
      const dividend = await analyzeDividend(data.code);
      const dividendMd = formatDividendMarkdown(dividend);
      analysisText += `\n\n${dividendMd}`;
    } catch {}
  }

  return {
    code: data.code, market: data.market, name,
    verdict: extractVerdict(analysisText),
    analysis: analysisText,
    warnings, outputFormat,
    generatedAt: new Date().toISOString(),
  };
}

// ── Batch analysis ────────────────────────────────────────

export async function analyzeMultipleStocks(
  stockDataList: StockData[],
  outputFormat: OutputFormat = "markdown",
  positions?: Record<string, PositionInfo>,
  includeDividend = false
): Promise<AnalysisResult[]> {
  const results: AnalysisResult[] = [];
  for (const data of stockDataList) {
    const position = positions?.[data.code];
    results.push(await analyzeStock(data, outputFormat, position, includeDividend));
  }
  return results;
}

// ── K-line chart analysis (VLM) ───────────────────────────

export async function analyzeChartImage(
  imageUrlOrBase64: string,
  stockCode: string,
  isBase64 = false
): Promise<string> {
  try {
    // OpenAI-compatible vision input: image_url with either a remote URL or a base64 data URI
    const imageUrl = isBase64
      ? `data:image/png;base64,${imageUrlOrBase64}`
      : imageUrlOrBase64;

    const completion = await chatCompletions({
      model: MODEL,
      messages: [
        { role: "system", content: "You are a technical analysis expert specializing in candlestick (K-line) pattern recognition. Answer in English." },
        {
          role: "user",
          content: [
            { type: "image_url", image_url: { url: imageUrl } },
            { type: "text", text: `This is the K-line chart of ${stockCode}. Analyze:\n1. Current candlestick pattern\n2. Trend direction\n3. Key support and resistance levels\n4. Volume confirmation\n5. Short-term action advice` },
          ],
        },
      ],
    });
    return completion.choices[0]?.message?.content ?? "⚠️ The VLM returned no content";
  } catch (err: any) {
    return `K-line chart analysis failed: ${err.message}`;
  }
}
