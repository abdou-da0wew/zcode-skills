---
name: image-edit
description: Implement AI image editing and modification capabilities using any OpenAI-compatible server that exposes the /images/edits endpoint. Use this skill when the user needs to edit existing images, create variations, modify visual content, redesign assets, or transform images based on text descriptions. Supports multiple image sizes and returns base64 encoded results. Works with any OpenAI-compatible LLM server (open-source or free), designed for the DiveeOI agent (OpenCode-based).
license: MIT
---

# Image Edit Skill

This skill guides the implementation of image editing and modification functionality using plain OpenAI-compatible HTTP calls (no SDK, no extra dependencies), enabling intelligent transformation and editing of images based on text descriptions.

It works with any OpenAI-compatible server that exposes the `POST /images/edits` route (open-source or free) — hosted OpenAI-compatible APIs and gateways fronting editable diffusion models (e.g. Stable Diffusion img2img backends) — and is designed for the DiveeOI agent (OpenCode-based).

## Skills Path

**Skill Location**: `{project_path}/skills/image-edit`

this skill is located at above path in your project.

**Reference Scripts**: Example test scripts are available in the `{Skill Location}/scripts/` directory for quick testing and reference. See `{Skill Location}/scripts/image-edit.ts` for a working example.

## Overview

Image Edit allows you to build applications that modify, transform, and enhance existing images using AI models. Perfect for redesigning assets, creating variations, improving visual content, and transforming images based on textual descriptions.

**IMPORTANT**: Keep your API key in backend code or environment variables only. Never hardcode credentials in client-side code.

## API Endpoint

The image editing functionality uses the standard OpenAI images-edit convention:

```
POST {LLM_BASE_URL}/images/edits        (multipart/form-data)
```

**Multipart form fields:**

```javascript
// form fields for POST /images/edits
{
  image: Blob,               // Required: the source image (binary upload)
  prompt: string,            // Required: description of the edit to apply
  model: string,             // Required: image editing model (IMAGE_EDIT_MODEL)
  size: string,              // Optional: output size (default: '1024x1024')
  n: number,                 // Optional: number of images (default: 1)
  response_format: 'b64_json' // Optional: request base64 output
}
```

**Returns**: JSON with `data[0].b64_json` containing the base64 encoded edited image (some servers return `data[0].base64` instead — the helper below accepts both).

**Server support note**: chat-only servers (plain Ollama, plain vLLM) do **not** implement `/images/edits`. Point `LLM_BASE_URL` at a gateway or image server that does. The route mapping documented here is the most common OpenAI-compatible convention.

## Prerequisites

- Node.js 18+ (for the global `fetch`, `FormData`, and `Blob` APIs) or any HTTP client
- An OpenAI-compatible server exposing `POST /images/edits`
- No npm packages required — examples use built-in APIs only

## Configuration (Environment Variables)

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_BASE_URL` | `http://localhost:11434/v1` | OpenAI-compatible base URL |
| `LLM_API_KEY` | (empty) | API key sent as `Authorization: Bearer <key>`; leave empty for local servers |
| `IMAGE_EDIT_MODEL` | falls back to `IMAGE_MODEL`, then `stable-diffusion-xl` | Image editing model name (server-dependent) |

### Shared Client Helper

All examples below use this helper (plain `fetch`, zero dependencies):

```javascript
const BASE_URL = process.env.LLM_BASE_URL ?? "http://localhost:11434/v1";
const API_KEY = process.env.LLM_API_KEY ?? "";
const IMAGE_EDIT_MODEL = process.env.IMAGE_EDIT_MODEL ?? process.env.IMAGE_MODEL ?? "stable-diffusion-xl";

// Turn an image source (local path, http(s) URL, or base64 data URL) into a Blob
async function imageSourceToBlob(imageSource) {
  if (imageSource.startsWith('data:')) {
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
  const fs = await import('fs');
  return new Blob([fs.readFileSync(imageSource)], { type: 'image/png' });
}

async function editImageRequest(imageSource, prompt, size) {
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
  return res.json();
}
```

## Basic Image Editing

### Simple Image Transformation

