// Video generation via an OpenAI-compatible server (async task API).
// Convention used here (documented, env-configurable):
//   - Create task:  POST {LLM_BASE_URL}/videos/generations
//   - Poll status:  GET  {LLM_BASE_URL}/videos/generations/{task_id}
// Supported by OpenAI-compatible gateways fronting open-source video models
// (e.g. Wan 2.x, CogVideoX, HunyuanVideo) and by aggregation gateways. The
// exact model id depends on your server - set VIDEO_MODEL.
//
// Configuration (environment variables):
//   LLM_BASE_URL - OpenAI-compatible base URL (default: http://localhost:11434/v1)
//   LLM_API_KEY  - API key sent as a Bearer token (default: empty)
//   VIDEO_MODEL  - video model name (default: wan2.1)

import fs from "fs";

const BASE_URL = process.env.LLM_BASE_URL ?? "http://localhost:11434/v1";
const API_KEY = process.env.LLM_API_KEY ?? "";
const VIDEO_MODEL = process.env.VIDEO_MODEL ?? "wan2.1";

function authHeaders(): Record<string, string> {
  return {
    "Content-Type": "application/json",
    ...(API_KEY ? { Authorization: `Bearer ${API_KEY}` } : {}),
  };
}

async function createVideoTask(body: Record<string, unknown>): Promise<any> {
  const res = await fetch(`${BASE_URL}/videos/generations`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({ model: VIDEO_MODEL, ...body }),
  });
  if (!res.ok) throw new Error(`Video task creation failed (${res.status}): ${await res.text()}`);
  return res.json();
}

async function queryVideoTask(taskId: string): Promise<any> {
  const res = await fetch(`${BASE_URL}/videos/generations/${taskId}`, {
    method: "GET",
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error(`Video task query failed (${res.status}): ${await res.text()}`);
  return res.json();
}

async function create() {
  try {
    console.log("Creating video generation task...");

    const task = await createVideoTask({
      prompt: "A cat is playing with a ball.",
      quality: "speed",
      with_audio: false,
      size: "1920x1080",
      fps: 30,
      duration: 5,
    });

    console.log(`Task created!`);
    console.log(`Task ID: ${task.id}`);
    console.log(`Task Status: ${task.task_status}`);
    console.log(`Model: ${task.model || 'N/A'}`);

    return { task };
  } catch (err: any) {
    console.error("Video generation failed:", err?.message || err);
    throw err;
  }
}

/**
 * Example: Image-to-Video Generation using base64
 * IMPORTANT: Using base64-encoded image data is STRONGLY RECOMMENDED over URLs
 * for better reliability and to avoid network-related issues.
 *
 * CRITICAL: Always match the MIME type to your actual image format.
 */
async function createFromImage(imagePath: string) {
  try {
    console.log("Creating image-to-video generation task...");
    console.log(`Reading image from: ${imagePath}`);

    // Read image file and convert to base64
    const imageBuffer = fs.readFileSync(imagePath);

    // Detect MIME type from file extension
    const imageExt = imagePath.split('.').pop()?.toLowerCase() || '';
    const mimeTypeMap: Record<string, string> = {
      'jpg': 'image/jpeg',
      'jpeg': 'image/jpeg',
      'png': 'image/png',
      'gif': 'image/gif',
      'webp': 'image/webp',
      'bmp': 'image/bmp'
    };
    const mimeType = mimeTypeMap[imageExt] || 'image/jpeg';  // Default to JPEG if unknown

    const base64Image = `data:${mimeType};base64,${imageBuffer.toString('base64')}`;

    console.log(`Image format detected: ${mimeType}`);
    console.log(`Image converted to base64 (${base64Image.substring(0, 50)}...)`);

    // Create video generation task with base64 image
    const task = await createVideoTask({
      image_url: base64Image,  // Use base64 with correct MIME type
      prompt: "Animate this scene with gentle motion",
      quality: "quality",
      size: "1920x1080",
      fps: 30,
      duration: 5,
    });

    console.log(`Task created!`);
    console.log(`Task ID: ${task.id}`);
    console.log(`Task Status: ${task.task_status}`);
    console.log(`Model: ${task.model || 'N/A'}`);

    return { task };
  } catch (err: any) {
    console.error("Image-to-video generation failed:", err?.message || err);
    throw err;
  }
}

async function query(taskId: string) {
  try {
    // First query
    let result = await queryVideoTask(taskId);

    if (result.task_status === 'SUCCESS') {
      // If the task finished immediately, return the result directly
      console.log("\nTask completed immediately, fetching result...");
      displayResult(result);
      return result;
    }

    // Poll for the result
    console.log("\nPolling for result...");
    let pollCount = 0;
    const maxPolls = 30; // Poll at most 30 times
    const pollInterval = 10000; // Query every 10 seconds

    while (result.task_status === 'PROCESSING' && pollCount < maxPolls) {
      pollCount++;
      console.log(`Poll ${pollCount}/${maxPolls}: Status is ${result.task_status}, waiting ${pollInterval / 1000}s...`);
      await new Promise(resolve => setTimeout(resolve, pollInterval));
      result = await queryVideoTask(taskId);
    }

    displayResult(result);
    return result;
  } catch (err: any) {
    console.error("Query failed:", err?.message || err);
    throw err;
  }
}

async function main() {
  try {
    // Method 1: Text-to-Video (default)
    const { task } = await create();

    // Method 2: Image-to-Video with base64 (RECOMMENDED for image input)
    // Uncomment the lines below and comment out the lines above to use image-to-video
    // Make sure to provide a valid image path
    // const { task } = await createFromImage('./path/to/your/image.jpg');

    await query(task.id);
  } catch (err: any) {
    console.error("Video generation failed:", err?.message || err);
    process.exit(1);
  }
}

function displayResult(result: any) {
  console.log("\n=== Result ===");
  console.log(`Task Status: ${result.task_status}`);
  console.log(`Model: ${result.model || 'N/A'}`);
  console.log(`Request ID: ${result.request_id || 'N/A'}`);

  if (result.task_status === 'SUCCESS') {
    // Try to get the video URL from several possible fields
    const videoUrl =
      result.video_result?.[0]?.url ||
      result.video_url ||
      result.url ||
      result.video;

    if (videoUrl) {
      console.log(`\n✅ Video generated successfully!`);
      console.log(`Video URL: ${videoUrl}`);
      console.log(`\nYou can open this URL in your browser or download it.`);
    } else {
      console.log(`\n⚠️ Task completed but video URL not found in response.`);
      console.log(`Full response:`, JSON.stringify(result, null, 2));
    }
  } else if (result.task_status === 'PROCESSING') {
    console.log(`\n⏳ Task is still processing. Please try again later.`);
    console.log(`Task ID: ${result.id || 'N/A'}`);
  } else if (result.task_status === 'FAIL') {
    console.log(`\n❌ Task failed.`);
    console.log(`Full response:`, JSON.stringify(result, null, 2));
  }
}

main();
