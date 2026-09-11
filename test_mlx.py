from mlx_lm import load, generate
import time

PROMPT = "Explain what makes Emma Watson amazing in 3 sentences."

print(">>> Prompt:", PROMPT)
print("-" * 50)

model, tokenizer = load("./models/qwen2.5-mlx-instruct")

start = time.time()
response = generate(model, tokenizer, prompt=PROMPT, max_tokens=150, verbose=True)
elapsed = time.time() - start
tokens = len(tokenizer.encode(response))

print("\\n" + "=" * 50)
print("📦 Model  : Qwen2.5-0.5B-Instruct-4bit (MLX)")
print(f"⏱  Time   : {elapsed:.2f}s")
print(f"🔢 Tokens : ~{tokens}")
print(f"⚡ Speed  : {tokens / elapsed:.1f} tok/s")
