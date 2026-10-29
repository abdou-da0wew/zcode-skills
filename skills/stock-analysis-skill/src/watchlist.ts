/**
 * watchlist.ts
 * Watchlist management + price alerts (persisted via the platform storage API)
 * Ports the original three alert types: target price / stop price / signal change
 */

import { chatCompletions, MODEL } from "./dataFetcher";
import { WatchlistItem, WatchlistAlert, Market, Verdict } from "./types";

const STORAGE_KEY = "watchlist-data";

// ── Storage wrapper ───────────────────────────────────────

async function loadWatchlist(): Promise<WatchlistItem[]> {
  try {
    const result = await (globalThis as any).storage?.get(STORAGE_KEY);
    if (result?.value) return JSON.parse(result.value) as WatchlistItem[];
  } catch {}
  return [];
}

async function saveWatchlist(items: WatchlistItem[]): Promise<void> {
  try {
    await (globalThis as any).storage?.set(STORAGE_KEY, JSON.stringify(items));
  } catch (err: any) {
    console.error("[watchlist] save failed:", err.message);
  }
}

// ── Fetch the current price ───────────────────────────────

async function fetchCurrentPrice(ticker: string): Promise<number | null> {
  try {
    const completion = await chatCompletions({
      model: MODEL,
      messages: [{
        role: "user",
        content: `Look up the current share price of ${ticker}. Return a single JSON: {"price": number} and nothing else.`,
      }],
    });
    const raw = completion.choices[0]?.message?.content ?? "{}";
    const parsed = JSON.parse(raw.replace(/```json|```/g, "").trim());
    return typeof parsed.price === "number" ? parsed.price : null;
  } catch {
    return null;
  }
}

function detectMarket(code: string): Market {
  if (/^\d{6}$/.test(code)) return "CN";
  if (/^\d{4,5}\.HK$/i.test(code)) return "HK";
  return "US";
}

// ── Add to watchlist ──────────────────────────────────────

export async function addToWatchlist(
  ticker: string,
  opts: {
    targetPrice?: number;
    stopPrice?: number;
    alertOnSignal?: boolean;
    notes?: string;
  } = {}
): Promise<{ success: boolean; action: string; message: string; item?: WatchlistItem }> {
  ticker = ticker.toUpperCase();
  const currentPrice = await fetchCurrentPrice(ticker);

  if (currentPrice === null) {
    return { success: false, action: "error", message: `Could not fetch the price of ${ticker}; please confirm the ticker is correct` };
  }

  const watchlist = await loadWatchlist();
  const existingIdx = watchlist.findIndex((i) => i.ticker === ticker);

  if (existingIdx >= 0) {
    // Update the existing record
    const existing = watchlist[existingIdx];
    if (opts.targetPrice !== undefined) existing.targetPrice = opts.targetPrice;
    if (opts.stopPrice !== undefined) existing.stopPrice = opts.stopPrice;
    if (opts.alertOnSignal !== undefined) existing.alertOnSignal = opts.alertOnSignal;
    if (opts.notes !== undefined) existing.notes = opts.notes;
    watchlist[existingIdx] = existing;
    await saveWatchlist(watchlist);

    return { success: true, action: "updated", message: `Updated the watchlist settings for ${ticker}`, item: existing };
  }

  // New entry
  const item: WatchlistItem = {
    ticker,
    market: detectMarket(ticker),
    addedAt: new Date().toISOString(),
    priceAtAdd: currentPrice,
    targetPrice: opts.targetPrice ?? null,
    stopPrice: opts.stopPrice ?? null,
    alertOnSignal: opts.alertOnSignal ?? false,
    lastSignal: null,
    lastCheck: null,
    notes: opts.notes ?? null,
  };

  watchlist.push(item);
  await saveWatchlist(watchlist);

  const alertDesc = [
    opts.targetPrice ? `target price $${opts.targetPrice}` : null,
    opts.stopPrice ? `stop price $${opts.stopPrice}` : null,
    opts.alertOnSignal ? "signal-change alert" : null,
  ].filter(Boolean).join(", ");

  return {
    success: true, action: "added",
    message: `Added ${ticker} to the watchlist (current price $${currentPrice}${alertDesc ? `, configured: ${alertDesc}` : ""})`,
    item,
  };
}

// ── Remove from watchlist ─────────────────────────────────

export async function removeFromWatchlist(
  ticker: string
): Promise<{ success: boolean; message: string }> {
  ticker = ticker.toUpperCase();
  const watchlist = await loadWatchlist();
  const filtered = watchlist.filter((i) => i.ticker !== ticker);

  if (filtered.length === watchlist.length) {
    return { success: false, message: `${ticker} is not in the watchlist` };
  }

  await saveWatchlist(filtered);
  return { success: true, message: `Removed ${ticker} from the watchlist` };
}

// ── List the watchlist ────────────────────────────────────

