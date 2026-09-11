"""MLX-Testing -- Apple Silicon duel: MLX vs Ollama (Qwen2.5-0.5B)."""
import json, os, time

import requests
from mlx_lm import load, generate, stream_generate
from mlx_lm.sample_utils import make_sampler

BANNER = """\
*** MLX-Testing -- Apple Silicon Duel: MLX vs Ollama (Qwen2.5-0.5B) ***
Same prompt. Same model. Two engines. One winner.
"""

PROMPT = "Write 100 separate, different words describing Emma Watson."
MAX_TOKENS = 300
TEMPERATURE = 0.7
TOP_P = 0.9
OLLAMA_MODEL = "qwen2.5:0.5b"
MLX_MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "models", "qwen2.5-mlx-instruct")

GOODBYES = [
    "Goodbye! Go touch grass - your Mac did the heavy lifting.",
    "Goodbye! The duel is over... until next prompt.",
]


def parse_quit_key(s):
    k = (s or "").strip().lower()
    if k == "":
        return "again"
    if k == "q":
        return "quit"
    if k == "x":
        return "quit_delete"
    return "invalid"


def format_results(ollama, mlx):
    return (
        "\n" + "=" * 50 + "\n"
        "RESULTS\n" + "=" * 50 + "\n"
        f"{'':20} {'Ollama':>10} {'MLX':>10}\n"
        f"{'Time':<20} {ollama['time']:>9.2f}s {mlx['time']:>9.2f}s\n"
        f"{'Tokens generated':<20} {ollama['tokens']:>10} {mlx['tokens']:>10}\n"
        f"{'Speed (tok/s)':<20} {ollama['speed']:>9.1f} {mlx['speed']:>9.1f}\n"
    )


def run_ollama(prompt):
    start = time.time()
    r = requests.post("http://localhost:11434/api/generate", json={
        "model": OLLAMA_MODEL, "prompt": prompt, "stream": True,
        "options": {"num_predict": MAX_TOKENS,
                    "temperature": TEMPERATURE, "top_p": TOP_P},
    }, stream=True, timeout=120)
    r.raise_for_status()
    tokens = 0
    for line in r.iter_lines():
        if line:
            chunk = json.loads(line)
            print(chunk.get("response", ""), end="", flush=True)
            if chunk.get("done"):
                tokens = chunk.get("eval_count", 0)
    elapsed = time.time() - start
    return {"time": elapsed, "tokens": tokens,
            "speed": tokens / elapsed if elapsed else 0.0}


def run_mlx(model, tokenizer, sampler, prompt):
    messages = [{"role": "user", "content": prompt}]
    formatted = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True)
    n = 0
    start = time.time()
    for resp in stream_generate(model, tokenizer, prompt=formatted,
                                max_tokens=MAX_TOKENS, sampler=sampler):
        print(resp.text, end="", flush=True)
        n += 1
    elapsed = time.time() - start
    return {"time": elapsed, "tokens": n,
            "speed": n / elapsed if elapsed else 0.0}


def ask(text):
    try:
        return input(text)
    except (KeyboardInterrupt, EOFError):
        return None


def main():
    print(BANNER, flush=True)
    print("Loading the model...", flush=True)
    print("(First run loads ~300MB into memory - give it a minute.)", flush=True)
    model, tokenizer = load(MLX_MODEL_DIR)
    print("Warming up the engines...", flush=True)
    generate(model, tokenizer, prompt="hi", max_tokens=1, verbose=False)
    sampler = make_sampler(temp=TEMPERATURE, top_p=TOP_P)
    print("Ready. Let's duel.\n")
    while True:
        print()
        raw = ask("Enter prompt > ".center(60))
        if raw is None:
            print("\n" + GOODBYES[0])
            return 0
        prompt = raw.strip()
        print()
        if not prompt:
            print("Empty prompt - try again.")
            continue
        print("\n--- Ollama ---\n")
        o = run_ollama(prompt)
        print("\n\n--- MLX ---\n")
        m = run_mlx(model, tokenizer, sampler, prompt)
        print(format_results(o, m))
        while True:
            print()
            print("[ENTER] Another round")
            print()
            print("[Q] Quit")
            print()
            print("[X] Quit + delete downloads")
            print()
            raw = ask("> ")
            if raw is None:
                print("\n" + GOODBYES[0])
                return 0
            key = parse_quit_key(raw)
            if key == "again":
                break
            if key == "quit":
                print(GOODBYES[0])
                return 0
            if key == "quit_delete":
                print("DELETE-REQUESTED")
                return 42
            print("Press ENTER, Q, or X.")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\n" + GOODBYES[0])
        raise SystemExit(0)
