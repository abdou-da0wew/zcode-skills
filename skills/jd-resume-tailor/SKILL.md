---
name: jd-resume-tailor
description: Given a JD and an existing resume, performs "JD parsing + targeted resume rewriting". Parses the JD to extract hard skills, soft skills, and nice-to-haves; runs a gap analysis against the resume; produces a resume rewritten for that specific role — highlighting relevant experience, closing keyword gaps, and preserving the candidate's real history without fabricating anything. Trigger this skill when the user says "tailor my resume for this role / this company", "match my resume against this JD", "I want to apply to this job, how should I change my resume", "optimize this resume for company X", "make me a targeted version of this resume", or provides both JD text and a resume file. **Do NOT use this skill to write a resume from scratch** — that's resume-builder's job.
---

# JD ⇄ Resume Tailor (JD parsing + targeted resume rewriting)

This skill's scope is narrow: **it only solves "you already have a JD + an existing resume, and you want the highest-hit-rate version"**.

What it does not do:
- Write a new resume (go to `resume-builder`)
- Explore directions / recommend jobs (go to `job-intent-tracker`)
- Generate interview questions (go to `interview-prep`)

---

## When to Trigger

Strong signals:
- User provides a JD link / JD text + a resume → **always triggers**
- "Tailor my resume for this role"
- "Compare my resume against this JD"
- "I want to apply for role Y at company X, check my resume"
- "Make a targeted version"

Weak signals (confirm first):
- JD provided but no resume → ask "Could you share your resume? If you don't have one yet, I can help you build one from scratch (resume-builder)"
- Resume provided with just "improve my resume" → ask "Which JD is this for? Without a JD, use resume-builder for general optimization"

---

## Workflow

### Step 1: Parse the JD

Input may be:
- Plain text (user pastes it)
- A link (**do not** auto-fetch; ask the user to paste the JD text; if the user authorizes fetching, use web_fetch)
- A screenshot (use OCR / vision recognition; have the user confirm the extraction)
- A doc/pdf file

Call the script:

```bash
python scripts/parse_jd.py --jd-file <jd.txt> --out jd_parsed.json
```

The script extracts from the JD:
- **Hard skills, must-have** (skills following strong signal words like "must", "required", "at least X years")
- **Hard skills, nice-to-have** (weak signals like "plus", "preferred", "familiarity with ___ is a plus")
- **Soft-skill signals** (communication / driving initiatives / cross-team / working under pressure, etc.)
- **Responsibility verbs + objects** ("own X" / "build Y" / "drive Z")
- **Special requirements** (travel / education / certifications / languages / location)

Show the results to the user and have them **confirm / correct the extraction** (no key must-haves may be missed).

### Step 2: Parse the Resume

Input: the user's uploaded resume file (.pdf / .docx / .md / .txt).

Call the appropriate skill to parse:
- pdf → pdf skill
- docx → docx skill

Extract: basic info, education, and for each work / project experience (company, role, dates, responsibility bullets), plus the skills list.

### Step 3: Gap Analysis

Call:

```bash
python scripts/jd_gap.py --jd jd_parsed.json --resume resume.txt --out gap.md
```

The script outputs three lists:

1. **Perfect hits** (JD must-haves with clear evidence in the resume)
2. **Implicit hits** (the JD asks for X; the resume shows related experience with different wording → can be "mentioned" when rewriting)
3. **True gaps** (required by the JD but entirely absent from the resume)

Split "true gaps" into two kinds:
- **Recoverable**: the user actually did something similar but never wrote it down → ask "Have you done X?"
- **Unrecoverable**: the user genuinely hasn't done it → **never fabricate**; suggest the user honestly address it in the cover letter or summary and emphasize transferable skills

### Step 4: Targeted Rewriting

Rewrite the resume following these principles:

**a. Reorder experiences**: put the most JD-relevant work / projects first (don't change real dates, but you may split projects into "relevant projects / other projects")

**b. Rewrite every bullet**:
- Weave the JD's "responsibility verbs" naturally into bullets (e.g. if the JD says "lead ___ system design" and the resume says "participated", change it to "led" — only if the user actually led it)
- Keep numbers and make them prominent ("1M users" is a good thing; don't hide it)
- Add JD keywords (if the JD says "A/B testing" but the resume says "gray-release comparison", change it to "A/B testing (gray-release comparison)")

**c. Rewrite the Summary**: 2-3 lines on why you're the right person for this role, **directly mapping to the JD's must-haves**

**d. Reorder the skills list**: move skills mentioned in the JD to the front (only if actually known)

**e. Facts that must not change**:
- Company names, role titles, start/end dates, education — unchanged, to the letter
- Project scale, user counts, revenue figures — cannot be invented; only fill in exact values after the user confirms

### Step 5: Self-Check + Report

Output three files:
1. `resume_tailored_<company>_<role>.md` (the rewritten resume)
2. `gap_analysis.md` (the gap analysis report)
3. An ATS hit-rate comparison in chat: "before: X% → after: Y%"

Also: honestly flag **which bullets were rewritten by inference from existing information**, so the user can review before applying.

---

## Anti-patterns (do not do)

- ❌ Fabricating experiences ("add a project you never did" — absolutely forbidden, even if the user asks)
- ❌ Pasting whole JD paragraphs into the resume (HR spots it instantly, and ATS anti-cheat heuristics will flag it)
- ❌ Keyword stuffing (a long list of skill words tacked on at the end to game the hit rate — HR sees through it)
- ❌ Changing "participated" to "led" without asking the user about their actual role → must verify first
- ❌ Not showing the user the gap analysis and silently rewriting → the user loses "ownership" of their resume

## Collaboration with Other Skills

- After rewriting, the user says "help me prepare for this company's interview" → hand off to `interview-prep`, passing the JD + tailored resume
- User says "I want to know what other similar roles I could apply to" → hand off to `job-intent-tracker`
- User says "my resume is weak overall, can we redo it from scratch" → hand off to `resume-builder`
