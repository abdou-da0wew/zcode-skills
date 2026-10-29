---
name: ai-news-collector
description: AI news aggregation and buzz-ranking tool. Triggers when the user asks about the latest happenings in AI, e.g. "Any AI news today?", "Summarize this week's AI developments", "Any hot new AI products lately?", "What is the AI community talking about?". Coverage: new product launches, research papers, industry news, funding announcements, open-source project updates, community viral phenomena, trending AI tools/agent projects. Outputs an English summary list ranked by buzz, with links to the original sources.
---

# AI News Collector

Collect, aggregate, and rank AI news by buzz.

## Core Principle

**Do not just search "AI news today".** Generic searches return SEO aggregator pages and trend-prediction articles, and systematically miss community-level viral phenomena (e.g. open-source tools blowing up, meme-level events). You must use a multi-dimensional, layered search strategy.

## Workflow

### 1. Multi-dimensional layered search (minimum 8 searches, 10-12 recommended)

Run searches across the following **6 dimensions**, at least once per dimension:

#### Dimension A: Weekly roundups / newsletters (top priority 🔑)

These are the highest-density sources — a single article can cover 10+ news items.

```
Search terms:
- "last week in AI" [current month year]
- "AI weekly roundup" [current month year]
- "the batch AI newsletter"
- site:substack.com AI news [current month]
```

After finding a roundup, use web_fetch to get the full text and extract every news lead from it.

#### Dimension B: Community buzz / virality (key dimension 🔑)

Capture bottom-up community hits — generic searches almost never reach this layer.

```
Search terms:
- "viral AI tool" OR "viral AI agent"
- "AI trending" site:reddit.com OR site:news.ycombinator.com
- "GitHub trending AI" OR "AI open source trending"
- AI buzzing OR "everyone is talking about" AI
- "most popular AI" this week
```

#### Dimension C: Product launches and model updates

```
Search terms:
- "AI model release" OR "LLM launch" [current month]
- "AI product launch" [current month year]
- OpenAI OR Anthropic OR Google OR Meta AI announcement
- Chinese-language coverage: search jiqizhixin.com / qbitai.com with localized terms for "large model release" or "new AI product"
```

#### Dimension D: Funding and business

```
Search terms:
- "AI startup funding" [current month year]
- "AI acquisition" OR "AI IPO"
- Chinese-language coverage: localized terms for "AI funding" or "AI investment"
```

#### Dimension E: Research breakthroughs

```
Search terms:
- "AI breakthrough" OR "AI paper" [current month]
- "state of the art" machine learning
- Chinese-language coverage: localized terms for "AI paper" or "machine learning breakthrough"
```

#### Dimension F: Regulation and policy

```
Search terms:
- "AI regulation" OR "AI policy" [current month year]
- "AI law" OR "AI governance"
- Chinese-language coverage: localized terms for "AI regulation" or "AI act"
```

### 2. Cross-validation and gap-filling

After the first round of searches, check for gaps:

- If a newsletter mentioned a project/event that the first round did not cover → run a dedicated search for that project
- If the same event is mentioned by 3+ different sources → it is very likely a hot topic; dig deeper for more details
- If Chinese-language and English-language media highlight completely different stories → cover both sides

### 3. Search keyword design principles (anti-pattern checklist)

| ❌ Don't search like this | ✅ Search like this | Why |
|---|---|---|
| "AI news today February 2026" | "AI weekly roundup February 2026" | The former returns aggregator pages; the latter returns curated content |
| "AI news today" | "viral AI tool" + "AI model release" searched separately | Generic searches cannot cover community phenomena |
| "artificial intelligence breaking news" | Search by dimension | Too broad, returns noise |
| Adding an exact year-month-day to the query | Use "this week" "today" "latest" | Exact dates skew toward prediction/outlook articles |
| Writing after only 3 searches | At least 8 searches across 6 dimensions | 3 searches cover less than 30% |

### 4. Overall buzz assessment

Rate each news item's buzz (1-5 stars) based on these signals:

| Signal | Weight | Notes |
|------|------|------|
| Multiple outlets reporting the same event | ⭐⭐⭐ High | 3+ sources = confirmed hot topic |
| Evidence of community virality | ⭐⭐⭐ High | GitHub stars surging, Twitter flooded, HN front page |
| From an authoritative source (top conference, major vendor announcement) | ⭐⭐⭐ High | But note: vendor PR ≠ real buzz |
| Actual user experience reports | ⭐⭐ Medium | People actually using it > just announced |
| Technical significance / scope of impact | ⭐⭐ Medium | |
| Controversy (safety, ethics debates) | ⭐⭐ Medium | Controversy often signals high impact |
| Recency (newer = hotter) | ⭐ Low-Medium | Secondary ranking factor |

### 5. Output format

Sort by buzz, descending, and output **15-25 items**:

```
## 🔥 AI News Digest (YYYY-MM-DD)

### ⭐⭐⭐⭐⭐ Highest buzz

1. **[News title]**
   > One-sentence summary (50 characters max)
   > 🔗 [Source name](URL)

### ⭐⭐⭐⭐ High buzz

2. ...

### ⭐⭐⭐ Medium buzz

...

---
📊 Collected XX news items | XX searches | Dimensions covered: A/B/C/D/E/F | Updated: HH:MM
```

### 6. Deduplication and merging

- When the same event is reported by multiple outlets, merge into one entry and pick the most authoritative/detailed source
- Note "reported by multiple outlets" in the summary to signal the buzz level
- Renamed projects count as the same event (e.g. Clawdbot → Moltbot → OpenClaw)

## Recommended news sources

See [references/sources.md](references/sources.md).

## Notes

- Prefer HTTPS links
- For paywalled/inaccessible content, mark it as "subscription required"
- Stay objective; do not editorialize about the news content
- Do not start writing until you have run at least 8 searches
- If a dimension returns empty results, re-run it with different keywords
