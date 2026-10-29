---
name: gaokao-recommend-schools
description: >-
  Based on the recommended major list, the student profile, and the volunteer list, the
  agent analyzes and recommends universities with personalized reasons, outputting a
  structured school_recommendation.json. Use it for gaokao university recommendation,
  choosing a university, or laying out reach/match/safety schools.
---

# Recommended Universities & Reasons

This skill is the **fourth step** of the pipeline: with the major directions already
decided, it recommends universities from `parsed.json` and explains the reasons.

## Upstream / downstream

- **Upstream**: `student.json` + `parsed.json` + `major_recommendation.json`
- **Downstream**: [gaokao-generate-report](../gaokao-generate-report/SKILL.md)

## Inputs

1. `student.json` — preferred cities, family situation, career direction, etc.
2. `parsed.json` — university tags, cities, reach/match/safety tiers, admission probabilities
3. `major_recommendation.json` — the already-recommended majors and directions, used to judge how well a university's majors fit

## Agent analysis tasks

1. Prioritize universities that **include already-recommended majors** or whose **strong disciplines match the chosen major directions**.
2. Combine `preferred_cities`, city industry opportunities (see the city table in [career_reference.md](career_reference.md)), and university tiers (985/211/Double First-Class, etc.).
3. Balance the reach/match/safety layout: place core targets in the match tier, and make sure both reach-tier elite universities and safety schools are represented.
4. Pick **6–12** universities and write a personalized `modal` recommendation reason for each.

## Recommendation reasons should cover

- **Location advantage**: the city's industries and internship/employment resources
- **University tier**: tags and social recognition
- **Major fit**: the connection with `major_recommendation.json`
- **Admission value**: whether the tier and probability match the student's expectations

## Hard constraints

Each entry's `university_name` and `university_code` in `recommended_schools` must be **exactly identical** to `parsed.json`.

## Output

Save as `output/school_recommendation.json`; see [examples/school_recommendation_template.json](examples/school_recommendation_template.json) for the structure.

```json
{
  "school_strategy": "University-tier layout strategy (how reach/match/safety are allocated)",
  "recommended_schools": [
    {
      "university_name": "...",
      "university_code": "...",
      "modal": {
        "title": "Why this school is recommended: ...",
        "body": "<h4>Reasons for recommendation</h4><ul><li>...</li></ul>"
      }
    }
  ]
}
```

## Delivering to the user

- Give the user the absolute path of the saved JSON
- Explain in natural language the university-recommendation logic and the tier layout

## Additional resources

- [career_reference.md](career_reference.md) — city-industry and university-tier reference
