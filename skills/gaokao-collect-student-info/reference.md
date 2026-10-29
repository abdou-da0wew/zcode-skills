# Smart Volunteer Recommendation API Quick Reference

## Endpoints

| Item | Value |
|------|-------|
| Path | `POST /zp/volunteer/intelligenceVolunteer` |
| Content-Type | `application/json` |
| Auth | none (public skill-test endpoint) |
| Default BASE_URL | From the `ZP_API_BASE_URL` env var (point it at your deployed volunteer-recommendation service; the fetch-volunteers scripts also accept `--base-url`) |
| Full URL | `{BASE_URL}/zp/volunteer/intelligenceVolunteer` |

## Request body fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| province | string | ✓ | Gaokao province (Chinese province name, e.g. `"\u5c71\u4e1c"` = Shandong) |
| classify | string | ✓ | `"\u6587\u79d1"` (liberal arts) / `"\u7406\u79d1"` (science) / `"\u7269\u7406"` (physics) / `"\u5386\u53f2"` (history) / `"\u7efc\u5408"` (comprehensive) |
| score | integer | ✓ | Gaokao score |
| batch | string | ✓ | Application batch (e.g. `"\u672c\u79d1\u6279"` = undergraduate batch) |
| subjects | string \| null | mode-dependent | Comma-separated subject combination |
| gradeType | string \| null | Beijing/Shanghai/Tianjin only | `"\u672c\u79d1"` (undergraduate) / `"\u4e13\u79d1"` (vocational) |
| rank | integer \| null | | Provincial rank |
| universitys | string \| null | | Desired universities, `,`-separated |
| provinces | string \| null | | Province preferences |
| tags | string \| null | | University attribute preferences |
| majorClass | string \| null | | Major-class preferences |
| universityNum | integer | | Number of recommended universities, default 30 |
| majorNum | integer | | Majors per group, default 6 |
| isAdjust | boolean | | Accepts major adjustment |
| volunteerType | string | | ACADEMY_GROUP / ACADEMY_MAJOR / MAJOR_GROUP |
| returnUniversityNum | integer | | Number of already-filled volunteers |
| intentionNum | integer | | Number of already-filled intentions |

## Provinces and subject-combination modes

See [gaokao-fetch-volunteers/reference.md](../gaokao-fetch-volunteers/reference.md) for empirically verified behavior. When collecting `student.json`, always fill `classify` / `subjects` / `gradeType` correctly for the province:

| Mode | Provinces | classify | subjects | gradeType |
|------|-----------|----------|----------|-----------|
| Old system | Xinjiang | liberal arts / science | do not send | do not send |
| 3+1+2 | 23 provinces | physics / history | **all three subjects** (including the primary, e.g. `"\u7269\u7406,\u5316\u5b66,\u751f\u7269"`) | do not send |
| 3+3 | Shanghai, Beijing, Tianjin, Shandong, Zhejiang, Hainan | comprehensive | three subjects (Zhejiang may choose technology) | only Beijing/Shanghai/Tianjin: undergraduate / vocational |

**Tibet**: not supported by the test environment. **Xinjiang**: `score` is required; do not send only a rank.

**Static batch fallback (prefer the batch/list API)**:

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
