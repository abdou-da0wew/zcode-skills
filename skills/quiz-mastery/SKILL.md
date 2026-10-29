---
name: quiz-mastery
description: Question generation, quizzes, review, and mastery tracking. **Trigger this skill first when the user says any of "review", "reinforce", or "go over"**. Also triggers for requests related to "questions/review": turn study material / PDFs / documents into question practice ("make a few questions from this PDF"), import a question file for practice ("I have a question file, help me work through it"), review previously studied content ("review yesterday's", "reinforce this", "go over yesterday's", "arrange my reviews with Ebbinghaus"), forgetting-curve tracking, and mastery scoring. **🔴 Mandatory rule**: after every successful question generation/import, **before showing the questions for the first time you must ask** "Want me to generate a web practice page?" — if the user says yes, call the quiz-html skill. Does NOT handle: long-term study project progress management or planning (→ study-buddy).
---

# Quiz Mastery

## Two Core Capabilities

### Capability 1: Generate questions from study material
1. The user provides study material (.md / .txt / .docx / .pdf / .ppt / .pptx)
2. Call `generate_from_material.py` to get the knowledge-point extraction prompt
3. Send the prompt to the LLM to get the knowledge points JSON
4. Call `service.save_knowledge_points()` to save the knowledge points
5. Call `run_quiz.py` to generate the question prompt
6. Send the prompt to the LLM to get the questions JSON
7. **⭐ Ask the user whether to generate a web practice page** (see the "Web practice integration" section below)
   - Yes → call the `quiz-html` skill to generate the HTML and open it
   - No → continue with the regular flow
8. Present the questions one by one and collect answers
9. Call `submit_answers.py` to submit and grade

### Capability 2: Practice from a question file
1. The user provides a question file (.md / .txt / .docx / .pdf / .ppt / .pptx)
2. Call `import_quiz.py` to get the question-parsing prompt
3. Send the prompt to the LLM to get normalized questions JSON
4. Call `service.import_questions()` to import the questions and create a session
5. **⭐ Ask the user whether to generate a web practice page** (see the "Web practice integration" section below)
   - Yes → call the `quiz-html` skill to generate the HTML and open it
   - No → continue with the regular flow
6. Present the questions one by one and collect answers
7. Call `submit_answers.py` to submit and grade

## When to Use (Trigger Conditions)

1. **User asks directly**: "make a few questions", "test me", "quick quiz", "practice questions", "quiz me"
2. **User says "review", "reinforce", "go over"**: trigger immediately
3. **Practice based on an existing question file**: trigger when the user uploads a question file

> ⚠️ **Do NOT handle study-buddy's "instant practice"** — that pipeline is handled by study-buddy through the external `exam_take` flow and does not call this skill.

## Fallback When There Is No History

When the user says "review" but `data/user_progress/` is empty (new user / never answered anything):
- **Do not force-start the review flow** — there is nothing to review
- Proactively tell the user: "There's no history data to review yet. Want to generate some questions from a piece of study material first?"
- Guide the user into "Capability 1: Generate questions from study material"

## Difficulty System

| Level | Meaning | Description |
|------|------|------|
| L1 | Recall | Basic memorization and understanding; tests concept recognition and basic facts |
| L2 | Understand | Deeper understanding; tests concept discrimination, explaining principles, simple application |
| L3 | Apply | Synthesis; tests real-scenario application, analysis, and problem solving |

- **First quiz**: always starts at L1
- **Correct at current level**: level up (max L3)
- **Wrong at current level**: level down (min L1)

## Question Type Allocation Rules

| Level | Choice | True/False | Fill-blank | Short answer |
|------|--------|--------|--------|--------|
| L1 | 70% | 30% | - | - |
| L2 | 50% | 20% | 30% | - |
| L3 | 40% | 20% | 20% | 20% |

## Number of Questions

- **Default is 3 questions per round** (show 3 questions in one message; the user answers all of them once, then they are graded together)
- Max **15 questions per round** (the user may ask to adjust the count)
- Keep short-answer questions rare; they are not auto-graded (marked `needs_review` and judged by the external LLM / a human)

## Weak Knowledge Point Tracking

- **Marked weak**: cumulative wrong count ≥ 3
- **Never cleared**: weak knowledge points only grow, never shrink; they are kept as a historical archive
- Internal data is stored in `data/user_progress/` (wrong counts, Ebbinghaus stages, etc.)
- **Sync to USER.md section 3, "Weak knowledge points"** (written directly by this skill, source=`quiz-mastery`):
  | Knowledge point | Wrong count | Source | Notes |
  - Knowledge point already in the table → update its wrong count
  - Not in the table → add a new row

## Forgetting-Curve Review Mechanism

Based on the Ebbinghaus forgetting curve, reviews are scheduled at **1 day → 2 days → 4 days → 7 days → 15 days** intervals:
- Correct answer: review_stage +1 (advance to the next interval)
- Wrong answer: review_stage reset to 0 (start over)
- Review recommendations include: knowledge points about to be forgotten + weak knowledge points from the last 3 days

