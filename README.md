# 🥊 MLX-Testing

**Which is faster on your Mac — MLX or Ollama? Let's find out.**

There are two popular ways to run an AI model locally on Apple Silicon.
This tool runs your prompt through **both**, side by side, and shows you
who wins — in plain numbers.

---

## What it does

You type one prompt. It gets answered twice:

1. once by **MLX** (Apple's own AI framework, built for Mac chips)
2. once by **Ollama** (the popular app for running models locally)

Both get the exact same model and the exact same settings, so the race is
fair. At the end you get a simple scoreboard:

```text
                     Ollama        MLX
Time                   5.00s      2.50s
Tokens generated         100        100
Speed (tok/s)           20.0       40.0
```

Bigger speed number = faster. That's it.

---

## What you need

- A Mac with an Apple Silicon chip (M1, M2, M3, …)
- Python 3.14
- Ollama — install it with:

```bash
brew install ollama
```

---

## How to run it

```bash
pip install -r requirements.txt
./setup.sh
MLX-Testing
```

The first run downloads what it needs, then asks for your prompt:

```text
Enter prompt >
```

After each round, pick what to do next:

| Key     | What happens                              |
|---------|-------------------------------------------|
| `ENTER` | Go again with a new prompt                |
| `Q`     | Quit (keeps everything it downloaded)     |
| `X`     | Quit and delete the downloaded test files |

`Ctrl+C` quits just like `Q`. Nothing keeps running in the background
after you leave.

---

## Try it without downloading anything

```bash
MLX-Testing --self-test
```

Shows you what a duel looks like, using fake numbers. No models needed.
