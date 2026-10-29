---
name: quiz-html
description: Generates a **standalone, runnable web practice page** (HTML file) from an array of questions. After the user completes quiz-mastery's "generate questions from material" or "extract questions from a file" flow, proactively ask whether they want to "practice in a web page"; once confirmed, call this skill to inject the questions into the template and produce an HTML file for the user. Also triggers when the user directly asks to "turn these questions into a web page / HTML / practice page". Does NOT handle: question generation (→ quiz-mastery), grading (→ quiz-mastery), long-term review plans (→ study-buddy).
---

# Web Quiz Page Builder (Quiz HTML Builder)

Turns a JSON array of questions → a **single-file HTML practice page**, including:
- 📂 Category filtering (subject / submodule) + study status filtering (mastered / untried / mistakes)
- 🎯 4 question types: multiple choice / true-false / fill-in-the-blank / short answer
- 🤖 Automatic answer marking; wrong answers are filed into the mistake log automatically (one retry offered on a first mistake)
- ⌨️ Full keyboard shortcuts (A/B/C/D · Enter · arrow keys · Space)
- 📝 Mock exam mode (time limit + single submission + results page)
- 🌓 Light/dark theme toggle · localStorage persistence · mobile friendly

## Core Trigger Scenarios

### Scenario 1: Proactively ask after quiz-mastery generates/imports questions ⭐
This is the skill's **main entry point**. When `quiz-mastery` completes either of these flows:
- "Generate questions from material": `generate_from_material.py` → questions JSON → `service.import_questions()` into the store
- "Extract questions from a file": `import_quiz.py` → parsed into questions JSON → into the store

once quiz-mastery finishes generating questions and before showing them to the user, **proactively ask**:
> "Your questions are ready! Want me to turn them into a web practice page? You can work through them in the browser — wrong answers are recorded automatically, plus theme switching and mock exams 🎯"

If the user says yes ("sure", "make a web page", "go ahead", or any affirmative) → call this skill.
If the user says no ("no thanks", "never mind", "let's practice right here") → continue with the regular chat-based practice flow.

### Scenario 2: User directly asks for a web page
Trigger phrases:
- "turn these questions into a web page", "make an HTML practice page", "generate a quiz page"
- "I want to practice in the browser", "make a web version"
- "export the questions as HTML"

## How to Call

### One-line summary
```bash
python3 scripts/build_quiz_html.py <questions.json> [--title "..." --open]
```

### Standard flow

