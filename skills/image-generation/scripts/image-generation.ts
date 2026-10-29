// Image generation via an OpenAI-compatible server.
// Route: POST {LLM_BASE_URL}/images/generations
// Supported by gateways that front open-source diffusion models (e.g. Stable
// Diffusion XL/3, FLUX, Qwen-Image) and by most OpenAI-compatible API
// aggregators. The exact model id depends on your server - set IMAGE_MODEL.
//
// Configuration (environment variables):
//   LLM_BASE_URL - OpenAI-compatible base URL (default: http://localhost:11434/v1)
//   LLM_API_KEY  - API key sent as a Bearer token (default: empty)
//   IMAGE_MODEL  - image model name (default: stable-diffusion-xl)

import fs from 'fs';

const BASE_URL = process.env.LLM_BASE_URL ?? "http://localhost:11434/v1";
const API_KEY = process.env.LLM_API_KEY ?? "";
const IMAGE_MODEL = process.env.IMAGE_MODEL ?? "stable-diffusion-xl";

async function main(prompt: string, size: '1024x1024' | '768x1344' | '864x1152' | '1344x768' | '1152x864' | '1440x720' | '720x1440', outFile: string) {
        try {
                const res = await fetch(`${BASE_URL}/images/generations`, {
                        method: 'POST',
                        headers: {
                                'Content-Type': 'application/json',
                                ...(API_KEY ? { Authorization: `Bearer ${API_KEY}` } : {}),
                        },
                        body: JSON.stringify({
                                model: IMAGE_MODEL,
                                prompt,
                                size,
                                response_format: 'b64_json',
                        }),
                });
                if (!res.ok) throw new Error(`Image generation request failed (${res.status}): ${await res.text()}`);

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
                console.log(`Image saved to ${outFile}`);
        } catch (err: any) {
                console.error('Image generation failed:', err?.message || err);
        }
}

main('A cute kitten', '1024x1024', './output.png');
