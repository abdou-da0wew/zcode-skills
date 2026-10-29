---
name: VLM
description: Implement vision-based AI chat capabilities against any OpenAI-compatible server using plain HTTP calls. Use this skill when the user needs to analyze images, describe visual content, or create applications that combine image understanding with conversational AI. Supports image URLs and base64 encoded images for multimodal interactions. Works with any OpenAI-compatible LLM server (open-source or free), designed for the DiveeOI agent (OpenCode-based).
license: MIT
---

# VLM(Vision Chat) Skill

This skill guides the implementation of vision chat functionality using plain OpenAI-compatible HTTP calls (no SDK, no extra dependencies), enabling AI models to understand and respond to images combined with text prompts.

It works with any OpenAI-compatible LLM server (open-source or free) — Ollama, vLLM, LM Studio, OpenRouter, and most gateways — provided the configured model is vision-capable (e.g. `qwen2.5-vl`, `llama3.2-vision`, `minicpm-v`). Designed for the DiveeOI agent (OpenCode-based).

## Skills Path

**Skill Location**: `{project_path}/skills/VLM`

this skill is located at above path in your project.

**Reference Scripts**: Example test scripts are available in the `{Skill Location}/scripts/` directory for quick testing and reference. See `{Skill Location}/scripts/vlm.ts` for a working example.

## Overview

Vision Chat allows you to build applications that can analyze images, extract information from visual content, and answer questions about images through natural language conversation.

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

For simple image analysis tasks, you can use `curl` instead of writing code. This is ideal for quick image descriptions, testing vision capabilities, or simple automation.

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

### Multiple Images

