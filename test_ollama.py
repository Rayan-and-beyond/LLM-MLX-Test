import requests
import json
import time

PROMPT = "Explain what makes Emma Watson amazing  in 3 sentences."

print(">>> Prompt:", PROMPT)
print("-" * 50)

start = time.time()
r = requests.post("http://localhost:11434/api/generate", json={
    "model": "qwen2.5:0.5b",
    "prompt": PROMPT,
    "stream": True
}, stream=True)

for line in r.iter_lines():
    if line:
        chunk = json.loads(line)
        print(chunk["response"], end="", flush=True)
        if chunk.get("done"):
            elapsed = time.time() - start
            tokens = chunk.get("eval_count", 0)
            print("\\n" + "=" * 50)
            print("📦 Model  : qwen2.5:0.5b (Ollama / GGUF)")
            print(f"⏱  Time   : {elapsed:.2f}s")
            print(f"🔢 Tokens : {tokens}")
            print(f"⚡ Speed  : {tokens / elapsed:.1f} tok/s")
