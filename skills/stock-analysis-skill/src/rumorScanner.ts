/**
 * rumorScanner.ts
 * Rumor and early-signal scanner (backed by the platform finance skill)
 * Replaces the original Twitter bird CLI + Google News with finance-skill news + LLM extraction
 *
 * Scan scope: M&A rumors / insider trading / analyst actions / SEC & regulatory developments / early market signals
 */

import { chatCompletions, MODEL } from "./dataFetcher";
import { RumorItem, RumorScanResult, RumorType } from "./types";

// ── Scoring logic (ported from the original calculate_rumor_score) ──

function calcImpactScore(
  type: RumorType,
  text: string,
  hasHighEngagement = false
): { score: number; reason: string } {
  let score = 1;
  const reasons: string[] = [];

  switch (type) {
    case "ma":
      score += 5; reasons.push("M&A / acquisition rumor — largest market impact"); break;
    case "insider":
      score += 4; reasons.push("Insider trading signal — may foreshadow a major move"); break;
    case "analyst":
      score += 3; reasons.push("Analyst rating change — affects institutional pricing"); break;
    case "regulatory":
      score += 3; reasons.push("Regulatory development — directly affects operating compliance"); break;
    case "earnings":
      score += 2; reasons.push("Earnings expectation change"); break;
    default:
      score += 1;
  }

  if (/breaking|just in|alert|urgent/i.test(text)) {
    score += 2; reasons.push("Breaking news");
  }
  if (hasHighEngagement) {
    score += 2; reasons.push("High market attention");
  }

  return { score: Math.min(10, score), reason: reasons.join("; ") };
}

// ── Fetch market rumor news through the finance skill ────

async function fetchRumorNews(): Promise<string> {
  const completion = await chatCompletions({
    model: MODEL,
    messages: [{
      role: "user",
      content: `Fetch today's latest US-market items of the following types, at most 3 per type:
1. Merger/acquisition rumors
2. Insider buying/selling activity
3. Analyst rating changes (upgrades/downgrades)
4. SEC investigations or regulatory developments
5. Major earnings warnings or guidance raises

Return in JSON format, structured as:
[{
  "type": "ma|insider|analyst|regulatory|earnings",
  "ticker": "stock ticker or null",
  "headline": "headline",
  "source": "source",
  "sentiment": "positive|negative|neutral",
  "date": "YYYY-MM-DD"
}]
Return JSON only; only the latest items from today or the last 2 days; never fabricate.`,
    }],
  });
  return completion.choices[0]?.message?.content ?? "[]";
}

// ── LLM extraction of structured rumors from news ─────────

async function extractRumors(rawNews: string): Promise<RumorItem[]> {
  try {
    const parsed: any[] = JSON.parse(rawNews.replace(/```json|```/g, "").trim());

    return parsed.map((item) => {
      const type = (item.type as RumorType) ?? "general";
      const text = item.headline ?? "";
      const { score, reason } = calcImpactScore(type, text);

      return {
        type,
        ticker: item.ticker ?? null,
        headline: text,
        source: item.source ?? "finance",
        impactScore: score,
        impactReason: reason,
        sentiment: item.sentiment ?? "neutral",
        date: item.date ?? new Date().toISOString().slice(0, 10),
      } as RumorItem;
    }).sort((a, b) => b.impactScore - a.impactScore);
  } catch {
    return [];
  }
}

// ── Aggregate the most-discussed stocks ───────────────────

function aggregateTopTickers(rumors: RumorItem[]): { ticker: string; count: number }[] {
  const counts: Record<string, number> = {};
  for (const r of rumors) {
    if (r.ticker) {
      counts[r.ticker] = (counts[r.ticker] ?? 0) + 1;
    }
  }
  return Object.entries(counts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(([ticker, count]) => ({ ticker, count }));
}

// ── Main scan function ────────────────────────────────────

export async function scanRumors(): Promise<RumorScanResult> {
  const scannedAt = new Date().toISOString();

  let rumors: RumorItem[] = [];

  try {
    const rawNews = await fetchRumorNews();
    rumors = await extractRumors(rawNews);
  } catch (err: any) {
    console.error("[scanRumors] failed:", err.message);
  }

  const topTickers = aggregateTopTickers(rumors);

  // Build summary
  const maCount = rumors.filter((r) => r.type === "ma").length;
  const insiderCount = rumors.filter((r) => r.type === "insider").length;
  const analystCount = rumors.filter((r) => r.type === "analyst").length;

  const summary = rumors.length === 0
    ? "No major rumors or early signals today."
    : `Scanned ${rumors.length} signals: ${maCount} M&A rumors, ${insiderCount} insider moves, ${analystCount} analyst changes.${topTickers.length > 0 ? ` Most discussed: ${topTickers.slice(0, 3).map((t) => `$${t.ticker}`).join(", ")}.` : ""}`;

  return { scannedAt, rumors, topTickers, summary };
}

// ── Formatted output ──────────────────────────────────────

export function formatRumorMarkdown(result: RumorScanResult): string {
  const typeLabel: Record<RumorType, string> = {
    ma: "🏢 M&A Rumors",
    insider: "👔 Insider Moves",
    analyst: "📊 Analyst Changes",
    regulatory: "⚖️ Regulatory Developments",
    earnings: "📈 Earnings Expectations",
    general: "📰 Market Signals",
  };

  const sentimentEmoji: Record<string, string> = {
    positive: "🟢", negative: "🔴", neutral: "⚪",
  };

  let md = `## 🔮 Rumor & Early-Signal Scan
**Scan time:** ${new Date(result.scannedAt).toLocaleString("en-US")}
**${result.summary}**

`;

  if (result.rumors.length === 0) {
    md += "_No major rumors today._\n";
    return md;
  }

  // Group by type
  const grouped: Partial<Record<RumorType, RumorItem[]>> = {};
  for (const r of result.rumors) {
    if (!grouped[r.type]) grouped[r.type] = [];
    grouped[r.type]!.push(r);
  }

  for (const [type, items] of Object.entries(grouped)) {
    md += `### ${typeLabel[type as RumorType] ?? type}\n\n`;
    for (const item of items!.slice(0, 3)) {
      md += `**[Impact ${item.impactScore}/10]** ${sentimentEmoji[item.sentiment]} ${item.headline}\n`;
      if (item.ticker) md += `> Related ticker: $${item.ticker}\n`;
      md += `> Source: ${item.source} | ${item.date} | ${item.impactReason}\n\n`;
    }
  }

  // Buzz ranking
  if (result.topTickers.length > 0) {
    md += `### 📊 Rumor Buzz Ranking\n`;
    md += result.topTickers.map((t) =>
      `- $${t.ticker}: mentioned ${t.count} time(s)`
    ).join("\n");
    md += "\n";
  }

  return md;
}
