---
name: ASR
description: Implement speech-to-text (ASR/automatic speech recognition) capabilities using any OpenAI-compatible server that exposes the /audio/transcriptions endpoint. Use this skill when the user needs to transcribe audio files, convert speech to text, build voice input features, or process audio recordings. Supports multipart audio uploads and returns accurate text transcriptions. Works with any OpenAI-compatible LLM server (open-source or free), designed for the DiveeOI agent (OpenCode-based).
license: MIT
---

# ASR (Speech to Text) Skill

This skill guides the implementation of speech-to-text (ASR) functionality using plain HTTP calls to an OpenAI-compatible `/audio/transcriptions` endpoint (no SDK, no extra dependencies), enabling accurate transcription of spoken audio into text.

It works with any OpenAI-compatible server that implements the audio transcription route (open-source or free) — faster-whisper-server, whisper.cpp server, Speaches, Groq, OpenAI, and most API gateways — and is designed for the DiveeOI agent (OpenCode-based).

## Skills Path

**Skill Location**: `{project_path}/skills/ASR`

this skill is located at above path in your project.

**Reference Scripts**: Example test scripts are available in the `{Skill Location}/scripts/` directory for quick testing and reference. See `{Skill Location}/scripts/asr.ts` for a working example.

## Overview

Speech-to-Text (ASR - Automatic Speech Recognition) allows you to build applications that convert spoken language in audio files into written text, enabling voice-controlled interfaces, transcription services, and audio content analysis.

**IMPORTANT**: Keep your API key in backend code or environment variables only. Never hardcode credentials in client-side code.

## Prerequisites

- Node.js 18+ (for the global `fetch`, `FormData`, and `Blob` APIs) or any HTTP client
- An OpenAI-compatible server exposing `POST /audio/transcriptions`
- No npm packages required — examples use built-in APIs only

## Configuration (Environment Variables)

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_BASE_URL` | `http://localhost:11434/v1` | OpenAI-compatible base URL of the server hosting the transcription model |
| `LLM_API_KEY` | (empty) | API key sent as `Authorization: Bearer <key>`; leave empty for local servers |
| `ASR_MODEL` | `whisper-1` | Transcription model name (e.g. `whisper-1`, `whisper-large-v3`, `base.en`) |

### Shared Client Helper

All examples below use this helper (plain `fetch`, zero dependencies):

```javascript
const BASE_URL = process.env.LLM_BASE_URL ?? "http://localhost:11434/v1";
const API_KEY = process.env.LLM_API_KEY ?? "";
const ASR_MODEL = process.env.ASR_MODEL ?? "whisper-1";

async function transcribeFile(filePath) {
  const fs = await import('fs');
  const audioBuffer = fs.readFileSync(filePath);
  const blob = new Blob([audioBuffer]);

  const form = new FormData();
  form.append('file', blob, filePath.split('/').pop());
  form.append('model', ASR_MODEL);
  form.append('response_format', 'json');

  const res = await fetch(`${BASE_URL}/audio/transcriptions`, {
    method: 'POST',
    headers: {
      ...(API_KEY ? { Authorization: `Bearer ${API_KEY}` } : {}),
    },
    body: form,
  });
  if (!res.ok) throw new Error(`ASR request failed (${res.status}): ${await res.text()}`);
  const data = await res.json();
  return data.text;
}
```

## CLI Usage (For Simple Tasks)

For simple audio transcription tasks, you can use `curl` instead of writing code. This is ideal for quick transcriptions, testing audio files, or batch processing.

### Basic Transcription from File

```bash
# Transcribe an audio file (multipart upload, OpenAI-style)
curl -s "$LLM_BASE_URL/audio/transcriptions" \
  ${LLM_API_KEY:+-H "Authorization: Bearer $LLM_API_KEY"} \
  -F file=@./audio.wav \
  -F model=whisper-1

# Save transcription to JSON file
curl -s "$LLM_BASE_URL/audio/transcriptions" \
  -F file=@./recording.mp3 -F model=whisper-1 \
  -o transcript.json

# Transcribe and view output
curl -s "$LLM_BASE_URL/audio/transcriptions" \
  -F file=@./interview.wav -F model=whisper-1 -F response_format=json
```