```bash
# Analyze multiple images at once (multiple content parts)
curl -s "$LLM_BASE_URL/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5-vl",
    "messages": [{
      "role": "user",
      "content": [
        {"type": "text", "text": "Compare these two images"},
        {"type": "image_url", "image_url": {"url": "https://example.com/before.jpg"}},
        {"type": "image_url", "image_url": {"url": "https://example.com/after.jpg"}}
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

- PNG (.png)
- JPEG (.jpg, .jpeg)
- GIF (.gif)
- WebP (.webp)
- BMP (.bmp)

### When to Use CLI vs Code

**Use curl for:**
- Quick image analysis
- Testing vision model capabilities
- One-off image descriptions
- Simple automation scripts

**Use code for:**
- Multi-turn conversations with images
- Dynamic image analysis in applications
- Batch processing with custom logic
- Production applications with complex workflows

## Recommended Approach

For better performance and reliability, use base64 encoding to pass images to the model instead of image URLs.

## Supported Content Types

The vision chat API accepts multimodal content parts. Three part types are commonly seen in the ecosystem:

### 1. **image_url** - For Image Files
Use this type for static images (PNG, JPEG, GIF, WebP, etc.). Universally supported by vision servers.
```typescript
{
    role: 'user',
    content: [
        { type: 'text', text: prompt },
        { type: 'image_url', image_url: { url: imageUrl } }
    ]
}
```

### 2. **video_url** - For Video Files
Use this type for video content (MP4, AVI, MOV, etc.). Support depends on the server/model (video VLMs such as Qwen-VL-Video style deployments).
```typescript
{
    role: 'user',
    content: [
        { type: 'text', text: prompt },
        { type: 'video_url', video_url: { url: videoUrl } }
    ]
}
```

### 3. **file_url** - For Document Files
Use this type for document files (PDF, DOCX, TXT, etc.). Support depends on the server; many deployments only accept `image_url` and `text`.
```typescript
{
    role: 'user',
    content: [
        { type: 'text', text: prompt },
        { type: 'file_url', file_url: { url: fileUrl } }
    ]
}
```

**Note**: You can combine multiple content types in a single message. For example, you can include both text and multiple images, or text with both an image and a document.

## Basic Vision Chat Implementation

### Single Image Analysis

```javascript
async function analyzeImage(imageUrl, question) {
  const response = await chatCompletions({
    model: MODEL,
    messages: [
      {
        role: 'user',
        content: [
          {
            type: 'text',
            text: question
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

// Usage
const result = await analyzeImage(
  'https://example.com/product.jpg',
  'Describe this product in detail'
);
console.log('Analysis:', result);
```

### Multiple Images Analysis

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
  'Compare these two images and describe the differences'
);
```

### Base64 Image Support

```javascript
import fs from 'fs';

async function analyzeLocalImage(imagePath, question) {
  // Read image file and convert to base64
  const imageBuffer = fs.readFileSync(imagePath);
  const base64Image = imageBuffer.toString('base64');
  const mimeType = imagePath.endsWith('.png') ? 'image/png' : 'image/jpeg';

  const response = await chatCompletions({
    model: MODEL,
    messages: [
      {
        role: 'user',
        content: [
          {
            type: 'text',
            text: question
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
```

## Advanced Use Cases

### Conversational Vision Chat

```javascript
class VisionChatSession {
  constructor() {
    this.messages = [];
  }

  async addImage(imageUrl, initialQuestion) {
    this.messages.push({
      role: 'user',
      content: [
        {
          type: 'text',
          text: initialQuestion
        },
        {
          type: 'image_url',
          image_url: { url: imageUrl }
        }
      ]
    });

    return this.getResponse();
  }

  async followUp(question) {
    this.messages.push({
      role: 'user',
      content: [
        {
          type: 'text',
          text: question
        }
      ]
    });

    return this.getResponse();
  }

  async getResponse() {
    const response = await chatCompletions({
      model: MODEL,
      messages: this.messages
    });

    const assistantMessage = response.choices[0]?.message?.content;

    this.messages.push({
      role: 'assistant',
      content: assistantMessage
    });

    return assistantMessage;
  }
}

// Usage
const session = new VisionChatSession();

const initial = await session.addImage(
  'https://example.com/chart.jpg',
  'What does this chart show?'
);
console.log('Initial analysis:', initial);

const followup = await session.followUp('What are the key trends?');
console.log('Follow-up:', followup);
```

### Image Classification and Tagging

```javascript
async function classifyImage(imageUrl) {
  const prompt = `Analyze this image and provide:
1. Main subject/category
2. Key objects detected
3. Scene description
4. Suggested tags (comma-separated)

Format your response as JSON.`;

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
            image_url: { url: imageUrl }
          }
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
```

### OCR and Text Extraction

```javascript
async function extractText(imageUrl) {
  const response = await chatCompletions({
    model: MODEL,
    messages: [
      {
        role: 'user',
        content: [
          {
            type: 'text',
            text: 'Extract all text from this image. Preserve the layout and formatting as much as possible.'
          },
          {
            type: 'image_url',
            image_url: { url: imageUrl }
          }
        ]
      }
    ]
  });

  return response.choices[0]?.message?.content;
}
```

## Best Practices

### 1. Image Quality and Size
- Use high-quality images for better analysis results
- Optimize image size to balance quality and processing speed
- Supported formats: JPEG, PNG, WebP

### 2. Prompt Engineering
- Be specific about what information you need from the image
- Structure complex requests with numbered lists or bullet points
- Provide context about the image type (photo, diagram, chart, etc.)

### 3. Error Handling
```javascript
async function safeVisionChat(imageUrl, question) {
  try {
    const response = await chatCompletions({
      model: MODEL,
      messages: [
        {
          role: 'user',
          content: [
            { type: 'text', text: question },
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
    console.error('Vision chat error:', error);
    return {
      success: false,
      error: error.message
    };
  }
}
```

### 4. Performance Optimization
- Reuse HTTP connections when processing multiple images
- Use appropriate image formats (JPEG for photos, PNG for diagrams)
- Consider image preprocessing for large batches

### 5. Security Considerations
- Validate image URLs before processing
- Sanitize user-provided image data
- Implement rate limiting for public-facing APIs
- Never expose API keys in client-side code

## Common Use Cases

1. **Product Analysis**: Analyze product images for e-commerce applications
2. **Document Understanding**: Extract information from receipts, invoices, forms
3. **Medical Imaging**: Assist in preliminary analysis (with appropriate disclaimers)
4. **Quality Control**: Detect defects or anomalies in manufacturing
5. **Content Moderation**: Analyze images for policy compliance
6. **Accessibility**: Generate alt text for images automatically
7. **Visual Search**: Understand and categorize images for search functionality

## Integration Examples

### Express.js API Endpoint

```javascript
import express from 'express';

const app = express();
app.use(express.json());

app.post('/api/analyze-image', async (req, res) => {
  try {
    const { imageUrl, question } = req.body;

    if (!imageUrl || !question) {
      return res.status(400).json({
        error: 'imageUrl and question are required'
      });
    }

    const response = await chatCompletions({
      model: MODEL,
      messages: [
        {
          role: 'user',
          content: [
            { type: 'text', text: question },
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

app.listen(3000, () => {
  console.log('Vision chat API running on port 3000');
});
```

## Troubleshooting

**Issue**: "API key must be kept server-side"
- **Solution**: Read `LLM_API_KEY` from environment variables and only use it in server-side code

**Issue**: Image not loading or being analyzed
- **Solution**: Verify the image URL is accessible and returns a valid image format; for local files prefer base64 data URLs

**Issue**: "Model does not support image input"
- **Solution**: Point `LLM_MODEL` at a vision-capable model (e.g. `qwen2.5-vl`, `llama3.2-vision`, `minicpm-v`)

**Issue**: Poor analysis quality
- **Solution**: Provide more specific prompts and ensure image quality is sufficient

**Issue**: Slow response times
- **Solution**: Optimize image size and consider caching frequently analyzed images

## Remember

- Works with any OpenAI-compatible LLM server (open-source or free) — Ollama, vLLM, LM Studio, OpenRouter, and more
- Designed for the DiveeOI agent (OpenCode-based)
- The configured model must be vision-capable (`LLM_MODEL`)
- Vision requests are plain `chat/completions` calls with `image_url` content parts; base64 data URLs (`data:<mime>;base64,...`) are the most reliable input
- `video_url` and `file_url` content parts exist in the ecosystem but support depends on the server
- Structure prompts clearly for best results
- Handle errors gracefully in production applications
- Consider user privacy when processing images
