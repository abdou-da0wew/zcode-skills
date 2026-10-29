#!/usr/bin/env tsx
/**
 * generate.ts - Unified entry point (OpenAI-compatible HTTP version)
 * Source material -> podcast_script.md + podcast.wav
 *
 * Uses plain HTTP calls against an OpenAI-compatible LLM server and an
 * OpenAI-compatible /audio/speech TTS endpoint. No proprietary SDK, no CLI
 * dependency, no extra npm packages.
 *
 * Configuration (environment variables):
 *   LLM_BASE_URL    - OpenAI-compatible base URL (default: http://localhost:11434/v1)
 *   LLM_API_KEY     - API key sent as a Bearer token (default: empty)
 *   LLM_MODEL       - chat model used for script writing (default: qwen2.5)
 *   TTS_MODEL       - TTS model name (default: tts-1)
 *   TTS_HOST_VOICE  - voice id for the host (default: onyx; availability depends on server)
 *   TTS_GUEST_VOICE - voice id for the guest (default: nova; availability depends on server)
 *   SEARCH_BASE_URL - metasearch endpoint for --topic mode (SearXNG JSON API convention,
 *                     e.g. http://localhost:8080; default: http://localhost:8080)
 *   SEARCH_API_KEY  - optional API key for the search endpoint
 *
 * Usage:
 *   tsx generate.ts --input=material.txt --out_dir=out
 *   tsx generate.ts --input=material.md --out_dir=out --duration=5
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import os from 'os';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// -----------------------------
// Environment / endpoints
// -----------------------------
const BASE_URL = process.env.LLM_BASE_URL ?? 'http://localhost:11434/v1';
const API_KEY = process.env.LLM_API_KEY ?? '';
const LLM_MODEL = process.env.LLM_MODEL ?? 'qwen2.5';
const TTS_MODEL = process.env.TTS_MODEL ?? 'tts-1';
const TTS_HOST_VOICE = process.env.TTS_HOST_VOICE ?? 'onyx';
const TTS_GUEST_VOICE = process.env.TTS_GUEST_VOICE ?? 'nova';
const SEARCH_BASE_URL = (process.env.SEARCH_BASE_URL ?? 'http://localhost:8080').replace(/\/+$/, '');
const SEARCH_API_KEY = process.env.SEARCH_API_KEY ?? '';

// -----------------------------
// Types
// -----------------------------
interface GenConfig {
  mode: 'dual' | 'single-male' | 'single-female';
  temperature: number;
  durationManual: number;
  charsPerMin: number;
  hostName: string;
  guestName: string;
  audience: string;
  tone: string;
  maxAttempts: number;
  timeoutSec: number;
  voiceHost: string;
  voiceGuest: string;
  speed: number;
  pauseMs: number;
}

interface Segment {
  idx: number;
  speaker: 'host' | 'guest';
  name: string;
  text: string;
}

// -----------------------------
// Config
// -----------------------------
const DEFAULT_CONFIG: GenConfig = {
  mode: 'dual',
  temperature: 0.9,
  durationManual: 0,
  charsPerMin: 900, // ~150 spoken words/min for English text (~6 chars per word)
  hostName: 'Alex',
  guestName: 'Sam',
  audience: 'curious beginners and busy professionals',
  tone: 'relaxed but information-dense',
  maxAttempts: 3,
  timeoutSec: 300,
  voiceHost: TTS_HOST_VOICE,
  voiceGuest: TTS_GUEST_VOICE,
  speed: 1.0,
  pauseMs: 200,
};

const DURATION_RANGE_LOW = 3;
const DURATION_RANGE_HIGH = 20;
const BUDGET_TOLERANCE = 0.15;

// -----------------------------
// Functions
// -----------------------------

function parseArgs(): { [key: string]: any } {
  const args = process.argv.slice(2);
  const result: { [key: string]: any } = {};

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      if (key.includes('=')) {
        const [k, v] = key.split('=');
        result[k] = v;
      } else if (i + 1 < args.length && !args[i + 1].startsWith('--')) {
        result[key] = args[i + 1];
        i++;
      } else {
        result[key] = true;
      }
    }
  }

  return result;
}

function readText(filePath: string): string {
  let content = fs.readFileSync(filePath, 'utf-8');
  content = content.replace(/\r\n/g, '\n');
  content = content.replace(/\n{3,}/g, '\n\n');
  content = content.replace(/[ \t]{2,}/g, ' ');
  content = content.replace(/-\n/g, '');
  return content.trim();
}

function countNonWsChars(text: string): number {
  return text.replace(/\s+/g, '').length;
}

function chooseDurationMinutes(inputChars: number, low: number = DURATION_RANGE_LOW, high: number = DURATION_RANGE_HIGH): number {
  const estimated = Math.max(low, Math.min(high, Math.floor(inputChars / 1000)));
  return estimated;
}

function charBudget(durationMin: number, charsPerMin: number, tolerance: number): [number, number, number] {
  const target = durationMin * charsPerMin;
  const low = Math.floor(target * (1 - tolerance));
  const high = Math.ceil(target * (1 + tolerance));
  return [target, low, high];
}

function buildPrompts(
  material: string,
  cfg: GenConfig,
  durationMin: number,
  budgetTarget: number,
  budgetLow: number,
  budgetHigh: number,
  attemptHint: string = ''
): [string, string] {
  let system: string;
  let user: string;

  if (cfg.mode === 'dual') {
    system = (
      `You are a podcast scriptwriter who excels at turning source material into a two-host dialogue podcast.` +
      `The roles are fixed: male host "${cfg.hostName}" and female guest "${cfg.guestName}".` +
      `You write in a spoken, conversational style with moderate information density, natural breathing room, and rhythm.` +
      `You must strictly follow the output format and the word budget.`
    );

    const hintBlock = attemptHint ? `\n[CORRECTION HINT FROM THE PREVIOUS ATTEMPT]\n${attemptHint}\n` : '';

    user = `Rewrite the [SOURCE MATERIAL] below into an English podcast script, in the form of a two-person dialogue (male host ${cfg.hostName} + female guest ${cfg.guestName}).
Duration target: ${durationMin} minutes.

[HARD CONSTRAINTS]
1) The total length must be between ${budgetLow} and ${budgetHigh} characters (target roughly ${budgetTarget} characters).
2) Strictly alternate turns: every paragraph must start with "${cfg.hostName}:" or "${cfg.guestName}:" (the name wrapped in double asterisks).
3) It must contain a complete narrative structure (but do NOT write structural labels inside the dialogue):
   - Opening: a hook + introduction of today's topic
   - Body: content from 3 different angles, connected with natural transitions
   - Wrap-up: recap the key points + one actionable piece of advice (1 sentence, clearly actionable)
4) Do not write structural labels like "Key point 1" or "First point" in the dialogue; use natural transitions such as "speaking of which", "here's another interesting thing", "also", etc.
5) Do not read the source verbatim and do not quote long passages; use spoken, conversational phrasing.
6) Audience: ${cfg.audience}
7) Style: ${cfg.tone}

[BREATHING ROOM AND NATURAL DIALOGUE - IMPORTANT!]
To create the breathing room of a real podcast:
1) Add conversational interjections in moderation: mm, oh, ah, right, exactly, haha, wow, gosh, etc.
2) Use interactive phrasing: "you're right about that", "now that's interesting", "wait, let me think", "I see what you mean"
3) Add hints of thinking and pausing: "hmm, that question...", "how should I put it...", "actually..."
4) Avoid overly dense information; keep each paragraph to 3-5 sentences to give listeners time to digest
5) Use analogies and everyday examples to explain complex concepts
6) The two speakers should respond to and follow up on each other, not talk past each other
7) Connect different topics with natural transitions; never use labels like "Key point 1/2/3"

[OUTPUT FORMAT EXAMPLE]
**${cfg.hostName}**: Opening...
**${cfg.guestName}**: Response...
(keep alternating until the end)

${hintBlock}
[SOURCE MATERIAL]
${material}
`;
  } else {
    const speakerName = cfg.mode === 'single-male' ? cfg.hostName : cfg.guestName;
    const gender = cfg.mode === 'single-male' ? 'male' : 'female';

    system = (
      `You are a ${gender} solo podcast host named "${speakerName}".` +
      `You excel at turning source material into a monologue-style podcast, like a lecture, a book share, or a knowledge explainer.` +
      `You write in a spoken, conversational style with moderate information density, natural breathing room, and rhythm.` +
      `You must strictly follow the output format and the word budget.`
    );

    const hintBlock = attemptHint ? `\n[CORRECTION HINT FROM THE PREVIOUS ATTEMPT]\n${attemptHint}\n` : '';

    user = `Rewrite the [SOURCE MATERIAL] below into an English solo podcast script, in the form of a monologue (host: ${speakerName}).
Duration target: ${durationMin} minutes.

[HARD CONSTRAINTS]
1) The total length must be between ${budgetLow} and ${budgetHigh} characters (target roughly ${budgetTarget} characters).
2) Everything is spoken by "${speakerName}" alone; every paragraph starts with "${speakerName}:" (the name wrapped in double asterisks).
3) It must contain a complete narrative structure (but do NOT write structural labels inside the dialogue):
   - Opening: a hook + introduction of today's topic
   - Body: content from 3 different angles, connected with natural transitions
   - Wrap-up: recap the key points + one actionable piece of advice (1 sentence, clearly actionable)
4) Do not write structural labels like "Key point 1" or "First point" in the dialogue; use natural transitions such as "speaking of which", "here's another interesting thing", "also", etc.
5) Do not read the source verbatim and do not quote long passages; use spoken, conversational phrasing.
6) Audience: ${cfg.audience}
7) Style: ${cfg.tone}

[BREATHING ROOM FOR A SOLO PODCAST - IMPORTANT!]
To create a natural solo-podcast rhythm:
1) Add conversational interjections in moderation: mm, oh, ah, right, exactly, haha, wow, gosh, etc.
2) Use self-question-and-answer phrasing: "you might ask... and the answer is...", "why is that? Let me explain..."
3) Add hints of thinking and pausing: "hmm, that question...", "how should I put it...", "actually..."
4) Avoid overly dense information; keep each paragraph to 3-5 sentences to give listeners time to digest
5) Use analogies and everyday examples to explain complex concepts
6) Talk like you are chatting with a friend, not reading an essay aloud

[OUTPUT FORMAT EXAMPLE]
**${speakerName}**: Opening - hello everyone, I'm ${speakerName}, today we're talking about...
**${speakerName}**: Speaking of which, something really interesting happened recently...
(everything is spoken by ${speakerName}, output paragraph by paragraph)

${hintBlock}
[SOURCE MATERIAL]
${material}
`;
  }

  return [system, user];
}

async function chatCompletions(body: Record<string, unknown>): Promise<any> {
  const res = await fetch(`${BASE_URL}/chat/completions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(API_KEY ? { Authorization: `Bearer ${API_KEY}` } : {}),
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`LLM request failed (${res.status}): ${await res.text()}`);
  return res.json();
}

async function callLLM(
  systemPrompt: string,
  userPrompt: string,
  temperature: number
): Promise<string> {
  const completion = await chatCompletions({
    model: LLM_MODEL,
    messages: [
      { role: 'system', content: systemPrompt },
      { role: 'user', content: userPrompt },
    ],
    temperature,
  });

  const content = completion.choices[0]?.message?.content || '';
  return content;
}

/**
 * Web search via a pluggable, self-hostable metasearch endpoint.
 * Convention: SearXNG JSON API (GET {SEARCH_BASE_URL}/search?q=...&format=json),
 * which is the most common open-source search convention. Works with any
 * SearXNG instance (public or self-hosted) or any endpoint that returns
 * {"results": [{"title"|"url"|"content", ...}]}.
 */