```javascript
import fs from 'fs';

async function editImage(imageSource, editPrompt, outputPath, size = '1024x1024') {
  const response = await editImageRequest(imageSource, editPrompt, size);

  const imageBase64 = response.data[0].b64_json ?? response.data[0].base64;

  // Save edited image
  const buffer = Buffer.from(imageBase64, 'base64');
  fs.writeFileSync(outputPath, buffer);

  console.log(`Edited image saved to ${outputPath}`);
  return outputPath;
}

// Usage - Using remote image URL
await editImage(
  'https://example.com/landscape.jpg',
  'Transform this landscape into a night scene with stars and moon',
  './landscape_night.png'
);

// Usage - Using local image converted to base64 data URL
import { readFileSync } from 'fs';
const imageBuffer = readFileSync('./photo.jpg');
const base64Image = imageBuffer.toString('base64');
const dataUrl = `data:image/jpeg;base64,${base64Image}`;

await editImage(
  dataUrl,
  'Change the cat to a dog, keep everything else the same',
  './dog_version.png'
);
```

### Create Image Variations

```javascript
async function createVariation(imageSource, baseDescription, variation, outputPath, size = '1024x1024') {
  // Combine base description with variation request
  const prompt = `${baseDescription}, ${variation}`;

  const response = await editImageRequest(imageSource, prompt, size);

  const imageBase64 = response.data[0].b64_json ?? response.data[0].base64;
  const buffer = Buffer.from(imageBase64, 'base64');
  fs.writeFileSync(outputPath, buffer);

  return {
    path: outputPath,
    prompt: prompt,
    variation: variation
  };
}

// Usage - Create variations from original image
await createVariation(
  'https://example.com/headshot.jpg',
  'Professional headshot photo',
  'with blue background instead of gray',
  './headshot_blue.png'
);

await createVariation(
  './smartphone.png',
  'Product photo of smartphone',
  'on wooden table instead of white background',
  './product_wood.png'
);
```

### Multiple Image Sizes for Editing

```javascript
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

async function editImageWithSize(imageSource, editPrompt, size, outputPath) {
  if (!SUPPORTED_SIZES.includes(size)) {
    throw new Error(`Unsupported size: ${size}. Use one of: ${SUPPORTED_SIZES.join(', ')}`);
  }

  const response = await editImageRequest(imageSource, editPrompt, size);

  const imageBase64 = response.data[0].b64_json ?? response.data[0].base64;
  const buffer = Buffer.from(imageBase64, 'base64');
  fs.writeFileSync(outputPath, buffer);

  return {
    path: outputPath,
    size: size,
    fileSize: buffer.length
  };
}

// Usage - Edit with different aspect ratios
await editImageWithSize(
  './logo.png',
  'Redesign the logo to be more modern and minimalist',
  '1024x1024',
  './logo_redesigned.png'
);

await editImageWithSize(
  'https://example.com/portrait.jpg',
  'Transform the portrait to landscape orientation, sunset lighting',
  '1344x768',
  './portrait_landscape.png'
);
```

## CLI Tool Usage

The `curl` command provides a convenient way to edit images directly from the command line.

### Basic CLI Usage

```bash
# Edit image with full options (multipart upload, OpenAI-style)
curl -s "$LLM_BASE_URL/images/edits" \
  ${LLM_API_KEY:+-H "Authorization: Bearer $LLM_API_KEY"} \
  -F image=@./photo.png \
  -F prompt="Change the background to sunset colors" \
  -F model=stable-diffusion-xl \
  -F size=1024x1024 \
  -F response_format=b64_json \
  | jq -r '.data[0].b64_json' | base64 -d > ./edited.png

# Specify output size
curl -s "$LLM_BASE_URL/images/edits" \
  -F image=@./design.png \
  -F prompt="Redesign in modern style" \
  -F size=1344x768 \
  -F response_format=b64_json \
  | jq -r '.data[0].b64_json' | base64 -d > ./modern.png
```

### CLI Parameters

- `image=@<path>`: **Required** - Original image uploaded as multipart form data
- `prompt`: **Required** - Description of the edit to apply
- `model`: Optional - Image editing model (default: `IMAGE_EDIT_MODEL`)
- `size`: Optional - Image size, default is 1024x1024
- `n`: Optional - Number of images to generate (default: 1)

