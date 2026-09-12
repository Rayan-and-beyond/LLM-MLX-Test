# Contributing

One prompt, two engines, identical rules. A contribution that makes the race unfair is worse than no contribution.

Before opening a pull request:

```bash
python -m pytest tests/ -q
```

Rules:

- Both sides get the exact same model, prompt, and limits. If your change touches measurement, show the scoreboard before and after on the same machine.
- Keep the portable core portable. `tests/test_duel.py` must pass on Linux CI with no MLX, no Ollama, no model downloads. CI stubs `mlx_lm` with no-op callables so the pure functions import cleanly. Mac-only code stays behind the runner flags.
- Bigger speed number = faster. Keep the output that plain: time, tokens, tok/s. No new columns without updating the README's example table and the mermaid diagram.
- New engine support (beyond MLX/Ollama) starts as an issue with your scoreboard numbers first — PR second.