async function webSearch(query: string, num: number): Promise<Array<{ name: string; snippet: string; url: string }>> {
  const url = `${SEARCH_BASE_URL}/search?q=${encodeURIComponent(query)}&format=json`;
  const res = await fetch(url, {
    headers: {
      'Accept': 'application/json',
      ...(SEARCH_API_KEY ? { Authorization: `Bearer ${SEARCH_API_KEY}` } : {}),
    },
  });
  if (!res.ok) throw new Error(`Search request failed (${res.status}): ${await res.text()}`);

  const data: any = await res.json();
  const results: any[] = Array.isArray(data?.results) ? data.results : [];

  // Normalize to the {name, snippet, url} shape used by the script builder
  return results.slice(0, num).map((r: any) => ({
    name: r.title ?? r.name ?? '',
    snippet: r.content ?? r.snippet ?? '',
    url: r.url ?? '',
  }));
}

function scriptToSegments(script: string, hostName: string, guestName: string): Segment[] {
  const segments: Segment[] = [];
  const lines = script.split('\n');

  let current: Segment | null = null;
  let idx = 0;

  const hostPrefix = `**${hostName}**:`;
  const guestPrefix = `**${guestName}**:`;

  for (const rawLine of lines) {
    const line = rawLine.trim();
    if (!line) continue;

    if (line.startsWith(hostPrefix)) {
      idx++;
      current = {
        idx,
        speaker: 'host',
        name: hostName,
        text: line.slice(hostPrefix.length).trim(),
      };
      segments.push(current);
    } else if (line.startsWith(guestPrefix)) {
      idx++;
      current = {
        idx,
        speaker: 'guest',
        name: guestName,
        text: line.slice(guestPrefix.length).trim(),
      };
      segments.push(current);
    } else {
      if (current) {
        current.text = (current.text + ' ' + line).trim();
      }
    }
  }

  return segments;
}