### Transcription from Base64 (shell-decoded)

```bash
# Decode a base64 audio payload to a temp file, then upload it
echo "UklGRiQAAABXQVZFZm10..." | base64 -d > /tmp/audio.wav
curl -s "$LLM_BASE_URL/audio/transcriptions" \
  -F file=@/tmp/audio.wav -F model=whisper-1 -o result.json
```

### CLI Parameters

- `file=@<path>`: **Required** - Audio file uploaded as multipart form data
- `model=<name>`: **Required** - Transcription model (default: `whisper-1`, override with `ASR_MODEL`)
- `response_format`: Optional - `json` (default), `text`, `srt`, `verbose_json` (server-dependent)
- `language`: Optional - ISO-639-1 language hint (server-dependent)

### Supported Audio Formats

The transcription route supports various audio formats including:
- WAV (.wav)
- MP3 (.mp3)
- Other common audio formats (server-dependent: m4a, flac, ogg, webm)

### When to Use CLI vs Code

**Use curl for:**
- Quick audio file transcriptions
- Testing audio recognition accuracy
- Simple batch processing scripts
- One-off transcription tasks

**Use code for:**
- Real-time audio transcription in applications
- Integration with recording systems
- Custom audio processing workflows
- Production applications with streaming audio

## Basic ASR Implementation

### Simple Audio Transcription

```javascript
import fs from 'fs';

async function transcribeAudio(audioFilePath) {
  // Read audio file and upload it as multipart form data
  const audioFile = fs.readFileSync(audioFilePath);
  const blob = new Blob([audioFile]);

  const form = new FormData();
  form.append('file', blob, 'audio.wav');
  form.append('model', ASR_MODEL);
  form.append('response_format', 'json');

  const res = await fetch(`${BASE_URL}/audio/transcriptions`, {
    method: 'POST',
    headers: {
      ...(API_KEY ? { Authorization: `Bearer ${API_KEY}` } : {}),
    },
    body: form,
  });
  if (!res.ok) throw new Error(`ASR request failed (${res.status}): ${await res.text()}`);

  const response = await res.json();
  return response.text;
}

// Usage
const transcription = await transcribeAudio('./audio.wav');
console.log('Transcription:', transcription);
```

### Transcribe Multiple Audio Files

```javascript
import fs from 'fs';

async function transcribeBatch(audioFilePaths) {
  const results = [];

  for (const filePath of audioFilePaths) {
    try {
      const audioFile = fs.readFileSync(filePath);
      const blob = new Blob([audioFile]);

      const form = new FormData();
      form.append('file', blob, filePath.split('/').pop());
      form.append('model', ASR_MODEL);

      const res = await fetch(`${BASE_URL}/audio/transcriptions`, {
        method: 'POST',
        headers: {
          ...(API_KEY ? { Authorization: `Bearer ${API_KEY}` } : {}),
        },
        body: form,
      });
      if (!res.ok) throw new Error(`ASR request failed (${res.status})`);
      const response = await res.json();

      results.push({
        file: filePath,
        success: true,
        transcription: response.text
      });
    } catch (error) {
      results.push({
        file: filePath,
        success: false,
        error: error.message
      });
    }
  }

  return results;
}

// Usage
const files = ['./interview1.wav', './interview2.wav', './interview3.wav'];
const transcriptions = await transcribeBatch(files);

transcriptions.forEach(result => {
  if (result.success) {
    console.log(`${result.file}: ${result.transcription}`);
  } else {
    console.error(`${result.file}: Error - ${result.error}`);
  }
});
```

## Advanced Use Cases

### Audio File Processing with Metadata

