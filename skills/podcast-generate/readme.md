# Podcast Generate Skill (TypeScript Online Version)

Automatically turn a document into a dialogue podcast, with duration adjusted to the content length (3-20 minutes):
- Automatically extracts the core content
- Generates an editable podcast script
- Synthesizes audio via an OpenAI-compatible `/audio/speech` endpoint

This is a TypeScript version that uses **plain OpenAI-compatible HTTP calls** (no proprietary SDK), suitable for online environments.

---

## Quick Start

### One-command generation (script + audio)

```bash
npm run generate -- --input=test_data/material.txt --out_dir=out
```

**Final output:**
- `out/podcast_script.md` - Podcast script (Markdown format)
- `out/podcast.wav` - Final podcast audio

---

## Directory Structure

```text
podcast-generate/
├── readme.md               # Usage documentation (this file)
├── SKILL.md                # Skill capabilities and interface conventions
├── package.json            # Node.js dependency configuration
├── tsconfig.json           # TypeScript compilation configuration
├── generate.ts             # ⭐ Unified entry point (the only file you need)
└── test_data/
    └── material.txt        # Sample input material
```

---

## Requirements

- **Node.js 18+** (for the global `fetch` API)
- An **OpenAI-compatible LLM server** for script generation (Ollama, vLLM, LM Studio, OpenRouter, ...)
- An **OpenAI-compatible TTS endpoint** (`/audio/speech`) for audio synthesis
- Optional: a **SearXNG-style search endpoint** for `--topic` mode

**No proprietary SDK or CLI is needed** — this code uses plain HTTP calls only.

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

---

## Installation

```bash
npm install
```

---

## Usage

### Option 1: Generate from a file

```bash
npm run generate -- --input=material.txt --out_dir=out
```

### Option 2: Generate from web search

```bash
npm run generate -- --topic="latest AI news" --out_dir=out
npm run generate -- --topic="quantum computing applications" --out_dir=out --duration=8
```

### Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--input` | Input material file path; supports txt/md/docx/pdf and other text formats (mutually exclusive with --topic) | - |
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

## Usage Examples

### Dual-host dialogue podcast (default)

```bash
npm run generate -- --input=material.txt --out_dir=out
```

### Single male-host podcast

```bash
npm run generate -- --input=material.txt --out_dir=out --mode=single-male
```

### Specify a 5-minute duration

```bash
npm run generate -- --input=material.txt --out_dir=out --duration=5
```

### Customize role names

```bash
npm run generate -- --input=material.txt --out_dir=out --host_name=Jordan --guest_name=Taylor
```

### Use different voices

```bash
npm run generate -- --input=material.txt --out_dir=out --voice_host=alloy --voice_guest=shimmer
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

Open-source engines (Kokoro, Piper, Coqui) expose their own voice ids — set the CLI flags or `TTS_HOST_VOICE` / `TTS_GUEST_VOICE` accordingly.

---

## Technical Architecture

### generate.ts (unified entry point)
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

## License

MIT
