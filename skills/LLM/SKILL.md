---
name: LLM
description: Implement large language model (LLM) chat completions against any OpenAI-compatible server using plain HTTP calls. Use this skill when the user needs to build conversational AI applications, chatbots, AI assistants, or any text generation features. Supports multi-turn conversations, system prompts, and context management. Works with any OpenAI-compatible LLM server (open-source or free), designed for the DiveeOI agent (OpenCode-based).
license: MIT
---

# LLM (Large Language Model) Skill

This skill guides the implementation of chat completions functionality using plain OpenAI-compatible HTTP calls (no SDK, no extra dependencies), enabling powerful conversational AI and text generation capabilities.

It works with any OpenAI-compatible LLM server (open-source or free) — Ollama, vLLM, LM Studio, OpenRouter, llama.cpp server, and most API gateways — and is designed for the DiveeOI agent (OpenCode-based).

## Skills Path

**Skill Location**: `{project_path}/skills/LLM`

this skill is located at above path in your project.

**Reference Scripts**: Example test scripts are available in the `{Skill Location}/scripts/` directory for quick testing and reference. See `{Skill Location}/scripts/chat.ts` for a working example.

## Overview

The LLM skill allows you to build applications that leverage large language models for natural language understanding and generation, including chatbots, AI assistants, content generation, and more.

**IMPORTANT**: Keep your API key in backend code or environment variables only. Never hardcode credentials in client-side code.

## Prerequisites

- Node.js 18+ (for the global `fetch` API) or any HTTP client
- An OpenAI-compatible LLM server reachable at `LLM_BASE_URL`
- No npm packages required — examples use the built-in `fetch`

## Configuration (Environment Variables)

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_BASE_URL` | `http://localhost:11434/v1` | OpenAI-compatible base URL (Ollama: `http://localhost:11434/v1`, vLLM: `http://host:8000/v1`, LM Studio: `http://localhost:1234/v1`, OpenRouter: `https://openrouter.ai/api/v1`) |
| `LLM_API_KEY` | (empty) | API key sent as `Authorization: Bearer <key>`; leave empty for local servers |
| `LLM_MODEL` | `qwen2.5` | Model name, e.g. `qwen2.5`, `llama3.1`, `deepseek-r1`, `mistral` |

### Shared Client Helper

All examples below use this tiny helper (plain `fetch`, zero dependencies):

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

For simple, one-off chat completions, you can use `curl` instead of writing code. This is ideal for quick tests, simple queries, or automation scripts.

### Basic Chat

```bash
# Simple question
curl -s "$LLM_BASE_URL/chat/completions" \
  -H "Content-Type: application/json" \
  ${LLM_API_KEY:+-H "Authorization: Bearer $LLM_API_KEY"} \
  -d '{"model": "qwen2.5", "messages": [{"role": "user", "content": "What is the capital of France?"}]}'

# Save response to file
curl -s "$LLM_BASE_URL/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{"model": "qwen2.5", "messages": [{"role": "user", "content": "Explain quantum computing"}]}' \
  -o response.json
```

### With System Prompt

```bash
# Custom system prompt for specific behavior
curl -s "$LLM_BASE_URL/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5",
    "messages": [
      {"role": "system", "content": "You are an expert code reviewer"},
      {"role": "user", "content": "Review this code: function add(a,b) { return a+b; }"}
    ]
  }' -o review.json
```

### With Streaming

```bash
# Stream tokens as they are generated
curl -s "$LLM_BASE_URL/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{"model": "qwen2.5", "messages": [{"role": "user", "content": "Write a short poem"}], "stream": true}'
```

### CLI Parameters

- Request body fields follow the standard OpenAI Chat Completions schema:
  - `model`: **Required** - Model name (e.g. `qwen2.5`)
  - `messages`: **Required** - Array of `{role, content}` messages
  - `temperature`, `top_p`, `max_tokens`: Optional - Sampling controls
  - `stream`: Optional - Stream the response in real-time

### When to Use CLI vs Code

