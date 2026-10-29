---
name: gaokao-fetch-volunteers
description: >-
  Calls the smart gaokao volunteer recommendation API with the student's basic info and
  major/city/university preferences (mapped to optional API parameters) to fetch the
  reach/match/safety volunteer list and parse it into parsed.json. Use it to fetch
  recommended universities, build the reach/match/safety volunteer list, or call the
  volunteer API.
---

# Fetch Recommended Volunteers

This skill is **step two** of the pipeline: read `student.json`, **extract the student's
preferences and map them to optional API parameters**, call the volunteer API, and output
`parsed.json`.

> **Exact API string values:** the API expects Chinese string values for `province`,
> `classify`, `subjects`, `batch`, `gradeType`, `universitys`, `provinces`, `tags`, and
> `majorClass`. Docs below show them as JSON `\uXXXX` escapes
> (e.g. `"\u5c71\u4e1c"` = Shandong). Write them exactly like that (or as the equivalent
> UTF-8 characters). See [reference.md](reference.md) for the full value table.

## Pipeline position

- **Upstream**: [gaokao-collect-student-info](../gaokao-collect-student-info/SKILL.md) → `student.json`
- **Downstream**: [gaokao-recommend-majors](../gaokao-recommend-majors/SKILL.md), [gaokao-recommend-schools](../gaokao-recommend-schools/SKILL.md), [gaokao-generate-report](../gaokao-generate-report/SKILL.md)

## Environment setup

```bash
cd gaokao-fetch-volunteers
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Steps

### 1. Extract preferences from the auxiliary info (agent-required)

Read `student.json` and, following [preference_mapping.md](preference_mapping.md), complete/write the following fields:

| Field | Mapped to API |
|-------|---------------|
| `preferred_universities` | `universitys` |
| `preferred_provinces` / `preferred_cities` | `provinces` |
| `preferred_tags` | `tags` |
| `preferred_major_classes` | `majorClass` |

Extraction sources: `interests`, `career_direction`, `preferred_cities`, `notes`, and any university/major/tier preferences stated in the conversation.

If step 1 (collection) already wrote them in a structured form, verify and complete them here; **the preference fields must not be empty arrays when calling the API** (unless the student has no preferences).

### 2. Build the API request

```bash
python3 scripts/build_api_request.py \
  -i output/student.json \
  -o output/api_request.json \
  --summary output/preference_summary.json
```

The script converts `preferred_*` into optional API parameters; `preferred_cities` are automatically resolved into `provinces` (see `preference_mapping.md`).

`build_api_request.py` calls `province_config.validate_classify` to verify that `classify` matches the province's subject-combination mode.

### 2.5 Pre-flight parameter check (required)

Before calling the API, verify `student.json` / `api_request.json` against [reference.md](reference.md):

| Check | Rule |
|-------|------|
| `classify` | Xinjiang → liberal arts/science; 3+1+2 provinces → physics/history; 3+3 provinces → comprehensive. **A wrong value makes the batch list empty** |
| `subjects` | 3+1+2: **all three subjects** (primary + two electives, e.g. `"\u7269\u7406,\u5316\u5b66,\u751f\u7269"`); 3+3: all three; Xinjiang: do not send; Beijing/Shanghai/Tianjin vocational is handled by the script |
| `gradeType` | **Only Beijing/Shanghai/Tianjin** send undergraduate or vocational; all other provinces must be `null` or omitted |
| `score` | Required for Xinjiang (no score-rank table there; a rank alone cannot be reverse-mapped) |
| `batch` | May use the generic `"\u672c\u79d1\u6279"` (undergraduate) / `"\u4e13\u79d1\u6279"` (vocational); batch/list resolves it into the province's specific batch name |
| Tibet | Not supported by the test environment; fall back to the collection step and inform the user |

**Batch**: the user-facing value may be the generic `"\u672c\u79d1\u6279"` / `"\u4e13\u79d1\u6279"`; the script resolves the province-specific batch name via batch/list (e.g. Shandong → `"\u666e\u901a\u7c7b\u4e00\u6bb5"`). If the API fails, use the static fallback table in [reference.md](reference.md).

### 3. Call the volunteer API (two phases: batch list → volunteer list)

```bash
python3 scripts/fetch_volunteers.py \
  --config output/api_request.json \
  -o output/parsed.json
```

Or in one step (built-in request construction):

```bash
python3 scripts/fetch_volunteers.py \
  --student output/student.json \
  -o output/parsed.json
```

The script first calls `batch/list` to resolve the specific `batch` and `volunteerType` from score and subjects, then requests the volunteer recommendation endpoint. Parameter normalization is handled automatically by `scripts/province_config.py`. Pass `--no-auto-batch` to disable auto resolution.

**Two-phase SOP**:

```
1. GET  batch/list  →  province-specific batches + volunteerType
2. POST intelligenceVolunteer  →  fetch volunteers with the selected batch / volunteerType
```

Beijing/Shanghai/Tianjin also need `gradeType` in phase 1 (the script infers it from score / batch).

### 4. Explain to the user

Using `preference_summary.json` and the `stats` in `parsed.json`, explain:

- Which preference parameters were sent (universities / provinces / tiers / major classes)
- How many universities fall into reach / match / safety

## Optional API parameters

| API field | Meaning | Source |
|-----------|---------|--------|
| `universitys` | Desired universities | `preferred_universities` |
| `provinces` | Province preferences | `preferred_provinces`, or derived from cities |
| `tags` | University attributes | `preferred_tags` (985/211, etc.) |
| `majorClass` | Major-class preferences | `preferred_major_classes` |

Full API documentation: [reference.md](reference.md).

## Output structure (parsed.json)

| Field | Description |
|-------|-------------|
| `profile` | Echo of the parameters sent, including optional ones |
| `stats` | Reach / match / safety counts |
| `schools_by_type` | Schools grouped by tier |
| `request` | The actual API request body (including preference parameters) |
| `batch_resolution` | Batch resolution source, selected item, and available options |

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Recommendations don't match preferences | Check the optional parameters in `api_request.json` |
| No fillable batch | See [reference.md](reference.md); confirm `classify` matches the province's mode |
| Batch list is empty | Wrong `classify` (e.g. physics sent for a 3+3 province) — the script reports this explicitly |
| Tibet students | Not supported by the test environment; switch province or wait for platform support |
| Volunteer API returns 500 | Check reference: is `gradeType`/`subjects` correct for the province |
| Missing `subjects` | Required for 3+3/3+1+2; except Xinjiang and Beijing/Shanghai/Tianjin vocational |
| Only two subjects sent | 3+1+2 requires **all three subjects** (including physics/history); never only chemistry + biology |
| Preferences not applied | Confirm `preferred_*` fields were filled in step 1 or this step |

## Additional resources

- [preference_mapping.md](preference_mapping.md) — preference → API parameter mapping rules
- [reference.md](reference.md) — API, subject-combination modes, and batch API pitfalls
- [scripts/province_config.py](scripts/province_config.py) — per-province classify/subjects/gradeType validation and normalization
- [scripts/test_batch_api.py](scripts/test_batch_api.py) — regression test for the batch API across 31 provinces
- [examples/api_request_shandong.json](examples/api_request_shandong.json) — example with optional parameters
