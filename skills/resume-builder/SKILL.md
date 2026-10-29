---
name: resume-builder
description: Generates a resume from scratch or fully optimizes an existing one, and exports it to docx / pdf / markdown. Rewrites experiences using the STAR method, runs ATS keyword coverage checks, and picks a template by industry (internet product / tech / finance / general). Trigger this skill when the user says "help me write my resume / improve my resume / I don't know how to write a resume / my resume is too weak / my resume looks unprofessional / polish my resume / make me a resume template / export my resume / add keywords to my resume", or uploads a .pdf/.docx resume and asks "how should I improve it". Trigger even when the user only asks "what's wrong with my resume".
---

# Resume Builder

This skill does three things:

1. **Structured generation**: turn the user's experiences into a polished, professionally structured resume
2. **STAR-method rewriting**: transform weak sentences like "participated in X" into "did X, enabling Y, resulting in Z"
3. **ATS keyword optimization + multi-template export**: make sure the resume passes automated screening, and support docx/pdf/md export

Does not do: JD-targeted rewriting (that's jd-resume-tailor's job — go there for "tailor my resume to a specific JD")

---

## When to Trigger

- "Help me write a resume"
- "My resume is too weak / has no highlights / looks unprofessional"
- "Rewrite this experience with STAR"
- "Are there enough keywords in my resume?"
- "Export the resume as PDF / docx"
- User uploads a resume without saying "tailor it to a JD" → trigger this skill; if they say "tailor it for company X / role X" → call jd-resume-tailor

---

## Workflow

### Step 1: Understand the Resume's Current State

If the user **has a resume file** (.pdf / .docx / .md / .txt):
- pdf → parse with the pdf skill
- docx → parse with the docx skill
- Extract: basic info, education, work experience, project experience, skills, other

If the user **has no resume**:
- Use AskUserQuestion to collect information (see the question list in `references/intake_questions.md`)
- Ask 3-4 questions per round, gathered over multiple rounds, so the user doesn't drop off

### Step 2: Pick a Template

Read `references/templates/` to decide the structure:

- Internet product / operations / PM → `templates/internet.md`
- Engineering / R&D / data → `templates/tech.md`
- Finance / consulting / business → `templates/finance.md`
- General / cross-industry → `templates/general.md`

If the user hasn't specified a direction, use the general template, but **ask one question**: "Which direction will you mostly be applying to? I can use a layout better suited to it."

### Step 3: Rewrite Every Experience with STAR

Read `references/star_rewrite_guide.md` and apply STAR rewriting to each work / project bullet.

**STAR is not a rigid 4-section format** — it means every bullet contains:
- **A context signal** (one sentence sizing the problem or situation)
- **An action** (what you specifically did, with a verb)
- **A result** (number / percentage / ranking / scale)

If the user's information contains **no numbers**, proactively follow up: "Roughly how many users did this project have?" "About how much did this optimization improve things? Even an order of magnitude is fine if you're not sure."

### Step 4: ATS Keyword Check

Call the script:

```bash
python scripts/ats_check.py --resume <resume.md> \
    --industry internet \
    [--jd <jd.txt>]
```

The script will:
1. Extract keywords from the resume
2. Compare against the industry keyword library (from job-intent-tracker or this skill's `references/keywords/`)
3. Output two lists: "covered" / "suggested additions"
4. Give an ATS-friendliness score (font uniformity, table usage, special symbols, images, etc.)

**Hard rules for ATS-friendly resumes**:
- Don't use Word tables for experiences (many ATS can't parse them)
- Don't put dates inside decorative images
- Don't use two-column layouts (some ATS read column by column, scrambling the order)
- Don't insert icons / emoji in headings
- Use one of these fonts: Times New Roman / Source Han Serif / Arial / Helvetica

### Step 5: Multi-Format Export

Read `references/export_guide.md` and choose based on the user's needs:

**docx export** (the most universal; HR usually prefers docx):
- Call the docx skill
- Use `assets/resume_template.docx` as the template (if it exists)

**pdf export** (the final submission version):
- Recommended flow: docx first → then convert to pdf with Word/LibreOffice
- Generating pdf directly with reportlab looks bad; not recommended
- Call the pdf skill for post-processing (encryption / metadata cleanup)

**markdown export** (backup + GitHub):
- Just write the .md file

**Default behavior**: unless the user specifies, output both docx + md versions.

### Step 6: Self-Check & Feedback

After output, run one self-check (show it in chat for the user; no separate file needed):

```
✓ Length: < 1 page (new grad) / ≤ 2 pages (experienced)
✓ Contact info complete (phone + email, optionally GitHub/portfolio)
✓ Every experience has quantified results
✓ Keyword coverage (vs. <industry> keyword library): __%
✓ ATS friendliness: __/10
⚠ Pending user confirmation: <info still to be filled in>
```

---

## Anti-patterns (do not do)

- ❌ Making up numbers for the user (saying "improved 30%" when the user never said so) — must be based on information the user provided; if unknown, mark `[TODO: exact number]`
- ❌ Piling up adjectives ("excellent communication skills", "conscientious and responsible", "self-motivated") — delete them
- ❌ Writing more than 5 bullets for one experience — too dense and HR will skim past it
- ❌ Writing a long "self-evaluation" section — out of fashion; a 1-2 line summary is enough
- ❌ Giving every company the same number of bullets — write more for the important ones, less for the minor ones
- ❌ Using "familiar with / aware of / can use" as capability descriptions — rewrite as "used X to do Y"

## Collaboration with Other Skills

- User then says "tailor it for this company" → hand off to `jd-resume-tailor`
- User then says "prepare me for interviews" → hand off to `interview-prep`
- User comes to fix the resume without a direction in mind → ask back "What direction are you applying to?", and hand off to `job-intent-tracker` if needed
