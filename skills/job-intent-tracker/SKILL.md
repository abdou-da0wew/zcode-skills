---
name: job-intent-tracker
description: Helps users organize their job-search intent, generate target role profiles, and maintain a structured "application tracking sheet". Trigger proactively when the user says "I want to change jobs / I don't know what roles to apply for / help me see what roles suit me / help me manage my applications / I've applied to several places but can't keep track / I want to build a job-search OKR / help me organize my job-search direction", or uploads a resume without asking for resume edits. This skill also suits interns, new grads, and career switchers at the start of a job search doing three things: "self inventory + target profile + application management".
---

# Job Intent Tracker (job-search intent + application tracking)

This skill solves three core problems of the "job-search launch phase":

1. **Which roles should I apply for?** — extract signals from the user's background and work backwards to 2~3 target directions
2. **What does the target role look like?** — generate a "role profile / Target Profile" for each direction
3. **What have I applied to and how far along is it?** — maintain a structured tracking sheet (Excel / Markdown table)

Do not use this skill as "resume rewriting" or "interview question generation" — that's what resume-builder / jd-resume-tailor / interview-prep are for. This skill only cares about "direction" and "management".

---

## When to Trigger This Skill

Strong signals (basically always use it):
- "I want to change jobs / job-hop / find my next role"
- "Help me see what roles suit me"
- "Help me manage my applications / track the companies I applied to"
- "I have X years of Y experience — where should I go next?"
- "I applied to lots of places but lost track of the status"

Weak signals (confirm first, then use):
- The user only dropped a resume without stating a goal → first ask "Do you want to organize your direction, polish your resume, or prepare for interviews?"
- The user says "I want a job" but is vague → first ask "Do you already have a target direction, or would you like me to help you figure one out?"

---

## Workflow

Follow this order; do not skip a single step:

### Step 1: Background Intake

Use AskUserQuestion (or ask directly when that tool is unavailable) to collect the following. **Do not ask everything at once — split it into 2~3 rounds of 2~3 questions each**, otherwise the user will be put off by the "questionnaire feel".

Round 1 (must ask):
- Current / most recent job's role, company type, years of experience
- 3~5 core skills (keywords are fine)
- Target industry / target direction (if the user has one) — if not, that's fine, skip to Step 2

Round 2 (as needed):
- Expected salary range (skip if the user prefers not to say)
- City preference / open to remote
- Exclusions ("no sales / no overtime / no business travel", etc.)

Round 3 (deep signals; only ask when the first two rounds aren't enough to build a profile):
- The 1~2 projects they're proudest of
- What they dislike doing most
- Where they see themselves in 5 years

If the user uploaded a resume .pdf / .docx, **first call the pdf or docx skill to extract the text**, then pull the above information from it, so the user doesn't have to retype everything.

### Step 2: Recommend Job Directions

Based on Step 1's information, generate 2~3 candidate directions. For each direction, spell out:

```
Direction N: <role name> (e.g. internet product manager / data analyst / quant researcher)
- Fit: high / medium / low (high = core skills are a direct hit; medium = 1~2 key skills to fill; low = requires a career-switch narrative)
- Fit rationale: based on the user's ___ experience and ___ skills
- Gaps: the user still needs ___ to become a strong candidate
- Typical employers: <3~5 concrete companies or company types>
- Salary band (for reference only): __k - __k (note "market reference only; advise the user to verify for their level")
```

**Important: do not only recommend "safe" directions.** If the user's skills allow, include at least one "stretch" direction and honestly flag the gaps.

### Step 3: Generate the Role Profile (Target Profile)

For the 1~2 directions the user **finally picks** (let the user choose), generate a detailed profile. The template is in `references/target_profile_template.md`; read that file before filling it in.

The profile must include: typical responsibilities, skill requirements must-have / nice-to-have, expected interview process, and a benchmark company list (tiered).

Read the industry keyword libraries to decide must-have / nice-to-have:
- Internet product / operations / PM → `references/keywords_internet.md`
- Tech / engineering / data → `references/keywords_tech.md`
- Finance / consulting / business → `references/keywords_finance.md`
- General / cross-industry → `references/keywords_general.md`

### Step 4: Create the Application Tracking Sheet

Call `scripts/init_tracker.py` to generate the initial tracking sheet. The script supports two formats:

```bash
python scripts/init_tracker.py --format xlsx --output /path/to/tracker.xlsx
# or
python scripts/init_tracker.py --format md --output /path/to/tracker.md
```

xlsx is recommended by default (the user can sort and add conditional formatting). If the user explicitly wants something lightweight, use md.

The tracking sheet's column structure (predefined in the script; do not change):
Company, Role, Source (recruiter / careers site / referral / job board), JD link, Application date, Current stage (applied / written test / first interview / second interview / HR interview / Offer / Rejected / No response), Next action, Deadline, Salary range, Referrer, Notes

### Step 5: Build a "Job-Search Dashboard" with an Artifact (optional but recommended)

If the `mcp__cowork__create_artifact` tool is available in the current environment, proactively offer: "Want me to turn this tracking sheet into a dashboard you can open every day?"

If the user agrees, create an HTML artifact rendered from the tracking sheet data:
- Top KPIs: total applications / interviews entered / offers / pending follow-ups
- Middle table: Kanban view grouped by "current stage"
- Bottom reminders: companies silent for 3+ days, tasks with deadlines approaching

---

## Output Style

- **Structured and actionable**; never vague advice like "you should send out more resumes"
- For salary and industry judgments, **always label "market reference, not a promise"**
- When recommending directions, don't flatter (don't push every user toward "high-paying AI roles"); assess fit honestly
- If the user rejects a direction, don't push — ask why, then adjust

---

## Collaboration with Other Skills

- After the user picks a direction and says "now help me revise my resume" → call `resume-builder` and pass it the role profile
- The user says "tailor it to this company's JD" → call `jd-resume-tailor`
- The user says "help me prep for interviews" → call `interview-prep` and pass it the role profile

Output hand-off sentences like "I've saved your role profile to ___; next you can have me revise your resume with resume-builder" so the agent can chain multi-step tasks smoothly.

---

## Anti-Patterns (don't do these)

- ❌ Opening with 8 questions in a row
- ❌ Pushing 5 directions without asking about the user's preferences
- ❌ No tracking sheet — just talking at the user in chat
- ❌ Shoving "operations / product / project manager" at every humanities-background user
- ❌ Seeing "AI / large language models" and blindly pushing LLM roles without assessing actual skill fit