function validateScript(
  script: string,
  cfg: GenConfig,
  budgetLow: number,
  budgetHigh: number
): [boolean, string[]] {
  const reasons: string[] = [];

  if (cfg.mode === 'dual') {
    const hostTag = `**${cfg.hostName}**:`;
    const guestTag = `**${cfg.guestName}**:`;

    if (!script.includes(hostTag)) reasons.push(`Missing host tag: ${hostTag}`);
    if (!script.includes(guestTag)) reasons.push(`Missing guest tag: ${guestTag}`);

    const turns = script.split('\n').filter(line =>
      line.startsWith(hostTag) || line.startsWith(guestTag)
    );
    if (turns.length < 8) reasons.push('Too few dialogue turns: at least 8 recommended');
  } else {
    const speakerName = cfg.mode === 'single-male' ? cfg.hostName : cfg.guestName;
    const speakerTag = `**${speakerName}**:`;

    if (!script.includes(speakerTag)) reasons.push(`Missing host tag: ${speakerTag}`);

    const turns = script.split('\n').filter(line => line.startsWith(speakerTag));
    if (turns.length < 5) reasons.push('Too few podcast segments: at least 5 recommended');
  }

  const n = countNonWsChars(script);
  if (n < budgetLow || n > budgetHigh) {
    reasons.push(`Character count outside budget: currently ~${n} chars, budget ${budgetLow}-${budgetHigh}`);
  }

  // Only check the opening and wrap-up; do not check for "Key point 1/2/3" labels
  // (they should not appear in the dialogue).
  const mustHave = ['opening', 'wrap-up'];
  for (const kw of mustHave) {
    if (!script.includes(kw)) {
      reasons.push(`Missing structural element: ${kw} (introduce it naturally in the dialogue)`);
    }
  }

  // Check that there are enough dialogue turns (ensures coverage of multiple topics)
  const lineCount = script.split('\n').filter(l => l.trim()).length;
  if (lineCount < 10) {
    reasons.push('Too few dialogue turns; at least 10 paragraphs recommended');
  }

  return [reasons.length === 0, reasons];
}

