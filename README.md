# MLX-Testing — Apple Silicon LLM Duel: MLX vs Ollama

## Purpose

Two ways to run the same open-weight LLM locally on a Mac — Apple's
[MLX](https://github.com/ml-explore/mlx) framework (`mlx-lm`, built for Apple
Silicon) versus [Ollama](https://ollama.com) (GGUF via llama.cpp) — but which
is actually faster on your chip?

This repo answers that with a fair fight: one command feeds **your prompt**
to **both** runners with **identical limits** (300 tokens, temperature 0.7,
top-p 0.9, Qwen2.5-0.5B-Instruct) and prints a head-to-head table of wall time,
tokens generated, and tokens/sec. MLX gets a one-token warmup first so cold
load doesn't skew the numbers; inference itself runs fully in memory, so the
comparison measures the engines, not your disk.

## Prerequisites

- macOS on Apple Silicon
- Python 3.14 with `venv`
- [Ollama](https://ollama.com) (`brew install ollama`)

## Quickstart

```bash
pip install -r requirements.txt
./setup.sh
MLX-Testing
```

Type a prompt at `Enter prompt >`. After each duel:

| Key     | Action                              |
|---------|-------------------------------------|
| `ENTER` | Another round                       |
| `Q`     | Quit, keep downloaded data          |
| `X`     | Quit and delete local test downloads|

`Ctrl+C` quits like `Q`. The Ollama server is started on demand and always
killed on exit. `X` deletes only the Ollama model blob (re-pulled next run) —
never your venv, code, or stored weights.

---

## Self-test (no models needed)

```bash
venv/bin/python duel.py --self-test
MLX-Testing --self-test
```
