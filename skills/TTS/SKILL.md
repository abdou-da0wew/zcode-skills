---
name: TTS
description: Implement text-to-speech (TTS) capabilities using any OpenAI-compatible server that exposes the /audio/speech endpoint. Use this skill when the user needs to convert text into natural-sounding speech, create audio content, build voice-enabled applications, or generate spoken audio files. Supports multiple voices, adjustable speed, and various audio formats. Works with any OpenAI-compatible LLM server (open-source or free), designed for the DiveeOI agent (OpenCode-based).
license: MIT
---

# TTS (Text to Speech) Skill

This skill guides the implementation of text-to-speech (TTS) functionality using plain HTTP calls to an OpenAI-compatible `/audio/speech` endpoint (no SDK, no extra dependencies), enabling conversion of text into natural-sounding speech audio.

It works with any OpenAI-compatible server that implements the speech route (open-source or free) — gateways fronting Kokoro, Piper, Coqui, and similar open-source TTS engines, plus hosted OpenAI-compatible APIs — and is designed for the DiveeOI agent (OpenCode-based).

## Skills Path

**Skill Location**: `{project_path}/skills/TTS`

This skill is located at the above path in your project.

**Reference Scripts**: See `{Skill Location}/tts.ts` for a working example.

## Overview

Text-to-Speech allows you to build applications that generate spoken audio from text input, supporting various voices, speeds, and output formats for diverse use cases.

**IMPORTANT**: Keep your API key in backend code or environment variables only. Never hardcode credentials in client-side code.

## API Limitations and Constraints

Before implementing TTS functionality, be aware of these common limitations (exact values depend on your server):

### Input Text Constraints
- **Maximum length**: server-dependent; the OpenAI convention is 4096 characters per request (some servers allow less)
- Text exceeding the limit must be split into smaller chunks

### Audio Parameters
- **Speed range**: 0.5 to 2.0 (OpenAI convention)
  - 0.5 = half speed (slower)
  - 1.0 = normal speed (default)
  - 2.0 = double speed (faster)
- **Volume**: not part of the OpenAI `/audio/speech` convention; most servers ignore extra fields. Apply gain offline when needed.

### Format and Streaming
- **Streaming limitation**: when `stream: true` is enabled, many servers only support the `pcm` format
- **Non-streaming**: usually supports `wav`, `pcm`, and `mp3` formats
- **Sample rate**: 24000 Hz is common (server-dependent)

### Best Practice for Long Text
```javascript
function splitTextIntoChunks(text, maxLength = 1000) {
  const chunks = [];
  const sentences = text.match(/[^.!?]+[.!?]+/g) || [text];

  let currentChunk = '';
  for (const sentence of sentences) {
    if ((currentChunk + sentence).length <= maxLength) {
      currentChunk += sentence;
    } else {
      if (currentChunk) chunks.push(currentChunk.trim());
      currentChunk = sentence;
    }
  }
  if (currentChunk) chunks.push(currentChunk.trim());

  return chunks;
}
```

## Prerequisites

- Node.js 18+ (for the global `fetch` API) or any HTTP client
- An OpenAI-compatible server exposing `POST /audio/speech`
- No npm packages required — examples use built-in APIs only

## Configuration (Environment Variables)

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_BASE_URL` | `http://localhost:11434/v1` | OpenAI-compatible base URL of the server hosting the TTS model |
| `LLM_API_KEY` | (empty) | API key sent as `Authorization: Bearer <key>`; leave empty for local servers |
| `TTS_MODEL` | `tts-1` | TTS model name (server-dependent) |
| `TTS_VOICE` | `alloy` | Voice id (server-dependent; see Available Voices below) |

### Shared Client Helper

```javascript
const BASE_URL = process.env.LLM_BASE_URL ?? "http://localhost:11434/v1";
const API_KEY = process.env.LLM_API_KEY ?? "";
const TTS_MODEL = process.env.TTS_MODEL ?? "tts-1";
const TTS_VOICE = process.env.TTS_VOICE ?? "alloy";
```