```javascript
import fs from 'fs';
import path from 'path';

async function transcribeWithMetadata(audioFilePath) {
  // Get file metadata
  const stats = fs.statSync(audioFilePath);
  const audioFile = fs.readFileSync(audioFilePath);
  const blob = new Blob([audioFile]);

  const form = new FormData();
  form.append('file', blob, path.basename(audioFilePath));
  form.append('model', ASR_MODEL);

  const startTime = Date.now();

  const res = await fetch(`${BASE_URL}/audio/transcriptions`, {
    method: 'POST',
    headers: {
      ...(API_KEY ? { Authorization: `Bearer ${API_KEY}` } : {}),
    },
    body: form,
  });
  if (!res.ok) throw new Error(`ASR request failed (${res.status})`);
  const response = await res.json();

  const endTime = Date.now();

  return {
    filename: path.basename(audioFilePath),
    filepath: audioFilePath,
    fileSize: stats.size,
    transcription: response.text,
    wordCount: response.text.split(/\s+/).length,
    processingTime: endTime - startTime,
    timestamp: new Date().toISOString()
  };
}

// Usage
const result = await transcribeWithMetadata('./meeting_recording.wav');
console.log('Transcription Details:', JSON.stringify(result, null, 2));
```

### Real-time Audio Processing Service

```javascript
import fs from 'fs';
import crypto from 'crypto';

class ASRService {
  constructor() {
    this.transcriptionCache = new Map();
  }

  generateCacheKey(audioBuffer) {
    return crypto.createHash('md5').update(audioBuffer).digest('hex');
  }

  async transcribe(audioFilePath, useCache = true) {
    const audioBuffer = fs.readFileSync(audioFilePath);
    const cacheKey = this.generateCacheKey(audioBuffer);

    // Check cache
    if (useCache && this.transcriptionCache.has(cacheKey)) {
      return {
        transcription: this.transcriptionCache.get(cacheKey),
        cached: true
      };
    }

    // Transcribe audio via multipart upload
    const blob = new Blob([audioBuffer]);

    const form = new FormData();
    form.append('file', blob, 'audio.wav');
    form.append('model', ASR_MODEL);

    const res = await fetch(`${BASE_URL}/audio/transcriptions`, {
      method: 'POST',
      headers: {
        ...(API_KEY ? { Authorization: `Bearer ${API_KEY}` } : {}),
      },
      body: form,
    });
    if (!res.ok) throw new Error(`ASR request failed (${res.status})`);
    const response = await res.json();

    // Cache result
    if (useCache) {
      this.transcriptionCache.set(cacheKey, response.text);
    }

    return {
      transcription: response.text,
      cached: false
    };
  }

  clearCache() {
    this.transcriptionCache.clear();
  }

  getCacheSize() {
    return this.transcriptionCache.size;
  }
}

// Usage
const asrService = new ASRService();

const result1 = await asrService.transcribe('./audio.wav');
console.log('First call (not cached):', result1);

const result2 = await asrService.transcribe('./audio.wav');
console.log('Second call (cached):', result2);
```

### Directory Transcription

```javascript
import fs from 'fs';
import path from 'path';

async function transcribeDirectory(directoryPath, outputJsonPath) {
  // Get all audio files
  const files = fs.readdirSync(directoryPath);
  const audioFiles = files.filter(file =>
    /\.(wav|mp3|m4a|flac|ogg)$/i.test(file)
  );

  const results = {
    directory: directoryPath,
    totalFiles: audioFiles.length,
    processedAt: new Date().toISOString(),
    transcriptions: []
  };

  for (const filename of audioFiles) {
    const filePath = path.join(directoryPath, filename);

    try {
      const audioFile = fs.readFileSync(filePath);
      const blob = new Blob([audioFile]);

      const form = new FormData();
      form.append('file', blob, filename);
      form.append('model', ASR_MODEL);

      const res = await fetch(`${BASE_URL}/audio/transcriptions`, {
        method: 'POST',
        headers: {
          ...(API_KEY ? { Authorization: `Bearer ${API_KEY}` } : {}),
        },
        body: form,
      });
      if (!res.ok) throw new Error(`ASR request failed (${res.status})`);
      const response = await res.json();

      results.transcriptions.push({
        filename: filename,
        success: true,
        text: response.text,
        wordCount: response.text.split(/\s+/).length
      });

      console.log(`✓ Transcribed: ${filename}`);
    } catch (error) {
      results.transcriptions.push({
        filename: filename,
        success: false,
        error: error.message
      });

      console.error(`✗ Failed: ${filename} - ${error.message}`);
    }
  }

  // Save results to JSON
  fs.writeFileSync(
    outputJsonPath,
    JSON.stringify(results, null, 2)
  );

  return results;
}

// Usage
const results = await transcribeDirectory(
  './audio-recordings',
  './transcriptions.json'
);

console.log(`\nProcessed ${results.totalFiles} files`);
console.log(`Successful: ${results.transcriptions.filter(t => t.success).length}`);
console.log(`Failed: ${results.transcriptions.filter(t => !t.success).length}`);
```

