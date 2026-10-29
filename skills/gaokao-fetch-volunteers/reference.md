# Smart Volunteer Recommendation API Quick Reference

## Two-phase call flow

`fetch_volunteers.py` calls the batch API first, then the volunteer recommendation API:

1. **Batch list** `GET /zp/volunteer/batch/list?province=\u5c71\u4e1c&classify=\u7efc\u5408&score=651` (Shandong, comprehensive, 651)
2. **Volunteer recommendation** `POST /zp/volunteer/intelligenceVolunteer` (the `batch` and `volunteerType` in the request body come from the phase-1 selection)

`classify` values: `"\u6587\u79d1"` (liberal arts), `"\u7406\u79d1"` (science),
`"\u7269\u7406"` (physics), `"\u5386\u53f2"` (history), `"\u7efc\u5408"` (comprehensive) —
fill per province and subject-combination mode (see below).

Batch selection rule: exact batch name → filter by `gradeType` / undergraduate-vocational batch → among qualified batches pick the one with the highest control line.

The parsed result `parsed.json` contains a `batch_resolution` field recording the batch source and available options.

## Batch list endpoint

| Item | Value |
|------|-------|
| Path | `GET /zp/volunteer/batch/list` |
| Parameters | `province`, `classify`, `score`; Beijing/Shanghai/Tianjin also need `gradeType` |
| Response | `{ status, message, result: [{ batch, score, gradeType, type, ... }] }` |

`result[].type` corresponds to the volunteer API's `volunteerType` (e.g. `MAJOR_GROUP`). `gradeType` is only used for batch filtering; it is written into the volunteer request body **only for Beijing/Shanghai/Tianjin**.

## Volunteer recommendation endpoint

| Item | Value |
|------|-------|
| Path | `POST /zp/volunteer/intelligenceVolunteer` |
| Content-Type | `application/json` |
| Auth | depends on the server you point at |
| BASE_URL | `$ZP_API_BASE_URL` environment variable (set it to your gaokao volunteer-recommendation API server) |
| Full URL | `{BASE_URL}/zp/volunteer/intelligenceVolunteer` |

## Request body fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| province | string | ✓ | Gaokao province (Chinese province name) |
| classify | string | ✓ | liberal arts / science / physics / history / comprehensive |
| score | integer | ✓ | Gaokao score |
| batch | string | ✓ | Application batch (resolvable via batch/list) |
| subjects | string \| null | mode-dependent | Comma-separated subject combination |
| gradeType | string \| null | Beijing/Shanghai/Tianjin | undergraduate / vocational |
| rank | integer \| null | | Provincial rank |
| universitys | string \| null | | Desired universities, `,`-separated; from `student.preferred_universities` |
| provinces | string \| null | | Province preferences; from `preferred_provinces` or derived from `preferred_cities` |
| tags | string \| null | | University attribute preferences; from `preferred_tags` (e.g. 985, 211) |
| majorClass | string \| null | | Major-class preferences; from `preferred_major_classes` |
| universityNum | integer | | Number of recommended universities, default 30 |
| majorNum | integer | | Majors per group, default 6 |
| isAdjust | boolean | | Accepts major adjustment |
| volunteerType | string | | ACADEMY_GROUP / ACADEMY_MAJOR / MAJOR_GROUP |
| returnUniversityNum | integer | | Number of already-filled volunteers |
| intentionNum | integer | | Number of already-filled intentions |

## Provinces and subject-combination modes (empirically verified)

### Old system (Xinjiang only)

| Field | Value |
|-------|-------|
| classify | `"\u6587\u79d1"` (liberal arts) or `"\u7406\u79d1"` (science) — never physics/history/comprehensive |
| subjects | omit or `null` (do **not** send the string `"null"`) |
| gradeType | omit |
| score | **required** (Xinjiang has no score-rank table; a rank alone cannot be reverse-mapped) |

### 3+1+2 (23 provinces)

Guangdong, Jiangsu, Hebei, Hubei, Hunan, Fujian, Liaoning, Chongqing, Gansu, Heilongjiang, Jilin, Anhui, Jiangxi, Guizhou, Guangxi, Yunnan, Inner Mongolia, Sichuan, Ningxia, Shanxi, Henan, Shaanxi, Qinghai

| Field | Value |
|-------|-------|
| classify | `"\u7269\u7406"` (physics) or `"\u5386\u53f2"` (history) — matches the 3+1+2 primary subject |
| subjects | **all three subjects**, comma-separated: `primary,elective1,elective2`. Must include the primary subject consistent with `classify`; **never only the two electives** |