function makeRetryHint(reasons: string[], cfg: GenConfig, budgetLow: number, budgetHigh: number): string {
  const lines = ['Please strictly fix the following problems and regenerate:'];
  for (const r of reasons) lines.push(`- ${r}`);
  lines.push(`- The total length must be between ${budgetLow}-${budgetHigh} characters.`);

  if (cfg.mode === 'dual') {
    lines.push(`- Every paragraph must start with "${cfg.hostName}:" or "${cfg.guestName}:" (names wrapped in double asterisks).`);
  } else {
    const speakerName = cfg.mode === 'single-male' ? cfg.hostName : cfg.guestName;
    lines.push(`- Everything is spoken by one person; every paragraph must start with "${speakerName}:" (name wrapped in double asterisks).`);
  }

  lines.push('- Include an opening and a wrap-up; connect different topics with natural transitions and never use labels like "Key point 1/2/3".');
  return lines.join('\n');
}

async function ttsRequest(
  text: string,
  voice: string,
  speed: number
): Promise<Buffer> {
  // OpenAI-compatible speech endpoint: POST {BASE_URL}/audio/speech
  // Returns raw binary audio in the requested format.
  const res = await fetch(`${BASE_URL}/audio/speech`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(API_KEY ? { Authorization: `Bearer ${API_KEY}` } : {}),
    },
    body: JSON.stringify({
      model: TTS_MODEL,
      input: text,
      voice: voice,
      speed: speed,
      response_format: 'wav',
      stream: false,
    }),
  });
  if (!res.ok) throw new Error(`TTS request failed (${res.status}): ${await res.text()}`);

  const arrayBuffer = await res.arrayBuffer();
  const buffer = Buffer.from(new Uint8Array(arrayBuffer));
  return buffer;
}