export async function listWatchlist(): Promise<{
  items: Array<WatchlistItem & {
    currentPrice: number | null;
    changePct: number | null;
    toTargetPct: number | null;
    toStopPct: number | null;
  }>;
  count: number;
}> {
  const watchlist = await loadWatchlist();
  if (!watchlist.length) return { items: [], count: 0 };

  const items = await Promise.all(watchlist.map(async (item) => {
    const currentPrice = await fetchCurrentPrice(item.ticker);

    const changePct = currentPrice && item.priceAtAdd
      ? parseFloat((((currentPrice - item.priceAtAdd) / item.priceAtAdd) * 100).toFixed(2))
      : null;

    const toTargetPct = currentPrice && item.targetPrice
      ? parseFloat((((item.targetPrice - currentPrice) / currentPrice) * 100).toFixed(2))
      : null;

    const toStopPct = currentPrice && item.stopPrice
      ? parseFloat((((item.stopPrice - currentPrice) / currentPrice) * 100).toFixed(2))
      : null;

    return { ...item, currentPrice, changePct, toTargetPct, toStopPct };
  }));

  return { items, count: items.length };
}

// ── Check alerts ──────────────────────────────────────────

export async function checkAlerts(
  currentSignals?: Record<string, Verdict>
): Promise<{ alerts: WatchlistAlert[]; count: number }> {
  const watchlist = await loadWatchlist();
  const alerts: WatchlistAlert[] = [];
  const now = new Date().toISOString();

  for (const item of watchlist) {
    const currentPrice = await fetchCurrentPrice(item.ticker);
    if (currentPrice === null) continue;

    // Target price alert
    if (item.targetPrice && currentPrice >= item.targetPrice) {
      alerts.push({
        ticker: item.ticker,
        alertType: "target_hit",
        message: `🎯 ${item.ticker} has reached its target price! Current $${currentPrice.toFixed(2)} ≥ target $${item.targetPrice}`,
        currentPrice,
        triggerValue: item.targetPrice,
        timestamp: now,
      });
    }

    // Stop price alert
    if (item.stopPrice && currentPrice <= item.stopPrice) {
      alerts.push({
        ticker: item.ticker,
        alertType: "stop_hit",
        message: `🛑 ${item.ticker} has hit its stop price! Current $${currentPrice.toFixed(2)} ≤ stop $${item.stopPrice}`,
        currentPrice,
        triggerValue: item.stopPrice,
        timestamp: now,
      });
    }

    // Signal change alert
    if (item.alertOnSignal && currentSignals?.[item.ticker]) {
      const newSignal = currentSignals[item.ticker];
      if (item.lastSignal && newSignal !== item.lastSignal) {
        alerts.push({
          ticker: item.ticker,
          alertType: "signal_change",
          message: `📊 ${item.ticker} signal change: ${item.lastSignal} → ${newSignal}`,
          currentPrice,
          triggerValue: `${item.lastSignal} → ${newSignal}`,
          timestamp: now,
        });
      }
      // Update the latest signal
      item.lastSignal = newSignal;
    }

    item.lastCheck = now;
  }

  // Save the updated lastSignal and lastCheck
  await saveWatchlist(watchlist);

  return { alerts, count: alerts.length };
}

// ── Format the watchlist (Markdown) ───────────────────────

export function formatWatchlistMarkdown(data: Awaited<ReturnType<typeof listWatchlist>>): string {
  if (data.count === 0) {
    return `## 📋 Watchlist\n\n_The watchlist is empty. Use \`/stock_watch AAPL\` to add a stock._\n`;
  }

  let md = `## 📋 Watchlist (${data.count} total)\n\n`;
  md += `| Ticker | Current | vs. Entry | Target | Stop | To Target | Latest Signal |\n`;
  md += `|------|--------|--------|--------|--------|--------|----------|\n`;

  for (const item of data.items) {
    const price = item.currentPrice ? `$${item.currentPrice.toFixed(2)}` : "N/A";
    const change = item.changePct !== null
      ? `${item.changePct > 0 ? "🟢+" : "🔴"}${item.changePct.toFixed(2)}%`
      : "—";
    const target = item.targetPrice ? `$${item.targetPrice}` : "—";
    const stop = item.stopPrice ? `$${item.stopPrice}` : "—";
    const toTarget = item.toTargetPct !== null ? `${item.toTargetPct > 0 ? "+" : ""}${item.toTargetPct.toFixed(1)}%` : "—";
    const signal = item.lastSignal ?? "—";

    md += `| ${item.ticker} | ${price} | ${change} | ${target} | ${stop} | ${toTarget} | ${signal} |\n`;
  }

  // Triggered alerts
  const triggered = data.items.filter(
    (i) => (i.targetPrice && i.currentPrice && i.currentPrice >= i.targetPrice) ||
            (i.stopPrice && i.currentPrice && i.currentPrice <= i.stopPrice)
  );

  if (triggered.length > 0) {
    md += `\n### ⚡ Triggered Alerts\n`;
    for (const item of triggered) {
      if (item.targetPrice && item.currentPrice && item.currentPrice >= item.targetPrice) {
        md += `- 🎯 **${item.ticker}** reached its target price $${item.targetPrice}\n`;
      }
      if (item.stopPrice && item.currentPrice && item.currentPrice <= item.stopPrice) {
        md += `- 🛑 **${item.ticker}** hit its stop $${item.stopPrice}\n`;
      }
    }
  }

  return md;
}

// ── Format alert results (Markdown) ───────────────────────

export function formatAlertsMarkdown(result: Awaited<ReturnType<typeof checkAlerts>>): string {
  if (result.count === 0) {
    return `## 🔔 Watchlist Alert Check\n\n_No alerts triggered at the moment._\n`;
  }

  let md = `## 🔔 Watchlist Alerts (${result.count} triggered)\n\n`;
  for (const alert of result.alerts) {
    md += `- ${alert.message}\n`;
  }
  return md;
}
