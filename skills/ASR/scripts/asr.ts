// ASR (speech-to-text) via an OpenAI-compatible server.
// Works with any OpenAI-compatible server that exposes POST /audio/transcriptions
// (multipart upload), e.g. faster-whisper-server, whisper.cpp server, Speaches,
// Groq, OpenAI, and most API gateways.
//
// Configuration (environment variables):
//   LLM_BASE_URL - OpenAI-compatible base URL (default: http://localhost:11434/v1)
//   LLM_API_KEY  - API key sent as a Bearer token (default: empty)
//   ASR_MODEL    - transcription model name (default: whisper-1)

import fs from 'fs';
import path from 'path';

const BASE_URL = process.env.LLM_BASE_URL ?? "http://localhost:11434/v1";
const API_KEY = process.env.LLM_API_KEY ?? "";
const ASR_MODEL = process.env.ASR_MODEL ?? "whisper-1";

async function transcribeFile(inputFile: string): Promise<string> {
  // Read the audio file and upload it as multipart/form-data
  const audioBuffer = fs.readFileSync(inputFile);
  const blob = new Blob([audioBuffer]);

  const form = new FormData();
  form.append('file', blob, path.basename(inputFile));
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

  const result: any = await res.json();
  return result.text ?? '';
}

async function main(inputFile: string) {
        if (!fs.existsSync(inputFile)) {
                console.error(`Audio file not found: ${inputFile}`);
        return;
        }

        try {
                const text = await transcribeFile(inputFile);

                console.log('Transcription result:');
                console.log(text || '(empty transcription)');
        } catch (err: any) {
                console.error('ASR failed:', err?.message || err);
        }
}

main('./output.wav');
