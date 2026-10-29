---
name: image-generation
description: Implement AI image generation capabilities using any OpenAI-compatible server that exposes the /images/generations endpoint. Use this skill when the user needs to create images from text descriptions, generate visual content, create artwork, design assets, or build applications with AI-powered image creation. Supports multiple image sizes and returns base64 encoded images. Works with any OpenAI-compatible LLM server (open-source or free), designed for the DiveeOI agent (OpenCode-based).
license: MIT
---

# Image Generation Skill

This skill guides the implementation of image generation functionality using plain OpenAI-compatible HTTP calls (no SDK, no extra dependencies), enabling creation of high-quality images from text descriptions.

It works with any OpenAI-compatible server that exposes the `POST /images/generations` route (open-source or free) — gateways fronting open-source diffusion models (Stable Diffusion XL/3, FLUX, Qwen-Image) and hosted OpenAI-compatible APIs — and is designed for the DiveeOI agent (OpenCode-based).

## Skills Path

**Skill Location**: `{project_path}/skills/image-generation`

this skill is located at above path in your project.

**Reference Scripts**: Example test scripts are available in the `{Skill Location}/scripts/` directory for quick testing and reference. See `{Skill Location}/scripts/image-generation.ts` for a working example.

## Overview

Image Generation allows you to build applications that create visual content from text prompts using AI models, enabling creative workflows, design automation, and visual content production.

**IMPORTANT**: Keep your API key in backend code or environment variables only. Never hardcode credentials in client-side code.

## Prerequisites

- Node.js 18+ (for the global `fetch` API) or any HTTP client
- An OpenAI-compatible server exposing `POST /images/generations`
- No npm packages required — examples use built-in APIs only

## Configuration (Environment Variables)

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_BASE_URL` | `http://localhost:11434/v1` | OpenAI-compatible base URL |
| `LLM_API_KEY` | (empty) | API key sent as `Authorization: Bearer <key>`; leave empty for local servers |
| `IMAGE_MODEL` | `stable-diffusion-xl` | Image model name (server-dependent, e.g. `stable-diffusion-xl`, `flux.1-schnell`, `qwen-image`) |

### Shared Client Helper

All examples below use this helper (plain `fetch`, zero dependencies):

```javascript
const BASE_URL = process.env.LLM_BASE_URL ?? "http://localhost:11434/v1";
const API_KEY = process.env.LLM_API_KEY ?? "";
const IMAGE_MODEL = process.env.IMAGE_MODEL ?? "stable-diffusion-xl";

async function generateImageRequest(prompt, size) {
  const res = await fetch(`${BASE_URL}/images/generations`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(API_KEY ? { Authorization: `Bearer ${API_KEY}` } : {}),
    },
    body: JSON.stringify({
      model: IMAGE_MODEL,
      prompt: prompt,
      size: size,
      response_format: 'b64_json',
    }),
  });
  if (!res.ok) throw new Error(`Image generation request failed (${res.status}): ${await res.text()}`);
  return res.json();
}
```

## Basic Image Generation

### Simple Image Creation

```javascript
import fs from 'fs';

async function generateImage(prompt, outputPath) {
  const response = await generateImageRequest(prompt, '1024x1024');

  const imageBase64 = response.data[0].b64_json ?? response.data[0].base64;

  // Save image
  const buffer = Buffer.from(imageBase64, 'base64');
  fs.writeFileSync(outputPath, buffer);

  console.log(`Image saved to ${outputPath}`);
  return outputPath;
}

// Usage
await generateImage(
  'A cute cat playing in the garden',
  './cat_image.png'
);
```

### Multiple Image Sizes

```javascript
import fs from 'fs';

// Commonly supported sizes (server-dependent)
const SUPPORTED_SIZES = [
  '1024x1024',  // Square
  '768x1344',   // Portrait
  '864x1152',   // Portrait
  '1344x768',   // Landscape
  '1152x864',   // Landscape
  '1440x720',   // Wide landscape
  '720x1440'    // Tall portrait
];

async function generateImageWithSize(prompt, size, outputPath) {
  if (!SUPPORTED_SIZES.includes(size)) {
    throw new Error(`Unsupported size: ${size}. Use one of: ${SUPPORTED_SIZES.join(', ')}`);
  }

  const response = await generateImageRequest(prompt, size);

  const imageBase64 = response.data[0].b64_json ?? response.data[0].base64;
  const buffer = Buffer.from(imageBase64, 'base64');
  fs.writeFileSync(outputPath, buffer);

  return {
    path: outputPath,
    size: size,
    fileSize: buffer.length
  };
}

// Usage - Different sizes
await generateImageWithSize(
  'A beautiful landscape',
  '1344x768',
  './landscape.png'
);

await generateImageWithSize(
  'A portrait of a person',
  '768x1344',
  './portrait.png'
);
```

