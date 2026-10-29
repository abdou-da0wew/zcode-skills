# Paper Enrichment Prompt

You are enriching academic papers with additional content before they are sent as chat cards.

For each paper in the `papers` array that is missing a summary (i.e., the `summary` field is empty or contains only placeholder text), generate:

1. **summary** — A concise summary (1-2 sentences, starting with "This paper..."). Describe the core contribution and significance. Keep established terms (e.g., RAG, LLM, Transformer) as-is.
2. **keywords** — 2-4 keywords. Keep well-known English acronyms as-is.
3. **comment** — If the paper's venue is a well-known conference/journal, annotate its tier, e.g., "Published in AAAI (CCF-A)". Leave empty if unknown.

Default output language is English. If your host/channel targets another language (e.g. Chinese), write the summary, keywords, and comment in that language instead — keep English technical terms as-is.

Rules:
- Do NOT fabricate information not present in the paper's title/abstract.
- Do NOT generate or modify `famous_authors`.
- If the abstract is missing or too short to summarize, write "Insufficient abstract information; please refer to the original paper."
- Preserve all other fields unchanged.

## Input

The papers are in `papers_summarized.json` at the path provided. The file structure:

```json
{
  "status": "success",
  "profile_topics": ["topic1", "topic2"],
  "papers": [
    {
      "title": "...",
      "summary": "...(may be missing)...",
      "keywords": ["kw1", "kw2"],
      "authors": ["..."],
      "comment": "",
      ...other fields preserved as-is...
    }
  ]
}
```

## Output

Write the enriched data back to the same `papers_summarized.json` path, preserving all fields. Only update `summary`, `keywords`, and `comment` for papers that need enrichment.
