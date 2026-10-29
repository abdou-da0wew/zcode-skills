/**
 * dividend.ts
 * Dividend analysis module (backed by the finance skill)
 * Ports the original scoring logic: safety score / CAGR / consecutive growth years / payout sustainability
 */

import { chatCompletions, MODEL } from "./dataFetcher";
import { DividendAnalysis, PayoutStatus, IncomeRating } from "./types";

// ── Core scoring logic (identical to the original) ────────

function calcPayoutStatus(payoutRatio: number | null): PayoutStatus {
  if (payoutRatio === null) return "unknown";
  if (payoutRatio < 40) return "safe";
  if (payoutRatio < 60) return "moderate";
  if (payoutRatio < 80) return "high";
  return "unsustainable";
}

function calcSafetyScore(data: {
  payoutRatio: number | null;
  dividendGrowth5y: number | null;
  consecutiveYears: number | null;
  dividendYield: number | null;
}): { score: number; factors: string[] } {
  let score = 50;
  const factors: string[] = [];

  // Payout ratio (±20)
  if (data.payoutRatio !== null) {
    if (data.payoutRatio < 40) { score += 20; factors.push(`Healthy payout ratio (${data.payoutRatio.toFixed(0)}%)`); }
    else if (data.payoutRatio < 60) { score += 10; factors.push(`Moderate payout ratio (${data.payoutRatio.toFixed(0)}%)`); }
    else if (data.payoutRatio < 80) { score -= 10; factors.push(`High payout ratio (${data.payoutRatio.toFixed(0)}%)`); }
    else { score -= 20; factors.push(`Unsustainable payout ratio (${data.payoutRatio.toFixed(0)}%)`); }
  }

  // 5-year growth rate (±15)
  if (data.dividendGrowth5y !== null) {
    if (data.dividendGrowth5y > 10) { score += 15; factors.push(`Strong dividend growth (${data.dividendGrowth5y.toFixed(1)}% CAGR)`); }
    else if (data.dividendGrowth5y > 5) { score += 10; factors.push(`Good dividend growth (${data.dividendGrowth5y.toFixed(1)}% CAGR)`); }
    else if (data.dividendGrowth5y > 0) { score += 5; factors.push(`Modest dividend growth (${data.dividendGrowth5y.toFixed(1)}% CAGR)`); }
    else { score -= 15; factors.push(`Declining dividend (${data.dividendGrowth5y.toFixed(1)}% CAGR)`); }
  }

  // Consecutive growth years (±15)
  if (data.consecutiveYears !== null) {
    if (data.consecutiveYears >= 25) { score += 15; factors.push(`Dividend aristocrat (${data.consecutiveYears} consecutive years of growth)`); }
    else if (data.consecutiveYears >= 10) { score += 10; factors.push(`Long-term stable dividend (${data.consecutiveYears} years)`); }
    else if (data.consecutiveYears >= 5) { score += 5; factors.push(`Stable dividend (${data.consecutiveYears} years)`); }
  }

  // High yield risk (-10)
  if (data.dividendYield !== null) {
    if (data.dividendYield > 8) { score -= 10; factors.push(`Yield too high (${data.dividendYield.toFixed(1)}%); verify sustainability`); }
    else if (data.dividendYield < 1) { factors.push(`Low yield (${data.dividendYield.toFixed(2)}%)`); }
  }

  return { score: Math.max(0, Math.min(100, score)), factors };
}

function calcIncomeRating(safetyScore: number): IncomeRating {
  if (safetyScore >= 80) return "excellent";
  if (safetyScore >= 60) return "good";
  if (safetyScore >= 40) return "moderate";
  return "poor";
}

// ── Fetch dividend data through the finance skill ────────

async function fetchDividendData(ticker: string): Promise<Record<string, any>> {
  const completion = await chatCompletions({
    model: MODEL,
    messages: [{
      role: "user",
      content: `Look up the dividend data for ${ticker}. Return JSON only, including:
name (company name), currentPrice (current share price),
dividendYield (annual dividend yield %), annualDividend (annual dividend per share),
trailingEps (trailing 12-month EPS),
exDividendDate (ex-dividend date in YYYY-MM-DD format),
paymentFrequency ("monthly"/"quarterly"/"annual", judged from the payout frequency),
dividendHistory (array of annual dividends for the last 5 years, each with year and total, sorted newest first),
consecutiveYears (number of consecutive years of dividend growth, integer),
dividendGrowth5y (5-year dividend CAGR %).
Fill missing fields with null; never fabricate data.`,
    }],
  });

  const raw = completion.choices[0]?.message?.content ?? "{}";
  return JSON.parse(raw.replace(/```json|```/g, "").trim());
}

// ── Main analysis function ────────────────────────────────

