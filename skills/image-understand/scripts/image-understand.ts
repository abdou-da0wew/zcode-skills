// Image understanding via an OpenAI-compatible server.
// Works with any OpenAI-compatible server: Ollama, vLLM, LM Studio, OpenRouter, ...
// NOTE: point LLM_MODEL at a vision-capable model (e.g. qwen2.5-vl, llama3.2-vision,
// minicpm-v) or the request will fail.
//
// Configuration (environment variables):
//   LLM_BASE_URL - OpenAI-compatible base URL (default: http://localhost:11434/v1)
//   LLM_API_KEY  - API key sent as a Bearer token (default: empty)
//   LLM_MODEL    - vision model name (default: qwen2.5)

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

async function main(imageUrl: string, prompt: string) {
        try {
                // If a local file path is given, convert it to a base64 data URL
                // (recommended: more reliable than remote URLs). Remote http(s)
                // URLs are passed through unchanged.
                let imageSource = imageUrl;
                if (fs.existsSync(imageUrl)) {
                        const imageBuffer = fs.readFileSync(imageUrl);
                        const base64Image = imageBuffer.toString('base64');
                        const ext = imageUrl.toLowerCase().split('.').pop() || '';
                        const mimeMap: Record<string, string> = {
                                png: 'image/png',
                                jpg: 'image/jpeg',
                                jpeg: 'image/jpeg',
                                gif: 'image/gif',
                                webp: 'image/webp',
                                bmp: 'image/bmp',
                        };
                        const mimeType = mimeMap[ext] || 'image/jpeg';
                        imageSource = `data:${mimeType};base64,${base64Image}`;
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
                                        { type: 'image_url', image_url: { url: imageSource } }
                                ]
                        }
                ];

                const response = await chatCompletions({
                        model: MODEL,
                        messages,
                });

                const reply = response.choices?.[0]?.message?.content;
                console.log('Image Understanding Result:');
                console.log(reply ?? JSON.stringify(response, null, 2));
        } catch (err: any) {
                console.error('Image understanding failed:', err?.message || err);
        }
}

// Example usage - analyze an image (local path or remote URL both work)
main(
        "./sample-image.png",
        "Please analyze this image and describe what you see in detail."
);