### Supported Sizes

- `1024x1024`, `768x1344`, `864x1152`, `1344x768`, `1152x864`, `1440x720`, `720x1440` (server-dependent)

### CLI Use Cases for Image Editing

```bash
edit() { curl -s "$LLM_BASE_URL/images/edits" -F image=@"$2" -F prompt="$1" \
  -F model="${IMAGE_EDIT_MODEL:-stable-diffusion-xl}" -F size="${4:-1024x1024}" \
  -F response_format=b64_json | jq -r '.data[0].b64_json' | base64 -d > "$3"; }

# Redesign existing asset
edit "Redesign the logo with gradients and modern styling" ./logo.png ./logo_v2.png

# Change color scheme
edit "Change color scheme to blue and white, professional style" ./original.png ./recolored.png 1440x720

# Style transformation
edit "Transform to oil painting style, vibrant colors" ./photo.jpg ./oil_painting.png 1152x864

# Background replacement
edit "Replace background with modern office setting" ./portrait.png ./new_background.png 1344x768

# Lighting adjustment
edit "Adjust to golden hour lighting, warm tones" ./landscape.jpg ./golden_hour.png

# Element modification
edit "Replace the red car with a blue motorcycle" ./scene.png ./modified.png 1344x768

# Mood transformation
edit "Transform to dark moody atmosphere with dramatic lighting" ./bright.jpg ./moody.png 1440x720
```

## Advanced Use Cases

### Batch Image Editing

```javascript
import fs from 'fs';
import path from 'path';

async function batchEditImages(editInstructions, outputDir, size = '1024x1024') {
  // Ensure output directory exists
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  const results = [];

  for (let i = 0; i < editInstructions.length; i++) {
    try {
      const instruction = editInstructions[i];
      const filename = `edited_${i + 1}.png`;
      const outputPath = path.join(outputDir, filename);

      const response = await editImageRequest(instruction.imageSource, instruction.prompt, size);

      const imageBase64 = response.data[0].b64_json ?? response.data[0].base64;
      const buffer = Buffer.from(imageBase64, 'base64');
      fs.writeFileSync(outputPath, buffer);

      results.push({
        success: true,
        instruction: instruction.prompt,
        path: outputPath,
        size: buffer.length
      });

      console.log(`✓ Edited: ${filename}`);
    } catch (error) {
      results.push({
        success: false,
        instruction: editInstructions[i].prompt,
        error: error.message
      });

      console.error(`✗ Failed: ${editInstructions[i].prompt} - ${error.message}`);
    }
  }

  return results;
}

// Usage - Create multiple variations from the same image
const editInstructions = [
  {
    imageSource: './original.jpg',
    prompt: 'Change background to blue gradient'
  },
  {
    imageSource: './original.jpg',
    prompt: 'Transform to black and white, high contrast'
  },
  {
    imageSource: './original.jpg',
    prompt: 'Add sunset lighting effects'
  }
];

const results = await batchEditImages(editInstructions, './edited-images');
console.log(`Edited ${results.filter(r => r.success).length} images`);
```

### Image Editing Service

