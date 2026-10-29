// Video understanding via an OpenAI-compatible server.
// Works with any OpenAI-compatible server: Ollama, vLLM, LM Studio, OpenRouter, ...
// NOTE: point LLM_MODEL at a video-capable vision model; support for the
// `video_url` content part depends on the server (e.g. vLLM with a video VLM,
// gateways fronting Qwen-VL-Video style models).
//
// Configuration (environment variables):
//   LLM_BASE_URL - OpenAI-compatible base URL (default: http://localhost:11434/v1)
//   LLM_API_KEY  - API key sent as a Bearer token (default: empty)
//   LLM_MODEL    - video vision model name (default: qwen2.5)

import fs from 'fs';

const BASE_URL = process.env.LLM_BASE_URL ?? "http://localhost:11434/v1";
const API_KEY = process.env.LLM_API_KEY ?? "";
const MODEL = process.env.LLM_MODEL ?? "qwen2.5";

interface VisionMessage {
  role: string;
  content: Array<Record<string, unknown>>;
}

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

async function main(videoUrl: string, prompt: string) {
        try {
                // If a local file path is given, convert it to a base64 data URL.
                // Remote http(s) URLs are passed through unchanged.
                let videoSource = videoUrl;
                if (fs.existsSync(videoUrl)) {
                        const videoBuffer = fs.readFileSync(videoUrl);
                        const base64Video = videoBuffer.toString('base64');
                        const ext = videoUrl.toLowerCase().split('.').pop() || '';
                        const mimeMap: Record<string, string> = {
                                mp4: 'video/mp4',
                                avi: 'video/x-msvideo',
                                mov: 'video/quicktime',
                                webm: 'video/webm',
                                mkv: 'video/x-matroska',
                        };
                        const mimeType = mimeMap[ext] || 'video/mp4';
                        videoSource = `data:${mimeType};base64,${base64Video}`;
                }

                const messages: VisionMessage[] = [
                        {
                                role: 'system',
                                content: [
                                        { type: 'text', text: 'Output only text, no markdown.' }
                                ]
                        },
                        {
                                role: 'user',
                                content: [
                                        { type: 'text', text: prompt },
                                        { type: 'video_url', video_url: { url: videoSource } }
                                ]
                        }
                ];

                const response = await chatCompletions({
                        model: MODEL,
                        messages,
                });

                const reply = response.choices?.[0]?.message?.content;
                console.log('Video Understanding Result:');
                console.log(reply ?? JSON.stringify(response, null, 2));
        } catch (err: any) {
                console.error('Video understanding failed:', err?.message || err);
        }
}

// Example usage - analyze a video
main(
        "https://example.com/sample-video.mp4",
        "Please analyze this video and describe the main events, actions, and key moments in chronological order."
);