**Use curl for:**
- Quick one-off questions
- Simple automation scripts
- Testing prompts
- Single-turn conversations

**Use code for:**
- Multi-turn conversations with context
- Custom conversation management
- Integration with web applications
- Complex chat workflows
- Production applications

## Basic Chat Completions

### Simple Question and Answer

```javascript
async function askQuestion(question) {
  const completion = await chatCompletions({
    model: MODEL,
    messages: [
      {
        role: 'system',
        content: 'You are a helpful assistant.'
      },
      {
        role: 'user',
        content: question
      }
    ]
  });

  const response = completion.choices[0]?.message?.content;
  return response;
}

// Usage
const answer = await askQuestion('What is the capital of France?');
console.log('Answer:', answer);
```

### Custom System Prompt

```javascript
async function customAssistant(systemPrompt, userMessage) {
  const completion = await chatCompletions({
    model: MODEL,
    messages: [
      {
        role: 'system',
        content: systemPrompt
      },
      {
        role: 'user',
        content: userMessage
      }
    ]
  });

  return completion.choices[0]?.message?.content;
}

// Usage - Code reviewer
const codeReview = await customAssistant(
  'You are an expert code reviewer. Analyze code for bugs, performance issues, and best practices.',
  'Review this function: function add(a, b) { return a + b; }'
);

// Usage - Creative writer
const story = await customAssistant(
  'You are a creative fiction writer who writes engaging short stories.',
  'Write a short story about a robot learning to paint.'
);

console.log(codeReview);
console.log(story);
```

## Multi-turn Conversations

### Conversation History Management

```javascript
class ConversationManager {
  constructor(systemPrompt = 'You are a helpful assistant.') {
    this.messages = [
      {
        role: 'system',
        content: systemPrompt
      }
    ];
  }

  async sendMessage(userMessage) {
    // Add user message to history
    this.messages.push({
      role: 'user',
      content: userMessage
    });

    // Get completion
    const completion = await chatCompletions({
      model: MODEL,
      messages: this.messages
    });

    const assistantResponse = completion.choices[0]?.message?.content;

    // Add assistant response to history
    this.messages.push({
      role: 'assistant',
      content: assistantResponse
    });

    return assistantResponse;
  }

  getHistory() {
    return this.messages;
  }

  clearHistory(systemPrompt = 'You are a helpful assistant.') {
    this.messages = [
      {
        role: 'system',
        content: systemPrompt
      }
    ];
  }

  getMessageCount() {
    // Subtract 1 for system message
    return this.messages.length - 1;
  }
}

// Usage
const conversation = new ConversationManager();

const response1 = await conversation.sendMessage('Hi, my name is John.');
console.log('AI:', response1);

const response2 = await conversation.sendMessage('What is my name?');
console.log('AI:', response2); // Should remember the name is John

console.log('Total messages:', conversation.getMessageCount());
```

### Context-Aware Conversations

```javascript
class ContextualChat {
  constructor() {
    this.messages = [];
  }

  startConversation(role, context) {
    // Set up system prompt with context
    const systemPrompt = `You are ${role}. Context: ${context}`;

    this.messages = [
      {
        role: 'system',
        content: systemPrompt
      }
    ];
  }

  async chat(userMessage) {
    this.messages.push({
      role: 'user',
      content: userMessage
    });

    const completion = await chatCompletions({
      model: MODEL,
      messages: this.messages
    });

    const response = completion.choices[0]?.message?.content;

    this.messages.push({
      role: 'assistant',
      content: response
    });

    return response;
  }
}

// Usage - Customer support scenario
const support = new ContextualChat();

support.startConversation(
  'a customer support agent for TechCorp',
  'The user has ordered product #12345 which is delayed due to shipping issues.'
);

const reply1 = await support.chat('Where is my order?');
console.log('Support:', reply1);

const reply2 = await support.chat('Can I get a refund?');
console.log('Support:', reply2);
```

## Advanced Use Cases

### Content Generation