## Best Practices

### 1. Audio Format Handling

```javascript
import fs from 'fs';

async function transcribeAnyFormat(audioFilePath) {
  // Supported formats: WAV, MP3, M4A, FLAC, OGG, etc. (server-dependent)
  const validExtensions = ['.wav', '.mp3', '.m4a', '.flac', '.ogg'];
  const ext = audioFilePath.toLowerCase().substring(audioFilePath.lastIndexOf('.'));

  if (!validExtensions.includes(ext)) {
    throw new Error(`Unsupported audio format: ${ext}`);
  }

  const audioFile = fs.readFileSync(audioFilePath);
  const blob = new Blob([audioFile]);

  const form = new FormData();
  form.append('file', blob, audioFilePath.split('/').pop());
  form.append('model', ASR_MODEL);

  const res = await fetch(`${BASE_URL}/audio/transcriptions`, {
    method: 'POST',
    headers: {
      ...(API_KEY ? { Authorization: `Bearer ${API_KEY}` } : {}),
    },
    body: form,
  });
  if (!res.ok) throw new Error(`ASR request failed (${res.status})`);
  const response = await res.json();

  return response.text;
}
```

### 2. Error Handling

```javascript
import fs from 'fs';

async function safeTranscribe(audioFilePath) {
  try {
    // Validate file exists
    if (!fs.existsSync(audioFilePath)) {
      throw new Error(`File not found: ${audioFilePath}`);
    }

    // Check file size (e.g., limit to 100MB)
    const stats = fs.statSync(audioFilePath);
    const fileSizeMB = stats.size / (1024 * 1024);

    if (fileSizeMB > 100) {
      throw new Error(`File too large: ${fileSizeMB.toFixed(2)}MB (max 100MB)`);
    }

    // Transcribe
    const audioFile = fs.readFileSync(audioFilePath);
    const blob = new Blob([audioFile]);

    const form = new FormData();
    form.append('file', blob, audioFilePath.split('/').pop());
    form.append('model', ASR_MODEL);

    const res = await fetch(`${BASE_URL}/audio/transcriptions`, {
      method: 'POST',
      headers: {
        ...(API_KEY ? { Authorization: `Bearer ${API_KEY}` } : {}),
      },
      body: form,
    });
    if (!res.ok) throw new Error(`ASR request failed (${res.status})`);
    const response = await res.json();

    if (!response.text || response.text.trim().length === 0) {
      throw new Error('Empty transcription result');
    }

    return {
      success: true,
      transcription: response.text,
      filePath: audioFilePath,
      fileSize: stats.size
    };
  } catch (error) {
    console.error('Transcription error:', error);
    return {
      success: false,
      error: error.message,
      filePath: audioFilePath
    };
  }
}
```

### 3. Post-Processing Transcriptions

```javascript
function cleanTranscription(text) {
  // Remove excessive whitespace
  text = text.replace(/\s+/g, ' ').trim();

  // Capitalize first letter of sentences
  text = text.replace(/(^\w|[.!?]\s+\w)/g, match => match.toUpperCase());

  // Remove filler words (optional)
  const fillers = ['um', 'uh', 'ah', 'like', 'you know'];
  const fillerPattern = new RegExp(`\\b(${fillers.join('|')})\\b`, 'gi');
  text = text.replace(fillerPattern, '').replace(/\s+/g, ' ');

  return text;
}

async function transcribeAndClean(audioFilePath) {
  const raw = await transcribeAudio(audioFilePath);

  return {
    raw: raw,
    cleaned: cleanTranscription(raw)
  };
}
```

