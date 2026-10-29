---
name: gaokao-recommend-majors
description: >-
  Based on the student profile and the API volunteer list, the agent analyzes and
  recommends suitable major directions, career outcomes, and a concrete list of
  majors, outputting a structured major_recommendation.json. Use it for gaokao
  major recommendation, choosing a major, or career-direction analysis.
---

# Recommended Majors & Career Directions

This skill is the **third step** of the pipeline: pure agent analysis, no rule-based
scripts. It combines the student's interests, scores, career intentions, and the real
majors in `parsed.json` to produce personalized major recommendations.

## Upstream / downstream

- **Upstream**: `student.json` + `parsed.json` (from info collection and volunteer fetching)
- **Downstream**: [gaokao-recommend-schools](../gaokao-recommend-schools/SKILL.md) reads `major_recommendation.json`

## Inputs

1. `student.json` — the student's complete profile
2. `parsed.json` — reach/match/safety volunteers and each school's `majors` (including the `claim` subject requirements and admission probabilities)

## Agent analysis tasks

1. Read [career_reference.md](career_reference.md) to learn the common major classes and career outcomes (**reference only, not hard rules**).
2. Weigh subject requirements, per-subject scores, interests, family situation, and career direction to decide on 2–4 **major directions** (`major_directions`).
3. Pick the **8–15** best-matching concrete majors from `parsed.json` and write them into `recommended_majors`.
4. Write the comprehensive opening `intro` and the overall `strategy` (major-first perspective).

## Hard constraints

Each entry's `university_name`, `university_code`, `major_name`, and `major_code` in `recommended_majors` must be **exactly identical** to `parsed.json`, otherwise the final report cannot display the 🔥 tag.

Before generating, search `parsed.json` to confirm the field values.

## Output

Save as `output/major_recommendation.json`; see [examples/major_recommendation_template.json](examples/major_recommendation_template.json) for the structure.

```json
{
  "student": { "...auxiliary profile fields..." },
  "intro": "Comprehensive evaluation opening (HTML <strong> allowed)",
  "strategy": "Application strategy (major-first perspective)",
  "major_directions": [
    { "icon": "🧑‍💻", "title": "...", "match_level": "Very high", "description": "..." }
  ],
  "recommended_majors": [
    {
      "major_name": "...",
      "major_code": "...",
      "university_name": "...",
      "university_code": "...",
      "modal": { "title": "...", "body": "<h4>...</h4><ul>...</ul>" }
    }
  ]
}
```

## Delivering to the user

- Give the user the absolute path of the saved JSON
- Explain in natural language the recommended major directions and why the top majors were chosen

## Additional resources

- [career_reference.md](career_reference.md) — major / career-direction reference
