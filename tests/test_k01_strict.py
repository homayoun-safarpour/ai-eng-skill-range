import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
KATA = ROOT / "katas/K01-loop-contract"
HEADINGS = ["Done", "Verifier", "Stop layers", "State file", "Irreversible"]


def run(submission, strict=False):
    args = [sys.executable, "-m", "skillrange", "grade", "K01", "--submission", str(submission)]
    if strict:
        args.append("--strict")
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=True)


@pytest.mark.parametrize("body", ["", "   ", "<!-- fill later -->", "<!--\nfill later\n-->"])
def test_empty_verifier_is_strict_only_failure(tmp_path, body):
    text = "\n\n".join(
        f"## {index}. {name}\n{body if name == 'Verifier' else 'A concrete decision.'}"
        for index, name in enumerate(HEADINGS, 1)
    )
    (tmp_path / "LOOP_CONTRACT.md").write_text(text, encoding="utf-8")
    assert run(tmp_path).returncode == 0
    result = run(tmp_path, strict=True)
    assert result.returncode == 2
    assert "## 2. Verifier" in result.stdout


def test_strict_golden_pass_and_missing_headings():
    assert run(KATA / "fixtures/pass", strict=True).returncode == 0
    assert run(KATA / "fixtures/fail", strict=True).returncode == 2


def test_named_empty_verifier_fixture():
    submission = KATA / "fixtures/empty-verifier"
    assert run(submission).returncode == 0
    result = run(submission, strict=True)
    assert result.returncode == 2
    assert "## 2. Verifier" in result.stdout


def test_strict_does_not_count_comment_or_next_heading(tmp_path):
    text = "\n\n".join(f"## {i}. {name}\nDecision." for i, name in enumerate(HEADINGS, 1))
    text = text.replace("## 2. Verifier\nDecision.", "## 2. Verifier\n<!-- later -->\n### Notes\nUnrelated.")
    (tmp_path / "LOOP_CONTRACT.md").write_text(text, encoding="utf-8")
    result = run(tmp_path, strict=True)
    assert result.returncode == 2
    assert "FAIL: empty sections:" in result.stdout