function ensureSilenceWav(filePath: string, params: { nchannels: number; sampwidth: number; framerate: number }, ms: number): void {
  const { nchannels, sampwidth, framerate } = params;
  const nframes = Math.floor((framerate * ms) / 1000);
  const silenceFrame = Buffer.alloc(sampwidth * nchannels, 0);
  const frames = Buffer.alloc(silenceFrame.length * nframes, 0);

  const header = Buffer.alloc(44);
  header.write('RIFF', 0);
  header.writeUInt32LE(36 + frames.length, 4);
  header.write('WAVE', 8);
  header.write('fmt ', 12);
  header.writeUInt32LE(16, 16);
  header.writeUInt16LE(1, 20);
  header.writeUInt16LE(nchannels, 22);
  header.writeUInt32LE(framerate, 24);
  header.writeUInt32LE(framerate * nchannels * sampwidth, 28);
  header.writeUInt16LE(nchannels * sampwidth, 32);
  header.writeUInt16LE(sampwidth * 8, 34);
  header.write('data', 36);
  header.writeUInt32LE(frames.length, 40);

  fs.writeFileSync(filePath, Buffer.concat([header, frames]));
}

function wavParams(filePath: string): { nchannels: number; sampwidth: number; framerate: number } {
  const buffer = fs.readFileSync(filePath);
  const nchannels = buffer.readUInt16LE(22);
  const sampwidth = buffer.readUInt16LE(34) / 8;
  const framerate = buffer.readUInt32LE(24);
  return { nchannels, sampwidth, framerate };
}

