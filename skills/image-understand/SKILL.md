---
name: image-understand
description: Implement specialized image understanding capabilities using any OpenAI-compatible server via plain HTTP calls. Use this skill when the user needs to analyze static images, extract visual information, perform OCR, detect objects, classify images, or understand visual content. Optimized for PNG, JPEG, GIF, WebP, and BMP formats. Works with any OpenAI-compatible LLM server (open-source or free), designed for the DiveeOI agent (OpenCode-based).
license: MIT
---

# Image Understanding Skill

This skill provides specialized image understanding functionality using plain OpenAI-compatible HTTP calls (no SDK, no extra dependencies), enabling AI models to analyze, describe, and extract information from static images.

It works with any OpenAI-compatible LLM server (open-source or free) — Ollama, vLLM, LM Studio, OpenRouter, and most gateways — provided the configured model is vision-capable. Designed for the DiveeOI agent (OpenCode-based).

## Skills Path

**Skill Location**: `{project_path}/skills/image-understand`

this skill is located at above path in your project.

**Reference Scripts**: Example test scripts are available in the `{Skill Location}/scripts/` directory for quick testing and reference. See `{Skill Location}/scripts/image-understand.ts` for a working example.

## Overview

Image Understanding focuses specifically on static image analysis, providing capabilities for:
- Image description and scene understanding
- Object detection and recognition
- OCR (Optical Character Recognition) and text extraction
- Image classification and categorization
- Visual content analysis
- Quality assessment
- Accessibility (alt text generation)

**IMPORTANT**: Keep your API key in backend code or environment variables only. Never hardcode credentials in client-side code.

## Prerequisites

- Node.js 18+ (for the global `fetch` API) or any HTTP client
- An OpenAI-compatible server with a **vision-capable** model installed
- No npm packages required — examples use built-in APIs only

## Configuration (Environment Variables)

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_BASE_URL` | `http://localhost:11434/v1` | OpenAI-compatible base URL |
| `LLM_API_KEY` | (empty) | API key sent as `Authorization: Bearer <key>`; leave empty for local servers |
| `LLM_MODEL` | `qwen2.5` | **Vision-capable** model name (e.g. `qwen2.5-vl`, `llama3.2-vision`, `minicpm-v`) |

### Shared Client Helper

All examples below use this helper (plain `fetch`, zero dependencies):

```javascript
const BASE_URL = process.env.LLM_BASE_URL ?? "http://localhost:11434/v1";
const API_KEY = process.env.LLM_API_KEY ?? "";
const MODEL = process.env.LLM_MODEL ?? "qwen2.5";

async function chatCompletions(body) {
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
```

## CLI Usage (For Simple Tasks)

For quick image analysis tasks, you can use `curl` instead of writing code. This is ideal for simple image descriptions, testing, or automation.

### Basic Image Analysis

```bash
# Describe an image from URL
curl -s "$LLM_BASE_URL/chat/completions" \
  -H "Content-Type: application/json" \
  ${LLM_API_KEY:+-H "Authorization: Bearer $LLM_API_KEY"} \
  -d '{
    "model": "qwen2.5-vl",
    "messages": [{
      "role": "user",
      "content": [
        {"type": "text", "text": "What'"'"'s in this image?"},
        {"type": "image_url", "image_url": {"url": "https://example.com/photo.jpg"}}
      ]
    }]
  }'
```

### Analyze Local Images

```bash
# Analyze a local image file: encode it to a base64 data URL first
B64=$(base64 -w0 ./photo.jpg)
curl -s "$LLM_BASE_URL/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5-vl",
    "messages": [{
      "role": "user",
      "content": [
        {"type": "text", "text": "What objects are in this photo?"},
        {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,'"$B64"'"}}
      ]
    }]
  }' -o description.json
```

### Multiple Images Comparison

