from __future__ import annotations

import json
from .models import Question


def build_extraction_prompt(content: str) -> dict:
    """Build a prompt for LLM to parse questions from a question file.

    Args:
        content: Raw text content containing questions.

    Returns:
        dict with 'system_prompt' and 'user_prompt' keys.
    """
    system_prompt = (
        "You are a professional question-parsing assistant. Identify and parse every "
        "question in the question file provided by the user.\n"
        "Strictly output in the required JSON format; do not output anything else."
    )

    user_prompt = f"""Parse all questions from the following question file content.

## Question file content

{content}

## Parsing requirements
1. Identify each question's type:
   - single_choice: multiple choice (has A/B/C/D style options)
   - true_false: true/false (judge right or wrong)
   - fill_blank: fill-in-the-blank (has blanks to fill in)
   - short_answer: short answer (requires a written response)
2. Extract all information for each question
3. If a question has an answer and explanation, extract those too
4. Assign a unique ID to each question

## Output format
Output a plain JSON array; each element has the following shape:
```json
[
  {{
    "id": "q_001",
    "knowledge_point_ids": [],
    "level": 1,
    "type": "single_choice",
    "prompt": "Question text",
    "options": ["A. Option one", "B. Option two", "C. Option three", "D. Option four"],
    "answer": "A",
    "explanation": "Explanation (if available)"
  }}
]
```

Notes:
- type must be one of single_choice, true_false, fill_blank, short_answer
- For choice questions, answer is the option letter (A/B/C/D)
- For true/false questions, answer is "True" or "False"
- For fill-blank questions, answer is the correct answer text
- For short-answer questions, answer is the reference answer (if available)
- If knowledge_point_ids cannot be determined, leave an empty array
- level defaults to 1; adjust it if the question's difficulty is apparent

Output the JSON array directly, without markdown code fences or any other text."""

    return {
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
    }


def parse_questions_json(json_str: str) -> list[Question]:
    """Parse LLM-returned JSON string into a list of Question objects.

    Args:
        json_str: JSON string containing a list of question dicts.

    Returns:
        List of Question objects.

    Raises:
        json.JSONDecodeError: If json_str is not valid JSON.
        ValueError: If the parsed data is not a list.
    """
    # Try to extract JSON from possible markdown code blocks
    cleaned = json_str.strip()
    if cleaned.startswith("```"):
        # Remove markdown code block markers
        lines = cleaned.split("\n")
        # Remove first line (```json or ```)
        lines = lines[1:]
        # Remove last line (```)
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        cleaned = "\n".join(lines)

    data = json.loads(cleaned)
    if not isinstance(data, list):
        raise ValueError(f"Expected a JSON array, got {type(data).__name__}")

    questions: list[Question] = []
    for item in data:
        q = Question(
            id=item.get("id", "q_unknown"),
            knowledge_point_ids=item.get("knowledge_point_ids", []),
            level=item.get("level", 1),
            type=item.get("type", "single_choice"),
            prompt=item.get("prompt", ""),
            options=item.get("options", []),
            answer=item.get("answer"),
            explanation=item.get("explanation", ""),
            source_refs=item.get("source_refs", []),
        )
        questions.append(q)

    return questions