1. **Obtain the questions JSON** (an array; each item is one question)
   - Source A: LLM output after quiz-mastery generates questions (already in the standard format)
   - Source B: a question array pasted directly by the user
   - Source C: questions read from the store (quiz-mastery's `data/sessions/<sid>/questions.json`)

2. **Write to a temporary JSON file**:
   ```python
   import json, tempfile
   from pathlib import Path
   tmp = Path(tempfile.mkdtemp()) / "questions.json"
   tmp.write_text(json.dumps(questions, ensure_ascii=False), encoding="utf-8")
   ```

3. **Call the script**:
   ```bash
   python3 ~/Desktop/studybuddy_4.0/skills/quiz-html/scripts/build_quiz_html.py \
       /tmp/xxx/questions.json \
       --title "📚 Physics · Thermal Practice" \
       --output ~/Desktop/quiz_physics_thermal_20260518.html \
       --open
   ```

4. **Parse the returned JSON**:
   ```json
   {
     "success": true,
     "output_path": "/Users/.../quiz_xxx.html",
     "question_count": 8,
     "title": "📚 Physics · Thermal Practice",
     "subtitle": "8 questions total · choice×5 · true-false×2 · fill-blank×1 · Physics",
     "id": "q_1779091201",
     "size_bytes": 63752
   }
   ```

5. **Tell the user**: report the HTML path and mention the page is already open in the browser, ready to practice ✨

## Question JSON Field Standard

Fully compatible with the quiz-mastery output format, **plus two optional fields** `category` / `memory_tip`:

| Field | Required | Description |
|---|---|---|
| `type` | ✅ | `single_choice` / `true_false` / `fill_blank` / `short_answer` |
| `prompt` | ✅ | Question text. The `question` field is also accepted (auto-converted) |
| `options` | required for choice questions | `["A. xxx", "B. yyy", ...]` |
| `answer` | ✅ | Letter for choice questions; `"True"`/`"False"` for true-false; text for fill-blank / short-answer |
| `explanation` | recommended | Explanation (strongly recommended, especially for K-12 students) |
| `knowledge_point` | recommended | Knowledge point (used for second-level sidebar grouping) |
| `category` | recommended | Category path, **use the "Subject / Submodule" format**: `"Physics / Electricity"`, `"Math / Fractions"` |
| `level` | optional | Difficulty 1-3 |
| `memory_tip` | optional | Memory tip, highlighted in an orange card (a K-12 killer feature) |

### Example
```json
[
  {
    "type": "single_choice",
    "prompt": "Which statement about the current in a parallel circuit is correct?",
    "options": [
      "A. The main-line current equals the difference between the branch currents",
      "B. The main-line current equals the sum of the branch currents",
      "C. All branch currents are equal",
      "D. The main-line current is more than twice any single branch current"
    ],
    "answer": "B",
    "explanation": "In a parallel circuit, **the main-line current equals the sum of the branch currents**: I = I₁ + I₂ + ...",
    "knowledge_point": "Current rule for parallel circuits",
    "category": "Physics / Electricity",
    "level": 1,
    "memory_tip": "🧠 At a parallel junction: what goes in comes out — current never disappears"
  }
]
```

## Design Principles

### 1. Auto-fill category so filtering is meaningful
If questions lack the `category` field, fill it in (even by inferring the subject). Otherwise all questions pile into the "General" category and category filtering becomes useless.

### 2. category uses "Subject / Submodule"
- ✅ `"Physics / Electricity"`, `"Physics / Thermodynamics"` → produces 4 fine-grained chips at the top
- ❌ `"Physics"` → produces only 1; submodules still show in the sidebar, but filtering granularity is coarser

### 3. Knowledge points and categories are different levels
- `category` = horizontal classification (which subject/chapter), used for **top chip filtering**
- `knowledge_point` = fine-grained knowledge point, used for **second-level sidebar grouping**

### 4. Output file naming
By default the output goes to the same directory as the questions JSON, named `quiz_<title_slug>_<timestamp>.html`.
**Passing `--output` explicitly is recommended** — e.g. to `~/Desktop/` or another fixed directory so the user can find it.

## Working Example (full quiz-mastery handoff)

```python
# 1. quiz-mastery has finished generating questions; you have the question array
questions = [
    {"type": "single_choice", "prompt": "...", "options": [...], "answer": "A",
     "explanation": "...", "knowledge_point": "...", "category": "Physics / Electricity"},
    # ...
]

# 2. agent asks the user: "Want this as a web page?"
# 3. user: "Yes"
# 4. agent writes a temp file + calls the skill

import json, subprocess, tempfile
from pathlib import Path

tmp_dir = Path(tempfile.mkdtemp(prefix="quiz_"))
qjson = tmp_dir / "questions.json"
qjson.write_text(json.dumps(questions, ensure_ascii=False), encoding="utf-8")

output = Path.home() / "Desktop" / "quiz_physics_electricity.html"

result = subprocess.run([
    "python3",
    str(Path.home() / "Desktop/studybuddy_4.0/skills/quiz-html/scripts/build_quiz_html.py"),
    str(qjson),
    "--title", "📚 Physics · Electricity Practice",
    "--output", str(output),
    "--open",
], capture_output=True, text=True)

info = json.loads(result.stdout)
# info["output_path"] = "/Users/.../Desktop/quiz_physics_electricity.html"
```

Then tell the user:
> "All done — the page opened automatically ✨
> Path: `~/Desktop/quiz_physics_electricity.html`
> Take your time; wrong answers are recorded automatically, and next time you can filter by 'mistakes' to focus on them 💪"

## Boundaries with Other Skills

| Task | Use |
|---|---|
| Generate questions from material | **quiz-mastery** |
| Extract questions from files | **quiz-mastery** |
| Grading, mastery tracking, Ebbinghaus scheduling | **quiz-mastery** |
| Turn questions into a web page for browser practice | **quiz-html** (this skill) |
| Study plans, long-term follow-up | **study-buddy** |

## Failure Handling

- `exit 1`: bad arguments / file not found / template missing → report the error and ask the user to check paths
- `exit 2`: JSON format problem / invalid question data → tell the user which questions were skipped and suggest checking fields
- Some questions skipped but valid ones exist: generation still succeeds, but stderr lists the skipped questions — mention to the user "Skipped N questions, reason: ..."