```bash
# Compare multiple images
curl -s "$LLM_BASE_URL/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5-vl",
    "messages": [{
      "role": "user",
      "content": [
        {"type": "text", "text": "Compare these two images and highlight the differences"},
        {"type": "image_url", "image_url": {"url": "https://example.com/photo1.jpg"}},
        {"type": "image_url", "image_url": {"url": "https://example.com/photo2.jpg"}}
      ]
    }]
  }' -o comparison.json
```

### CLI Parameters

- Request body fields follow the standard OpenAI Chat Completions schema:
  - `model`: **Required** - Vision-capable model name
  - `messages`: **Required** - Array of messages; multimodal messages use content parts (`text`, `image_url`)
  - `temperature`, `max_tokens`: Optional - Sampling controls
  - `stream`: Optional - Stream the response in real-time

### Supported Image Formats

- PNG (.png) - Best for diagrams, screenshots, graphics with transparency
- JPEG (.jpg, .jpeg) - Best for photos and complex images
- GIF (.gif) - Supports both static and animated images
- WebP (.webp) - Modern format with good compression
- BMP (.bmp) - Uncompressed bitmap format

### When to Use CLI vs Code

**Use curl for:**
- Quick image analysis or descriptions
- One-off OCR tasks
- Testing image understanding capabilities
- Simple batch processing scripts
- Generating alt text for accessibility

**Use code for:**
- Multi-turn conversations about images
- Complex image processing pipelines
- Production applications with error handling
- Custom integration with your application logic
- Batch processing with custom business logic

## Recommended Approach

For better performance and reliability, use base64 encoding to pass images to the model instead of image URLs.

## Basic Image Understanding Implementation

### Single Image Analysis

```javascript
async function analyzeImage(imageUrl, prompt) {
  const response = await chatCompletions({
    model: MODEL,
    messages: [
      {
        role: 'user',
        content: [
          {
            type: 'text',
            text: prompt
          },
          {
            type: 'image_url',
            image_url: {
              url: imageUrl
            }
          }
        ]
      }
    ]
  });

  return response.choices[0]?.message?.content;
}

// Usage examples
const description = await analyzeImage(
  'https://example.com/landscape.jpg',
  'Describe this landscape in detail, including colors, lighting, and mood'
);

const objectDetection = await analyzeImage(
  'https://example.com/room.jpg',
  'List all objects visible in this room'
);
```

### Multiple Images Comparison

```javascript
async function compareImages(imageUrls, question) {
  const content = [
    {
      type: 'text',
      text: question
    },
    ...imageUrls.map(url => ({
      type: 'image_url',
      image_url: { url }
    }))
  ];

  const response = await chatCompletions({
    model: MODEL,
    messages: [
      {
        role: 'user',
        content: content
      }
    ]
  });

  return response.choices[0]?.message?.content;
}

// Usage
const comparison = await compareImages(
  [
    'https://example.com/before.jpg',
    'https://example.com/after.jpg'
  ],
  'What are the key differences between these before and after images?'
);
```

### Base64 Image Support (Recommended)

```javascript
import fs from 'fs';
import path from 'path';

async function analyzeLocalImage(imagePath, prompt) {
  // Read image file and convert to base64
  const imageBuffer = fs.readFileSync(imagePath);
  const base64Image = imageBuffer.toString('base64');

  // Determine MIME type based on file extension
  const ext = path.extname(imagePath).toLowerCase();
  const mimeTypes = {
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.webp': 'image/webp',
    '.bmp': 'image/bmp'
  };
  const mimeType = mimeTypes[ext] || 'image/jpeg';

  const response = await chatCompletions({
    model: MODEL,
    messages: [
      {
        role: 'user',
        content: [
          {
            type: 'text',
            text: prompt
          },
          {
            type: 'image_url',
            image_url: {
              url: `data:${mimeType};base64,${base64Image}`
            }
          }
        ]
      }
    ]
  });

  return response.choices[0]?.message?.content;
}

// Usage
const result = await analyzeLocalImage(
  './product-photo.jpg',
  'Analyze this product image for e-commerce listing'
);
```

## Advanced Use Cases

### OCR and Text Extraction

