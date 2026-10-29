// Image editing via an OpenAI-compatible server.
// Route: POST {LLM_BASE_URL}/images/edits (multipart/form-data, per the OpenAI
// images convention). This route is supported by OpenAI and by OpenAI-compatible
// gateways that front editable image models (e.g. Stable Diffusion img2img
// backends). Many chat-only servers (Ollama, plain vLLM) do NOT expose it -
// in that case point LLM_BASE_URL at a gateway that provides /images/edits.
//
// Configuration (environment variables):
//   LLM_BASE_URL     - OpenAI-compatible base URL (default: http://localhost:11434/v1)
//   LLM_API_KEY      - API key sent as a Bearer token (default: empty)
//   IMAGE_EDIT_MODEL - image editing model name (default: falls back to IMAGE_MODEL,
//                      then "stable-diffusion-xl")

import fs from 'fs';
import path from 'path';

const BASE_URL = process.env.LLM_BASE_URL ?? "http://localhost:11434/v1";
const API_KEY = process.env.LLM_API_KEY ?? "";
const IMAGE_EDIT_MODEL = process.env.IMAGE_EDIT_MODEL ?? process.env.IMAGE_MODEL ?? "stable-diffusion-xl";

// Turn the image source (local path, http(s) URL, or base64 data URL) into a Blob
// suitable for multipart upload.
async function imageSourceToBlob(imageSource: string): Promise<Blob> {
  if (imageSource.startsWith('data:')) {
    // data URL: data:<mime>;base64,<payload>
    const [meta, payload] = imageSource.split(',', 2);
    const mime = meta.slice(5).split(';')[0] || 'image/png';
    return new Blob([Buffer.from(payload, 'base64')], { type: mime });
  }
  if (/^https?:\/\//i.test(imageSource)) {
    const res = await fetch(imageSource);
    if (!res.ok) throw new Error(`Failed to download source image (${res.status})`);
    const mime = res.headers.get('content-type') ?? 'image/png';
    return new Blob([Buffer.from(await res.arrayBuffer())], { type: mime });
  }
  // Local file path
  const ext = path.extname(imageSource).toLowerCase();
  const mimeMap: Record<string, string> = {
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.webp': 'image/webp',
    '.bmp': 'image/bmp',
  };
  const buffer = fs.readFileSync(imageSource);
  return new Blob([buffer], { type: mimeMap[ext] ?? 'image/png' });
}

async function main(imageSource: string, prompt: string, size: '1024x1024' | '768x1344' | '864x1152' | '1344x768' | '1152x864' | '1440x720' | '720x1440', outFile: string) {
        try {
                const imageBlob = await imageSourceToBlob(imageSource);

                const form = new FormData();
                form.append('image', imageBlob, 'image.png');
                form.append('prompt', prompt);
                form.append('model', IMAGE_EDIT_MODEL);
                form.append('size', size);
                form.append('response_format', 'b64_json');
                form.append('n', '1');

                const res = await fetch(`${BASE_URL}/images/edits`, {
                        method: 'POST',
                        headers: {
                                ...(API_KEY ? { Authorization: `Bearer ${API_KEY}` } : {}),
                        },
                        body: form,
                });
                if (!res.ok) throw new Error(`Image edit request failed (${res.status}): ${await res.text()}`);

                const response: any = await res.json();

                // Accept both OpenAI-style `b64_json` and SDK-style `base64` fields
                const base64 = response?.data?.[0]?.b64_json ?? response?.data?.[0]?.base64;
                if (!base64) {
                        console.error('No image data returned by the API');
                        console.log('Full response:', JSON.stringify(response, null, 2));
                        return;
                }

                const buffer = Buffer.from(base64, 'base64');
                fs.writeFileSync(outFile, buffer);
                console.log(`Edited image saved to ${outFile}`);
        } catch (err: any) {
                console.error('Image editing failed:', err?.message || err);
        }
}

// Example usage - Edit an image
// You can use a local file path, an https URL, or a base64 data URL for the imageSource
main(
        './photo.jpg',  // or use: 'https://example.com/photo.jpg' or 'data:image/jpeg;base64,/9j/4AAQ...'
        'Transform this photo to have a sunset background with warm golden tones',
        '1024x1024',
        './output.png'
);
