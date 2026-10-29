# Shared Task Instructions: Skills Localization for Open-Source Release

You are working inside `/home/z/my-project/skills/`. Your specific batch of files is listed in the batch file given in your task prompt. The user wants these AI-agent skills published as an open-source repo for the **DiveeOI agent (an OpenCode-based agent)** usable with **general open-source / free LLMs** (Ollama, vLLM, LM Studio, OpenRouter, Qwen, Llama, DeepSeek, Mistral, etc.).

## Two jobs on every assigned file

### Job 1 — Translate ALL Chinese to English
- Translate every Simplified/Traditional Chinese string to natural, professional English: prose, comments, docstrings, UI labels, log messages, JSON string values, HTML visible text, CSS comments, YAML descriptions.
- KEEP valid syntax: markdown structure, JSON validity (translate values, NOT keys), YAML frontmatter validity, code correctness.
- KEEP unchanged: URLs (unless Z.ai-owned, see Job 2), file paths, code identifiers, env var names, CLI flags, placeholders like `{{name}}`, regexes, `<sub>`/`<super>` HTML-ish tags in markdown.
- Chinese punctuation (，。：；！？（）“”‘’、) → English punctuation.

### Job 2 — De-brand Z.ai / GLM, re-target to DiveeOI + open-source LLMs
Rebranding table (apply consistently in every assigned file):
| Found | Replace with |
|---|---|
| `Z.AI` / `Z.ai` / `z.ai` as author/company | `DiveeOI` (e.g. frontmatter `author: DiveeOI`, LICENSE → `Copyright (c) 2026 DiveeOI contributors`) |
| "Z.ai" as the running agent/platform ("在 Z.ai 中", "Z.ai's agent") | "the DiveeOI agent (OpenCode-based)" or "the agent" |
| GLM model names (`GLM-4.6`, `glm-4-flash`, `glm-4.5v`, ...) | generic open-source examples: `qwen2.5`, `llama3.1`, `deepseek-r1` — or configurable via env where code |
| `z-ai-web-dev-sdk` (package import) | rewrite to plain OpenAI-compatible HTTP calls (pattern below) |
| `open.bigmodel.cn`, `chatglm.cn`, `api.z.ai`, `chat.z.ai` endpoints | `LLM_BASE_URL` env-configured OpenAI-compatible endpoint |
| `智谱` / `Zhipu` / `清言` / `Qingyan` / `ChatGLM` | generic ("the LLM", "your model", "DiveeOI") |
| "Z.ai skills" / zai-org GitHub links | "this skills collection" / repo-neutral wording |

**SDK rewrite pattern** — every script importing `z-ai-web-dev-sdk` must be rewritten with the SAME behavior, CLI, and function signatures, but zero new npm/pip dependencies:

TypeScript:
```ts
// Works with any OpenAI-compatible server: Ollama, vLLM, LM Studio, OpenRouter, ...
const BASE_URL = process.env.LLM_BASE_URL ?? "http://localhost:11434/v1";
const API_KEY = process.env.LLM_API_KEY ?? "";
const MODEL = process.env.LLM_MODEL ?? "qwen2.5";

async function chatCompletions(body: Record<string, unknown>): Promise<any> {
  const res = await fetch(`${BASE_URL}/chat/completions`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(API_KEY ? { Authorization: `Bearer ${API_KEY}` } : {}),
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`LLM request failed (${res.status}): ${await res.text()}`);
  return res.json();
}
```
`zai.chat.completions.create({messages, ...})` → `chatCompletions({model: MODEL, messages, ...})` (drop Z.ai-only params like `thinking:`); response parsing `response.choices?.[0]?.message?.content` stays valid.
Python: same idea with `urllib.request` or `requests` (whichever the file already uses) + `os.environ`.
Multimodal scripts (image/video/audio): keep the OpenAI-compatible route mapping — `/images/generations`, `/images/edits`, `/audio/transcriptions`, `/audio/speech`, or plain `chat/completions` with base64 input for vision. Document the env vars at the top of the script and in the SKILL.md usage section.

### Job 3 — Chinese file/folder names → English
- Rename any assigned file or folder whose NAME contains CJK characters (e.g. `点阵.html`, `case（无限画布：作品集）/`) to kebab-case English.
- After renaming, `grep -r` the whole `skills/` tree for the old name and update every reference (indexes, SKILL.mds, scripts). Rename with `git mv` if the file is tracked, else `mv`.

## Hard constraints
- Do NOT touch files outside your batch list, EXCEPT reference updates for files you renamed (grep repo-wide for those names).
- Do NOT modify binaries (.jpg/.png/.pyc/.woff...). If a binary's content is Chinese (e.g. screenshot), just leave it.
- Do NOT delete any skill functionality, examples, or sections. Translate/replace, don't truncate.
- SKILL.md frontmatter: translate `description:` fully; keep `name:` value as-is if ASCII.
- Where a doc explains "which LLM/agent this skill needs", phrase it as: works with any OpenAI-compatible LLM server (open-source or free), designed for the DiveeOI agent (OpenCode-based).

## Verification (mandatory before you report done)
Run inside `/home/z/my-project/skills/` scoped to YOUR skills' directories:
1. `grep -rlP '[\x{4e00}-\x{9fff}\x{3000}-\x{303f}\x{ff00}-\x{ffef}]' <your dirs>` → must return nothing (except binaries).
2. `grep -rliE 'z-ai-web-dev-sdk|z\.ai|bigmodel\.cn|chatglm|zhipu|智谱|清言|qingyan' <your dirs>` → must return nothing.
3. `grep -rn 'GLM-[0-9]\|glm-[0-9]' <your dirs>` → nothing.
Fix every hit, re-run until clean. Note: `.pyc` and images are acceptable leftovers.

## Report back
- Number of files modified, files renamed (old → new), files where you did SDK rewrites, any leftover you could not fix and why.
