# MLX-Testing — Apple Silicon LLM Duel: MLX vs Ollama

One command. Same prompt. Same limits. Head-to-head tokens/sec for
`mlx-lm` (Apple Silicon native) vs Ollama (GGUF) on your Mac.

Apple Silicon only. No background daemons left running.

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
