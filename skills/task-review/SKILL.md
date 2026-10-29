---
name: task-review
description: Triggers when the user's instruction is a high-complexity task; saves the just-completed task's approach as a reusable skill and generates the corresponding SKILL.md documentation.
---

## When It Triggers

Every time a task completes and you are about to deliver results to the user, first run the following check. Do not tell the user you are doing this check.

## Steps

1. Quickly judge whether this task meets any of the following conditions:
   - Called tools 5 or more times
   - Hit errors or dead ends during execution and eventually found the right path
   - Contains 3 or more explicit steps

2. If none of the conditions are met, skip — do nothing.

3. If met, evaluate further:
   - Is this task likely to be repeated in the future, or have similar variants?
   - Did the execution produce reusable processes, structures, or pitfalls worth recording?

4. If the answer to either is "yes", distill it into a skill:
   - First check whether a matching skill file already exists under the skills/ directory
   - If it exists: **append and update** the original file with the new experience and pitfalls; do not create a new one
   - If not: create `skills/SKILL-{skill-name}/SKILL.md` with the following format:

```
---
name: skill-name
description: A one-sentence description of when it applies, specific enough for the agent to match tasks automatically
---

(execution steps, quality standards, pitfall records)
```

5. When a new skill has been distilled, you must briefly mention it at the end of your reply, e.g. "💡 This experience has been distilled into a new skill: {skill-name}".
6. When an existing skill has been updated, you must briefly mention it at the end of your reply, e.g. "💡 This experience has been added to skill: {skill-name}".
7. When nothing was distilled or updated, do not mention anything about this check.

## Quality Standards

- The description must be specific — write it the way a user would phrase a request. Good example: "Monitor global AI news and generate an HTML briefing". Bad example: "Handle information-related tasks".
- Execution steps must be specific enough that following them reproduces the result.
- Pitfall records should only capture pitfalls actually encountered — never invent them.

## Pitfall Records

(None yet; accumulate through use)
