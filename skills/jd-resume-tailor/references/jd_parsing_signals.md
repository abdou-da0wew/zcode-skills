# JD Parsing Signal Words Reference

## Must-have strong signal words

When these words appear in a JD sentence, the skill / experience that follows is most likely a hard requirement:

- Must / Required / Should / Essential
- At least X years / X+ years / No less than
- "Needs to have" / "Requires"
- "Prerequisite" / "Hard requirement"
- Engineering background / Top-tier university / Master's degree or above / PhD

English JDs:
- Required / Must have / Mandatory / Essential
- Minimum X years
- Strong proficiency in / Expert in
- Demonstrated experience with

## Nice-to-have weak signal words

- Plus / Preferred / Preferred candidates
- Candidates familiar with ___ preferred
- Experience with ___ is a plus
- "Basic understanding of ___ is sufficient"
- Bonus points

English:
- Preferred / Nice to have / Plus / Bonus / Desirable
- Familiar with / Exposure to
- A plus / Would be a plus

## Responsibility verbs (echoing them in resume bullets aligns with the JD)

English: Lead / Drive / Build / Design / Architect / Develop / Implement / Optimize / Manage / Coordinate / Execute / Own

## Special requirements

- **Education**: Bachelor's / Master's / PhD or above; school tier
- **Years of experience**: X-Y years (state the range; not stating a max leaves flexibility)
- **Languages**: fluent spoken English / CET-6 / IELTS X / native speaker
- **Certifications**: CFA / CPA / PMP / AWS Solutions Architect, etc.
- **Travel / relocation / overtime**: "willing to travel", "weekend shifts on rotation", "project-based 996 schedule"
- **Location**: city + remote / hybrid or not

## Anti-signals (be alert when you see these)

- "Other tasks assigned by leadership" → fuzzy job boundaries
- "Strong ability to work under pressure" → heavy overtime
- "Embrace change / rapid iteration" → unstable business direction
- "Flat communication / no hierarchy" → may actually be more chaotic
- "Full benefits + holiday gifts" featured prominently in the JD → benefits may be all there is

## Output format (what Step 1 shows the user)

```json
{
  "company": "Company X",
  "position": "Role X",
  "must_have": [
    {"item": "5+ years of consumer product experience", "evidence": "JD line X"},
    {"item": "Proficient in SQL", "evidence": "JD line Y"}
  ],
  "nice_to_have": [
    {"item": "Overseas business experience", "evidence": "JD line Z"}
  ],
  "soft_skills": ["cross-team drive", "data-driven decisions"],
  "responsibilities": [
    "Lead product planning for the ___ business line",
    "Drive iteration through data analysis"
  ],
  "special_requirements": {
    "education": "Bachelor's degree or above",
    "years": "5+",
    "language": "Fluent spoken English",
    "location": "Shanghai; short-term travel acceptable"
  }
}
```