Example: `classify = "\u7269\u7406"` with `subjects = "\u7269\u7406,\u5316\u5b66,\u751f\u7269"` (✓); `subjects = "\u5316\u5b66,\u751f\u7269"` (✗ missing physics)

Electives are limited to: chemistry, biology, politics, geography.
| gradeType | omit |

### 3+3 (6 provinces)

Shanghai, Beijing, Tianjin, Shandong, Zhejiang, Hainan

| Field | Value |
|-------|-------|
| classify | always `"\u7efc\u5408"` (comprehensive) |
| subjects | three subjects, comma-separated; Zhejiang may choose `"\u6280\u672f"` (technology) |
| gradeType | **only Beijing/Shanghai/Tianjin**: `"\u672c\u79d1"` (undergraduate) / `"\u4e13\u79d1"` (vocational) |

**Full-score differences**: Shandong/Zhejiang 750; Hainan 900; Shanghai undergraduate 660; Beijing/Tianjin undergraduate 750; Beijing/Shanghai/Tianjin vocational 450 (Chinese/math/English only).

### Beijing/Shanghai/Tianjin gradeType rules

Both the `batch/list` and volunteer APIs **require** `gradeType` for these cities:

```
GET .../batch/list?province=\u5317\u4eac&classify=\u7efc\u5408&score=650&gradeType=\u672c\u79d1
```

If not provided, the script infers it: `batch = "\u4e13\u79d1\u6279"` (vocational batch) → vocational; `score ≤ 450` → vocational; otherwise → undergraduate.

| Scenario | subjects | gradeType |
|----------|----------|-----------|
| Beijing undergraduate | `"\u7269\u7406,\u5316\u5b66,\u751f\u7269"` | `"\u672c\u79d1"` |
| Beijing vocational | the string `"null"` (API requirement, not JSON null) | `"\u4e13\u79d1"` |
| Zhejiang/Shandong/Hainan | three-subject combination | omit |

### Tibet

The test environment **has not integrated this province**; any classify returns `status=500` — it is not a parameter error. The script reports the lack of support during validation.

### Common pitfalls (batch API)

| Symptom | Cause | Fix |
|---------|-------|-----|
| `status=0` but `result=[]` | classify does not match the province's mode (e.g. physics sent for Shandong) | change classify per the tables above |
| Volunteer API 500 (Shandong etc.) | `gradeType` sent by mistake | only Beijing/Shanghai/Tianjin send it; remove elsewhere |
| Volunteer API 500 (Shandong etc.) | missing `subjects` or only two subjects | 3+1+2 requires **all three subjects** (including physics/history) |
| Volunteer API 500 (Xinjiang) | `subjects` is the string `"null"` | omit the subjects field entirely |
| Beijing vocational 500 | subjects is JSON null or omitted | use the string `"null"` |

`scripts/province_config.py` encapsulates these validations and parameter normalization; `scripts/test_batch_api.py` can regression-test all 31 provinces.

### Static batch fallback (when batch/list fails)

| Province | batch value |
|----------|-------------|
| Tianjin | `"\u672c\u79d1\u6279A\u6bb5"` (undergraduate batch, segment A) |
| Zhejiang | `"\u666e\u901a\u7c7b\u4e00\u6bb5"` (general category, segment 1) |
| Shandong | `"\u666e\u901a\u7c7b\u4e00\u6bb5"` (general category, segment 1) |
| Sichuan, Yunnan | `"\u672c\u79d1\u6279B\u6bb5"` (undergraduate batch, segment B) |
| Gansu | `"\u672c\u79d1\u6279"` (undergraduate batch) |
| Ningxia | `"\u672c\u79d1\u6279B\u6bb5"` (undergraduate batch, segment B) |
| Xinjiang | `"\u672c\u79d1\u4e00\u6279"` (undergraduate, first batch) |
| Tibet | not supported by the test environment (error 2222010, invalid gaokao province) |

## Response structure

The public skill-test endpoint returns `{ status, message, result }` (`status=0` means success); the scripts normalize it into a unified format.

```json
{
  "status": 0,
  "message": "success",
  "result": {
    "province": "...",
    "schoolList": [
      {
        "universityName": "",
        "universityCode": "",
        "universityMajorGroup": "",
        "enrollProbability": 20,
        "type": "CHONG",
        "majorList": [ { "majorName": "", "claim": "", "type": "CHONG" } ]
      }
    ]
  }
}
```

The legacy envelope `{ code, msg, body }` (`code=200`) is also supported.

`type` enum: `CHONG` = reach, `WEN` = match, `BAO` = safety, `NAN` = difficult, `YI` = easy.

`score` / `parityScore` are usually JSON-encoded strings such as `[{"2025":"660,2153,60"}]` (score, rank, planned seats).
