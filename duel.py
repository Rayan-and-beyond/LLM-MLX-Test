# duel.py (helpers; full loop arrives in Task 2)
BANNER = """\
*** MLX-Testing -- Apple Silicon Duel: MLX vs Ollama (Qwen2.5-0.5B) ***
Same prompt, same limits, head-to-head tok/s. Ollama auto-starts/kills.
"""

PROMPT = "Write 100 separate, different words describing Emma Watson."
MAX_TOKENS = 300
TEMPERATURE = 0.7
TOP_P = 0.9
OLLAMA_MODEL = "qwen2.5:0.5b"
MLX_MODEL_DIR = "./models/qwen2.5-mlx-instruct"


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
