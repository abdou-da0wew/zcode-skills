---
name: Podcast Generate
description: Generate podcast episodes from user-provided content or by searching the web for specified topics. If user uploads a text file/article, creates a dual-host dialogue podcast (or single-host upon request). If no content is provided, searches the web for information about the user-specified topic and generates a podcast. Duration scales with content size (3-20 minutes). Uses any OpenAI-compatible LLM server for script generation and an OpenAI-compatible /audio/speech endpoint for TTS audio synthesis. Outputs both a podcast script (Markdown) and a complete audio file (WAV). Designed for the DiveeOI agent (OpenCode-based).
license: MIT
---

# Podcast Generate Skill (TypeScript Version)

Automatically generate podcast scripts and audio from user-provided material or web search results.

This skill is suitable for:
- Quickly understanding and podcast-ifying long-form content
- Presenting knowledge content in audio form
- In-depth discussion of trending topics
- Searching real-time information and producing a podcast

---

## Capabilities

### What this skill can do
- **Generate from a file**: takes a document (txt/md/docx/pdf and other text formats) and produces a dialogue podcast script and audio
- **Generate from web search**: given a user-specified topic, searches the web for the latest information and produces a podcast script and audio
- Automatically controls duration, adjusting to content length (3-20 minutes)
- Generates a Markdown podcast script (human-editable)
- Synthesizes high-quality audio via an OpenAI-compatible TTS endpoint and stitches it into the final podcast

### What this skill currently does not do
- Does not generate mp3 / subtitles / timestamps
- Does not support three or more podcast roles
- Does not add background music or sound effects

---

## Files and Responsibilities

This skill consists of the following files:

- `generate.ts`
  Unified entry point (supports file mode and search mode)
  - **File mode**: reads a user-provided text file → generates the podcast
  - **Search mode**: queries a web-search endpoint for material → generates the podcast
  - Uses plain OpenAI-compatible HTTP calls for LLM script generation
  - Uses the OpenAI-compatible `/audio/speech` endpoint for TTS audio generation
  - Automatically stitches audio segments
  - Outputs only the final files

- `readme.md`
  Usage documentation

- `SKILL.md`
  This file, describing the skill's capabilities, boundaries, and usage conventions

- `package.json`
  Node.js project configuration and dependencies

- `tsconfig.json`
  TypeScript compilation configuration

---

## Input and Output Conventions

### Input (choose one)

**Option 1: File upload**
- A material file (txt / md / docx / pdf and other text formats)
- No length limit; the skill automatically condenses it to a suitable length

**Option 2: Web search**
- The user specifies a search topic
- The material is gathered automatically via a web-search endpoint
- Multiple search results are merged as the source material

### Output (only 2 files)

- `podcast_script.md`
  Podcast script (Markdown format, human-editable)

- `podcast.wav`
  The final stitched podcast audio

**No intermediate files are output** (such as segments.jsonl, meta.json, etc.)

---

## Running

### Environment
- Node.js 18+ (for the global `fetch` API)
- An OpenAI-compatible LLM server (Ollama, vLLM, LM Studio, OpenRouter, ...) for script generation
- An OpenAI-compatible TTS endpoint (`/audio/speech`) for audio synthesis
- Optional: a SearXNG-style search endpoint (JSON API) for search mode

**No proprietary SDK or CLI is needed**

### Configuration (Environment Variables)

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_BASE_URL` | `http://localhost:11434/v1` | OpenAI-compatible base URL |
| `LLM_API_KEY` | (empty) | API key for bearer auth; leave empty for local servers |
| `LLM_MODEL` | `qwen2.5` | Chat model used for script writing |
| `TTS_MODEL` | `tts-1` | TTS model name |
| `TTS_HOST_VOICE` | `onyx` | Voice id for the host (server-dependent) |
| `TTS_GUEST_VOICE` | `nova` | Voice id for the guest (server-dependent) |
| `SEARCH_BASE_URL` | `http://localhost:8080` | Metasearch endpoint (SearXNG JSON API convention) for `--topic` mode |
| `SEARCH_API_KEY` | (empty) | Optional API key for the search endpoint |

### Install dependencies
```bash
npm install
```

---

## Usage Examples

### Generate a podcast from a file

```bash
npm run generate -- --input=test_data/material.txt --out_dir=out
```

### Generate a podcast from web search

```bash
# Search for a topic and generate a podcast
npm run generate -- --topic="latest AI breakthroughs" --out_dir=out

# Specify the topic and duration
npm run generate -- --topic="quantum computing use cases" --out_dir=out --duration=8

# Search and generate a single-host podcast
npm run generate -- --topic="climate change impact" --out_dir=out --mode=single-male
```

---

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--input` | Input material file path (mutually exclusive with --topic) | - |
| `--topic` | Search topic keywords (mutually exclusive with --input) | - |
| `--out_dir` | Output directory (required) | - |
| `--mode` | Podcast mode: dual / single-male / single-female | dual |
| `--duration` | Manually specify minutes (3-20); 0 means automatic | 0 |
| `--host_name` | Host/presenter name | Alex |
| `--guest_name` | Guest name | Sam |
| `--voice_host` | Host voice id | onyx |
| `--voice_guest` | Guest voice id | nova |
| `--speed` | Speech speed (0.5-2.0) | 1.0 |
| `--pause_ms` | Pause between segments in milliseconds | 200 |

---

## Available Voices

Voice availability depends on your TTS server. Servers following the OpenAI convention typically expose:

| Voice | Character |
|-------|-----------|
| alloy | balanced, neutral |
| echo | calm, steady |
| fable | expressive, storyteller |
| onyx | deep, authoritative |
| nova | bright, energetic |
| shimmer | warm, friendly |

Open-source engines (Kokoro, Piper, Coqui) expose their own voice ids — set `TTS_HOST_VOICE` / `TTS_GUEST_VOICE` or the CLI flags accordingly.

---

## Technical Architecture

### generate.ts (unified entry point)
- **File mode**: reads a user-provided file → generates the podcast
- **Search mode**: queries the search endpoint → gathers material → generates the podcast
- **LLM**: plain OpenAI-compatible HTTP call (`POST {LLM_BASE_URL}/chat/completions`)
- **TTS**: plain OpenAI-compatible HTTP call (`POST {LLM_BASE_URL}/audio/speech`)
- **No proprietary SDK or CLI needed**
- Automatically stitches audio segments
- Outputs only the final files; intermediate files are cleaned up automatically

### LLM calls
- System prompt: podcast scriptwriter role
- User prompt: contains the material + hard constraints + breathing-room requirements
- Output validation: character count, structure, speaker tags
- Automatic retries: up to 3 attempts

### TTS calls
- Uses `POST {LLM_BASE_URL}/audio/speech` with `{model, input, voice, speed, response_format}`
- Supports custom voices and speed
- Automatically stitches multiple wav segments
- Temporary files are cleaned up automatically

---

## Output Example

### podcast_script.md (excerpt)
```markdown
**Alex**: Hello everyone, and welcome to today's podcast. Today we're talking about a fascinating topic...

**Sam**: Yes, this topic is really interesting. I've been following it lately too...

**Alex**: Speaking of which, let me give you an example...
```

---

## License

MIT