```javascript
async function extractText(imageUrl, options = {}) {
  const prompt = options.preserveLayout
    ? 'Extract all text from this image. Preserve the exact layout, formatting, and structure.'
    : 'Extract all visible text from this image.';

  const response = await chatCompletions({
    model: MODEL,
    messages: [
      {
        role: 'user',
        content: [
          { type: 'text', text: prompt },
          { type: 'image_url', image_url: { url: imageUrl } }
        ]
      }
    ]
  });

  return response.choices[0]?.message?.content;
}

// Usage examples
const receiptText = await extractText(
  'https://example.com/receipt.jpg',
  { preserveLayout: true }
);

const businessCardInfo = await extractText(
  'https://example.com/business-card.jpg'
);
```

### Object Detection and Counting

```javascript
async function detectObjects(imageUrl, objectType) {
  const prompt = objectType
    ? `Count and locate all ${objectType} in this image. Provide their positions and describe each one.`
    : 'Detect and list all objects in this image with their approximate locations.';

  const response = await chatCompletions({
    model: MODEL,
    messages: [
      {
        role: 'user',
        content: [
          { type: 'text', text: prompt },
          { type: 'image_url', image_url: { url: imageUrl } }
        ]
      }
    ]
  });

  return response.choices[0]?.message?.content;
}

// Usage
const peopleCount = await detectObjects(
  'https://example.com/crowd.jpg',
  'people'
);

const allObjects = await detectObjects(
  'https://example.com/room.jpg'
);
```

### Image Classification and Tagging

```javascript
async function classifyAndTag(imageUrl) {
  const prompt = `Analyze this image and provide a comprehensive classification:
1. Primary category (e.g., nature, urban, portrait, product)
2. Subject matter (main focus of the image)
3. Style or mood (e.g., professional, casual, artistic, vintage)
4. Color palette description
5. Suggested tags (10-15 keywords, comma-separated)

Format your response as structured JSON.`;

  const response = await chatCompletions({
    model: MODEL,
    messages: [
      {
        role: 'user',
        content: [
          { type: 'text', text: prompt },
          { type: 'image_url', image_url: { url: imageUrl } }
        ]
      }
    ]
  });

  const content = response.choices[0]?.message?.content;

  try {
    return JSON.parse(content);
  } catch (e) {
    return { rawResponse: content };
  }
}

// Usage
const classification = await classifyAndTag(
  'https://example.com/photo.jpg'
);
console.log('Tags:', classification.tags);
```

### Quality Assessment

```javascript
async function assessImageQuality(imageUrl) {
  const prompt = `Assess the technical quality of this image:
1. Sharpness and focus (1-10)
2. Exposure and brightness (1-10)
3. Color balance (1-10)
4. Composition (1-10)
5. Any technical issues (blur, noise, artifacts, etc.)
6. Overall quality rating (1-10)
7. Suggestions for improvement

Provide specific feedback for each criterion.`;

  const response = await chatCompletions({
    model: MODEL,
    messages: [
      {
        role: 'user',
        content: [
          { type: 'text', text: prompt },
          { type: 'image_url', image_url: { url: imageUrl } }
        ]
      }
    ]
  });

  return response.choices[0]?.message?.content;
}
```

### Accessibility - Alt Text Generation

```javascript
async function generateAltText(imageUrl, context = '') {
  const prompt = context
    ? `Generate concise, descriptive alt text for this image. Context: ${context}. Focus on the most important visual elements that convey the image's purpose.`
    : 'Generate concise, descriptive alt text for this image suitable for screen readers. Focus on key visual elements.';

  const response = await chatCompletions({
    model: MODEL,
    messages: [
      {
        role: 'user',
        content: [
          { type: 'text', text: prompt },
          { type: 'image_url', image_url: { url: imageUrl } }
        ]
      }
    ]
  });

  return response.choices[0]?.message?.content;
}

