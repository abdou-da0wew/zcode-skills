---
name: gaokao-generate-report
description: >-
  Merges student info, the volunteer list, major recommendations, and school
  recommendations into a combined analysis and renders an HTML gaokao application report
  with the reach/match/safety volunteer list. Use it for gaokao application report
  generation, producing the final application plan, or visualizing the volunteer table.
---

# Generate the Application Report

This skill is **step five** of the pipeline: merge the preceding JSON files and render the HTML report.

## Pipeline position

- **Upstream**:
  - `parsed.json` (volunteer list)
  - `major_recommendation.json` (major recommendations)
  - `school_recommendation.json` (school recommendations)
- **Output**: `volunteer_report.html`

## Environment setup

```bash
cd gaokao-generate-report
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Steps

### 1. Merge into analysis.json

```bash
python3 scripts/merge_analysis.py \
  --majors output/major_recommendation.json \
  --schools output/school_recommendation.json \
  -o output/analysis.json
```

`merge_analysis.py` merges the major and school recommendations into the `analysis.json` structure required by `generate_html.py`.

### 2. Generate the HTML

```bash
python3 scripts/generate_html.py \
  -i output/parsed.json \
  -a output/analysis.json \
  -o output/volunteer_report.html
```

### 3. Deliver to the user

Provide the **absolute path** to `volunteer_report.html` and briefly explain the report structure:

1. **Overall assessment & advice** (major directions + school strategy)
2. **Volunteer recommendation list** (Reach / Match / Safety; 👍 recommended school / 🔥 recommended major badges open detail modals on click)

> Tier labels come from the API's `type` codes: `CHONG` = Reach, `WEN` = Match, `BAO` = Safety, `NAN` = Difficult, `YI` = Easy.

## Pre-merge checklist

| Check | Description |
|-------|-------------|
| Major fields consistent | `recommended_majors` name/code match `parsed.json` exactly |
| School fields consistent | `recommended_schools` name/code match `parsed.json` exactly |
| Copy complete | `intro`, `strategy`, `school_strategy` are non-empty |

If any recommendation fields do not match before merging, go back to the corresponding skill and fix the JSON first.

## Additional resources

- [examples/analysis_merged_example.json](examples/analysis_merged_example.json) — complete example of the merged structure
