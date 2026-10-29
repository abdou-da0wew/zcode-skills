/**
 * index.ts — skill main entry
 *
 * Supported commands:
 *   run()              — single-stock analysis (main flow)
 *   runDividend()      — dividend analysis
 *   runRumorScan()     — rumor scan
 *   runWatchlistAdd()  — add a stock to the watchlist
 *   runWatchlistList() — list the watchlist
 *   runWatchlistCheck()— check alerts
 *   runWatchlistRemove()— remove a stock from the watchlist
 *   runChartAnalysis() — K-line chart analysis
 *
 * Works with any OpenAI-compatible LLM server (Ollama, vLLM, LM Studio, OpenRouter, ...):
 * configure via the LLM_BASE_URL / LLM_API_KEY / LLM_MODEL environment variables.
 */

import { fetchMultipleStocks, fetchMarketOverview, fetchGlobalMacro, chatCompletions, MODEL } from "./dataFetcher";
import { analyzeMultipleStocks, analyzeChartImage } from "./analyzer";
import { analyzeDividends, formatDividendMarkdown } from "./dividend";
import { scanRumors, formatRumorMarkdown } from "./rumorScanner";
import {
  addToWatchlist, removeFromWatchlist,
  listWatchlist, checkAlerts,
  formatWatchlistMarkdown, formatAlertsMarkdown,
} from "./watchlist";
import { SkillInput, StockInput, OutputFormat, AnalysisResult, PositionInfo, Verdict } from "./types";

// ── Input parsing ─────────────────────────────────────────

function parseInput(raw: unknown): {
  stocks: string[];
  positions: Record<string, PositionInfo>;
  outputFormat: OutputFormat;
  mode: "full" | "quote";
  includeMarketReview: boolean;
  includeGlobalMacro: boolean;
  includeDividend: boolean;
} {
  const stocks: string[] = [];
  const positions: Record<string, PositionInfo> = {};
  let outputFormat: OutputFormat = "markdown";
  let mode: "full" | "quote" = "full";
  let includeMarketReview = false;
  let includeGlobalMacro = true;
  let includeDividend = false;

  if (typeof raw === "string") {
    raw.split(/[,\s]+/).map((s) => s.trim().toUpperCase()).filter(Boolean).forEach((c) => stocks.push(c));
  } else if (typeof raw === "object" && raw !== null) {
    const input = raw as any;
    const rawStocks: (string | StockInput)[] = input.stocks ?? (input.stock ? [input.stock] : []);
    for (const s of rawStocks) {
      if (typeof s === "string") stocks.push(s.trim().toUpperCase());
      else if (s.code) {
        const code = s.code.trim().toUpperCase();
        stocks.push(code);
        if (s.position) positions[code] = s.position;
      }
    }
    outputFormat = input.outputFormat ?? input.format ?? "markdown";
    mode = input.mode ?? "full";
    includeMarketReview = input.includeMarketReview ?? false;
    includeGlobalMacro = input.includeGlobalMacro ?? true;
    includeDividend = input.includeDividend ?? false;
  }

  return { stocks, positions, outputFormat, mode, includeMarketReview, includeGlobalMacro, includeDividend };
}

function log(msg: string) { console.log(`[${new Date().toISOString()}] ${msg}`); }

// ── Report assembly ───────────────────────────────────────

function buildFullReport(
  results: AnalysisResult[],
  globalMacro?: string,
  marketOverview?: string
): string {
  const date = new Date().toLocaleDateString("en-US");
  const buy   = results.filter((r) => ["Buy", "Strong Buy"].includes(r.verdict)).length;
  const watch = results.filter((r) => r.verdict === "Hold").length;
  const sell  = results.filter((r) => r.verdict === "Sell").length;

  let output = `# 📈 Stock Intelligence Analysis Report
**Generated:** ${date} | **${results.length} stock(s) analyzed** | 🟢 Buy/Strong Buy ${buy} 🟡 Hold ${watch} 🔴 Sell ${sell}

`;
  if (globalMacro) output += `---\n\n## 🌍 Global Macro Snapshot\n\n${globalMacro}\n\n`;
  if (marketOverview) output += `---\n\n## 🎯 Market Overview\n\n${marketOverview}\n\n`;
  output += `---\n\n## 📊 Per-Stock Decision Dashboards\n\n`;
  output += results.map((r) => {
    const warn = r.warnings.length > 0 ? `\n> ⚠️ **Warning:** ${r.warnings.join(" | ")}\n` : "";
    return `${warn}\n${r.analysis}\n\n---\n`;
  }).join("\n");

  return output;
}

// ── Call the pdf/docx skills ──────────────────────────────

