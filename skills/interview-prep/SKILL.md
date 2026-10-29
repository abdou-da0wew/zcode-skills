---
name: interview-prep
description: Helps the user prepare for interviews. Based on the target JD, company, and role direction, generates "high-frequency interview questions + reference answers + a question bank categorized into behavioral / technical / case / role-specific", and produces a printable "Interview Prep Handbook". Trigger this skill whenever the user says "help me prepare for an interview", "I have an interview tomorrow / the day after", "interview questions", "interview experiences", "mock interview", "I'm interviewing at company X for role Y", "help me build my STAR stories", "how do I answer this interview question", or "how should I introduce myself / explain why I'm leaving / talk about strengths and weaknesses". Do NOT use this skill to edit resumes (use jd-resume-tailor / resume-builder) or to recommend career directions (use job-intent-tracker).
---

# Interview Prep

It does 4 things:

1. **Break down the interview scenario**: identify the target company / role / interview round (first round / second round / final round / HR round)
2. **Generate a question bank**: pull questions on demand from 4 categories (behavioral, technical, case, role-specific)
3. **Generate reference answers**: use frameworks such as STAR / SCQA / MECE, grounded in the facts from the user's resume
4. **Produce a "prep handbook"**: a printable .md / .docx / .pdf containing questions + reference approaches + a self-check list

---

## When to Trigger

Strong signals:
- "Help me prepare for an interview / mock interview"
- "Interview tomorrow / next week"
- Mentions a specific company + role
- "High-frequency interview questions / classic interview questions"
- "How do I answer ___?"
- "How should I introduce myself / explain why I'm leaving / negotiate expected salary?"

Weak signals (confirm first):
- Only says "I want to learn about interviewing" → ask which direction / which round

---

## Workflow

### Step 1: Lock Down the Interview Scenario

Use AskUserQuestion to collect:
- Target company (specific name / big tech vs. startup vs. foreign company / company type)
- Target role (precise to the direction, e.g. "user-growth PM" rather than "product manager")
- Interview round (first / second / final / HR round / full-loop rehearsal)
- Time pressure (tomorrow / this week / next week or later) — affects "breadth vs. depth"
- Materials the user already has (JD / resume / public company info / known interviewer background)

If the user provided a JD and a resume, **call jd-resume-tailor's parse_jd.py first** to extract the key job requirements and avoid parsing them twice.

### Step 2: Question Selection Strategy

Decide the question-bank structure by "round + direction + time available". Read the corresponding files:

- Behavioral (asked in every round) → `references/behavioral.md`
- Technical (main battlefield for engineering / data roles) → `references/technical.md`
- Case (consulting / strategy / senior PM) → `references/case.md`
- HR round (the last mile for any role) → `references/hr_round.md`
- Role-specific question banks:
  - Internet product / operations / PM → `references/role_internet.md`
  - Engineering / R&D / data → `references/role_tech.md`
  - Finance / consulting / business → `references/role_finance.md`

Recommended question volume:
- **Interviewing tomorrow**: 5-8 questions per category, focused on high-frequency ones
- **3-7 days out**: 10-15 questions per category
- **More than 1 week**: full coverage + mock rounds

### Step 3: Generate Reference Answers

**Key principle: reference answers must be based on the user's real experiences from the resume, not generic boilerplate.**

Call `scripts/star_story_builder.py` (if a resume is available):

```bash
python scripts/star_story_builder.py --resume resume.md \
    --questions questions.json --out answers.md
```

Or, if there is no resume, use the generic answer frameworks (read from references/answer_frameworks.md) as templates and let the user fill in the blanks.

Format of a reference answer:
```
[Question] ___
[What It Tests] What ability the HR / interviewer is looking for
[Answer Framework] One of STAR / SCQA / MECE / 5W1H
[Suggested Length] X minutes (usually 1.5-3 minutes)
[Reference Answer (based on your ___ experience in the resume)]
  S: The context / problem at the time
  T: Your task / goal
  A: Your specific actions (the highlight — include details)
  R: Quantified results + reflection
[Likely Follow-ups] 1. ___ 2. ___ 3. ___
```

### Step 4: Produce the "Prep Handbook"

Call the docx skill to generate a complete `interview_prep_<company>_<role>.docx` with this structure:

```
Cover: company + role + interview date + countdown
1. Company / role quick brief (1 page)
2. Self-introduction (both Chinese and English versions, tailored to the role)
3. Behavioral question bank (X questions) + reference answers
4. Technical / Case question bank (X questions) + reference approaches
5. Questions-to-ask list (what you ask the interviewer)
6. Salary negotiation script
7. Interview-day checklist (route / dress / items / mindset)
```

**Also output a condensed .md version** so the user can review it on the subway / on the way.

### Step 5: Mock Interview (optional - only when the user explicitly asks)

If the user says "let's do a mock", enter interactive mode:
- Ask 1 question at a time
- Wait for the user's answer (voice / text)
- Give feedback across 3 dimensions: content / structure / delivery
- If the user says "next question" or "give me a harder one", continue

During the mock, **stay in the interviewer persona**: use a real interviewer's tone, follow-up style, and pressure points (but do not become an attacker — stay constructive).

---

## Anti-patterns (do not do)

- ❌ Handing over a generic "50 questions" list to get it over with → must customize by company / role
- ❌ Reference answers full of empty phrases like "I have excellent communication skills" → must use concrete stories
- ❌ Never letting the user practice, answering everything for them → misses the value of rehearsal
- ❌ Fabricating experiences the user doesn't have for STAR stories → the user will get exposed in the interview
- ❌ HR-round answers that sound too "coached" (mechanical) → provide "3 versions in different styles" for the user to choose from

## Collaboration with Other Skills

- User says "my resume isn't strong enough, fix the resume first" → hand off to `jd-resume-tailor` or `resume-builder`
- User says "I'm still unsure whether to apply" → hand off to `job-intent-tracker`
- After the interview the user says "I want to review how it went" → stay in this skill, enter "interview debrief mode": ask about performance, sticking points, follow-ups, and help the user prepare for the next round