export async function analyzeDividend(ticker: string): Promise<DividendAnalysis> {
  ticker = ticker.toUpperCase();

  let raw: Record<string, any> = {};
  try {
    raw = await fetchDividendData(ticker);
  } catch (err: any) {
    return {
      ticker, name: ticker, currentPrice: null,
      dividendYield: null, annualDividend: null,
      payoutRatio: null, payoutStatus: "unknown",
      dividendGrowth5y: null, consecutiveYears: null,
      exDividendDate: null, paymentFrequency: null,
      safetyScore: 0, safetyFactors: [`Data fetch failed: ${err.message}`],
      incomeRating: "poor", dividendHistory: [],
      summary: `Failed to fetch dividend data for ${ticker}.`,
    };
  }

  // No dividend
  if (!raw.annualDividend || raw.annualDividend === 0) {
    return {
      ticker, name: raw.name ?? ticker,
      currentPrice: raw.currentPrice ?? null,
      dividendYield: null, annualDividend: null,
      payoutRatio: null, payoutStatus: "no_dividend",
      dividendGrowth5y: null, consecutiveYears: null,
      exDividendDate: null, paymentFrequency: null,
      safetyScore: 0, safetyFactors: ["This stock pays no dividend"],
      incomeRating: "no_dividend", dividendHistory: [],
      summary: `${ticker} currently pays no dividend.`,
    };
  }

  // Compute payout ratio
  const payoutRatio = (raw.trailingEps && raw.trailingEps > 0 && raw.annualDividend)
    ? parseFloat(((raw.annualDividend / raw.trailingEps) * 100).toFixed(1))
    : null;

  const payoutStatus = calcPayoutStatus(payoutRatio);
  const { score: safetyScore, factors: safetyFactors } = calcSafetyScore({
    payoutRatio,
    dividendGrowth5y: raw.dividendGrowth5y ?? null,
    consecutiveYears: raw.consecutiveYears ?? null,
    dividendYield: raw.dividendYield ?? null,
  });

  const incomeRating = calcIncomeRating(safetyScore);

  // Build summary
  const parts: string[] = [];
  if (raw.dividendYield) parts.push(`yield ${Number(raw.dividendYield).toFixed(2)}%`);
  if (payoutRatio) parts.push(`payout ratio ${payoutRatio.toFixed(0)}%`);
  if (raw.dividendGrowth5y) parts.push(`5-year growth ${Number(raw.dividendGrowth5y) > 0 ? "+" : ""}${Number(raw.dividendGrowth5y).toFixed(1)}%`);
  if (raw.consecutiveYears && raw.consecutiveYears >= 5) parts.push(`${raw.consecutiveYears} consecutive years of growth`);

  const ratingLabel: Record<IncomeRating, string> = {
    excellent: "excellent", good: "good", moderate: "moderate", poor: "poor", no_dividend: "no dividend",
  };

  return {
    ticker,
    name: raw.name ?? ticker,
    currentPrice: raw.currentPrice ?? null,
    dividendYield: raw.dividendYield ? Number(Number(raw.dividendYield).toFixed(2)) : null,
    annualDividend: raw.annualDividend ?? null,
    payoutRatio,
    payoutStatus,
    dividendGrowth5y: raw.dividendGrowth5y ? Number(Number(raw.dividendGrowth5y).toFixed(2)) : null,
    consecutiveYears: raw.consecutiveYears ?? null,
    exDividendDate: raw.exDividendDate ?? null,
    paymentFrequency: raw.paymentFrequency ?? null,
    safetyScore,
    safetyFactors,
    incomeRating,
    dividendHistory: raw.dividendHistory ?? [],
    summary: `${ticker} (${raw.name ?? ""}): ${parts.join(", ")}. Rating: ${ratingLabel[incomeRating]}`,
  };
}

// ── Formatted output (Markdown dashboard) ─────────────────

export function formatDividendMarkdown(analysis: DividendAnalysis): string {
  if (analysis.incomeRating === "no_dividend") {
    return `### 💰 Dividend Analysis · ${analysis.ticker}\n\nThis stock currently pays no dividend.`;
  }

  const ratingEmoji: Record<IncomeRating, string> = {
    excellent: "🏆", good: "✅", moderate: "⚠️", poor: "❌", no_dividend: "—",
  };

  const payoutLabel: Record<string, string> = {
    safe: "✅ Safe", moderate: "⚠️ Moderate", high: "⚠️ High", unsustainable: "❌ Unsustainable", unknown: "N/A",
  };

  let md = `### 💰 Dividend Analysis · ${analysis.ticker} (${analysis.name})

| Metric | Value |
|------|------|
| Dividend yield | ${analysis.dividendYield ? `${analysis.dividendYield}%` : "N/A"} |
| Annual dividend per share | ${analysis.annualDividend ? `$${analysis.annualDividend}` : "N/A"} |
| Payout frequency | ${analysis.paymentFrequency ?? "N/A"} |
| Ex-dividend date | ${analysis.exDividendDate ?? "N/A"} |
| Payout ratio | ${analysis.payoutRatio ? `${analysis.payoutRatio}% (${payoutLabel[analysis.payoutStatus]})` : "N/A"} |
| 5-year dividend growth | ${analysis.dividendGrowth5y ? `${analysis.dividendGrowth5y > 0 ? "+" : ""}${analysis.dividendGrowth5y}%` : "N/A"} |
| Consecutive growth years | ${analysis.consecutiveYears ?? "N/A"} |

**Safety score: ${analysis.safetyScore}/100 ${ratingEmoji[analysis.incomeRating]} Income rating: ${analysis.incomeRating.toUpperCase()}**

Scoring rationale:
${analysis.safetyFactors.map((f) => `- ${f}`).join("\n")}
`;

  if (analysis.dividendHistory.length > 0) {
    md += `\nRecent dividend history:\n`;
    md += analysis.dividendHistory.slice(0, 5).map((h) => `- ${h.year}: $${h.total}`).join("\n");
  }

  return md;
}

// ── Batch analysis ────────────────────────────────────────

export async function analyzeDividends(tickers: string[]): Promise<DividendAnalysis[]> {
  const results: DividendAnalysis[] = [];
  for (const ticker of tickers) {
    results.push(await analyzeDividend(ticker));
    await new Promise((r) => setTimeout(r, 200));
  }
  return results;
}
