---
name: gaokao-collect-student-info
description: >-
  Gaokao (college entrance exam) application info collection: takes the student's own
  wording as the source of truth, gathers the API-required fields (province, score,
  subject combination, etc.) plus auxiliary profile info (interests, family situation,
  career direction), avoiding paraphrasing or over-generalization, and outputs a
  structured student.json. Use it to open a gaokao application consultation, register
  student info, or collect data before filling the application form.
---

# Gaokao Student Info Collection

This skill is the **first step** of the recommendation pipeline. It only talks with the
user and produces `student.json`; it never calls the API and never makes recommendations.

> **Exact API string values:** the gaokao API expects Chinese string values for
> `province`, `classify`, `subjects`, `batch`, and `gradeType`. This doc shows them as
> JSON `\uXXXX` escapes (e.g. `"\u5c71\u4e1c"` = Shandong). Write them exactly like that
> (or as the equivalent UTF-8 characters) into `student.json`. See
> [reference.md](reference.md) for the full value table.

## Core principle: preserve the student's original wording

**Collect only, do not process.** Downstream major/school recommendations depend on
**how the students describe themselves**; heavy rewriting creates information gaps.

| Practice | Explanation |
|----------|-------------|
| ✅ Keep original wording | For text fields like `interests`, `family_situation`, `career_direction`, `notes`, **use the student's own sentences or a faithful complete rendering** — no polishing, no embellishing, no summarizing on their behalf |
| ✅ Record faithfully | Colloquialisms, repetition, and vague wording are all fine; you may quote their exact words in `notes` instead of rewriting them into a "standard answer" |
| ✅ Only minimal structuring | For API-required fields (`province`, `score`, `classify`, `subjects`), only normalize the format (integer scores, comma-separated subjects) |
| ✅ Explicit info only | Record `preferred_*` fields only for universities, cities, tiers, and major classes the student **explicitly mentioned**; never invent them |
| ❌ No over-interpreting | Do not rewrite "I want to write code" into "Computer Science and Technology direction"; do not invent career plans the student never expressed; do not make major/school recommendations or infer preferences at this stage |

When reading back to the user for confirmation, **quote their original words** rather
than substituting your own rewritten version.

## Pipeline position

- **Upstream**: none
- **Downstream**: [gaokao-fetch-volunteers](../gaokao-fetch-volunteers/SKILL.md) reads this skill's output and maps preferences to optional API parameters

## Collection checklist

### API-required (written to the top level of `student.json`)

| Field | Description | Example |
|-------|-------------|---------|
| `province` | Gaokao province (API value = Chinese province name) | `"\u5c71\u4e1c"` = Shandong |
| `classify` | Liberal arts / science / physics / history / comprehensive | `"\u7efc\u5408"` = comprehensive |
| `score` | Gaokao score (integer) | 650 |
| `batch` | Application batch | `"\u672c\u79d1\u6279"` = undergraduate batch |
| `subjects` | 3+1+2: **all three subjects** (primary + two electives); 3+3: all three; old system: `null` | `"\u7269\u7406,\u5316\u5b66,\u751f\u7269"` = physics, chemistry, biology |
| `gradeType` | Only Beijing/Shanghai/Tianjin: undergraduate or vocational | `"\u672c\u79d1"` = undergraduate |
| `rank` | Provincial rank; `null` if unknown | 5000 |

### Auxiliary profile (original wording first; for downstream analysis)

| Field | Description | How to fill |
|-------|-------------|-------------|
| `interests` | Hobbies and interests | **The student's own words** — comma-separated or natural sentences; do not summarize |
| `family_situation` | Family situation | **The student's own words** — keep their statements about finances, location, attitude toward further study, etc. |
| `career_direction` | Future career / development direction | **The student's own words** — record even vague answers verbatim; do not draw conclusions |
| `subject_scores` | Per-subject scores | Numeric fields as reported by the student |
| `preferred_cities` | Preferred cities | Only cities the student **explicitly mentioned** |
| `preferred_provinces` | Preferred provinces | Record if the student mentioned them; otherwise may stay empty (downstream derives them from cities) |
| `preferred_universities` | Desired universities | Use the **full name or the exact name the student used**; never silently replace abbreviations |
| `preferred_tags` | University tier preference | Only what the student **actually said** (e.g. "I want a 985"); do not infer on your own |
| `preferred_major_classes` | Major-class preference | Only majors/directions the student **explicitly mentioned**; do not derive from interests |
| `notes` | Anything else | Original words, taboos, special requests that don't fit the fields above |

The mapping from preference fields to API parameters is handled downstream by
[gaokao-fetch-volunteers](../gaokao-fetch-volunteers/SKILL.md); at this stage you do
**not** need to rewrite or complete `preferred_*` just to satisfy API parameters.

## Workflow