```javascript
class ContentGenerator {
  async generateBlogPost(topic, tone = 'professional') {
    const completion = await chatCompletions({
      model: MODEL,
      messages: [
        {
          role: 'system',
          content: `You are a professional content writer. Write in a ${tone} tone.`
        },
        {
          role: 'user',
          content: `Write a blog post about: ${topic}. Include an introduction, main points, and conclusion.`
        }
      ]
    });

    return completion.choices[0]?.message?.content;
  }

  async generateProductDescription(productName, features) {
    const completion = await chatCompletions({
      model: MODEL,
      messages: [
        {
          role: 'system',
          content: 'You are an expert at writing compelling product descriptions for e-commerce.'
        },
        {
          role: 'user',
          content: `Write a product description for "${productName}". Key features: ${features.join(', ')}.`
        }
      ]
    });

    return completion.choices[0]?.message?.content;
  }

  async generateEmailResponse(originalEmail, intent) {
    const completion = await chatCompletions({
      model: MODEL,
      messages: [
        {
          role: 'system',
          content: 'You are a professional email writer. Write clear, concise, and polite emails.'
        },
        {
          role: 'user',
          content: `Original email: "${originalEmail}"\n\nWrite a ${intent} response.`
        }
      ]
    });

    return completion.choices[0]?.message?.content;
  }
}

// Usage
const generator = new ContentGenerator();

const blogPost = await generator.generateBlogPost(
  'The Future of Artificial Intelligence',
  'informative'
);
console.log('Blog Post:', blogPost);

const productDesc = await generator.generateProductDescription(
  'Smart Watch Pro',
  ['Heart rate monitoring', 'GPS tracking', 'Waterproof', '7-day battery life']
);
console.log('Product Description:', productDesc);
```

### Data Analysis and Summarization

```javascript
async function analyzeData(data, analysisType) {
  const prompts = {
    summarize: 'You are a data analyst. Summarize the key insights from the data.',
    trend: 'You are a data analyst. Identify trends and patterns in the data.',
    recommendation: 'You are a business analyst. Provide actionable recommendations based on the data.'
  };

  const completion = await chatCompletions({
    model: MODEL,
    messages: [
      {
        role: 'system',
        content: prompts[analysisType] || prompts.summarize
      },
      {
        role: 'user',
        content: `Analyze this data:\n\n${JSON.stringify(data, null, 2)}`
      }
    ]
  });

  return completion.choices[0]?.message?.content;
}

// Usage
const salesData = {
  Q1: { revenue: 100000, customers: 250 },
  Q2: { revenue: 120000, customers: 280 },
  Q3: { revenue: 150000, customers: 320 },
  Q4: { revenue: 180000, customers: 380 }
};

const summary = await analyzeData(salesData, 'summarize');
const trends = await analyzeData(salesData, 'trend');
const recommendations = await analyzeData(salesData, 'recommendation');

console.log('Summary:', summary);
console.log('Trends:', trends);
console.log('Recommendations:', recommendations);
```

### Code Generation and Debugging

```javascript
class CodeAssistant {
  async generateCode(description, language) {
    const completion = await chatCompletions({
      model: MODEL,
      messages: [
        {
          role: 'system',
          content: `You are an expert ${language} programmer. Write clean, efficient, and well-commented code.`
        },
        {
          role: 'user',
          content: `Write ${language} code to: ${description}`
        }
      ]
    });

    return completion.choices[0]?.message?.content;
  }

  async debugCode(code, issue) {
    const completion = await chatCompletions({
      model: MODEL,
      messages: [
        {
          role: 'system',
          content: 'You are an expert debugger. Identify bugs and suggest fixes.'
        },
        {
          role: 'user',
          content: `Code:\n${code}\n\nIssue: ${issue}\n\nFind the bug and suggest a fix.`
        }
      ]
    });

    return completion.choices[0]?.message?.content;
  }

  async explainCode(code) {
    const completion = await chatCompletions({
      model: MODEL,
      messages: [
        {
          role: 'system',
          content: 'You are a programming teacher. Explain code clearly and simply.'
        },
        {
          role: 'user',
          content: `Explain what this code does:\n\n${code}`
        }
      ]
    });

    return completion.choices[0]?.message?.content;
  }
}

// Usage
const codeAssist = new CodeAssistant();

const newCode = await codeAssist.generateCode(
  'Create a function that sorts an array of objects by a specific property',
  'JavaScript'
);
console.log('Generated Code:', newCode);

const bugFix = await codeAssist.debugCode(
  'function add(a, b) { return a - b; }',
  'This function should add numbers but returns wrong results'
);
console.log('Debug Suggestion:', bugFix);
```

