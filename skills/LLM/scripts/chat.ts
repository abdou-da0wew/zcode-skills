// Chat completions via an OpenAI-compatible server.
// Works with any OpenAI-compatible server: Ollama, vLLM, LM Studio, OpenRouter, ...
//
// Configuration (environment variables):
//   LLM_BASE_URL - OpenAI-compatible base URL (default: http://localhost:11434/v1)
//   LLM_API_KEY  - API key sent as a Bearer token (default: empty)
//   LLM_MODEL    - model name (default: qwen2.5; also try llama3.1, deepseek-r1, ...)

const BASE_URL = process.env.LLM_BASE_URL ?? "http://localhost:11434/v1";
const API_KEY = process.env.LLM_API_KEY ?? "";
const MODEL = process.env.LLM_MODEL ?? "qwen2.5";

interface ChatMessage {
  role: "system" | "user" | "assistant";
  content: string | Array<Record<string, unknown>>;
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

async function main(prompt: string) {
  try {
    const messages: ChatMessage[] = [
      {
        role: "system",
        content: "Hi, I'm a helpful assistant.",
      },
      {
        role: "user",
        content: prompt,
      },
    ];

    const response = await chatCompletions({
      model: MODEL,
      messages,
      stream: false,
    });

    const reply = response.choices?.[0]?.message?.content;
    console.log("Chat reply:");
    console.log(reply ?? JSON.stringify(response, null, 2));
  } catch (err: any) {
    console.error("Chat failed:", err?.message || err);
  }
}

main('What is the capital of France?');
