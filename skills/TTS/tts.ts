// TTS (text-to-speech) via an OpenAI-compatible server.
// Works with any OpenAI-compatible server that exposes POST /audio/speech
// (e.g. OpenAI-compatible gateways proxying Kokoro, Piper, Coqui, ...).
//
// Configuration (environment variables):
//   LLM_BASE_URL - OpenAI-compatible base URL (default: http://localhost:11434/v1)
//   LLM_API_KEY  - API key sent as a Bearer token (default: empty)
//   TTS_MODEL    - TTS model name (default: tts-1)
//   TTS_VOICE    - voice id (default: alloy; the available voices depend on the server)

import fs from "fs";

const BASE_URL = process.env.LLM_BASE_URL ?? "http://localhost:11434/v1";
const API_KEY = process.env.LLM_API_KEY ?? "";
const TTS_MODEL = process.env.TTS_MODEL ?? "tts-1";
const TTS_VOICE = process.env.TTS_VOICE ?? "alloy";

async function main(text: string, outFile: string) {
  try {
    const res = await fetch(`${BASE_URL}/audio/speech`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(API_KEY ? { Authorization: `Bearer ${API_KEY}` } : {}),
      },
      body: JSON.stringify({
        model: TTS_MODEL,
        voice: TTS_VOICE,
        input: text,
        speed: 1.0,
        response_format: "wav",
        stream: false,
      }),
    });
    if (!res.ok) throw new Error(`TTS request failed (${res.status}): ${await res.text()}`);

    // The endpoint returns raw binary audio; write it straight to disk.
    const arrayBuffer = await res.arrayBuffer();
    const buffer = Buffer.from(new Uint8Array(arrayBuffer));
    fs.writeFileSync(outFile, buffer);
    console.log(`TTS audio saved to ${outFile}`);
  } catch (err: any) {
    console.error("TTS failed:", err?.message || err);
  }
}

main("Hello, world!", "./output.wav");
