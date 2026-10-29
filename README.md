# zcode-skills

A collection of 67 AI-agent skills localized for **DiveeOI** — an OpenCode-based agent — and **any open-source or free LLM**.

All skills work with any OpenAI-compatible LLM server (Ollama, vLLM, LM Studio, OpenRouter, llama.cpp server, etc.). No proprietary SDKs or vendor-locked endpoints.

## Configuration

Most skills that call a model read these environment variables:

| Variable | Purpose | Default |
|---|---|---|
| `LLM_BASE_URL` | OpenAI-compatible API base URL | `http://localhost:11434/v1` |
| `LLM_API_KEY` | API key (empty for local servers) | — |
| `LLM_MODEL` | Model name | `qwen2.5` |

Modality-specific skills add their own variables (e.g. `ASR_MODEL`, `TTS_MODEL`, `TTS_VOICE`, `IMAGE_MODEL`, `VIDEO_MODEL`, `SEARCH_BASE_URL`) — see each skill's `SKILL.md` for details.

## Skill categories

- **AI & media**: ASR, LLM chat, TTS, VLM, image generation/edit/search/understanding, video generation/understanding, podcast generation
- **Documents**: docx, pdf, pptx, xlsx creation and analysis
- **Charts & design**: charts, visual design foundations, design templates & systems
- **Research**: deep research, literature survey, market research, AMiner academic search, research explorer
- **Career**: resume builder, JD tailoring, interview prep, job-intent tracking
- **Education**: quiz generation, study buddy, gaokao (college-admission) planning tools
- **Web & data**: fullstack dev, web shader extractor, stock analysis, finance, multi-search-engine
- **Fun & wellness**: dream interpretation, fortune analysis, gift evaluation, mindfulness meditation

## Usage

Each skill lives in its own directory with a `SKILL.md` describing when and how to use it, plus scripts, references, and examples. Point your OpenCode-compatible agent at this repository and the skills will be discoverable by their frontmatter descriptions.

## License

See the `LICENSE`/`LICENSE.txt` file in each skill directory.
