from __future__ import annotations

import json
from .models import KnowledgePoint


# Maximum questions per quiz round
MAX_QUESTIONS_PER_ROUND = 15

# Question type distribution by level
LEVEL_DISTRIBUTION = {
    1: {"single_choice": 70, "true_false": 30},
    2: {"single_choice": 50, "fill_blank": 30, "true_false": 20},
    3: {"single_choice": 40, "fill_blank": 20, "true_false": 20, "short_answer": 20},
}


class QuizGenerator:
    """Builds prompt templates for LLM-based quiz generation.

    This module does NOT call any LLM API. It constructs system_prompt and
    user_prompt that should be sent to an LLM by the caller (agent).
    """

    def generate_quiz(
        self,
        knowledge_points: list[KnowledgePoint],
        level: int = 1,
        num_questions: int | None = None,
    ) -> dict:
        """Build prompts for quiz generation.

        Args:
            knowledge_points: List of knowledge points to quiz on.
            level: Difficulty level (1, 2, or 3).
            num_questions: Number of questions to generate (max 15).

        Returns:
            dict with 'system_prompt' and 'user_prompt' keys.
        """
        level = max(1, min(3, level))
        if num_questions is None:
            num_questions = 3  # Default: 3 questions per round for efficiency
        num_questions = min(num_questions, MAX_QUESTIONS_PER_ROUND)

        distribution = LEVEL_DISTRIBUTION[level]
        distribution_text = "\n".join(
            f"  - {qtype}: {pct}%" for qtype, pct in distribution.items()
        )

        # Build knowledge point descriptions for the prompt
        kp_descriptions = []
        for kp in knowledge_points:
            desc_parts = [f"- **{kp.title}** (ID: {kp.id})"]
            if kp.definition:
                desc_parts.append(f"  Definition: {kp.definition}")
            if kp.description:
                desc_parts.append(f"  Description: {kp.description}")
            if kp.source and kp.source.snippets:
                desc_parts.append(f"  Source snippets: {'; '.join(kp.source.snippets)}")
            kp_descriptions.append("\n".join(desc_parts))

        kp_text = "\n\n".join(kp_descriptions)

        level_desc = {
            1: "Recall (basic memorization and understanding; tests concept recognition and basic facts)",
            2: "Understand (deeper understanding; tests concept discrimination, explaining principles, and simple application)",
            3: "Apply (synthesis; tests real-scenario application, analysis, and problem solving)",
        }

        system_prompt = (
            "You are a professional question-writing assistant. Generate high-quality quiz "
            "questions based on the knowledge point information provided.\n"
            "Strictly output in the required JSON format; do not output anything else.\n"
            "Questions must stay closely tied to each knowledge point's name, definition, and "
            "source description; never write questions that drift away from the source."
        )

        user_prompt = f"""Generate {num_questions} quiz questions based on the following knowledge points.

## Difficulty level
Level {level}: {level_desc[level]}

## Question type distribution
{distribution_text}

## Knowledge point information

{kp_text}

## Question-writing requirements
1. Every question must be linked to at least one knowledge point ID
2. Choice questions (single_choice): 4 options A/B/C/D; answer is the correct option letter
3. True/false questions (true_false): answer is "True" or "False"
4. Fill-blank questions (fill_blank): mark blanks with ____ in the prompt; answer is the correct answer text
5. Short-answer questions (short_answer): answer is the reference answer
6. Every question must include an explanation
7. Question content must be based on the knowledge point names, definitions, and descriptions above; do not go out of scope
8. **Every question must fill in the `category` and `knowledge_point` fields** (used for category filtering and sidebar grouping):
   - `category`: top-level category, a **short word** (2-6 characters recommended), used by the top category filter chips.
     Examples: Physics / Math / Law / History / Programming / General.
     Do **not** write long strings; do not include dates, numbers, book-title marks, or slashes.
   - `knowledge_point`: the name of the knowledge point this question belongs to (just use the linked knowledge point's title); used for sidebar grouping.
9. Total number of questions: {num_questions}

## Output format
Output a plain JSON array; each element has the following shape:
```json
[
  {{
    "id": "q_001",
    "knowledge_point_ids": ["kp_id"],
    "category": "Physics",
    "knowledge_point": "Newton's Second Law",
    "level": {level},
    "type": "single_choice",
    "prompt": "Question text",
    "options": ["A. Option one", "B. Option two", "C. Option three", "D. Option four"],
    "answer": "A",
    "explanation": "Explanation"
  }}
]
```

Output the JSON array directly, without markdown code fences or any other text."""

        return {
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
        }
