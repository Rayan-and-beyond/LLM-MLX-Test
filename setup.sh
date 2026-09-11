#!/usr/bin/env bash
# MLX-Testing ensure script. Run by the USER (Drive needs their session).
set -euo pipefail
REPO="$(cd "$(dirname "$0")" && pwd)"
HF_ID="mlx-community/Qwen2.5-0.5B-Instruct-4bit"
MODEL_SUB="qwen2.5-mlx-instruct"
OLLAMA_MODEL="qwen2.5:0.5b"
CHECK_ONLY=0
[ "${1:-}" = "--check-only" ] && CHECK_ONLY=1

DRIVE_DIR=""
[ -f "$REPO/config.local.json" ] && DRIVE_DIR="$("$REPO/venv/bin/python" -c "import json;print(json.load(open('$REPO/config.local.json')).get('drive_models_dir',''))" 2>/dev/null || true)" || true
TARGET="${MLX_MODEL_DIR:-${DRIVE_DIR:-$REPO/models}/$MODEL_SUB}"
[ -d "$REPO/models" ] && [ ! -L "$REPO/models" ] && [ -n "$DRIVE_DIR" ] && [ "$CHECK_ONLY" = 0 ] && mkdir -p "$DRIVE_DIR" && cp -r "$REPO/models/." "$DRIVE_DIR/" && rm -rf "$REPO/models" || true
[ -n "$DRIVE_DIR" ] && [ ! -e "$REPO/models" ] && [ "$CHECK_ONLY" = 0 ] && mkdir -p "$DRIVE_DIR" && ln -s "$DRIVE_DIR" "$REPO/models" || true

if [ ! -f "$TARGET/model.safetensors" ]; then
  [ "$CHECK_ONLY" = 1 ] && { echo "SETUP: weights missing at $TARGET (run setup.sh to fetch)"; exit 0; }
  "$REPO/venv/bin/python" -c "from huggingface_hub import snapshot_download; snapshot_download('$HF_ID', local_dir='$TARGET')"
fi
command -v ollama >/dev/null || { echo "SETUP: install ollama: brew install ollama"; exit 1; }
if ! curl -sf --max-time 2 http://localhost:11434/api/tags >/dev/null 2>&1; then
  ollama serve >/tmp/mlx-testing-ollama.log 2>&1 &
  for _ in $(seq 1 30); do curl -sf --max-time 2 http://localhost:11434/api/tags >/dev/null 2>&1 && break; sleep 1; done
fi
ollama list 2>/dev/null | grep -q "qwen2.5" || ollama pull "$OLLAMA_MODEL"
echo "SETUP: OK ($TARGET)"