## CLI Usage (For Simple Tasks)

For simple text-to-speech conversions, you can use `curl` instead of writing code. This is ideal for quick audio generation, testing voices, or simple automation.

### Basic TTS

```bash
# Convert text to speech (default WAV format) and save the raw audio bytes
curl -s "$LLM_BASE_URL/audio/speech" \
  -H "Content-Type: application/json" \
  ${LLM_API_KEY:+-H "Authorization: Bearer $LLM_API_KEY"} \
  -d '{"model": "tts-1", "input": "Hello, world", "voice": "alloy", "response_format": "wav"}' \
  --output ./hello.wav
```

### Different Voices and Speed

```bash
# Use a specific voice
curl -s "$LLM_BASE_URL/audio/speech" \
  -H "Content-Type: application/json" \
  -d '{"model": "tts-1", "input": "Welcome to our service", "voice": "nova", "response_format": "wav"}' \
  --output ./welcome.wav

# Adjust speech speed (0.5-2.0)
curl -s "$LLM_BASE_URL/audio/speech" \
  -H "Content-Type: application/json" \
  -d '{"model": "tts-1", "input": "This is faster speech", "voice": "alloy", "speed": 1.5, "response_format": "wav"}' \
  --output ./fast.wav
```

### Different Output Formats

```bash
# MP3 format
curl -s "$LLM_BASE_URL/audio/speech" \
  -H "Content-Type: application/json" \
  -d '{"model": "tts-1", "input": "Hello World", "voice": "alloy", "response_format": "mp3"}' \
  --output ./hello.mp3

# WAV format (default in these examples)
curl -s "$LLM_BASE_URL/audio/speech" \
  -H "Content-Type: application/json" \
  -d '{"model": "tts-1", "input": "Hello World", "voice": "alloy", "response_format": "wav"}' \
  --output ./hello.wav
```

### CLI Parameters

