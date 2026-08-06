"""Meta-tests for skill map completeness and kata contracts."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "skills" / "SKILL_MAP.md"
KATAS = ROOT / "katas"

REQUIRED_FILES = [
    "BRIEF.md",
    "SKILL.md",
    "rubric.md",
    "grader/run.py",
    "starter",
    "fixtures/fail",
    "fixtures/pass",
]


def test_skill_map_has_56_ids():
    text = MAP.read_text(encoding="utf-8")
    # Cluster tables use "| C1.S1 | description |" — kata index may repeat a lone skill id.
    ids = re.findall(r"\| (C\d\.S\d) \|", text)
    assert len(set(ids)) == 56, f"expected 56 unique skills, got {len(set(ids))}"
    for c in range(1, 8):
        for s in range(1, 9):
            assert f"C{c}.S{s}" in ids


def test_twenty_four_katas_present():
    dirs = sorted(p for p in KATAS.iterdir() if p.is_dir() and p.name.startswith("K"))
    assert len(dirs) == 24, f"expected 24 katas, got {len(dirs)}: {[d.name for d in dirs]}"


def test_each_kata_has_contract_files():
    for path in sorted(KATAS.iterdir()):
        if not path.is_dir() or not path.name.startswith("K"):
            continue
        for rel in REQUIRED_FILES:
            assert (path / rel).exists(), f"{path.name} missing {rel}"


def test_golden_pass_and_fail_exit_codes():
    dirs = sorted(p for p in KATAS.iterdir() if p.is_dir() and p.name.startswith("K"))
    for path in dirs:
        kid = path.name.split("-", 1)[0]
        fail = subprocess.run(
            [sys.executable, "-m", "skillrange", "grade", kid, "--submission", str(path / "fixtures" / "fail")],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        assert fail.returncode == 2, f"{kid} fail fixture: {fail.stdout} {fail.stderr}"
        passed = subprocess.run(
            [sys.executable, "-m", "skillrange", "grade", kid, "--submission", str(path / "fixtures" / "pass")],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        assert passed.returncode == 0, f"{kid} pass fixture: {passed.stdout} {passed.stderr}"