// Usage
const altText = await generateAltText(
  'https://example.com/hero-image.jpg',
  'Website hero section for a tech startup'
);
```

### Scene Understanding

```javascript
async function understandScene(imageUrl) {
  const prompt = `Provide a comprehensive scene analysis:
1. Setting/location type (indoor/outdoor, specific place)
2. Time of day and lighting conditions
3. Weather (if applicable)
4. People present (number, activities, interactions)
5. Key objects and their arrangement
6. Overall atmosphere and mood
7. Notable details or interesting elements`;

  const response = await chatCompletions({
    model: MODEL,
    messages: [
      {
        role: 'user',
        content: [
          { type: 'text', text: prompt },
          { type: 'image_url', image_url: { url: imageUrl } }
        ]
      }
    ]
  });

  return response.choices[0]?.message?.content;
}
```

## Batch Processing

### Process Multiple Images

```javascript
class ImageBatchProcessor {
  async processImage(imageUrl, prompt) {
    const response = await chatCompletions({
      model: MODEL,
      messages: [
        {
          role: 'user',
          content: [
            { type: 'text', text: prompt },
            { type: 'image_url', image_url: { url: imageUrl } }
          ]
        }
      ]
    });

    return response.choices[0]?.message?.content;
  }

  async processBatch(imageUrls, prompt) {
    const results = [];

    for (const imageUrl of imageUrls) {
      try {
        const result = await this.processImage(imageUrl, prompt);
        results.push({ imageUrl, success: true, result });
      } catch (error) {
        results.push({
          imageUrl,
          success: false,
          error: error.message
        });
      }
    }

    return results;
  }
}

// Usage
const processor = new ImageBatchProcessor();

const images = [
  'https://example.com/img1.jpg',
  'https://example.com/img2.jpg',
  'https://example.com/img3.jpg'
];

const results = await processor.processBatch(
  images,
  'Generate a short description suitable for social media'
);
```

## Best Practices

### 1. Image Quality and Preparation
- Use high-resolution images for better analysis accuracy
- Ensure images are well-lit and properly exposed
- For OCR, ensure text is clear and readable
- Optimize file size to balance quality and performance
- Supported formats: PNG (best for text/diagrams), JPEG (best for photos), WebP, GIF, BMP

### 2. Prompt Engineering for Images
- Be specific about what information you need
- Mention the type of image (photo, diagram, screenshot, etc.)
- For complex tasks, break down into specific questions
- Use structured prompts for JSON output
- Include context when relevant

### 3. Error Handling

```javascript
async function safeImageAnalysis(imageUrl, prompt) {
  try {
    const response = await chatCompletions({
      model: MODEL,
      messages: [
        {
          role: 'user',
          content: [
            { type: 'text', text: prompt },
            { type: 'image_url', image_url: { url: imageUrl } }
          ]
        }
      ]
    });

    return {
      success: true,
      content: response.choices[0]?.message?.content
    };
  } catch (error) {
    console.error('Image analysis error:', error);
    return {
      success: false,
      error: error.message
    };
  }
}
```

### 4. Performance Optimization
- Reuse HTTP connections for batch processing
- Use base64 encoding for local images
- Implement request throttling for large batches
- Consider image preprocessing (resize, compress) for large files

### 5. Security Considerations
- Validate image URLs before processing
- Implement rate limiting for public APIs
- Sanitize user-provided image data
- Never expose API keys in client-side code
- Implement content moderation for user-uploaded images

## Common Use Cases

1. **E-commerce Product Analysis**: Analyze product images, extract features, generate descriptions
2. **Document Processing**: Extract text from receipts, invoices, forms, business cards
3. **Content Moderation**: Detect inappropriate content, verify image compliance
4. **Quality Control**: Identify defects, assess product quality in manufacturing
5. **Accessibility**: Generate alt text for images automatically
6. **Image Cataloging**: Auto-tag and categorize image libraries
7. **Visual Search**: Understand and index images for search functionality
8. **Medical Imaging**: Preliminary analysis with appropriate disclaimers
9. **Real Estate**: Analyze property photos, extract features
10. **Social Media**: Generate captions, hashtags, and descriptions

## Integration Examples

### Express.js API Endpoint

```javascript
import express from 'express';
import multer from 'multer';