## Best Practices

### 1. Prompt Engineering

```javascript
// Bad: Vague prompt
const bad = await askQuestion('Tell me about AI');

// Good: Specific and structured prompt
async function askWithContext(topic, format, audience) {
  const completion = await chatCompletions({
    model: MODEL,
    messages: [
      {
        role: 'system',
        content: `You are an expert educator. Explain topics clearly for ${audience}.`
      },
      {
        role: 'user',
        content: `Explain ${topic} in ${format} format. Include practical examples.`
      }
    ]
  });

  return completion.choices[0]?.message?.content;
}

const good = await askWithContext('artificial intelligence', 'bullet points', 'beginners');
```

### 2. Error Handling

```javascript
async function safeCompletion(messages, retries = 3) {
  let lastError;

  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      const completion = await chatCompletions({
        model: MODEL,
        messages: messages
      });

      const response = completion.choices[0]?.message?.content;

      if (!response || response.trim().length === 0) {
        throw new Error('Empty response from AI');
      }

      return {
        success: true,
        content: response,
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

### 3. Context Management

```javascript
class ManagedConversation {
  constructor(maxMessages = 20) {
    this.maxMessages = maxMessages;
    this.systemPrompt = '';
    this.messages = [];
  }

  initialize(systemPrompt) {
    this.systemPrompt = systemPrompt;
    this.messages = [
      {
        role: 'system',
        content: systemPrompt
      }
    ];
  }

  async chat(userMessage) {
    // Add user message
    this.messages.push({
      role: 'user',
      content: userMessage
    });

    // Trim old messages if exceeding limit (keep system prompt)
    if (this.messages.length > this.maxMessages) {
      this.messages = [
        this.messages[0], // Keep system prompt
        ...this.messages.slice(-(this.maxMessages - 1))
      ];
    }

    const completion = await chatCompletions({
      model: MODEL,
      messages: this.messages
    });

    const response = completion.choices[0]?.message?.content;

    this.messages.push({
      role: 'assistant',
      content: response
    });

    return response;
  }

  getTokenEstimate() {
    // Rough estimate: ~4 characters per token
    const totalChars = this.messages
      .map(m => m.content.length)
      .reduce((a, b) => a + b, 0);
    return Math.ceil(totalChars / 4);
  }
}
```

### 4. Response Processing

```javascript
async function getStructuredResponse(query, format = 'json') {
  const formatInstructions = {
    json: 'Respond with valid JSON only. No additional text.',
    list: 'Respond with a numbered list.',
    markdown: 'Respond in Markdown format.'
  };

  const completion = await chatCompletions({
    model: MODEL,
    messages: [
      {
        role: 'system',
        content: `You are a helpful assistant. ${formatInstructions[format]}`
      },
      {
        role: 'user',
        content: query
      }
    ]
  });

  const response = completion.choices[0]?.message?.content;

  // Parse JSON if requested
  if (format === 'json') {
    try {
      return JSON.parse(response);
    } catch (e) {
      console.error('Failed to parse JSON response');
      return { raw: response };
    }
  }

  return response;
}

