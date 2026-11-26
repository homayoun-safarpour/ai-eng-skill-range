import json
from pathlib import Path

import pytest

from skillrange.cli import main

KEYS = ("goal", "max_turns", "budget", "no_progress")


def grade_values(tmp_path, data):
    (tmp_path / "stop_layers.json").write_text(json.dumps(data), encoding="utf-8")
    return main(["grade", "K07", "--submission", str(tmp_path)])


@pytest.mark.parametrize("key", KEYS)
@pytest.mark.parametrize("value", [5, True, ["stop"], {"rule": "stop"}, 0, False, None, "", "  "])
def test_k07_requires_nonempty_string_for_each_key(tmp_path, key, value):
    data = dict.fromkeys(KEYS, "stop")
    data[key] = value
    assert grade_values(tmp_path, data) == 2


@pytest.mark.parametrize("data", [[], "stop", True, None])
def test_k07_requires_an_object(tmp_path, data):
    assert grade_values(tmp_path, data) == 2


@pytest.mark.parametrize("key", KEYS)
def test_k07_requires_every_key(tmp_path, key):
    data = dict.fromkeys(KEYS, "stop")
    del data[key]
    assert grade_values(tmp_path, data) == 2


@pytest.mark.parametrize("value", ["0", "false", " stop "])
def test_k07_accepts_nonempty_strings(tmp_path, value):
    assert grade_values(tmp_path, dict.fromkeys(KEYS, value)) == 0