function joinWavsWave(outPath: string, wavPaths: string[], pauseMs: number): void {
  if (wavPaths.length === 0) throw new Error('No wav files to join.');

  const ref = wavPaths[0];
  const refParams = wavParams(ref);
  const silencePath = path.join(os.tmpdir(), `_silence_${Date.now()}.wav`);
  if (pauseMs > 0) ensureSilenceWav(silencePath, refParams, pauseMs);

  const chunks: Buffer[] = [];

  for (let i = 0; i < wavPaths.length; i++) {
    const wavPath = wavPaths[i];
    const buffer = fs.readFileSync(wavPath);
    const dataStart = buffer.indexOf('data') + 8;
    const data = buffer.subarray(dataStart);

    const params = wavParams(wavPath);
    if (params.nchannels !== refParams.nchannels ||
        params.sampwidth !== refParams.sampwidth ||
        params.framerate !== refParams.framerate) {
      throw new Error(`WAV params mismatch: ${wavPath}`);
    }

    chunks.push(data);

    if (pauseMs > 0 && i < wavPaths.length - 1) {
      const silenceBuffer = fs.readFileSync(silencePath);
      const silenceData = silenceBuffer.subarray(silenceBuffer.indexOf('data') + 8);
      chunks.push(silenceData);
    }
  }

  const totalDataSize = chunks.reduce((sum, buf) => sum + buf.length, 0);
  const header = Buffer.alloc(44);
  header.write('RIFF', 0);
  header.writeUInt32LE(36 + totalDataSize, 4);
  header.write('WAVE', 8);
  header.write('fmt ', 12);
  header.writeUInt32LE(16, 16);
  header.writeUInt16LE(1, 20);
  header.writeUInt16LE(refParams.nchannels, 22);
  header.writeUInt32LE(refParams.framerate, 24);
  header.writeUInt32LE(refParams.framerate * refParams.nchannels * refParams.sampwidth, 28);
  header.writeUInt16LE(refParams.nchannels * refParams.sampwidth, 32);
  header.writeUInt16LE(refParams.sampwidth * 8, 34);
  header.write('data', 36);
  header.writeUInt32LE(totalDataSize, 40);

  const output = Buffer.concat([header, ...chunks]);
  fs.writeFileSync(outPath, output);

  if (fs.existsSync(silencePath)) fs.unlinkSync(silencePath);
}