```javascript
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';

class ImageEditingService {
  constructor(outputDir = './edited-images') {
    this.outputDir = outputDir;
    this.editHistory = [];
  }

  async initialize() {
    if (!fs.existsSync(this.outputDir)) {
      fs.mkdirSync(this.outputDir, { recursive: true });
    }
  }

  generateFilename(editPrompt) {
    const hash = crypto
      .createHash('md5')
      .update(`${editPrompt}-${Date.now()}`)
      .digest('hex')
      .substring(0, 8);

    return `edited_${hash}.png`;
  }

  async edit(imageSource, editPrompt, options = {}) {
    const {
      size = '1024x1024',
      saveToHistory = true,
      filename = null
    } = options;

    const response = await editImageRequest(imageSource, editPrompt, size);

    const imageBase64 = response.data[0].b64_json ?? response.data[0].base64;
    const buffer = Buffer.from(imageBase64, 'base64');

    // Determine output path
    const outputFilename = filename || this.generateFilename(editPrompt);
    const outputPath = path.join(this.outputDir, outputFilename);

    fs.writeFileSync(outputPath, buffer);

    const result = {
      path: outputPath,
      imageSource: imageSource,
      editPrompt: editPrompt,
      size: size,
      fileSize: buffer.length,
      timestamp: new Date().toISOString()
    };

    // Save to history
    if (saveToHistory) {
      this.editHistory.push(result);
    }

    return result;
  }

  async createVariations(imageSource, basePrompt, variations, options = {}) {
    const results = [];

    for (const variation of variations) {
      const fullPrompt = `${basePrompt}, ${variation}`;
      const result = await this.edit(imageSource, fullPrompt, options);
      result.variation = variation;
      results.push(result);
    }

    return results;
  }

  getEditHistory() {
    return this.editHistory;
  }

  clearHistory() {
    this.editHistory = [];
  }
}

// Usage
const service = new ImageEditingService();
await service.initialize();

// Single edit
const edited = await service.edit(
  './original.jpg',
  'Transform to watercolor painting style',
  { size: '1024x1024' }
);

// Multiple variations from the same image
const variations = await service.createVariations(
  'https://example.com/product.png',
  'Professional product photo',
  [
    'with blue background',
    'with wooden surface',
    'with dramatic lighting'
  ]
);

console.log('Edit history:', service.getEditHistory());
```

### Style Transfer and Transformation

```javascript
async function applyStyleTransfer(imageSource, content, style, outputPath, size = '1024x1024') {
  const prompt = `${content} transformed into ${style} style, maintain composition and subject`;

  const response = await editImageRequest(imageSource, prompt, size);

  const imageBase64 = response.data[0].b64_json ?? response.data[0].base64;
  const buffer = Buffer.from(imageBase64, 'base64');
  fs.writeFileSync(outputPath, buffer);

  return {
    path: outputPath,
    content: content,
    style: style
  };
}

// Usage - Apply different styles to the same image
await applyStyleTransfer(
  './portrait.jpg',
  'Portrait photograph',
  'oil painting',
  './portrait_oil.png'
);

await applyStyleTransfer(
  'https://example.com/city.jpg',
  'City landscape',
  'watercolor',
  './city_watercolor.png'
);

await applyStyleTransfer(
  './product.png',
  'Product photo',
  'minimalist illustration',
  './product_minimal.png'
);
```

### Element Replacement

```javascript
async function replaceElement(imageSource, baseScene, replaceWhat, replaceWith, outputPath, size = '1024x1024') {
  const prompt = `${baseScene}, replace ${replaceWhat} with ${replaceWith}, keep everything else identical`;

  const response = await editImageRequest(imageSource, prompt, size);

  const imageBase64 = response.data[0].b64_json ?? response.data[0].base64;
  const buffer = Buffer.from(imageBase64, 'base64');
  fs.writeFileSync(outputPath, buffer);

  return {
    path: outputPath,
    modification: `${replaceWhat} → ${replaceWith}`
  };
}

// Usage
await replaceElement(
  './workspace.jpg',
  'Office workspace with laptop',
  'laptop',
  'desktop computer with dual monitors',
  './workspace_desktop.png'
);

await replaceElement(
  'https://example.com/living-room.jpg',
  'Living room interior with sofa',
  'blue sofa',
  'brown leather sofa',
  './living_room_leather.png'
);
```

## Best Practices

### 1. Effective Edit Prompts

```javascript
function buildEditPrompt(baseDescription, modification, preserveElements = []) {
  const components = [
    baseDescription,
    modification
  ];

  if (preserveElements.length > 0) {
    components.push(`keep ${preserveElements.join(', ')} unchanged`);
  }

  components.push('maintain overall composition');

  return components.filter(Boolean).join(', ');
}

// Usage
const editPrompt = buildEditPrompt(
  'Professional headshot photo',
  'change background to modern office',
  ['lighting', 'pose', 'expression']
);

// Result: "Professional headshot photo, change background to modern office, keep lighting, pose, expression unchanged, maintain overall composition"
```

