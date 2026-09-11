import time
import requests
from mlx_lm import load, generate

PROMPT = "Explain what a transformer neural network is in 3 sentences."

# ── OLLAMA ──────────────────────────────────────────────
print("=" * 50)
print("OLLAMA (GGUF / llama.cpp)")
print("=" * 50)

start = time.time()
r = requests.post("http://localhost:11434/api/generate", json={
    "model": "qwen2.5:0.5b",
    "prompt": PROMPT,
    "stream": False
})
ollama_time = time.time() - start
data = r.json()
ollama_tokens = data.get("eval_count", 0)

print(data["response"])
print(f"\n⏱  Time : {ollama_time:.2f}s")
print(f"🔢 Tokens: {ollama_tokens}")
print(f"⚡ Speed : {ollama_tokens / ollama_time:.1f} tok/s")

# ── MLX ─────────────────────────────────────────────────
print("\n" + "=" * 50)
print("MLX (Apple Silicon Native)")
print("=" * 50)

model, tokenizer = load("./models/qwen2.5-mlx")

start = time.time()
response = generate(model, tokenizer, prompt=PROMPT, max_tokens=150, verbose=False)
mlx_time = time.time() - start
mlx_tokens = len(tokenizer.encode(response))

print(response)
print(f"\n⏱  Time : {mlx_time:.2f}s")
print(f"🔢 Tokens: ~{mlx_tokens}")
print(f"⚡ Speed : {mlx_tokens / mlx_time:.1f} tok/s")