// Usage
const jsonData = await getStructuredResponse(
  'List three programming languages with their primary use cases',
  'json'
);
console.log(jsonData);
```

## Common Use Cases

1. **Chatbots & Virtual Assistants**: Build conversational interfaces for customer support
2. **Content Generation**: Create articles, product descriptions, marketing copy
3. **Code Assistance**: Generate, explain, and debug code
4. **Data Analysis**: Analyze and summarize complex data sets
5. **Language Translation**: Translate text between languages
6. **Educational Tools**: Create tutoring and learning applications
7. **Email Automation**: Generate professional email responses
8. **Creative Writing**: Story generation, poetry, and creative content

## Integration Examples

### Express.js Chatbot API

```javascript
import express from 'express';

const app = express();
app.use(express.json());

// Store conversations in memory (use database in production)
const conversations = new Map();

app.post('/api/chat', async (req, res) => {
  try {
    const { sessionId, message, systemPrompt } = req.body;

    if (!message) {
      return res.status(400).json({ error: 'Message is required' });
    }

    // Get or create conversation history
    let history = conversations.get(sessionId) || [
      {
        role: 'system',
        content: systemPrompt || 'You are a helpful assistant.'
      }
    ];

    // Add user message
    history.push({
      role: 'user',
      content: message
    });

    // Get completion
    const completion = await chatCompletions({
      model: MODEL,
      messages: history
    });

    const aiResponse = completion.choices[0]?.message?.content;

    // Add AI response to history
    history.push({
      role: 'assistant',
      content: aiResponse
    });

    // Save updated history
    conversations.set(sessionId, history);

    res.json({
      success: true,
      response: aiResponse,
      messageCount: history.length - 1
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

app.delete('/api/chat/:sessionId', (req, res) => {
  const { sessionId } = req.params;
  conversations.delete(sessionId);
  res.json({ success: true, message: 'Conversation cleared' });
});

app.listen(3000, () => {
  console.log('Chatbot API running on port 3000');
});
```

## Troubleshooting

**Issue**: "API key must be kept server-side"
- **Solution**: Read `LLM_API_KEY` from environment variables and never expose it in client-side code

**Issue**: Empty or incomplete responses
- **Solution**: Check that completion.choices[0]?.message?.content exists and is not empty

**Issue**: Conversation context getting too long
- **Solution**: Implement message trimming to keep only recent messages

**Issue**: Inconsistent responses
- **Solution**: Use more specific system prompts and provide clear instructions

**Issue**: Rate limiting errors
- **Solution**: Implement retry logic with exponential backoff

**Issue**: Connection refused
- **Solution**: Verify `LLM_BASE_URL` points at a running server (e.g. `ollama serve` with `OLLAMA_BASE_URL=http://localhost:11434/v1`)

**Issue**: Model not found
- **Solution**: Check the model name matches what the server offers (`ollama list`, `vllm serve --model ...`)

## Performance Tips

1. **Reuse HTTP Connections**: `fetch` with keep-alive reuses connections across requests
2. **Manage Context Length**: Trim old messages to avoid token limits
3. **Implement Caching**: Cache responses for common queries
4. **Use Specific Prompts**: Clear prompts lead to faster, better responses
5. **Handle Errors Gracefully**: Implement retry logic and fallback responses

## Security Considerations

1. **Input Validation**: Always validate and sanitize user input
2. **Rate Limiting**: Implement rate limits to prevent abuse
3. **API Key Protection**: Never expose `LLM_API_KEY` in client-side code
4. **Content Filtering**: Filter sensitive or inappropriate content
5. **Session Management**: Implement proper session handling and cleanup

## Remember

- Works with any OpenAI-compatible LLM server (open-source or free) — Ollama, vLLM, LM Studio, OpenRouter, and more
- Designed for the DiveeOI agent (OpenCode-based)
- All configuration comes from environment variables: `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL`
- Use the 'system' role for system prompts
- The endpoint is `POST {LLM_BASE_URL}/chat/completions` with a standard OpenAI request body
- Response parsing: `response.choices[0]?.message?.content`
- Implement proper error handling and retries for production
- Manage conversation history to avoid token limits
- Clear and specific prompts lead to better results
- Check `scripts/chat.ts` for a quick start example
