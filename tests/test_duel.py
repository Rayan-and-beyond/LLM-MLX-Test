# tests/test_duel.py
import os, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import duel


def test_parse_quit_key():
    assert duel.parse_quit_key("") == "again"
    assert duel.parse_quit_key("q") == "quit"
    assert duel.parse_quit_key("Q") == "quit"
    assert duel.parse_quit_key("x") == "quit_delete"
    assert duel.parse_quit_key("X") == "quit_delete"
    assert duel.parse_quit_key("  q  ") == "quit"
    assert duel.parse_quit_key("z") == "invalid"


def test_format_results_contains_table():
    out = duel.format_results(
        {"time": 5.0, "tokens": 100, "speed": 20.0},
        {"time": 2.5, "tokens": 100, "speed": 40.0},
    )
    assert "Ollama" in out and "MLX" in out
    assert "20.0" in out and "40.0" in out


if __name__ == "__main__":
    test_parse_quit_key()
    test_format_results_contains_table()
    print("tests/test_duel.py: 2 passed")