## CLI Tool Usage

The `curl` command provides a convenient way to generate images directly from the command line.

### Basic CLI Usage

```bash
# Generate image with full options (OpenAI-style JSON request)
curl -s "$LLM_BASE_URL/images/generations" \
  -H "Content-Type: application/json" \
  ${LLM_API_KEY:+-H "Authorization: Bearer $LLM_API_KEY"} \
  -d '{"model": "stable-diffusion-xl", "prompt": "A beautiful landscape", "size": "1024x1024", "response_format": "b64_json"}' \
  | jq -r '.data[0].b64_json' | base64 -d > ./image.png

# Specify size
curl -s "$LLM_BASE_URL/images/generations" \
  -H "Content-Type: application/json" \
  -d '{"model": "stable-diffusion-xl", "prompt": "A sunset", "size": "1344x768", "response_format": "b64_json"}' \
  | jq -r '.data[0].b64_json' | base64 -d > ./sunset.png

# Portrait orientation
curl -s "$LLM_BASE_URL/images/generations" \
  -H "Content-Type: application/json" \
  -d '{"model": "stable-diffusion-xl", "prompt": "A portrait", "size": "768x1344", "response_format": "b64_json"}' \
  | jq -r '.data[0].b64_json' | base64 -d > ./portrait.png
```

### CLI Use Cases

```bash
gen() { curl -s "$LLM_BASE_URL/images/generations" -H "Content-Type: application/json" \
  -d "{\"model\": \"${IMAGE_MODEL:-stable-diffusion-xl}\", \"prompt\": \"$1\", \"size\": \"${3:-1024x1024}\", \"response_format\": \"b64_json\"}" \
  | jq -r '.data[0].b64_json' | base64 -d > "$2"; }

# Website hero image
gen "Modern tech office with diverse team collaborating" ./hero.png 1440x720

# Product image
gen "Sleek smartphone on minimalist desk, professional product photography" ./product.png

# Blog post illustration
gen "Abstract visualization of data flowing through networks" ./blog_header.png 1344x768

# Social media content
gen "Vibrant illustration of community connection" ./social.png

# Website favicon/logo
gen "Simple geometric logo with blue gradient, minimal design" ./logo.png

# Background pattern
gen "Subtle geometric pattern, pastel colors, website background" ./bg_pattern.png 1440x720
```

## Advanced Use Cases

### Batch Image Generation

```javascript
import fs from 'fs';
import path from 'path';

async function generateImageBatch(prompts, outputDir, size = '1024x1024') {
  // Ensure output directory exists
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  const results = [];

  for (let i = 0; i < prompts.length; i++) {
    try {
      const prompt = prompts[i];
      const filename = `image_${i + 1}.png`;
      const outputPath = path.join(outputDir, filename);

      const response = await generateImageRequest(prompt, size);

      const imageBase64 = response.data[0].b64_json ?? response.data[0].base64;
      const buffer = Buffer.from(imageBase64, 'base64');
      fs.writeFileSync(outputPath, buffer);

      results.push({
        success: true,
        prompt: prompt,
        path: outputPath,
        size: buffer.length
      });

      console.log(`✓ Generated: ${filename}`);
    } catch (error) {
      results.push({
        success: false,
        prompt: prompts[i],
        error: error.message
      });

      console.error(`✗ Failed: ${prompts[i]} - ${error.message}`);
    }
  }

  return results;
}

// Usage
const prompts = [
  'A serene mountain landscape at sunset',
  'A futuristic city with flying cars',
  'An underwater coral reef teeming with life'
];

const results = await generateImageBatch(prompts, './generated-images');
console.log(`Generated ${results.filter(r => r.success).length} images`);
```

### Image Generation Service

