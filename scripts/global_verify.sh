#!/usr/bin/env bash
# Global verification: no CJK, no z.ai/GLM branding in any text file under skills/
cd /home/z/my-project/skills || exit 1

echo "=== 1. CJK check (text files) ==="
find . -type f ! -name "*.jpg" ! -name "*.jpeg" ! -name "*.png" ! -name "*.webp" \
  ! -name "*.gif" ! -name "*.pyc" ! -name "*.woff" ! -name "*.woff2" ! -name "*.ttf" \
  ! -name "*.otf" ! -name "*.ico" ! -name "*.mp3" ! -name "*.mp4" ! -name "*.pdf" \
  -print0 | xargs -0 grep -lP '[\x{4e00}-\x{9fff}\x{3000}-\x{303f}\x{ff00}-\x{ffef}]' 2>/dev/null
echo "CJK done (empty = clean)"

echo "=== 2. Brand check ==="
find . -type f ! -name "*.jpg" ! -name "*.jpeg" ! -name "*.png" ! -name "*.webp" \
  ! -name "*.gif" ! -name "*.pyc" ! -name "*.woff" ! -name "*.woff2" ! -name "*.ttf" \
  ! -name "*.otf" ! -name "*.ico" ! -name "*.mp3" ! -name "*.mp4" ! -name "*.pdf" \
  -print0 | xargs -0 grep -liE 'z-ai-web-dev-sdk|z\.ai|bigmodel\.cn|chatglm|zhipu|智谱|清言|qingyan|zai-org' 2>/dev/null
echo "Brand done (empty = clean)"

echo "=== 3. GLM model check ==="
find . -type f ! -name "*.jpg" ! -name "*.jpeg" ! -name "*.png" ! -name "*.webp" \
  ! -name "*.gif" ! -name "*.pyc" ! -name "*.woff" ! -name "*.woff2" ! -name "*.ttf" \
  ! -name "*.otf" ! -name "*.ico" ! -name "*.mp3" ! -name "*.mp4" ! -name "*.pdf" \
  -print0 | xargs -0 grep -lE 'GLM-[0-9]|glm-[0-9]|\bGLM\b' 2>/dev/null
echo "GLM done (empty = clean)"