## Common Use Cases

1. **Meeting Transcription**: Convert recorded meetings into searchable text
2. **Interview Processing**: Transcribe interviews for analysis and documentation
3. **Podcast Transcription**: Create text versions of podcast episodes
4. **Voice Notes**: Convert voice memos to text for easier reference
5. **Call Center Analytics**: Analyze customer service calls
6. **Accessibility**: Provide text alternatives for audio content
7. **Voice Commands**: Enable voice-controlled applications
8. **Language Learning**: Transcribe pronunciation practice

## Integration Examples

### Express.js API Endpoint

```javascript
import express from 'express';
import multer from 'multer';
import fs from 'fs';

const app = express();
const upload = multer({ dest: 'uploads/' });

app.post('/api/transcribe', upload.single('audio'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No audio file provided' });
    }

    const audioFile = fs.readFileSync(req.file.path);
    const blob = new Blob([audioFile]);

    const form = new FormData();
    form.append('file', blob, req.file.originalname || 'audio.wav');
    form.append('model', ASR_MODEL);

    const res = await fetch(`${BASE_URL}/audio/transcriptions`, {
      method: 'POST',
      headers: {
        ...(API_KEY ? { Authorization: `Bearer ${API_KEY}` } : {}),
      },
      body: form,
    });
    const response = await res.json();

    // Clean up uploaded file
    fs.unlinkSync(req.file.path);

    res.json({
      success: true,
      transcription: response.text,
      wordCount: response.text.split(/\s+/).length
    });
  } catch (error) {
    // Clean up on error
    if (req.file && fs.existsSync(req.file.path)) {
      fs.unlinkSync(req.file.path);
    }

    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

app.listen(3000, () => {
  console.log('ASR API running on port 3000');
});
```

## Troubleshooting

**Issue**: "Credentials exposed in client code"
- **Solution**: Read `LLM_API_KEY` from environment variables in server-side code only

**Issue**: Empty or incorrect transcription
- **Solution**: Verify audio quality and format. Check if audio contains clear speech

**Issue**: Large file processing fails
- **Solution**: Consider splitting large audio files into smaller segments

**Issue**: Slow transcription speed
- **Solution**: Implement caching for repeated transcriptions, optimize file sizes

**Issue**: Memory errors with large files
- **Solution**: Process files in chunks or increase Node.js memory limit

**Issue**: 404 on `/audio/transcriptions`
- **Solution**: Your server does not implement the OpenAI audio route. Point `LLM_BASE_URL` at a gateway or ASR server that does (faster-whisper-server, Speaches, Groq, etc.)

## Performance Tips

1. **Reuse HTTP Connections**: `fetch` with keep-alive reuses connections across requests
2. **Implement Caching**: Cache transcriptions for duplicate files
3. **Batch Processing**: Process multiple files efficiently with proper queuing
4. **Audio Optimization**: Compress audio files before processing when possible
5. **Async Operations**: Use Promise.all for parallel processing when appropriate

## Audio Quality Guidelines

For best transcription results:
- **Sample Rate**: 16kHz or higher
- **Format**: WAV, MP3, or M4A recommended
- **Noise Level**: Minimize background noise
- **Speech Clarity**: Clear pronunciation and normal speaking pace
- **File Size**: Under 100MB recommended for individual files

## Remember

- Works with any OpenAI-compatible server exposing `/audio/transcriptions` (faster-whisper-server, whisper.cpp server, Speaches, Groq, OpenAI, ...)
- Designed for the DiveeOI agent (OpenCode-based)
- Configuration via environment variables: `LLM_BASE_URL`, `LLM_API_KEY`, `ASR_MODEL`
- Audio files are uploaded as multipart form data (`file` + `model` fields)
- The endpoint returns JSON with a `text` field containing the transcription
- Keep your API key in server-side code only
- Implement proper error handling for production applications
- Consider audio quality for best transcription accuracy
- Clean up temporary files after processing
- Cache results for frequently transcribed files
