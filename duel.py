"""MLX-Testing -- Apple Silicon duel: MLX vs Ollama (Qwen2.5-0.5B)."""
import json, os, sys, time

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


QUIT_DELETE = "\x18"  # Ctrl+X


def ask(text):
    """Read one prompt line. Returns None on Ctrl+C/EOF (quit),
    "DELETE" on Ctrl+X (quit + delete downloads), else the typed line."""
    if not sys.stdin.isatty():
        try:
            line = input(text)
        except (KeyboardInterrupt, EOFError):
            return None
        if line.strip() == QUIT_DELETE:
            return "DELETE"
        return line
    import termios, tty
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    buf = []
    try:
        tty.setcbreak(fd)
        os.write(sys.stdout.fileno(), text.encode())
        sys.stdout.flush()
        while True:
            ch = os.read(fd, 32).decode("utf-8", "replace")
            if not ch:
                return None
            ch = ch[0]
            if ch == "\x03":
                raise KeyboardInterrupt
            if ch == QUIT_DELETE:
                os.write(sys.stdout.fileno(), b"\n")
                return "DELETE"
            if ch in ("\n", "\r"):
                os.write(sys.stdout.fileno(), b"\n")
                break
            if ch == "\x7f":
                if buf:
                    buf.pop()
                    os.write(sys.stdout.fileno(), b"\b \b")
                continue
            if ch < " ":
                continue
            buf.append(ch)
            os.write(sys.stdout.fileno(), ch.encode())
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return "".join(buf)


def main():
    print(BANNER, flush=True)
    print("Loading the model...", flush=True)
    print("(First run loads ~300MB into memory - give it a minute.)", flush=True)
    model, tokenizer = load(MLX_MODEL_DIR)
    print("Warming up the engines...", flush=True)
    generate(model, tokenizer, prompt="hi", max_tokens=1, verbose=False)
    sampler = make_sampler(temp=TEMPERATURE, top_p=TOP_P)
    print("Ready. Let's duel.")
    print("(Ctrl+C quits - Ctrl+X quits + deletes downloads)\n")
    while True:
        print()
        raw = ask("Enter prompt > ")
        if raw is None:
            print("\n" + GOODBYES[0])
            return 0
        if raw == "DELETE":
            print("Deleting test downloads...")
            return 42
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


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\n" + GOODBYES[0])
        raise SystemExit(0)
