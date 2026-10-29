# Student preferences → optional API parameters

Before **step two (fetching volunteers)**, the agent must extract preferences from the
auxiliary info in `student.json`, write them into the structured fields, then build the
API request.

> **Exact API string values:** the API expects Chinese strings for universities,
> provinces, tags, and major classes (they are matched against Chinese-language data).
> Values below are shown as JSON `\uXXXX` escapes — write them exactly like that (or as
> the equivalent UTF-8 characters).

## Mapping table

| student.json field | API field | Format | Description |
|--------------------|-----------|--------|-------------|
| `preferred_universities` | `universitys` | comma-separated string | Full university names, e.g. `"\u5317\u4eac\u822a\u7a7a\u822a\u5929\u5927\u5b66,\u534e\u4e1c\u5e08\u8303\u5927\u5b66"` (Beihang University, East China Normal University) |
| `preferred_provinces` | `provinces` | comma-separated string | Provinces the student wants to study in; auto-derived from `preferred_cities` if empty |
| `preferred_cities` | `provinces` (derived) | — | City mapping below; handled automatically by `build_api_request.py` |
| `preferred_tags` | `tags` | comma-separated string | University attributes, e.g. `985,211,"\u53cc\u4e00\u6d41"` (985, 211, Double First-Class) |
| `preferred_major_classes` | `majorClass` | comma-separated string | Official Ministry-of-Education major class names, e.g. `"\u8ba1\u7b97\u673a\u7c7b,\u7535\u5b50\u4fe1\u606f\u7c7b"` (Computer Science class, Electronic Information class) |

## Agent extraction rules

Recognize preferences from natural language and **write them into the corresponding
student.json fields** (either during step-1 collection or right before the API call in
step 2):

### University preference → `preferred_universities`

Specific schools the user mentions, plus tier shorthand such as "Tsinghua/Peking/Fudan/Jiaotong" or "I'm considering NUDT".

### City preference → `preferred_cities` + `preferred_provinces`

- Collect the city list into `preferred_cities`.
- Also derive provinces into `preferred_provinces` (may be merged and deduplicated with the city mapping results).

Common city → province mappings: Shenzhen/Guangzhou → Guangdong, Wuhan → Hubei, Hangzhou → Zhejiang, Nanjing/Suzhou → Jiangsu, Chengdu → Sichuan, Xi'an → Shaanxi.

### University tier preference → `preferred_tags`

| User says | tags value |
|-----------|------------|
| 985 / top-tier | `985` |
| 211 | `211` |
| Double First-Class | `"\u53cc\u4e00\u6d41"` |
| Postgraduate recommendation (baoyan) | `"\u4fdd\u7814\u8d44\u683c"` (baoyan-eligible) |
| Normal university (teacher training) | `"\u5e08\u8303"` |
| Strong in medicine | depends on specific schools, or tag `"\u533b\u5b66\u9662"` (medical school) if the API supports it |

### Major preference → `preferred_major_classes`

Combine `interests`, `career_direction`, and `subject_scores` to infer:

| Interest / career direction | Suggested majorClass values |
|-----------------------------|-----------------------------|
| Programming, internet, AI | `"\u8ba1\u7b97\u673a\u7c7b,\u8f6f\u4ef6\u5de5\u7a0b,\u7535\u5b50\u4fe1\u606f\u7c7b"` (Computer Science, Software Engineering, Electronic Information) |
| Electronics, chips, communications | `"\u7535\u5b50\u4fe1\u606f\u7c7b,\u5fae\u7535\u5b50\u79d1\u5b66\u4e0e\u5de5\u7a0b,\u96c6\u6210\u7535\u8def"` (Electronic Information, Microelectronics Science and Engineering, Integrated Circuits) |
| Medicine, clinical | `"\u4e34\u5e8a\u533b\u5b66\u7c7b,\u53e3\u8154\u533b\u5b66\u7c7b,\u836f\u5b66\u7c7b"` (Clinical Medicine, Stomatology, Pharmacy) |
| Mechanical, manufacturing, aerospace | `"\u673a\u68b0\u7c7b,\u822a\u7a7a\u822a\u5929\u7c7b,\u81ea\u52a8\u5316\u7c7b"` (Mechanical, Aerospace, Automation) |
| Economics, finance, management | `"\u7ecf\u6d4e\u5b66\u7c7b,\u91d1\u878d\u5b66\u7c7b,\u5de5\u5546\u7ba1\u7406\u7c7b"` (Economics, Finance, Business Administration) |
| Law | `"\u6cd5\u5b66\u7c7b"` (Law) |
| Teacher training, education | `"\u6559\u80b2\u5b66\u7c7b,\u4e2d\u56fd\u8bed\u8a00\u6587\u5b66\u7c7b,\u6570\u5b66\u7c7b"` (Education, Chinese Language and Literature, Mathematics) |

> Use the official Ministry-of-Education undergraduate major class names; separate
> multiple classes with ASCII commas; five or fewer is recommended.

### Taboos and exclusions → `notes` + omit parameters

Exclusionary preferences such as "no remote regions" go into `notes` for the downstream
recommendation skills; **never** put excluded provinces into `provinces`.

## Workflow

```
student.json (with preference fields)
    → agent verifies/completes preferred_* fields
    → build_api_request.py
    → api_request.json
    → fetch_volunteers.py
    → parsed.json
```

## Shandong example

Student: interested in programming/AI, prefers Beijing/Shanghai/Shenzhen, wants a 985,
computer-oriented majors.

```json
{
  "preferred_cities": ["\u5317\u4eac", "\u4e0a\u6d77", "\u6df1\u5733"],
  "preferred_provinces": ["\u5317\u4eac", "\u4e0a\u6d77", "\u5e7f\u4e1c"],
  "preferred_universities": ["\u5317\u4eac\u822a\u7a7a\u822a\u5929\u5927\u5b66", "\u534e\u4e1c\u5e08\u8303\u5927\u5b66"],
  "preferred_tags": ["985", "211"],
  "preferred_major_classes": ["\u8ba1\u7b97\u673a\u7c7b", "\u7535\u5b50\u4fe1\u606f\u7c7b", "\u81ea\u52a8\u5316\u7c7b"]
}
```

(`\u5317\u4eac` = Beijing, `\u4e0a\u6d77` = Shanghai, `\u6df1\u5733` = Shenzhen,
`\u5e7f\u4e1c` = Guangdong, `\u5317\u4eac\u822a\u7a7a\u822a\u5929\u5927\u5b66` = Beihang University,
`\u534e\u4e1c\u5e08\u8303\u5927\u5b66` = East China Normal University, `\u8ba1\u7b97\u673a\u7c7b` = Computer Science class,
`\u7535\u5b50\u4fe1\u606f\u7c7b` = Electronic Information class, `\u81ea\u52a8\u5316\u7c7b` = Automation class.)

Resulting API fragment:

```json
{
  "universitys": "\u5317\u4eac\u822a\u7a7a\u822a\u5929\u5927\u5b66,\u534e\u4e1c\u5e08\u8303\u5927\u5b66",
  "provinces": "\u5317\u4eac,\u4e0a\u6d77,\u5e7f\u4e1c",
  "tags": "985,211",
  "majorClass": "\u8ba1\u7b97\u673a\u7c7b,\u7535\u5b50\u4fe1\u606f\u7c7b,\u81ea\u52a8\u5316\u7c7b"
}
```