### 2. Size Selection for Different Edit Types

```javascript
function selectSizeForEdit(editType) {
  const sizeMap = {
    'background-change': '1440x720',
    'style-transfer': '1024x1024',
    'color-adjustment': '1024x1024',
    'element-replacement': '1344x768',
    'composition-change': '1152x864',
    'portrait-edit': '768x1344',
    'landscape-edit': '1344x768'
  };

  return sizeMap[editType] || '1024x1024';
}

// Usage
const size = selectSizeForEdit('background-change');
await editImage('Replace background with beach scene', './beach_bg.png', size);
```

### 3. Error Handling with Retry

```javascript
async function safeEditImage(imageSource, editPrompt, size, outputPath, retries = 3) {
  let lastError;

  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      const response = await editImageRequest(imageSource, editPrompt, size);

      const imageBase64 = response.data?.[0]?.b64_json ?? response.data?.[0]?.base64;
      if (!imageBase64) {
        throw new Error('Invalid response from image editing API');
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

## Common Image Editing Use Cases

1. **Background Replacement**: Change or remove backgrounds in photos
2. **Style Transformation**: Convert photos to paintings, illustrations, etc.
3. **Color Adjustment**: Change color schemes, saturation, mood
4. **Element Modification**: Replace or modify specific elements
5. **Composition Changes**: Adjust framing, orientation, layout
6. **Lighting Adjustments**: Modify lighting, shadows, highlights
7. **Asset Redesign**: Modernize or rebrand existing designs
8. **Quality Enhancement**: Improve overall visual quality
9. **Variation Creation**: Generate multiple versions of an image
10. **Format Conversion**: Transform between different styles or formats

## Integration Examples

### Express.js API Endpoint

```javascript
import express from 'express';
import fs from 'fs';
import path from 'path';

const app = express();
app.use(express.json());
app.use('/edited-images', express.static('edited-images'));

const outputDir = './edited-images';

async function init() {
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
}

