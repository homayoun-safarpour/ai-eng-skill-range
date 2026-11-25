"""Behaviour tests for the graders and the grade command (code review of 25 Nov 2026).

A grader holds its own expected answers and hidden cases. It never reads the expected
result from the submission. Each fixed grader has a `fixtures/cheat*` folder that used
to pass and must now fail.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from skillrange.cli import find_kata, load_grade_fn, main

ROOT = Path(__file__).resolve().parents[1]
KATAS = ROOT / "katas"


def _grade(kata_id: str, submission: Path) -> int:
    return main(["grade", kata_id, "--submission", str(submission)])


def _write(base: Path, rel: str, body: str) -> Path:
    path = base / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return base


# Finding 1: K02 read the expected answer from the submission's own status.json.


def test_k02_gate_that_always_exits_0_fails(tmp_path):
    sub = _write(tmp_path, "gate.py", "import sys\nsys.exit(0)\n")
    _write(sub, "status.json", '{"ok": true}')
    assert _grade("K02", sub) == 2


def test_k02_gate_that_ignores_missing_status_file_fails(tmp_path):
    body = (
        "import json, sys\n"
        "from pathlib import Path\n"
        "ok = json.loads(Path('status.json').read_text())['ok']\n"
        "sys.exit(0 if ok is True else 2)\n"
    )
    sub = _write(tmp_path, "gate.py", body)
    assert _grade("K02", sub) == 2


def test_k02_gate_that_treats_non_bool_ok_as_true_fails(tmp_path):
    body = (
        "import json, sys\n"
        "from pathlib import Path\n"
        "p = Path('status.json')\n"
        "if not p.is_file():\n"
        "    sys.exit(2)\n"
        "sys.exit(0 if json.loads(p.read_text()).get('ok') else 2)\n"
    )
    sub = _write(tmp_path, "gate.py", body)
    assert _grade("K02", sub) == 2


def test_k02_cheat_fixture_fails():
    assert _grade("K02", KATAS / "K02-exit-code-gate" / "fixtures" / "cheat") == 2


# Finding 8: K02 ran the gate with no timeout.


def test_k02_looping_gate_fails_on_timeout(tmp_path):
    sub = _write(tmp_path, "gate.py", "while True:\n    pass\n")
    grade = load_grade_fn(find_kata("K02"))
    grade.__globals__["TIMEOUT_S"] = 1
    assert grade(sub) == 2


# Finding 2: K18 checked only perfect agreement.


def test_k18_constant_one_fails(tmp_path):
    sub = _write(tmp_path, "kappa.py", 'def weighted_kappa(y1, y2, weights="linear"):\n    return 1.0\n')
    assert _grade("K18", sub) == 2


def test_k18_quadratic_weights_fail(tmp_path):
    body = (KATAS / "K18-weighted-kappa-ordinal" / "fixtures" / "pass" / "kappa.py").read_text(encoding="utf-8")
    body = body.replace("abs(i - j) / (k - 1)", "(abs(i - j) / (k - 1)) ** 2")
    sub = _write(tmp_path, "kappa.py", body)
    assert _grade("K18", sub) == 2


def test_k18_cheat_fixture_fails():
    assert _grade("K18", KATAS / "K18-weighted-kappa-ordinal" / "fixtures" / "cheat") == 2


# Finding 3: K01 passed empty headings and headings hidden in an HTML comment.

HEADINGS = "## 1. Done\n## 2. Verifier\n## 3. Stop layers\n## 4. State file\n## 5. Irreversible\n"


def test_k01_empty_headings_fail(tmp_path):
    sub = _write(tmp_path, "LOOP_CONTRACT.md", HEADINGS)
    assert _grade("K01", sub) == 2


def test_k01_headings_inside_html_comment_fail(tmp_path):
    sub = _write(tmp_path, "LOOP_CONTRACT.md", "<!--\n" + HEADINGS + "-->\n")
    assert _grade("K01", sub) == 2


def test_k01_sections_filled_with_html_comments_only_fail(tmp_path):
    body = "".join(f"{h}\n<!-- todo -->\n" for h in HEADINGS.splitlines())
    sub = _write(tmp_path, "LOOP_CONTRACT.md", body)
    assert _grade("K01", sub) == 2


def test_k01_headings_inside_code_fence_fail(tmp_path):
    body = "```\n" + "".join(f"{h}\ntext\n" for h in HEADINGS.splitlines()) + "```\n"
    sub = _write(tmp_path, "LOOP_CONTRACT.md", body)
    assert _grade("K01", sub) == 2


@pytest.mark.parametrize("name", ["cheat", "cheat_comment"])
def test_k01_cheat_fixtures_fail(name):
    assert _grade("K01", KATAS / "K01-loop-contract" / "fixtures" / name) == 2


# Finding 4: an unknown kata id gave a traceback and exit 1.


@pytest.mark.parametrize("kata_id", ["K99", "", "K", "loop"])
def test_unknown_kata_id_fails_with_exit_2(kata_id, capsys):
    assert main(["grade", kata_id]) == 2
    assert f"FAIL: unknown kata: {kata_id}" in capsys.readouterr().err


# Finding 5: malformed submission JSON crashed graders with exit 1.


def test_malformed_json_in_k07_fails_with_exit_2(tmp_path, capsys):
    sub = _write(tmp_path, "stop_layers.json", "not json")
    assert _grade("K07", sub) == 2
    assert "FAIL: grader error:" in capsys.readouterr().err


def test_wrong_json_shape_in_k16_fails_with_exit_2(tmp_path, capsys):
    sub = _write(tmp_path, "checkpoints.json", '["a", "b"]')
    assert _grade("K16", sub) == 2
    assert "FAIL: grader error:" in capsys.readouterr().err


# Finding 6: K04 accepted a function that is not Cohen kappa.


def test_k04_plus_or_minus_one_fails(tmp_path):
    sub = _write(tmp_path, "kappa.py", "def cohen_kappa(a, b):\n    return 1.0 if a == b else -1.0\n")
    assert _grade("K04", sub) == 2


def test_k04_nan_for_constant_raters_fails(tmp_path):
    body = (KATAS / "K04-judge-kappa-pair" / "fixtures" / "pass" / "kappa.py").read_text(encoding="utf-8")
    body = body.replace("return 1.0\n    return (po", "return float('nan')\n    return (po")
    sub = _write(tmp_path, "kappa.py", body)
    assert _grade("K04", sub) == 2


def test_k04_cheat_fixture_fails():
    assert _grade("K04", KATAS / "K04-judge-kappa-pair" / "fixtures" / "cheat") == 2


# Finding 7: K23 passed a workflow that mentions pytest only in a comment.


def test_k23_pytest_only_in_comment_fails(tmp_path):
    sub = _write(tmp_path, ".github/workflows/ci.yml", "# we do not run pytest here\njobs: {}\n")
    assert _grade("K23", sub) == 2


def test_k23_pytest_in_multiline_run_block_passes(tmp_path):
    body = (
        "name: CI\n"
        "jobs:\n"
        "  test:\n"
        "    runs-on: ubuntu-latest\n"
        "    steps:\n"
        "      - uses: actions/checkout@v4\n"
        "      - name: tests\n"
        "        run: |\n"
        "          pip install -e .\n"
        "          python -m pytest -q\n"
    )
    sub = _write(tmp_path, ".github/workflows/ci.yml", body)
    assert _grade("K23", sub) == 0


def test_k23_cheat_fixture_fails():
    assert _grade("K23", KATAS / "K23-ci-workflow-assert" / "fixtures" / "cheat") == 2
