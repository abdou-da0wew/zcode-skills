---
name: cheat-sheet
description: Condense PDF/Word/Markdown study material into a distilled knowledge-cheatsheet document. Supports three styles (quick-reference cards / mind-map style / Q&A style) and outputs a two-column, small-font PDF. Trigger when the user says "generate a knowledge cheatsheet", "generate a cheatsheet", "make me a quick-reference sheet", "condense this material onto one page", "make a knowledge card". **Does NOT handle**: generating quizzes from material (→ quiz-mastery) or long-term study projects (→ study-buddy).
---

# Cheatsheet Generator

## What You Do

Compress the user's study material (PDF/Word/Markdown/text) into a **two-column, small-font, information-dense** Cheatsheet document (PDF format).

**Core principle: keep only the substance, cut the fluff.**

---

## ⚠️ Iron Rule: Avoid Duplicate Creation

Before generating a Cheatsheet, **scan the output directory first** to check whether a file on the same topic already exists:
- **Exists** → ask the user "There's already a [file name] — overwrite / create new / skip?" and wait for the reply before acting
- **Does not exist** → generate directly
- **Never** overwrite without asking

---

## Workflow

### Step 1: Receive the material

The user provides study material files. Supported formats:
- `.pdf` — use the PDF skill's process route to extract text
- `.docx` — use the PDF skill's process route to extract text
- `.md` / `.txt` — read directly

**Text extraction commands:**
```bash
# Extract text from PDF
python3 "$PDF_SCRIPTS/pdf.py" extract.text <file_path>

# Convert Word to PDF first, then extract (if needed)
python3 "$PDF_SCRIPTS/pdf.py" convert.office <file_path>
```

where `$PDF_SCRIPTS` is the scripts directory path of the PDF skill, derived from the location of the PDF skill's SKILL.md.

If the user didn't provide a file but pasted text content directly, skip the extraction step and use the text as-is.

---

### Step 2: Choose a style

**You must ask the user** which style they want (do not choose for them):

Present these options:
1. 📋 **Quick-reference cards** — core concepts + definitions + key formulas/points at a glance; ideal for last-minute exam prep
2. 🌳 **Mind-map style** — organized hierarchically (heading → subheading → points) with an outline feel; ideal for structuring a subject
3. ❓ **Q&A style** — turns knowledge points into "question → answer" pairs; ideal for self-testing review

After the user chooses, proceed to Step 3.

---

### Step 3: LLM distills the content

Based on the chosen style, construct different prompts so the LLM distills cheatsheet content from the source text.

#### Style 1: Quick-reference cards

Distillation rules:
- Extract all core concepts, definitions, formulas, and key data
- Format each knowledge point as **term: one-sentence explanation**
- Group related knowledge points, each group with a small heading
- Keep important formulas/code snippets verbatim
- Cut all examples, transition sentences, and background filler

Output structure:
```
## [Group heading]
- **Term A**: one-sentence definition
- **Term B**: one-sentence definition
- 📐 Formula: `formula content`

## [Group heading]
...
```

#### Style 2: Mind-map style

Distillation rules:
- Extract the document's hierarchical structure (chapter → section → points)
- Summarize each node in the fewest possible words
- At most 3 levels deep (anything deeper won't fit on one page)
- Use indentation and symbols to express hierarchy

Output structure:
```
# Topic

## Level-1 branch
  ├─ Level-2 point
  │   ├─ Detail 1
  │   └─ Detail 2
  └─ Level-2 point
      └─ Detail
```

#### Style 3: Q&A style

Distillation rules:
- Convert each knowledge point into a question
- Keep answers to 1-3 sentences
- Order questions from basic to advanced
- Create discrimination questions for easily confused concepts

Output structure:
```
## [Topic group]

**Q: What is XXX?**
A: One-sentence answer.

**Q: Difference between XXX and YYY?**
A: Brief comparison.
```

---

### Step 4: User confirmation and adjustment

After the LLM generates the content, **show it to the user as text first** and ask:

> "The content is organized — anything you'd like to adjust? For example:
> - Should any sections be highlighted?
> - Should anything be removed or added?
> - Any layout preferences? (e.g. smaller font size, color-coded sections, etc.)"

After the user confirms it's OK, proceed to Step 5.
If the user requests changes → adjust → show again → wait for confirmation.

---

### Step 5: Generate the PDF

Call the PDF skill's **Report route (ReportLab)** to generate the two-column PDF.

**Layout spec (defaults):**

| Parameter | Default | Notes |
|------|--------|------|
| Page size | A4 | Adjustable on request |
| Columns | Two | Two-column by default; single column optional |
| Body font size | 8pt | Information density first; adjustable on request |
| Heading font size | 10pt (level 1) / 9pt (level 2) | |
| Line spacing | 1.2 | Compact but readable |
| Margins | 12mm on all sides | Maximizes content area |
| Fonts | UniSong/UniHei for CJK text, Helvetica for Latin | |

**Generation flow:**

1. Convert the LLM-distilled Markdown content into ReportLab layout instructions
2. Call the PDF skill's report route to generate the PDF
3. Tell the user the generated file path

**When calling the PDF skill, follow all rules in its SKILL.md**, including:
- CJK font checks
- Table overflow protection
- Page fill-rate checks
- Metadata settings

---

### Step 6: Deliver

Output to the user:
- 📄 The PDF file path
- File size and page count
- A note that they can keep adjusting

---

## Notes

### Content quality
- **Never fabricate content**: every knowledge point must come from the source text; no free-styling
- **Never omit key content**: core concepts, formulas, and definitions must be preserved
- **Keep original terminology**: do not substitute technical terms on your own

### File operations
- Generated PDFs are saved to the workspace root by default, named `cheatsheet_[topic]_[date].pdf`
- Duplicate checking: see "⚠️ Iron Rule: Avoid Duplicate Creation" above

---

## Relationship to Other Skills

| Skill | Relationship |
|-------|------|
| PDF skill | Its process route extracts text; its report route generates the PDF |
| study-buddy | study-buddy may recommend generating a cheatsheet after the user completes a study project |
| quiz-mastery | No direct relationship, but cheatsheet content can serve as a source of knowledge points for quiz generation |

---

## File Structure

```
skills/cheat-sheet/
├── SKILL.md              ← current file
```

This skill is a pure workflow guide and contains no standalone scripts. All file operations and PDF generation are done by calling the PDF skill.