```javascript
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';

class ImageGenerationService {
  constructor(outputDir = './generated-images') {
    this.outputDir = outputDir;
    this.cache = new Map();
  }

  async initialize() {
    if (!fs.existsSync(this.outputDir)) {
      fs.mkdirSync(this.outputDir, { recursive: true });
    }
  }

  generateCacheKey(prompt, size) {
    return crypto
      .createHash('md5')
      .update(`${prompt}-${size}`)
      .digest('hex');
  }

  async generate(prompt, options = {}) {
    const {
      size = '1024x1024',
      useCache = true,
      filename = null
    } = options;

    // Check cache
    const cacheKey = this.generateCacheKey(prompt, size);

    if (useCache && this.cache.has(cacheKey)) {
      const cachedPath = this.cache.get(cacheKey);
      if (fs.existsSync(cachedPath)) {
        return {
          path: cachedPath,
          cached: true,
          prompt: prompt,
          size: size
        };
      }
    }

    // Generate new image
    const response = await generateImageRequest(prompt, size);

    const imageBase64 = response.data[0].b64_json ?? response.data[0].base64;
    const buffer = Buffer.from(imageBase64, 'base64');

    // Determine output path
    const outputFilename = filename || `${cacheKey}.png`;
    const outputPath = path.join(this.outputDir, outputFilename);

    fs.writeFileSync(outputPath, buffer);

    // Cache result
    if (useCache) {
      this.cache.set(cacheKey, outputPath);
    }

    return {
      path: outputPath,
      cached: false,
      prompt: prompt,
      size: size,
      fileSize: buffer.length
    };
  }

  clearCache() {
    this.cache.clear();
  }

  getCacheSize() {
    return this.cache.size;
  }
}

// Usage
const service = new ImageGenerationService();
await service.initialize();

const result = await service.generate(
  'A modern office space',
  { size: '1440x720' }
);

console.log('Generated:', result.path);
```

### Website Asset Generator

```bash
# Using CLI for quick website asset generation
gen "Modern tech hero banner, blue gradient" ./assets/hero.png 1440x720
gen "Team collaboration illustration" ./assets/team.png 1344x768
gen "Simple geometric logo" ./assets/logo.png 1024x1024
```

## Best Practices

### 1. Effective Prompt Engineering

```javascript
function buildEffectivePrompt(subject, style, details = []) {
  const components = [
    subject,
    style,
    ...details,
    'high quality',
    'detailed'
  ];

  return components.filter(Boolean).join(', ');
}

// Usage
const prompt = buildEffectivePrompt(
  'mountain landscape',
  'oil painting style',
  ['sunset lighting', 'dramatic clouds', 'reflection in lake']
);

// Result: "mountain landscape, oil painting style, sunset lighting, dramatic clouds, reflection in lake, high quality, detailed"
```

### 2. Size Selection Helper

```javascript
function selectOptimalSize(purpose) {
  const sizeMap = {
    'hero-banner': '1440x720',
    'blog-header': '1344x768',
    'social-square': '1024x1024',
    'portrait': '768x1344',
    'product': '1024x1024',
    'landscape': '1344x768',
    'mobile-banner': '720x1440',
    'thumbnail': '1024x1024'
  };

  return sizeMap[purpose] || '1024x1024';
}

// Usage
const size = selectOptimalSize('hero-banner');
await generateImage('website hero image', size, './hero.png');
```

### 3. Error Handling

```javascript
import fs from 'fs';

async function safeGenerateImage(prompt, size, outputPath, retries = 3) {
  let lastError;

  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      const response = await generateImageRequest(prompt, size);

      const imageBase64 = response.data?.[0]?.b64_json ?? response.data?.[0]?.base64;
      if (!imageBase64) {
        throw new Error('Invalid response from image generation API');
      }

      const buffer = Buffer.from(imageBase64, 'base64');
      fs.writeFileSync(outputPath, buffer);

      return {
        success: true,
        path: outputPath,
        attempts: attempt
      };
    } catch (error) {
      lastError = error;
      console.error(`Attempt ${attempt} failed:`, error.message);

      if (attempt < retries) {
        // Wait before retry (exponential backoff)
        await new Promise(resolve => setTimeout(resolve, 1000 * attempt));
      }
    }
  }

  return {
    success: false,
    error: lastError.message,
    attempts: retries
  };
}
```

## Common Use Cases

1. **Website Design**: Generate hero images, backgrounds, and visual assets
2. **Marketing Materials**: Create social media graphics and promotional images
3. **Product Visualization**: Generate product mockups and variations
4. **Content Creation**: Produce blog post illustrations and thumbnails
5. **Brand Assets**: Create logos, icons, and brand imagery
6. **UI/UX Design**: Generate interface elements and illustrations
7. **Game Development**: Create concept art and game assets
8. **E-commerce**: Generate product images and lifestyle shots

