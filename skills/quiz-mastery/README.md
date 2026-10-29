# Quiz Mastery Skill

A standalone question-generation / review / mastery-tracking engine for the DiveeOI agent (OpenCode-based).

## Features

- **Generate questions from study material**: turn PDF / Word / Markdown study material into leveled quizzes (L1/L2/L3)
- **Import questions from a question file**: parse an existing question file, normalize it, and let the user practice
- **Answer grading**: automatic grading + per-question feedback
- **Mastery tracking**: records user progress across the three difficulty levels
- **Weak knowledge points**: cumulative wrong count ≥ 3 → marked weak (**only grows, never shrinks**; kept as a historical archive)
- **Forgetting-curve review**: schedules reviews based on the Ebbinghaus curve (1/2/4/7/15 days)

## Architecture

```
quiz-mastery/
├── SKILL.md                          # Skill metadata (read by the LLM)
├── README.md                         # this file (for humans)
├── skill.yaml                        # Skill configuration
├── scripts/
│   ├── generate_from_material.py     # Extract knowledge points from study material
│   ├── import_quiz.py                # Import questions from a question file
│   ├── run_quiz.py                   # Build the quiz-generation prompt
│   └── submit_answers.py             # Submit answers + grading
├── src/quiz_mastery/                 # Core engine
└── data/
    ├── knowledge_points/             # Document knowledge point definitions
    ├── user_progress/                # User mastery data (incl. weak flags, Ebbinghaus stages)
    └── sessions/                     # Quiz session records
```

## Quick Start

### 1. Extract knowledge points from study material

```bash
python3 scripts/generate_from_material.py <file_path> <document_id>
```

Outputs the knowledge-point extraction prompt (JSON). Send `prompts.system_prompt` and `prompts.user_prompt` to the LLM, then call `service.save_knowledge_points()` to save the resulting knowledge-point list.

### 2. Import from a question file

```bash
python3 scripts/import_quiz.py <file_path> <document_id> <user_id>
```

Outputs the question-parsing prompt (JSON). Send the prompt to the LLM to get normalized questions, then call `service.import_questions()` to import them.

### 3. Generate a quiz

```bash
python3 scripts/run_quiz.py <user_id> <document_id>
```

Automatically decides difficulty from the user's current mastery and outputs the question-generation prompt (JSON).

### 4. Submit answers

```bash
python3 scripts/submit_answers.py <user_id> <document_id> <session_id> '<answers_json>'
```

Returns: `score`, `total`, `accuracy`, and per-question `results`.

## Data Integration (relationship with the DiveeOI agent)

This skill **does not write to `memory/`**; it only writes to USER.md section 3, "Weak knowledge points". All other persistence is the responsibility of the calling agent — see SKILL.md for details.

| Data | Written by | Written where |
|------|------|--------|
| Knowledge point definitions, answer records, Ebbinghaus stages | this skill | `data/` directory |
| Weak knowledge points (wrong count ≥ 3) | this skill | USER.md section 3 (source=`quiz-mastery`) |
| Study project status, DAY schedule | study-buddy (upstream agent) | USER.md section 2 |

## Difficulty System

| Level | Meaning |
|------|------|
| L1 | Recall (basic memorization and understanding) |
| L2 | Understand (deeper understanding, application) |
| L3 | Apply (synthesis, problem solving) |

- First quiz always starts at L1
- Correct answers level up (max L3); wrong answers level down (min L1)

## Workflow

1. **Generate / Import**: create knowledge points + questions from study material or a question file
2. **Run**: generate the quiz
3. **Submit**: user answers → auto-grading → update mastery / weak flags
4. **Sync**: weak knowledge points are written to USER.md section 3