app.post('/api/edit-image', async (req, res) => {
  try {
    const {
      imageSource,           // URL, data URL, or local path
      editPrompt,
      size = '1024x1024',
      baseDescription = ''
    } = req.body;

    if (!imageSource || !editPrompt) {
      return res.status(400).json({
        error: 'imageSource and editPrompt are required'
      });
    }

    // Combine base description with edit instruction
    const fullPrompt = baseDescription
      ? `${baseDescription}, ${editPrompt}`
      : editPrompt;

    const response = await editImageRequest(imageSource, fullPrompt, size);

    const imageBase64 = response.data[0].b64_json ?? response.data[0].base64;
    const buffer = Buffer.from(imageBase64, 'base64');

    const filename = `edited_${Date.now()}.png`;
    const filepath = path.join(outputDir, filename);
    fs.writeFileSync(filepath, buffer);

    res.json({
      success: true,
      imageUrl: `/edited-images/${filename}`,
      editPrompt: fullPrompt,
      size: size
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

app.post('/api/create-variations', async (req, res) => {
  try {
    const {
      imageSource,      // URL, data URL, or local path
      baseDescription,
      variations,
      size = '1024x1024'
    } = req.body;

    if (!imageSource || !baseDescription || !variations || !Array.isArray(variations)) {
      return res.status(400).json({
        error: 'imageSource, baseDescription and variations array are required'
      });
    }

    const results = [];

    for (const variation of variations) {
      const fullPrompt = `${baseDescription}, ${variation}`;

      const response = await editImageRequest(imageSource, fullPrompt, size);

      const imageBase64 = response.data[0].b64_json ?? response.data[0].base64;
      const buffer = Buffer.from(imageBase64, 'base64');

      const filename = `variation_${Date.now()}_${Math.random().toString(36).substr(2, 9)}.png`;
      const filepath = path.join(outputDir, filename);
      fs.writeFileSync(filepath, buffer);

      results.push({
        variation: variation,
        imageUrl: `/edited-images/${filename}`
      });
    }

    res.json({
      success: true,
      results: results
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
    console.log('Image editing API running on port 3000');
  });
});
```

## CLI Integration in Scripts

### Shell Script for Batch Editing

```bash
#!/bin/bash

# Batch edit images with different styles
echo "Creating style variations..."

ORIGINAL_IMAGE="./product.jpg"
BASE="Professional product photo of laptop"
SIZES_MODEL="${IMAGE_EDIT_MODEL:-stable-diffusion-xl}"

edit_variant() {
  curl -s "$LLM_BASE_URL/images/edits" \
    -F image=@"$ORIGINAL_IMAGE" \
    -F prompt="$1" \
    -F model="$SIZES_MODEL" \
    -F size="${3:-1024x1024}" \
    -F response_format=b64_json \
    | jq -r '.data[0].b64_json' | base64 -d > "$2"
}

edit_variant "$BASE, modern minimalist style, white background" "./variations/minimal.png"
edit_variant "$BASE, dramatic lighting, dark background" "./variations/dramatic.png"
edit_variant "$BASE, on wooden desk, natural lighting" "./variations/natural.png"

echo "Variations created successfully!"
```

## Troubleshooting

**Issue**: "API key must be kept server-side"
- **Solution**: Read `LLM_API_KEY` from environment variables and only use it in server-side code

**Issue**: Invalid size parameter
- **Solution**: Use only sizes supported by your server, e.g. 1024x1024, 768x1344, 864x1152, 1344x768, 1152x864, 1440x720, 720x1440

**Issue**: Edited image doesn't match intention
- **Solution**: Be more specific in edit prompts. Include what to change AND what to preserve

**Issue**: 404 or 405 on `/images/edits`
- **Solution**: Your server does not implement the OpenAI images-edit route. Point `LLM_BASE_URL` at a gateway or image server that does

**Issue**: Image quality loss after editing
- **Solution**: Use larger size options and include quality terms in prompts

**Issue**: Inconsistent results across variations
- **Solution**: Include more specific base description and detailed modification instructions

## Edit Prompt Engineering Tips

### Good Edit Prompts
- ✓ "Change background to modern office, keep subject and lighting identical"
- ✓ "Transform to watercolor style, maintain composition and colors"
- ✓ "Replace red car with blue motorcycle, keep road and scenery unchanged"
- ✓ "Adjust to golden hour lighting, preserve all elements"

### Poor Edit Prompts
- ✗ "make it better"
- ✗ "change something"
- ✗ "different version"

### Edit Prompt Components
1. **Base Context**: What the image currently represents
2. **Modification**: What specific changes to make
3. **Preservation**: What elements to keep unchanged
4. **Quality**: Desired output quality or style

### Effective Edit Patterns

**Background Changes:**
```
"[Subject description], replace background with [new background], maintain subject lighting and pose"
```

**Style Transfers:**
```
"[Current description] transformed into [style name] style, preserve composition and key elements"
```

**Element Replacement:**
```
"[Scene description], replace [element A] with [element B], keep everything else identical"
```

**Color Adjustments:**
```
"[Image description], change color scheme to [colors], maintain contrast and composition"
```

## Supported Image Sizes

- `1024x1024` - Square (Best for general editing)
- `768x1344` - Portrait
- `864x1152` - Portrait
- `1344x768` - Landscape
- `1152x864` - Landscape
- `1440x720` - Wide landscape
- `720x1440` - Tall portrait

(Size availability is server-dependent; the list above reflects the most common convention.)

## Remember

- Works with any OpenAI-compatible server exposing `POST /images/edits` (hosted OpenAI-compatible APIs, gateways fronting editable diffusion models)
- Designed for the DiveeOI agent (OpenCode-based)
- Configuration via environment variables: `LLM_BASE_URL`, `LLM_API_KEY`, `IMAGE_EDIT_MODEL`
- The source image is uploaded as multipart form data (`image` field); the edit instruction goes in the `prompt` field
- The response contains the edited image as base64 (`data[0].b64_json`, or `data[0].base64` on some servers)
- Keep your API key in server-side code only
- Be specific about what to change AND what to preserve
- Include base description for better context
- Use appropriate size for the edit type
- Implement retry logic for production applications
- Test edit prompts iteratively for best results
- Consider creating variations to explore options
- Base64 images need to be decoded before saving
