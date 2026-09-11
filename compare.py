import requests, json, time
from mlx_lm import load, generate, stream_generate
from mlx_lm.sample_utils import make_sampler

PROMPT = "Write 100 separate, different words describing Emma Watson."
MAX_TOKENS = 300
TEMPERATURE = 0.7
TOP_P = 0.9

# ── WARM UP MLX ─────────────────────────────────────────
print("⏳ Warming up MLX...")
model, tokenizer = load("./models/qwen2.5-mlx-instruct")
generate(model, tokenizer, prompt="hi", max_tokens=1, verbose=False)
print("✅ MLX ready\n")

sampler = make_sampler(temp=TEMPERATURE, top_p=TOP_P)

# ── OLLAMA ──────────────────────────────────────────────
print("=" * 50)
print("OLLAMA (GGUF / llama.cpp)")
print("=" * 50)
print(">>> Prompt:", PROMPT)
print("-" * 50)

start = time.time()
r = requests.post("http://localhost:11434/api/generate", json={
    "model": "qwen2.5:0.5b",
    "prompt": PROMPT,
    "stream": True,
    "options": {
        "num_predict": MAX_TOKENS,
        "temperature": TEMPERATURE,
        "top_p": TOP_P
    }
}, stream=True)

for line in r.iter_lines():
    if line:
        chunk = json.loads(line)
        print(chunk["response"], end="", flush=True)
        if chunk.get("done"):
            ollama_time = time.time() - start
            ollama_tokens = chunk.get("eval_count", 0)

# ── MLX ─────────────────────────────────────────────────
print("\n\n" + "=" * 50)
print("MLX (Apple Silicon Native)")
print("=" * 50)
print(">>> Prompt:", PROMPT)
print("-" * 50)

messages = [{"role": "user", "content": PROMPT}]
formatted_prompt = tokenizer.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True
)

mlx_tokens = 0
start = time.time()
for response in stream_generate(model, tokenizer, prompt=formatted_prompt,
                                max_tokens=MAX_TOKENS, sampler=sampler):
    print(response.text, end="", flush=True)
    mlx_tokens += 1
mlx_time = time.time() - start

# ── RESULTS ─────────────────────────────────────────────
print("\n\n" + "=" * 50)
print("📊 RESULTS")
print("=" * 50)
print(f"{'':20} {'Ollama':>10} {'MLX':>10}")
print(f"{'Max tokens':<20} {MAX_TOKENS:>10} {MAX_TOKENS:>10}")
print(f"{'Temperature':<20} {TEMPERATURE:>10} {TEMPERATURE:>10}")
print(f"{'Top P':<20} {TOP_P:>10} {TOP_P:>10}")
print("-" * 42)
print(f"{'Time':<20} {ollama_time:>9.2f}s {mlx_time:>9.2f}s")
print(f"{'Tokens generated':<20} {ollama_tokens:>10} {mlx_tokens:>10}")
print(f"{'Speed (tok/s)':<20} {ollama_tokens/ollama_time:>9.1f} {mlx_tokens/mlx_time:>9.1f}")