## Integration Examples

### Express.js API Endpoint

```javascript
import express from 'express';
import fs from 'fs';
import path from 'path';

const app = express();
app.use(express.json());
app.use('/images', express.static('generated-images'));

const outputDir = './generated-images';

async function init() {
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
}

app.post('/api/generate-image', async (req, res) => {
  try {
    const { prompt, size = '1024x1024' } = req.body;

    if (!prompt) {
      return res.status(400).json({ error: 'Prompt is required' });
    }

    const response = await generateImageRequest(prompt, size);

    const imageBase64 = response.data[0].b64_json ?? response.data[0].base64;
    const buffer = Buffer.from(imageBase64, 'base64');

    const filename = `img_${Date.now()}.png`;
    const filepath = path.join(outputDir, filename);
    fs.writeFileSync(filepath, buffer);

    res.json({
      success: true,
      imageUrl: `/images/${filename}`,
      prompt: prompt,
      size: size
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

init().then(() => {
  app.listen(3000, () => {
    console.log('Image generation API running on port 3000');
  });
});
```

## CLI Integration in Scripts

### Shell Script Example

```bash
#!/bin/bash

# Generate website assets using CLI
echo "Generating website assets..."

gen() { curl -s "$LLM_BASE_URL/images/generations" -H "Content-Type: application/json" \
  -d "{\"model\": \"${IMAGE_MODEL:-stable-diffusion-xl}\", \"prompt\": \"$1\", \"size\": \"$3\", \"response_format\": \"b64_json\"}" \
  | jq -r '.data[0].b64_json' | base64 -d > "$2"; }

gen "Modern tech hero banner, blue gradient" ./assets/hero.png 1440x720
gen "Team collaboration illustration" ./assets/team.png 1344x768
gen "Simple geometric logo" ./assets/logo.png 1024x1024

echo "Assets generated successfully!"
```

## Troubleshooting

**Issue**: "API key must be kept server-side"
- **Solution**: Read `LLM_API_KEY` from environment variables and only use it in server-side code

**Issue**: Invalid size parameter
- **Solution**: Use only sizes supported by your server, e.g. 1024x1024, 768x1344, 864x1152, 1344x768, 1152x864, 1440x720, 720x1440

**Issue**: Generated image doesn't match prompt
- **Solution**: Make prompts more specific and descriptive. Include style, details, and quality terms

**Issue**: 404 on `/images/generations`
- **Solution**: Your server does not implement the OpenAI images route. Point `LLM_BASE_URL` at a gateway or image server that does

**Issue**: Image file is corrupted
- **Solution**: Verify base64 decoding and file writing are correct

## Prompt Engineering Tips

### Good Prompts
- ✓ "Professional product photography of wireless headphones, white background, studio lighting, high quality"
- ✓ "Mountain landscape at golden hour, oil painting style, dramatic clouds, detailed"
- ✓ "Modern minimalist logo for tech company, blue and white, geometric shapes"

### Poor Prompts
- ✗ "headphones"
- ✗ "picture of mountains"
- ✗ "logo"

### Prompt Components
1. **Subject**: What you want to see
2. **Style**: Art style, photography style, etc.
3. **Details**: Specific elements, colors, mood
4. **Quality**: "high quality", "detailed", "professional"

## Supported Image Sizes

- `1024x1024` - Square
- `768x1344` - Portrait
- `864x1152` - Portrait
- `1344x768` - Landscape
- `1152x864` - Landscape
- `1440x720` - Wide landscape
- `720x1440` - Tall portrait

(Size availability is server-dependent; the list above reflects the most common convention.)

## Remember

- Works with any OpenAI-compatible server exposing `POST /images/generations` (gateways fronting Stable Diffusion, FLUX, Qwen-Image, ..., or hosted OpenAI-compatible APIs)
- Designed for the DiveeOI agent (OpenCode-based)
- Configuration via environment variables: `LLM_BASE_URL`, `LLM_API_KEY`, `IMAGE_MODEL`
- The endpoint is `POST {LLM_BASE_URL}/images/generations` with `{model, prompt, size, response_format: "b64_json"}`
- The response contains the image as base64 (`data[0].b64_json`, or `data[0].base64` on some servers)
- Keep your API key in server-side code only
- Supported sizes are server-specific - use the provided list as guidance
- Base64 images need to be decoded before saving
- Consider caching for repeated prompts
- Implement retry logic for production applications
- Use descriptive prompts for better results