// -----------------------------
// Main
// -----------------------------
async function main() {
  const args = parseArgs();

  const inputPath = args.input;
  const outDir = args.out_dir;
  const topic = args.topic;

  // Validate arguments: exactly one of input or topic must be provided
  if ((!inputPath && !topic) || !outDir) {
    console.error('Usage: tsx generate.ts --input=<file> --out_dir=<dir>');
    console.error('   OR: tsx generate.ts --topic=<search-term> --out_dir=<dir>');
    console.error('');
    console.error('Examples:');
    console.error('  # From file');
    console.error('  npm run generate -- --input=article.txt --out_dir=out');
    console.error('  # From web search');
    console.error('  npm run generate -- --topic="latest AI news" --out_dir=out');
    process.exit(1);
  }

  // Merge config
  const cfg: GenConfig = {
    ...DEFAULT_CONFIG,
    mode: (args.mode || 'dual') as GenConfig['mode'],
    durationManual: parseInt(args.duration || '0'),
    hostName: args.host_name || DEFAULT_CONFIG.hostName,
    guestName: args.guest_name || DEFAULT_CONFIG.guestName,
    voiceHost: args.voice_host || DEFAULT_CONFIG.voiceHost,
    voiceGuest: args.voice_guest || DEFAULT_CONFIG.voiceGuest,
    speed: parseFloat(args.speed || String(DEFAULT_CONFIG.speed)),
    pauseMs: parseInt(args.pause_ms || String(DEFAULT_CONFIG.pauseMs)),
  };

  // Create output directory
  if (!fs.existsSync(outDir)) {
    fs.mkdirSync(outDir, { recursive: true });
  }

  // Fetch the source material depending on the mode
  let material: string;
  let inputSource: string;

  if (inputPath) {
    // Mode 1: read from a file
    console.log(`[MODE] Reading from file: ${inputPath}`);
    material = readText(inputPath);
    inputSource = `file:${inputPath}`;
  } else if (topic) {
    // Mode 2: web search
    console.log(`[MODE] Searching web for topic: ${topic}`);

    const searchResults = await webSearch(topic, 10);

    if (!Array.isArray(searchResults) || searchResults.length === 0) {
      console.error(`No search results found for "${topic}"`);
      process.exit(2);
    }

    console.log(`[SEARCH] Found ${searchResults.length} results`);

    // Convert the search results into text material
    material = searchResults
      .map((r: any, i: number) => `[Source ${i + 1}] ${r.name}\n${r.snippet}\nLink: ${r.url}`)
      .join('\n\n');

    inputSource = `web_search:${topic}`;
    console.log(`[SEARCH] Compiled material (${material.length} chars)`);
  } else {
    console.error('[ERROR] Neither --input nor --topic provided');
    process.exit(1);
  }

  const inputChars = material.length;

  // Calculate duration
  let durationMin: number;
  if (cfg.durationManual >= 3 && cfg.durationManual <= 20) {
    durationMin = cfg.durationManual;
  } else {
    durationMin = chooseDurationMinutes(inputChars, DURATION_RANGE_LOW, DURATION_RANGE_HIGH);
  }

  const [target, low, high] = charBudget(durationMin, cfg.charsPerMin, BUDGET_TOLERANCE);

  console.log(`[INFO] input_chars=${inputChars} duration=${durationMin}min budget=${low}-${high}`);

  let attemptHint = '';
  let lastScript: string | null = null;

  // Generate script
  for (let attempt = 1; attempt <= cfg.maxAttempts; attempt++) {
    const [systemPrompt, userPrompt] = buildPrompts(
      material,
      cfg,
      durationMin,
      target,
      low,
      high,
      attemptHint
    );

    try {
      console.log(`[LLM] Attempt ${attempt}/${cfg.maxAttempts}...`);
      const content = await callLLM(systemPrompt, userPrompt, cfg.temperature);
      lastScript = content;

      const [ok, reasons] = validateScript(content, cfg, low, high);

      if (ok) {
        break;
      }

      attemptHint = makeRetryHint(reasons, cfg, low, high);
      console.error(`[WARN] Validation failed:`, reasons.join(', '));
    } catch (error: any) {
      console.error(`[ERROR] LLM call failed: ${error.message}`);
      throw error;
    }
  }

  if (!lastScript) {
    console.error('[ERROR] No script output was generated.');
    process.exit(1);
  }

  // Write script
  const scriptPath = path.join(outDir, 'podcast_script.md');
  fs.writeFileSync(scriptPath, lastScript, 'utf-8');
  console.log(`[DONE] podcast_script.md -> ${scriptPath}`);

  // Parse segments
  const segments = scriptToSegments(lastScript, cfg.hostName, cfg.guestName);
  console.log(`[INFO] Parsed ${segments.length} segments`);

  // Generate TTS audio
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'podcast_segments_'));
  const produced: string[] = [];

  try {
    for (let i = 0; i < segments.length; i++) {
      const seg = segments[i];
      const text = seg.text.trim();
      if (!text) continue;

      let voice: string;
      if (cfg.mode === 'dual') {
        voice = seg.speaker === 'host' ? cfg.voiceHost : cfg.voiceGuest;
      } else if (cfg.mode === 'single-male') {
        voice = cfg.voiceHost;
      } else {
        voice = cfg.voiceGuest;
      }

      const wavPath = path.join(tmpDir, `seg_${seg.idx.toString().padStart(4, '0')}.wav`);

      console.log(`[TTS] [${i + 1}/${segments.length}] idx=${seg.idx} speaker=${seg.speaker} voice=${voice}`);

      const buffer = await ttsRequest(text, voice, cfg.speed);
      fs.writeFileSync(wavPath, buffer);
      produced.push(wavPath);
    }

    // Join segments
    const podcastPath = path.join(outDir, 'podcast.wav');
    console.log(`[JOIN] Joining ${produced.length} wav files -> ${podcastPath}`);

    joinWavsWave(podcastPath, produced, cfg.pauseMs);
    console.log(`[DONE] podcast.wav -> ${podcastPath}`);

  } finally {
    // Cleanup temp directory
    try {
      fs.rmSync(tmpDir, { recursive: true, force: true });
    } catch (error: any) {
      console.error(`[WARN] Failed to cleanup temp dir: ${error.message}`);
    }
  }

  console.log('\n[FINAL OUTPUT]');
  console.log(`  📄 podcast_script.md -> ${scriptPath}`);
  console.log(`  🎙️  podcast.wav       -> ${path.join(outDir, 'podcast.wav')}`);
}

main().catch(error => {
  console.error('[FATAL ERROR]', error);
  process.exit(1);
});