async function exportToFormat(content: string, format: "pdf" | "word"): Promise<string> {
  const isPDF = format === "pdf";
  const completion = await chatCompletions({
    model: MODEL,
    messages: [{
      role: "user",
      content: isPDF
        ? `Create a PDF document from the following stock research report. Requirements: A4 pages, English text, one page break per stock, color-coded verdicts, and a disclaimer at the end.\n\n${content}`
        : `Create a Word (.docx) document from the following stock research report. Requirements: preserve heading hierarchy, one page break per stock, render the battle plan as a table, and add a disclaimer at the end.\n\n${content}`,
    }],
  });
  return completion.choices[0]?.message?.content ?? `${isPDF ? "PDF" : "Word"} generation complete`;
}

// ══════════════════════════════════════════════════════════
// Main flow: single-stock analysis
// ══════════════════════════════════════════════════════════

export async function run(rawInput: unknown): Promise<{
  success: boolean; format: OutputFormat; content: string;
  summary: { total: number; buy: number; watch: number; sell: number; errors: number };
  error?: string;
}> {
  let parsed: ReturnType<typeof parseInput>;
  try { parsed = parseInput(rawInput); }
  catch (err: any) {
    return { success: false, format: "markdown", content: `❌ Input parsing failed: ${err.message}`,
      summary: { total: 0, buy: 0, watch: 0, sell: 0, errors: 0 }, error: err.message };
  }

  const { stocks, positions, outputFormat, mode, includeMarketReview, includeGlobalMacro, includeDividend } = parsed;
  if (!stocks.length) return { success: false, format: outputFormat, content: "❌ No stock tickers provided",
    summary: { total: 0, buy: 0, watch: 0, sell: 0, errors: 0 } };

  log(`Analyzing ${stocks.length} stock(s): ${stocks.join(", ")} | format: ${outputFormat}`);

  // Fetch macro data in parallel
  let globalMacro: string | undefined;
  let marketOverview: string | undefined;
  await Promise.all([
    includeGlobalMacro ? fetchGlobalMacro().then((r) => { globalMacro = r; }) : Promise.resolve(),
    includeMarketReview ? fetchMarketOverview().then((r) => { marketOverview = r; }) : Promise.resolve(),
  ]);

  // Fetch per-stock data
  let stockDataList;
  try {
    stockDataList = await fetchMultipleStocks(stocks, mode);
    log(`Data complete: ${stockDataList.filter((d) => !d.error).length}/${stocks.length}`);
  } catch (err: any) {
    return { success: false, format: outputFormat, content: `❌ Data fetch failed: ${err.message}`,
      summary: { total: stocks.length, buy: 0, watch: 0, sell: 0, errors: stocks.length }, error: err.message };
  }

  // LLM analysis
  const analysisResults = await analyzeMultipleStocks(stockDataList, outputFormat, positions, includeDividend);

  // Check watchlist signal changes (if any)
  const signals: Record<string, Verdict> = {};
  for (const r of analysisResults) signals[r.code] = r.verdict;
  await checkAlerts(signals).catch(() => {}); // silent update; does not block the main flow

  // Generate the report
  let content: string;
  try {
    const markdown = buildFullReport(analysisResults, globalMacro, marketOverview);
    if (outputFormat === "pdf") content = await exportToFormat(markdown, "pdf");
    else if (outputFormat === "word") content = await exportToFormat(markdown, "word");
    else content = markdown;
  } catch (err: any) {
    return { success: false, format: outputFormat, content: `❌ Report generation failed: ${err.message}`,
      summary: { total: stocks.length, buy: 0, watch: 0, sell: 0, errors: stocks.length }, error: err.message };
  }

  const summary = {
    total: analysisResults.length,
    buy: analysisResults.filter((r) => ["Buy", "Strong Buy"].includes(r.verdict)).length,
    watch: analysisResults.filter((r) => r.verdict === "Hold").length,
    sell: analysisResults.filter((r) => r.verdict === "Sell").length,
    errors: stockDataList.filter((d) => d.error).length,
  };

  log(`Done ✅ Buy:${summary.buy} Hold:${summary.watch} Sell:${summary.sell}`);
  return { success: true, format: outputFormat, content, summary };
}

// ══════════════════════════════════════════════════════════
// Dividend analysis
// ══════════════════════════════════════════════════════════

export async function runDividend(tickers: string | string[]): Promise<string> {
  const codes = Array.isArray(tickers) ? tickers : tickers.split(/[,\s]+/).filter(Boolean);
  log(`Dividend analysis: ${codes.join(", ")}`);
  const results = await analyzeDividends(codes.map((c) => c.toUpperCase()));

  let output = `# 💰 Dividend Analysis Report\n**Generated:** ${new Date().toLocaleDateString("en-US")}\n\n---\n\n`;
  for (const r of results) output += formatDividendMarkdown(r) + "\n\n---\n\n";
  output += "_The data above is for reference only and does not constitute investment advice._";
  return output;
}

