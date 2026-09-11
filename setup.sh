#!/usr/bin/env bash
# MLX-Testing ensure script. Fetches anything missing, then reports OK.
set -euo pipefail
REPO="$(cd "$(dirname "$0")" && pwd)"
HF_ID="mlx-community/Qwen2.5-0.5B-Instruct-4bit"
MODEL_SUB="qwen2.5-mlx-instruct"
OLLAMA_MODEL="qwen2.5:0.5b"
CHECK_ONLY=0
[ "${1:-}" = "--check-only" ] && CHECK_ONLY=1

TARGET="$REPO/models/$MODEL_SUB"

if [ ! -f "$TARGET/model.safetensors" ]; then
  [ "$CHECK_ONLY" = 1 ] && { echo "SETUP: weights missing at $TARGET"; exit 1; }
  "$REPO/venv/bin/python" -c "from huggingface_hub import snapshot_download; snapshot_download('$HF_ID', local_dir='$TARGET')"
fi
command -v ollama >/dev/null || { echo "SETUP: install ollama: brew install ollama"; exit 1; }
if ! curl -sf --max-time 2 http://localhost:11434/api/tags >/dev/null 2>&1; then
  ollama serve >/tmp/mlx-testing-ollama.log 2>&1 &
  for _ in $(seq 1 30); do curl -sf --max-time 2 http://localhost:11434/api/tags >/dev/null 2>&1 && break; sleep 1; done
fi
ollama list 2>/dev/null | grep -q "qwen2.5" || ollama pull "$OLLAMA_MODEL"
echo "SETUP: OK ($TARGET)"