1. Ask in natural language, item by item; ask only for what's missing; batching questions is fine.
2. **Determine the subject-combination mode by province and fill the API fields correctly**
   (see the table below and [reference.md](reference.md)).
3. Record the student's answers **faithfully** into the corresponding fields; format-normalize only the API-required fields.
4. Once the info is complete, save `output/student.json`, **read back the key content in the student's own words**, and ask them to confirm.

### Per-province classify / subjects / gradeType (SOP)

| Mode | Provinces | classify | subjects | gradeType |
|------|-----------|----------|----------|-----------|
| Old system | Xinjiang | Liberal arts **or** science | `null` (do not send subjects) | `null` |
| 3+1+2 | Guangdong, Jiangsu, Hebei, Hubei, Hunan, Fujian, Liaoning, Chongqing, Gansu, Heilongjiang, Jilin, Anhui, Jiangxi, Guizhou, Guangxi, Yunnan, Inner Mongolia, Sichuan, Ningxia, Shanxi, Henan, Shaanxi, Qinghai | Physics **or** history | **All three subjects**: `"\u7269\u7406,\u5316\u5b66,\u751f\u7269"` (must include the primary subject; never only the two electives) | `null` |
| 3+3 | Shanghai, Beijing, Tianjin, Shandong, Zhejiang, Hainan | **Comprehensive** (never physics/history) | Three subjects; Zhejiang may also choose technology (Generic Technology) | Only Beijing/Shanghai/Tianjin: `"\u672c\u79d1"` (undergraduate) / `"\u4e13\u79d1"` (vocational) |

**Collection tips**:

- Clarify whether the student is **liberal arts or science** (Xinjiang), **physics or history track** (3+1+2), or simply record their three subjects (3+3 uses `classify = "\u7efc\u5408"`).
- For **3+1+2, `subjects` must contain all three subjects** (e.g. physics-chemistry-biology), including the primary subject consistent with `classify`; never record only chemistry and biology.
- For Beijing/Shanghai/Tianjin, confirm whether the student applies for **undergraduate or vocational** (vocational only tests Chinese/math/English, 450-point scale).
- Xinjiang requires a **score**; a rank alone is not enough.
- **Tibet**: the test environment does not support the volunteer API — tell the user during collection.
- `batch` may use the student's generic phrasing such as `"\u672c\u79d1\u6279"` (undergraduate batch); downstream batch/list resolves it automatically.

## Output format

See [examples/student_template.json](examples/student_template.json) and
[examples/student_shandong.json](examples/student_shandong.json).

```json
{
  "province": "\u5c71\u4e1c",
  "classify": "\u7efc\u5408",
  "subjects": "\u7269\u7406,\u5316\u5b66,\u751f\u7269",
  "score": 650,
  "batch": "\u672c\u79d1\u6279",
  "rank": null,
  "gradeType": null,
  "interests": "<student's own words, do not rewrite>",
  "career_direction": "<student's own words, do not rewrite>",
  "family_situation": "<student's own words, do not rewrite>",
  "preferred_cities": ["\u5317\u4eac", "\u4e0a\u6d77", "\u6df1\u5733"],
  "preferred_provinces": ["\u5317\u4eac", "\u4e0a\u6d77", "\u5e7f\u4e1c"],
  "preferred_universities": ["\u5317\u4eac\u822a\u7a7a\u822a\u5929\u5927\u5b66"],
  "preferred_tags": ["985", "211"],
  "preferred_major_classes": ["\u8ba1\u7b97\u673a\u7c7b", "\u7535\u5b50\u4fe1\u606f\u7c7b"],
  "notes": "Not willing to consider remote regions"
}
```

(`\u5317\u4eac` = Beijing, `\u4e0a\u6d77` = Shanghai, `\u6df1\u5733` = Shenzhen,
`\u5e7f\u4e1c` = Guangdong, `\u5317\u4eac\u822a\u7a7a\u822a\u5929\u5927\u5b66` = Beihang University,
`\u8ba1\u7b97\u673a\u7c7b` = Computer Science class, `\u7535\u5b50\u4fe1\u606f\u7c7b` = Electronic Information class.)

## Notes

- `batch` is resolved downstream via batch/list, so the student's generic phrasing (e.g. `"\u672c\u79d1\u6279"`) is fine here.
- **`classify` must match the province's mode** (most common mistake: sending physics for Shandong). See [gaokao-fetch-volunteers/reference.md](../gaokao-fetch-volunteers/reference.md) for the full pitfall list.
- Exclusionary preferences (e.g. "no remote regions") go into `notes` in the student's own words — **not** into `preferred_provinces`, and do not rewrite them into formal language.
- When reading back for confirmation, show **the student's own wording**, not a polished agent version.
- Deliver the output path to the user as an absolute path.

## Additional resources

- [reference.md](reference.md) — province subject-combination modes and batch quick reference
- [preference_mapping.md](../gaokao-fetch-volunteers/preference_mapping.md) — preference → API parameter mapping
