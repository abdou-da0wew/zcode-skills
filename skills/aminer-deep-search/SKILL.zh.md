---
name: aminer-deep-search
version: 2.0.0
author: AMiner
contact: report@aminer.cn
description: >
  Activate this skill when the user wants deep, multi-round academic paper collection for a survey or literature review.
  The host model (the model running this skill) drives the loop itself: it expands queries, judges relevance, snowballs backward references, and decides when to stop.
  The bundled scripts are pure tool commands that call documented AMiner Open Platform endpoints and print JSON tool results only — no extra LLM configuration is needed.
  Use this skill for broad topic exploration, survey bibliography construction, and collecting hundreds of candidate papers with AMiner IDs and titles.
  Not intended for single-paper lookup or lightweight recommendations; use aminer-free-academic or aminer-daily-paper for those.
metadata:
  {
    "openclaw":
      {
        "requires": {
          "bins": ["python3"],
          "env": ["AMINER_API_KEY"]
        },
        "primaryEnv": "AMINER_API_KEY"
      }
  }
---

# AMiner Deep Search

Host-model-driven survey paper collection. You (the model reading this) are the controller: run the tool scripts, read their JSON output, judge relevance yourself, and iterate until the collection target is met.

## Scope

- In scope: survey-grade literature collection (hundreds of papers), keyword expansion, backward citation snowballing.
- Out of scope: single-paper lookup or Q&A (use `aminer-free-academic`), personalized recommendations (use `aminer-daily-paper`).

## Pre-flight

1. Check the key (never print its value):

```bash
[ -z "${AMINER_API_KEY:-}" ] && echo "AMINER_API_KEY missing" || echo "AMINER_API_KEY exists"
```

If missing, stop and ask the user to set `AMINER_API_KEY` (console: https://open.aminer.cn/open/board?tab=control). Never print the key.

2. Confirm `topic` and `target-size` (default 400). If the planned rounds are estimated to cost ≥¥5, tell the user and get confirmation before starting.

## Tools

Both scripts live under `scripts/` in this skill directory. stdout carries exactly one JSON document (the tool result); diagnostics and the `[cost]` fee trail go to stderr. The scripts do no relevance scoring — that is your job.

### `scripts/aminer_api.py` — AMiner API calls

| Subcommand | Endpoint | Price |
|---|---|---|
| `search --query Q [--size 20] [--year YYYY] [--order n_citation\|year] [--max-pages 3]` | GET `/api/paper/search/pro` + free `paper/info` enrichment | ¥0.01/page |
| `qa-search [--query "natural language question"] [--topic-high '[["wordA","wordB"],["wordC"]]'] [--size 20] [--year-from Y] [--year-to Y] [--citation-sort]` | POST `/api/paper/qa/search` (fixed `use_topic=true`: with `use_topic=false` the backend ignores `query`) + free enrichment | ¥0.05/call |
| `info --ids id1 id2 ...` | POST `/api/paper/info` (≤100 ids per batch) | Free |
| `references --ids id1 id2 ... [--per-seed 20]` | GET `/api/paper/relation` per seed + free enrichment | ¥0.10/seed |

Output shape: `search`/`qa-search`/`info` output `[{id, title, year?, venue?, abstract_slice?}]`; `references` additionally carries `source_paper_ids` (which seeds cite that paper), and the seeds themselves are excluded from the results.

### `scripts/paper_set.py` — cross-round state file (no network)

The state file defaults to `outputs/paper_set.json` under the working directory.

```bash
# Pipe kept results in (can be chained right after a search), deduplicated by id
python3 scripts/aminer_api.py search --query "..." | python3 scripts/paper_set.py add
# → {"added": N, "duplicates": M, "total": T}

python3 scripts/paper_set.py stats     # totals, expanded_seeds, per-year distribution
python3 scripts/paper_set.py mark-expanded --ids id1 id2   # record already-snowballed seeds
python3 scripts/paper_set.py export -o outputs/final_papers.json
```

`add` also accepts `--ids id1 id2 ...` to add bare ids directly. Entries with `source_paper_ids` (from `references`) automatically mark the corresponding seed as expanded.

To filter before adding, read the search output first, then pipe only the kept entries:

```bash
printf '%s' '[{"id":"...","title":"..."}]' | python3 scripts/paper_set.py add
```

## Per-Round Protocol (core)

### Round 0 — planning

- Derive 4–8 seed queries from the topic: synonyms, subfields, method names, datasets/benchmarks, common English abbreviations.
- Estimate rounds and cost (search ≈ ¥0.01–0.05/call, references ≈ ¥0.10/seed). If the estimate is ≥¥5, confirm with the user first.

### Each round (up to 12 by default), fixed five steps

1. **Search**: run 1–4 `search` / `qa-search` calls against the pending queue. Prefer `search` (cheaper); use `qa-search` when the query is a natural-language question.
2. **Filter and add**: read the stdout results, judge topical relevance yourself, and pipe only the kept entries into `paper_set.py add`. Never add papers you consider off-topic.
3. **Check progress**: run `stats` to see totals and this round's increment.
4. **Snowball**: pick ≤5 strong seeds from this round's newly added relevant papers (high relevance, top-ranked with `--order n_citation`, not already in `expanded_seeds`) and run `references --ids ...`. Filter the output for relevance again before adding. Seeds with no addable output should be recorded with `mark-expanded`.
5. **Decide the next round**:
   - A search returned <5 results or poor quality → switch to one rephrased query (at most 2 variants per direction, then switch to snowballing);
   - references keep producing many relevant papers → keep snowballing from new seeds;
   - reached `target-size`, results exhausted, or 2 consecutive rounds added <5 papers → stop.

### Wrap-up

Run `export`, then report: final paper count, total cost (sum the `[cost]` lines from stderr), and the output file path.

## Rules

1. Never fabricate paper IDs or titles; only cite data actually returned by the tools.
2. Free-first: metadata always comes from the free `paper/info` endpoint (built into the scripts); never call the paid `paper/detail` for bulk metadata.
3. Do not dump raw tool output into the final answer; report only counts and the export file path.
4. Never print or log `AMINER_API_KEY`.
5. If AMiner returns fewer papers than the target, report the actual number honestly; do not fabricate.