const app = express();
const upload = multer({ storage: multer.memoryStorage() });

// Analyze image from URL
app.post('/api/analyze-image', express.json(), async (req, res) => {
  try {
    const { imageUrl, prompt } = req.body;

    if (!imageUrl || !prompt) {
      return res.status(400).json({
        error: 'imageUrl and prompt are required'
      });
    }

    const response = await chatCompletions({
      model: MODEL,
      messages: [
        {
          role: 'user',
          content: [
            { type: 'text', text: prompt },
            { type: 'image_url', image_url: { url: imageUrl } }
          ]
        }
      ]
    });

    res.json({
      success: true,
      analysis: response.choices[0]?.message?.content
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Analyze uploaded image file
app.post('/api/analyze-upload', upload.single('image'), async (req, res) => {
  try {
    const { prompt } = req.body;
    const imageFile = req.file;

    if (!imageFile || !prompt) {
      return res.status(400).json({
        error: 'image file and prompt are required'
      });
    }

    // Convert to base64
    const base64Image = imageFile.buffer.toString('base64');
    const mimeType = imageFile.mimetype;

    const response = await chatCompletions({
      model: MODEL,
      messages: [
        {
          role: 'user',
          content: [
            { type: 'text', text: prompt },
            {
              type: 'image_url',
              image_url: {
                url: `data:${mimeType};base64,${base64Image}`
              }
            }
          ]
        }
      ]
    });

    res.json({
      success: true,
      analysis: response.choices[0]?.message?.content
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

app.listen(3000, () => {
  console.log('Image understanding API running on port 3000');
});
```

### Next.js API Route

```javascript
// pages/api/image-understand.js

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { imageUrl, prompt } = req.body;

    if (!imageUrl || !prompt) {
      return res.status(400).json({
        error: 'imageUrl and prompt are required'
      });
    }

    const response = await chatCompletions({
      model: process.env.LLM_MODEL ?? 'qwen2.5',
      messages: [
        {
          role: 'user',
          content: [
            { type: 'text', text: prompt },
            { type: 'image_url', image_url: { url: imageUrl } }
          ]
        }
      ]
    });

    res.status(200).json({
      success: true,
      analysis: response.choices[0]?.message?.content
    });
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
}
```

## Troubleshooting

**Issue**: "API key must be kept server-side"
- **Solution**: Read `LLM_API_KEY` from environment variables in server-side code only, never in client/browser code

**Issue**: Image not loading or being analyzed
- **Solution**: Verify the image URL is accessible, returns correct MIME type, and is in a supported format

**Issue**: "Model does not support image input"
- **Solution**: Point `LLM_MODEL` at a vision-capable model (e.g. `qwen2.5-vl`, `llama3.2-vision`, `minicpm-v`)

**Issue**: Poor OCR accuracy
- **Solution**: Ensure text is clear and readable, increase image resolution, ensure proper lighting and contrast

**Issue**: Inaccurate object detection or counting
- **Solution**: Use high-resolution images, provide specific prompts, break the task into steps

**Issue**: Slow response times
- **Solution**: Optimize image size (resize before upload), use base64 for local images, reuse HTTP connections for batch processing

**Issue**: Base64 encoding fails
- **Solution**: Verify file path is correct, check file permissions, ensure MIME type matches file extension

## Remember

- Works with any OpenAI-compatible LLM server (open-source or free) — Ollama, vLLM, LM Studio, OpenRouter, and more
- Designed for the DiveeOI agent (OpenCode-based)
- Configuration via environment variables: `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL` (must be a vision-capable model)
- Vision requests are plain `chat/completions` calls with `image_url` content parts
- Base64 encoding is recommended for better performance
- Structure prompts clearly for best results
- For complex counting and detailed analysis, ask the model to reason step by step in the prompt
- Handle errors gracefully in production
- Validate and sanitize user inputs
- Consider privacy and security when processing user images