## How to Call the Scripts

### 1. Extract knowledge points from study material

```bash
python3 scripts/generate_from_material.py <file_path> <document_id>
```

Outputs the knowledge-point extraction prompt (JSON); send prompts.system_prompt and prompts.user_prompt to the LLM.

### 2. Import questions from a question file

```bash
python3 scripts/import_quiz.py <file_path> <document_id> <user_id>
```

Outputs the question-parsing prompt (JSON); send prompts.system_prompt and prompts.user_prompt to the LLM.

### 3. Generate a quiz

```bash
python3 scripts/run_quiz.py <user_id> <document_id>
```

Automatically decides difficulty from the saved knowledge points and the user's current mastery, and outputs the question-generation prompt (JSON).

### 4. Submit answers

```bash
python3 scripts/submit_answers.py <user_id> <document_id> <session_id> '<answers_json>'
```

Parameter notes:
- `answers_json`: an answers dictionary in JSON format, e.g. `{"q_001": "A", "q_002": "True"}`

Returns the grading result: score, total, accuracy, per-question results.

## Question Generation Flow (for study-buddy callers)

1. Determine the knowledge point source (study material or an existing question file)
2. Run the corresponding extraction / import flow
3. Call `run_quiz.py` to generate the question prompt
4. **Show 3 questions to the user at a time** (all at once, clearly numbered — not one at a time); the user answers all of them once, then grading happens together
5. Collect the user's answers (the user may reply with answers to all 3 questions in one message)
6. Call `submit_answers.py` to submit and grade
7. Return the grading result to study-buddy, which writes it to its memory files

⚠️ **This skill only writes to USER.md section 3, "Weak knowledge points"** (source=`quiz-mastery`); it does not write to any other section, nor to `memory/`. All other persistence is handled by study-buddy.

## Data Directory Structure

```
skills/quiz-mastery/data/
├── knowledge_points/     ← knowledge point definitions (by document_id)
├── sessions/             ← quiz session records
└── user_progress/        ← user mastery data (incl. weak flags, forgetting curve)
```

## ⭐ Web Practice Integration (cooperation with quiz-html)

Every time you obtain the questions JSON (step 7 of Capability 1 / step 5 of Capability 2), **proactively ask the user**:

> "Your questions are ready! Want me to turn them into a web practice page? You can work through them in the browser — wrong answers are recorded automatically, plus theme switching and mock exams 🎯"

### Interpreting the User's Reply

| User says | Verdict | Action |
|---|---|---|
| "yes / sure / go ahead / make it / generate / web page / browser" | ✅ Yes | Call `quiz-html` |
| "no / no thanks / never mind / practice right here" | ❌ No | Continue with the regular chat flow |
| No reply / unclear | Default ❌ No | Continue with the regular flow; do not push |

### Concrete Steps for Calling quiz-html

```python
import json, subprocess, tempfile
from pathlib import Path

# 1. Write the question JSON you already have to a temp file
tmp_dir = Path(tempfile.mkdtemp(prefix="quiz_"))
qjson = tmp_dir / "questions.json"
qjson.write_text(json.dumps(questions, ensure_ascii=False), encoding="utf-8")

# 2. Decide the output path (~/Desktop recommended)
output = Path.home() / "Desktop" / f"quiz_{title_slug}.html"

# 3. Call the script
result = subprocess.run([
    "python3",
    str(Path.home() / "Desktop/studybuddy_4.0/skills/quiz-html/scripts/build_quiz_html.py"),
    str(qjson),
    "--title", page_title,        # e.g. "📚 Physics · Electricity Practice"
    "--output", str(output),
    "--open",                     # open in the browser automatically after generating
], capture_output=True, text=True)

info = json.loads(result.stdout)  # {"success": true, "output_path": "...", ...}
```

### Recommendations for Completing Question Fields

Before calling, it is best to fill in the following fields for each question (if they were not generated):
- `category`: **top-level category, a short word** (2-6 characters recommended), used by the web page's top category filter chips.
  - ✅ Recommended: `Physics` / `Math` / `Law` / `History` / `Programming` / `General`
  - ❌ Avoid long strings with dates/numbers/slashes like `General / 1. Securities Act (December 29, 1998...)`
  - If you really need two levels, separate them with `/` and keep the second level short too: `Physics / Electricity`
- `knowledge_point`: knowledge point name (used for sidebar grouping; may match quiz-mastery's KP title, without hierarchical prefixes)
- `memory_tip`: memory tip (optional; K-12 students find it very useful)

This is what makes the web page's category filtering, sidebar grouping, and memory cards work.

### Boundaries

| Task | Use |
|---|---|
| Generating questions, extracting questions | this skill (quiz-mastery) |
| Grading, mastery tracking | this skill (quiz-mastery) |
| **Questions → web practice page** | **quiz-html** |

After calling quiz-html, **still run quiz-mastery's grading flow** — the answer states in the web page are for the user's self-checking; the official mastery data must be written via `submit_answers.py`. The two run in parallel without conflict.
