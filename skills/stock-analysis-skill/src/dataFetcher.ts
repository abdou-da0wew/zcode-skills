/**
 * dataFetcher.ts — all data is fetched through the finance skill
 *
 * Works with any OpenAI-compatible LLM server: Ollama, vLLM, LM Studio, OpenRouter, ...
 * Environment variables:
 *   LLM_BASE_URL  — base URL of an OpenAI-compatible endpoint (default: http://localhost:11434/v1)
 *   LLM_API_KEY   — API key / bearer token, if your server requires one (default: empty)
 *   LLM_MODEL     — model name to use (default: qwen2.5)
 */

import { Market, FetchMode, StockData } from "./types";

const BASE_URL = process.env.LLM_BASE_URL ?? "http://localhost:11434/v1";
const API_KEY = process.env.LLM_API_KEY ?? "";
export const MODEL = process.env.LLM_MODEL ?? "qwen2.5";

// Node 18+ ships a global fetch; declare it minimally so the ES2020 lib config compiles.
declare const fetch: (input: string, init?: Record<string, unknown>) => Promise<{ ok: boolean; status: number; text(): Promise<string>; json(): Promise<any> }>;

/** Minimal OpenAI-compatible chat completions call (no extra dependencies). */
export async function chatCompletions(body: Record<string, unknown>): Promise<any> {
  const res = await fetch(`${BASE_URL}/chat/completions`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(API_KEY ? { Authorization: `Bearer ${API_KEY}` } : {}),
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`LLM request failed (${res.status}): ${await res.text()}`);
  return res.json();
}

export function detectMarket(code: string): Market {
  if (/^\d{6}$/.test(code)) return "CN";
  if (/^\d{4,5}\.HK$/i.test(code)) return "HK";
  return "US";
}

const MARKET_LABEL: Record<Market, string> = {
  CN: "A-share", HK: "HK stock", US: "US stock",
};

// ── Single stock data ──────────────────────────────────────

export async function fetchStockData(
  code: string,
  mode: FetchMode = "full"
): Promise<StockData> {
  const market = detectMarket(code);

  const prompt = mode === "quote"
    ? `Look up the real-time share price of ${code} (${MARKET_LABEL[market]}). Return JSON only, with fields:
       name, price, prev_close, change_pct, change_amount, volume, amount, turnover, volume_ratio, market_cap, pe_ttm, pb.`
    : `Fetch complete stock data for ${code} (${MARKET_LABEL[market]}). Return JSON only, including:
       name, price, prev_close, open, high, low, change_pct, change_amount, amplitude,
       volume, amount, turnover, volume_ratio, market_cap, pe_ttm, pb, high_52w, low_52w, dividend_yield,
       ma5, ma10, ma20, bias_pct (deviation from MA20, %),
       trend ("uptrend alignment" / "downtrend alignment" / "sideways consolidation"), overbought_warning (true if bias_pct>5),
       support (support level), resistance (resistance level), rsi,
       kline_recent_10 (last 10 daily candles, each with date/open/close/high/low/volume),
       profit_ratio (profit-taking ratio %), avg_cost (average cost), chip_concentration (chip concentration),
       roe, gross_margin, net_margin, debt_ratio, eps, revenue_growth,
       main_net (main-capital net inflow amount), main_net_pct (main-capital net inflow ratio %).
       Fill missing fields with null; never fabricate data.`;

  try {
    const completion = await chatCompletions({
      model: MODEL,
      messages: [{ role: "user", content: prompt }],
    });
    const raw = completion.choices[0]?.message?.content ?? "";
    const parsed = JSON.parse(raw.replace(/```json|```/g, "").trim());
    return { code, market, timestamp: new Date().toISOString(), ...parsed };
  } catch (err: any) {
    return { code, market, timestamp: new Date().toISOString(), error: err.message };
  }
}

// ── Batch fetching (serial) ────────────────────────────────

export async function fetchMultipleStocks(
  codes: string[],
  mode: FetchMode = "full"
): Promise<StockData[]> {
  const results: StockData[] = [];
  for (let i = 0; i < codes.length; i++) {
    results.push(await fetchStockData(codes[i], mode));
    if (i < codes.length - 1) await new Promise((r) => setTimeout(r, 300));
  }
  return results;
}

// ── Global macro ───────────────────────────────────────────

export async function fetchGlobalMacro(): Promise<string> {
  try {
    const completion = await chatCompletions({
      model: MODEL,
      messages: [{
        role: "user",
        content: `Summarize today's key global market information in concise Markdown, covering:
- Yesterday's closes and changes of the three major US indices (Dow / Nasdaq / S&P)
- US dollar index and CNY exchange rate movements
- Latest gold and crude oil prices
- Latest Federal Reserve policy moves (if any)
- 1-2 key macro events affecting A-shares/HK stocks
Keep it under 150 words.`,
      }],
    });
    return completion.choices[0]?.message?.content ?? "Failed to fetch global macro data";
  } catch (err: any) {
    return `Failed to fetch global macro data: ${err.message}`;
  }
}

// ── Market overview ────────────────────────────────────────

export async function fetchMarketOverview(): Promise<string> {
  try {
    const completion = await chatCompletions({
      model: MODEL,
      messages: [{
        role: "user",
        content: `Summarize today's A-share market data in Markdown, covering:
- Latest levels and changes of the SSE / SZSE / ChiNext / STAR 50 indices
- Number of advancers / decliners / limit-ups / limit-downs today, and total turnover
- Top 3 leading and top 3 lagging sectors
- Northbound capital net inflow
- A one-sentence outlook and position strategy
Keep it under 200 words.`,
      }],
    });
    return completion.choices[0]?.message?.content ?? "Failed to fetch market overview data";
  } catch (err: any) {
    return `Failed to fetch market overview data: ${err.message}`;
  }
}

// ── Data validation ────────────────────────────────────────

export function validateStockData(data: StockData): {
  valid: boolean;
  warnings: string[];
} {
  const warnings: string[] = [];
  if (data.error) return { valid: false, warnings: [`Data fetch failed: ${data.error}`] };
  if (!data.price) warnings.push("Price data missing");
  if (!data.ma5 && !data.ma20) warnings.push("Technical data missing");
  if (data.overbought_warning) warnings.push(`⚠️ Deviation rate ${data.bias_pct}% exceeds 5% — chasing highs is strictly prohibited`);
  if (!data.roe && !data.pe_ttm) warnings.push("Fundamental data incomplete");
  return { valid: !!data.price, warnings };
}