- Request body fields follow the standard OpenAI Speech schema:
  - `model`: **Required** - TTS model name (default: `tts-1`)
  - `input`: **Required** - Text to convert to speech (respect the server's max length)
  - `voice`: Optional - Voice id (default: `alloy`)
  - `speed`: Optional - Speech speed, 0.5-2.0 (default: 1.0)
  - `response_format`: Optional - Output format: `wav`, `mp3`, `pcm`, `opus`, `aac`, `flac` (server-dependent)
  - `stream`: Optional - Enable streaming output (often only supports `pcm`)

### When to Use CLI vs Code

**Use curl for:**
- Quick text-to-speech conversions
- Testing different voices and speeds
- Simple batch audio generation
- Command-line automation scripts

**Use code for:**
- Dynamic audio generation in applications
- Integration with web services
- Custom audio processing pipelines
- Production applications with complex requirements

## Basic TTS Implementation

### Simple Text to Speech

```javascript
import fs from 'fs';

async function textToSpeech(text, outputPath) {
  const res = await fetch(`${BASE_URL}/audio/speech`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(API_KEY ? { Authorization: `Bearer ${API_KEY}` } : {}),
    },
    body: JSON.stringify({
      model: TTS_MODEL,
      input: text,
      voice: 'alloy',
      speed: 1.0,
      response_format: 'wav',
      stream: false
    }),
  });
  if (!res.ok) throw new Error(`TTS request failed (${res.status}): ${await res.text()}`);

  // The endpoint returns raw binary audio
  const arrayBuffer = await res.arrayBuffer();
  const buffer = Buffer.from(new Uint8Array(arrayBuffer));

  fs.writeFileSync(outputPath, buffer);
  console.log(`Audio saved to ${outputPath}`);
  return outputPath;
}

// Usage
await textToSpeech('Hello, world!', './output.wav');
```

### Multiple Voice Options

```javascript
import fs from 'fs';

async function generateWithVoice(text, voice, outputPath) {
  const res = await fetch(`${BASE_URL}/audio/speech`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(API_KEY ? { Authorization: `Bearer ${API_KEY}` } : {}),
    },
    body: JSON.stringify({
      model: TTS_MODEL,
      input: text,
      voice: voice, // Available voices depend on the server (alloy, echo, fable, onyx, nova, shimmer, ...)
      speed: 1.0,
      response_format: 'wav',
      stream: false
    }),
  });
  if (!res.ok) throw new Error(`TTS request failed (${res.status})`);

  const arrayBuffer = await res.arrayBuffer();
  const buffer = Buffer.from(new Uint8Array(arrayBuffer));

  fs.writeFileSync(outputPath, buffer);
  return outputPath;
}

// Usage
await generateWithVoice('Welcome to our service', 'alloy', './welcome.wav');
```

### Adjustable Speed

```javascript
import fs from 'fs';

async function generateWithSpeed(text, speed, outputPath) {
  // Speed range (OpenAI convention): 0.5 to 2.0
  // 0.5 = half speed (slower)
  // 1.0 = normal speed (default)
  // 2.0 = double speed (faster)
  // Values outside the supported range may cause server errors

  const res = await fetch(`${BASE_URL}/audio/speech`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(API_KEY ? { Authorization: `Bearer ${API_KEY}` } : {}),
    },
    body: JSON.stringify({
      model: TTS_MODEL,
      input: text,
      voice: 'alloy',
      speed: speed,
      response_format: 'wav',
      stream: false
    }),
  });
  if (!res.ok) throw new Error(`TTS request failed (${res.status})`);

  const arrayBuffer = await res.arrayBuffer();
  const buffer = Buffer.from(new Uint8Array(arrayBuffer));

  fs.writeFileSync(outputPath, buffer);
  return outputPath;
}

// Usage - slower narration
await generateWithSpeed('This is an important announcement', 0.8, './slow.wav');

// Usage - faster narration
await generateWithSpeed('Quick update', 1.3, './fast.wav');
```

### Extra Parameters (Volume and Beyond)

```javascript
import fs from 'fs';

async function generateWithExtraParams(text, outputPath, extraParams = {}) {
  // NOTE: `volume` is not part of the OpenAI /audio/speech convention.
  // Servers that support it will honor the extra field; others ignore it.
  // For guaranteed loudness control, apply gain to the audio buffer afterwards.
  const res = await fetch(`${BASE_URL}/audio/speech`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(API_KEY ? { Authorization: `Bearer ${API_KEY}` } : {}),
    },
    body: JSON.stringify({
      model: TTS_MODEL,
      input: text,
      voice: 'alloy',
      speed: 1.0,
      response_format: 'wav',
      stream: false,
      ...extraParams   // e.g. { volume: 5.0 } on servers that support it
    }),
  });
  if (!res.ok) throw new Error(`TTS request failed (${res.status})`);

  const arrayBuffer = await res.arrayBuffer();
  const buffer = Buffer.from(new Uint8Array(arrayBuffer));

  fs.writeFileSync(outputPath, buffer);
  return outputPath;
}

// Usage - request louder audio on servers that support a volume field
await generateWithExtraParams('This is an announcement', './loud.wav', { volume: 5.0 });
```

## Advanced Use Cases

### Batch Processing

```javascript
import fs from 'fs';
import path from 'path';

async function batchTextToSpeech(textArray, outputDir) {
  const results = [];

  // Ensure output directory exists
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  for (let i = 0; i < textArray.length; i++) {
    try {
      const text = textArray[i];
      const outputPath = path.join(outputDir, `audio_${i + 1}.wav`);

      const res = await fetch(`${BASE_URL}/audio/speech`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(API_KEY ? { Authorization: `Bearer ${API_KEY}` } : {}),
        },
        body: JSON.stringify({
          model: TTS_MODEL,
          input: text,
          voice: 'alloy',
          speed: 1.0,
          response_format: 'wav',
          stream: false
        }),
      });
      if (!res.ok) throw new Error(`TTS request failed (${res.status})`);

      const arrayBuffer = await res.arrayBuffer();
      const buffer = Buffer.from(new Uint8Array(arrayBuffer));

      fs.writeFileSync(outputPath, buffer);
      results.push({
        success: true,
        text,
        path: outputPath
      });
    } catch (error) {
      results.push({
        success: false,
        text: textArray[i],
        error: error.message
      });
    }
  }

  return results;
}

// Usage
const texts = [
  'Welcome to chapter one',
  'Welcome to chapter two',
  'Welcome to chapter three'
];

const results = await batchTextToSpeech(texts, './audio-output');
console.log('Generated:', results.length, 'audio files');
```

### Dynamic Content Generation

```javascript
import fs from 'fs';

class TTSGenerator {
  async generateAudio(text, options = {}) {
    const {
      voice = 'alloy',
      speed = 1.0,
      format = 'wav'
    } = options;

    const res = await fetch(`${BASE_URL}/audio/speech`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(API_KEY ? { Authorization: `Bearer ${API_KEY}` } : {}),
      },
      body: JSON.stringify({
        model: TTS_MODEL,
        input: text,
        voice: voice,
        speed: speed,
        response_format: format,
        stream: false
      }),
    });
    if (!res.ok) throw new Error(`TTS request failed (${res.status})`);

    // The endpoint returns raw binary audio
    const arrayBuffer = await res.arrayBuffer();
    return Buffer.from(new Uint8Array(arrayBuffer));
  }

  async saveAudio(text, outputPath, options = {}) {
    const buffer = await this.generateAudio(text, options);
    if (buffer) {
      fs.writeFileSync(outputPath, buffer);
      return outputPath;
    }
    return null;
  }
}

// Usage
const generator = new TTSGenerator();

await generator.saveAudio(
  'Hello, this is a test',
  './output.wav',
  { speed: 1.2 }
);
```

### Next.js API Route Example

```javascript
import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  try {
    const { text, voice = 'alloy', speed = 1.0 } = await req.json();

    const res = await fetch(`${process.env.LLM_BASE_URL}/audio/speech`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(process.env.LLM_API_KEY
          ? { Authorization: `Bearer ${process.env.LLM_API_KEY}` }
          : {}),
      },
      body: JSON.stringify({
        model: process.env.TTS_MODEL ?? 'tts-1',
        input: text.trim(),
        voice: voice,
        speed: speed,
        response_format: 'wav',
        stream: false,
      }),
    });
    if (!res.ok) throw new Error(`TTS request failed (${res.status})`);

    // The endpoint returns raw binary audio
    const arrayBuffer = await res.arrayBuffer();
    const buffer = Buffer.from(new Uint8Array(arrayBuffer));

    // Return audio as response
    return new NextResponse(buffer, {
      status: 200,
      headers: {
        'Content-Type': 'audio/wav',
        'Content-Length': buffer.length.toString(),
        'Cache-Control': 'no-cache',
      },
    });
  } catch (error) {
    console.error('TTS API Error:', error);

    return NextResponse.json(
      {
        error: error instanceof Error ? error.message : 'Failed to generate speech, please try again later',
      },
      { status: 500 }
    );
  }
}
```

## Best Practices

### 1. Text Preparation
```javascript
function prepareTextForTTS(text) {
  // Remove excessive whitespace
  text = text.replace(/\s+/g, ' ').trim();

  // Expand common abbreviations for better pronunciation
  const abbreviations = {
    'Dr.': 'Doctor',
    'Mr.': 'Mister',
    'Mrs.': 'Misses',
    'etc.': 'et cetera'
  };

  for (const [abbr, full] of Object.entries(abbreviations)) {
    text = text.replace(new RegExp(abbr, 'g'), full);
  }

  return text;
}
```

### 2. Error Handling
```javascript
import fs from 'fs';

async function safeTTS(text, outputPath) {
  try {
    // Validate input
    if (!text || text.trim().length === 0) {
      throw new Error('Text input cannot be empty');
    }

    if (text.length > 4096) {
      throw new Error('Text input exceeds the maximum length supported by the server');
    }

    const res = await fetch(`${BASE_URL}/audio/speech`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(API_KEY ? { Authorization: `Bearer ${API_KEY}` } : {}),
      },
      body: JSON.stringify({
        model: TTS_MODEL,
        input: text,
        voice: 'alloy',
        speed: 1.0,
        response_format: 'wav',
        stream: false
      }),
    });
    if (!res.ok) throw new Error(`TTS request failed (${res.status})`);

    const arrayBuffer = await res.arrayBuffer();
    const buffer = Buffer.from(new Uint8Array(arrayBuffer));

    fs.writeFileSync(outputPath, buffer);

    return {
      success: true,
      path: outputPath,
      size: buffer.length
    };
  } catch (error) {
    console.error('TTS Error:', error);
    return {
      success: false,
      error: error.message
    };
  }
}
```

### 3. Connection Reuse

```javascript
// fetch with keep-alive reuses TCP connections automatically.
// For very high volumes, prefer a single long-lived HTTP agent over
// creating a new connection per request.
const res = await fetch(`${BASE_URL}/audio/speech`, { /* ... */ });
```

## Common Use Cases

1. **Audiobooks & Podcasts**: Convert written content to audio format
2. **E-learning**: Create narration for educational content
3. **Accessibility**: Provide audio versions of text content
4. **Voice Assistants**: Generate dynamic responses
5. **Announcements**: Create automated audio notifications
6. **IVR Systems**: Generate phone system prompts
7. **Content Localization**: Create audio in different languages

## Integration Examples

### Express.js API Endpoint

```javascript
import express from 'express';
import fs from 'fs';
import path from 'path';

const app = express();
app.use(express.json());

const outputDir = './audio-output';

async function init() {
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
}

app.post('/api/tts', async (req, res) => {
  try {
    const { text, voice = 'alloy', speed = 1.0 } = req.body;

    if (!text) {
      return res.status(400).json({ error: 'Text is required' });
    }

    const filename = `tts_${Date.now()}.wav`;
    const outputPath = path.join(outputDir, filename);

    const response = await fetch(`${BASE_URL}/audio/speech`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(API_KEY ? { Authorization: `Bearer ${API_KEY}` } : {}),
      },
      body: JSON.stringify({
        model: TTS_MODEL,
        input: text,
        voice: voice,
        speed: speed,
        response_format: 'wav',
        stream: false
      }),
    });
    if (!response.ok) throw new Error(`TTS request failed (${response.status})`);

    const arrayBuffer = await response.arrayBuffer();
    const buffer = Buffer.from(new Uint8Array(arrayBuffer));

    fs.writeFileSync(outputPath, buffer);

    res.json({
      success: true,
      audioUrl: `/audio/${filename}`,
      size: buffer.length
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.use('/audio', express.static('audio-output'));

init().then(() => {
  app.listen(3000, () => {
    console.log('TTS API running on port 3000');
  });
});
```

## Troubleshooting

**Issue**: "Input text exceeds maximum length"
- **Solution**: Text input length is server-limited (the OpenAI convention is 4096 characters). Split longer text into chunks using the `splitTextIntoChunks` function shown in the API Limitations section

**Issue**: "Invalid speed parameter" or unexpected speed behavior
- **Solution**: Speed must be between 0.5 and 2.0. Check your speed value is within this range

**Issue**: "Stream format not supported" with WAV/MP3
- **Solution**: Streaming mode often only supports PCM format. Either use `response_format: 'pcm'` with streaming, or disable streaming (`stream: false`) for WAV/MP3 output

**Issue**: "API key exposed in client code"
- **Solution**: Read `LLM_API_KEY` from environment variables in server-side code only

**Issue**: "TypeError: response.audio is undefined"
- **Solution**: The endpoint returns raw binary audio, use `await res.arrayBuffer()` instead of accessing `response.audio`

**Issue**: Generated audio file is empty or corrupted
- **Solution**: Ensure you're calling `await res.arrayBuffer()` and properly converting to Buffer: `Buffer.from(new Uint8Array(arrayBuffer))`

**Issue**: Audio sounds unnatural
- **Solution**: Prepare text properly (remove special characters, expand abbreviations)

**Issue**: Long processing times
- **Solution**: Break long text into smaller chunks and process in parallel

**Issue**: Next.js caching old API route
- **Solution**: Create a new API route endpoint or restart the dev server

**Issue**: 404 on `/audio/speech`
- **Solution**: Your server does not implement the OpenAI speech route. Point `LLM_BASE_URL` at a gateway or TTS server that does

## Performance Tips

1. **Reuse HTTP Connections**: `fetch` with keep-alive reuses connections across requests
2. **Implement Caching**: Cache generated audio for repeated text
3. **Batch Processing**: Process multiple texts efficiently
4. **Optimize Text**: Remove unnecessary content before generation
5. **Async Processing**: Use queues for handling multiple requests

## Important Notes

### API Constraints

**Input Text Length**: Server-dependent maximum per request (OpenAI convention: 4096 characters). For longer text:
```javascript
// Split long text into chunks
const longText = "..."; // Your long text here
const chunks = splitTextIntoChunks(longText, 1000);

for (const chunk of chunks) {
  const res = await fetch(`${BASE_URL}/audio/speech`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(API_KEY ? { Authorization: `Bearer ${API_KEY}` } : {}),
    },
    body: JSON.stringify({
      model: TTS_MODEL,
      input: chunk,
      voice: 'alloy',
      speed: 1.0,
      response_format: 'wav',
      stream: false
    }),
  });
  // Process each chunk...
}
```

**Streaming Format Limitation**: When using `stream: true`, many servers only support the `pcm` format. For `wav` or `mp3` output, use `stream: false`.

**Sample Rate**: Audio is commonly generated at 24000 Hz sample rate (server-dependent).

### Response Format

The `/audio/speech` endpoint returns raw **binary audio** in the requested format. Always use:

```javascript
// ✅ CORRECT
const res = await fetch(`${BASE_URL}/audio/speech`, { ... });
const arrayBuffer = await res.arrayBuffer();
const buffer = Buffer.from(new Uint8Array(arrayBuffer));

// ❌ WRONG - This will not work
const buffer = Buffer.from(response.audio); // response.audio is undefined
```

### Available Voices

Voice availability depends entirely on your server. Servers following the OpenAI convention typically expose:

- `alloy` - balanced, neutral
- `echo` - calm, steady
- `fable` - expressive, storyteller
- `onyx` - deep, authoritative
- `nova` - bright, energetic
- `shimmer` - warm, friendly

Open-source engines (Kokoro, Piper, Coqui) expose their own voice ids — check your server's documentation and set `TTS_VOICE` accordingly.

### Speed Range

- Minimum: `0.5` (half speed)
- Default: `1.0` (normal speed)
- Maximum: `2.0` (double speed)

**Important**: Speed values outside the supported range may result in server errors.

### Volume Range

- Not part of the OpenAI `/audio/speech` convention
- Servers that support it accept a `volume` field (typically `> 0`, up to `10`, default `1.0`)
- For portable behavior, apply gain to the audio buffer offline

## Remember

- Works with any OpenAI-compatible server exposing `/audio/speech` (gateways fronting Kokoro, Piper, Coqui, ..., or hosted OpenAI-compatible APIs)
- Designed for the DiveeOI agent (OpenCode-based)
- Configuration via environment variables: `LLM_BASE_URL`, `LLM_API_KEY`, `TTS_MODEL`, `TTS_VOICE`
- The endpoint is `POST {LLM_BASE_URL}/audio/speech` with `{model, input, voice, speed, response_format}` and returns **raw binary audio**
- **Input text length is server-limited** - split longer text into chunks
- **Speed should be between 0.5 and 2.0** - values outside this range may cause errors
- **Streaming often only supports PCM format** - use non-streaming for WAV or MP3 output
- Convert the response with `await res.arrayBuffer()` and `Buffer.from(new Uint8Array(arrayBuffer))`
- Keep your API key in server-side code only
- Implement error handling for production applications
- Consider caching for frequently generated content
- Clean up old audio files periodically to manage storage