// ══════════════════════════════════════════════════════════
// Rumor scan
// ══════════════════════════════════════════════════════════

export async function runRumorScan(): Promise<string> {
  log("Starting rumor scan...");
  const result = await scanRumors();
  return formatRumorMarkdown(result);
}

// ══════════════════════════════════════════════════════════
// Watchlist management
// ══════════════════════════════════════════════════════════

export async function runWatchlistAdd(
  ticker: string,
  opts: { targetPrice?: number; stopPrice?: number; alertOnSignal?: boolean; notes?: string } = {}
): Promise<string> {
  const result = await addToWatchlist(ticker, opts);
  return result.message;
}

export async function runWatchlistRemove(ticker: string): Promise<string> {
  const result = await removeFromWatchlist(ticker);
  return result.message;
}

export async function runWatchlistList(): Promise<string> {
  const data = await listWatchlist();
  return formatWatchlistMarkdown(data);
}

export async function runWatchlistCheck(): Promise<string> {
  const result = await checkAlerts();
  return formatAlertsMarkdown(result);
}

// ══════════════════════════════════════════════════════════
// K-line chart analysis
// ══════════════════════════════════════════════════════════

export async function runChartAnalysis(
  stockCode: string,
  imageUrlOrBase64: string,
  isBase64 = false
): Promise<{ success: boolean; content: string }> {
  try {
    const result = await analyzeChartImage(imageUrlOrBase64, stockCode, isBase64);
    return { success: true, content: result };
  } catch (err: any) {
    return { success: false, content: `K-line chart analysis failed: ${err.message}` };
  }
}

// ══════════════════════════════════════════════════════════
// CLI debugging
// ══════════════════════════════════════════════════════════

async function cli() {
  const args = process.argv.slice(2);
  const cmd = args[0];

  if (!cmd || cmd === "--help") {
    console.log(`
Stock Analysis Skill CLI

Commands:
  analyze <ticker,...> [markdown|pdf|word] [--market-review] [--dividend]
  dividend <ticker,...>
  rumors
  watch add <ticker> [--target price] [--stop price] [--signal]
  watch remove <ticker>
  watch list
  watch check

Examples:
  ts-node src/index.ts analyze 600519,00700.HK,AAPL
  ts-node src/index.ts analyze AAPL --dividend
  ts-node src/index.ts dividend JNJ PG KO
  ts-node src/index.ts rumors
  ts-node src/index.ts watch add AAPL --target 200 --stop 150
  ts-node src/index.ts watch list

Environment variables:
  LLM_BASE_URL   OpenAI-compatible endpoint (default: http://localhost:11434/v1)
  LLM_API_KEY    API key, if your server requires one
  LLM_MODEL      model name (default: qwen2.5)
    `);
    process.exit(0);
  }

  if (cmd === "analyze") {
    const codes = (args[1] ?? "").split(",").map((s) => s.trim()).filter(Boolean);
    const format = (["markdown", "pdf", "word"].find((f) => args.includes(f)) as OutputFormat) ?? "markdown";
    const includeMarketReview = args.includes("--market-review");
    const includeDividend = args.includes("--dividend");
    const result = await run({ stocks: codes, outputFormat: format, includeMarketReview, includeDividend });
    console.log(result.content);
    console.log("\n📊 Summary:", result.summary);

  } else if (cmd === "dividend") {
    const codes = args.slice(1).filter((a) => !a.startsWith("--"));
    console.log(await runDividend(codes));

  } else if (cmd === "rumors") {
    console.log(await runRumorScan());

  } else if (cmd === "watch") {
    const sub = args[1];
    if (sub === "add") {
      const ticker = args[2];
      const targetIdx = args.indexOf("--target");
      const stopIdx = args.indexOf("--stop");
      console.log(await runWatchlistAdd(ticker, {
        targetPrice: targetIdx >= 0 ? Number(args[targetIdx + 1]) : undefined,
        stopPrice: stopIdx >= 0 ? Number(args[stopIdx + 1]) : undefined,
        alertOnSignal: args.includes("--signal"),
      }));
    } else if (sub === "remove") {
      console.log(await runWatchlistRemove(args[2]));
    } else if (sub === "list") {
      console.log(await runWatchlistList());
    } else if (sub === "check") {
      console.log(await runWatchlistCheck());
    }
  }
}

if (require.main === module) {
  cli().catch((err) => { console.error(err); process.exit(1); });
}
