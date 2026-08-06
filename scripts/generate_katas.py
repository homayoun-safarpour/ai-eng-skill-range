#!/usr/bin/env python3
"""Generate all 24 katas with starters, graders, fixtures, briefs."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KATAS = ROOT / "katas"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip("\n"), encoding="utf-8")


def kata(
    kid: str,
    slug: str,
    skills: str,
    brief: str,
    rubric: str,
    starter_files: dict[str, str],
    fail_files: dict[str, str],
    pass_files: dict[str, str],
    grader: str,
) -> None:
    base = KATAS / f"{kid}-{slug}"
    write(base / "BRIEF.md", brief)
    write(base / "SKILL.md", f"# Skills\n\n{skills}\n")
    write(base / "rubric.md", rubric)
    write(base / "grader" / "run.py", grader)
    for name, body in starter_files.items():
        write(base / "starter" / name, body)
    for name, body in fail_files.items():
        write(base / "fixtures" / "fail" / name, body)
    for name, body in pass_files.items():
        write(base / "fixtures" / "pass" / name, body)


def main() -> None:
    # --- K01 ---
    kata(
        "K01",
        "loop-contract",
        "- C5.S1\n- C5.S2\n- C1.S7",
        """
        # K01 — Loop Contract

        Time box: 1–2h.

        Fill `LOOP_CONTRACT.md` with the five required decision headings used before
        automating an agent loop. Empty headings fail the grader.
        """,
        "Human: confirm each section has a concrete, machine-checkable note.",
        {"LOOP_CONTRACT.md": "# WIP\n\n## 1. Done\n\nTODO\n"},
        {"LOOP_CONTRACT.md": "# incomplete\n\n## 1. Done\n\nok\n"},
        {
            "LOOP_CONTRACT.md": """
            # Loop Contract

            ## 1. Done
            pytest -q exits 0

            ## 2. Verifier
            ruff + pytest (not the author of the change)

            ## 3. Stop layers
            goal + max 5 ticks + no-progress 2d

            ## 4. State file
            LOOP_STATE.md

            ## 5. Irreversible
            force-push and production deploy need human yes
            """
        },
        '''
        from pathlib import Path

        REQUIRED = [
            "## 1. Done",
            "## 2. Verifier",
            "## 3. Stop layers",
            "## 4. State file",
            "## 5. Irreversible",
        ]

        def grade(submission: Path) -> int:
            path = submission / "LOOP_CONTRACT.md"
            if not path.is_file():
                return 2
            text = path.read_text(encoding="utf-8")
            return 0 if all(h in text for h in REQUIRED) else 2
        ''',
    )

    # --- K02 ---
    kata(
        "K02",
        "exit-code-gate",
        "- C1.S4\n- C5.S6",
        """
        # K02 — Exit-code gate

        Time box: 1–2h.

        Implement `gate.py` that reads `status.json` with key `ok` (bool).
        Print PASS/FAIL and exit 0 when ok is true, else exit 2.
        """,
        "Human: gate must not exit 1 for ordinary fail; use 2.",
        {
            "gate.py": "import sys\nprint('TODO')\nsys.exit(1)\n",
            "status.json": json.dumps({"ok": True}),
        },
        {
            "gate.py": "import json,sys\nfrom pathlib import Path\nok=json.loads(Path('status.json').read_text())['ok']\nsys.exit(0 if ok else 2)\n",
            "status.json": json.dumps({"ok": False}),
        },
        {
            "gate.py": """
            import json, sys
            from pathlib import Path
            data = json.loads(Path(__file__).with_name('status.json').read_text(encoding='utf-8'))
            ok = bool(data.get('ok'))
            print('PASS' if ok else 'FAIL')
            raise SystemExit(0 if ok else 2)
            """,
            "status.json": json.dumps({"ok": True}),
        },
        '''
        import json
        import subprocess
        import sys
        from pathlib import Path

        def grade(submission: Path) -> int:
            gate = submission / "gate.py"
            status = submission / "status.json"
            if not gate.is_file() or not status.is_file():
                return 2
            # run with cwd=submission so relative status works; also patch for __file__ style
            proc = subprocess.run([sys.executable, str(gate)], cwd=submission, capture_output=True, text=True)
            data = json.loads(status.read_text(encoding="utf-8"))
            expect = 0 if data.get("ok") else 2
            return 0 if proc.returncode == expect else 2
        ''',
    )

    # Fix K02 fail fixture: gate should exit 2 when ok false - the fail fixture tests wrong behavior
    # Actually golden FAIL means the submission fails the grader (bad solution).
    # So fail fixture = broken gate (exits 1 always)
    write(
        KATAS / "K02-exit-code-gate" / "fixtures" / "fail" / "gate.py",
        "import sys\nsys.exit(1)\n",
    )
    write(
        KATAS / "K02-exit-code-gate" / "fixtures" / "fail" / "status.json",
        json.dumps({"ok": True}),
    )

    # --- K03 ---
    kata(
        "K03",
        "repro-signature-lite",
        "- C2.S1\n- C2.S2\n- C2.S8",
        """
        # K03 — Repro signature (lite)

        Time box: 2h.

        Provide `signature.json` with `data_sha256` matching sha256 of `data.bin`,
        and `env` string non-empty. Grader recomputes the hash.
        """,
        "Human: signature must fail if data.bin bytes change.",
        {
            "data.bin": "abc",
            "signature.json": json.dumps({"data_sha256": "wrong", "env": "py3"}),
        },
        {
            "data.bin": "abc",
            "signature.json": json.dumps({"data_sha256": "00", "env": "py3"}),
        },
        {},  # fill pass below after hash
        '''
        import hashlib
        import json
        from pathlib import Path

        def grade(submission: Path) -> int:
            data = submission / "data.bin"
            sig_path = submission / "signature.json"
            if not data.is_file() or not sig_path.is_file():
                return 2
            digest = hashlib.sha256(data.read_bytes()).hexdigest()
            sig = json.loads(sig_path.read_text(encoding="utf-8"))
            if sig.get("data_sha256") != digest:
                return 2
            if not str(sig.get("env") or "").strip():
                return 2
            return 0
        ''',
    )
    import hashlib

    digest = hashlib.sha256(b"abc").hexdigest()
    write(KATAS / "K03-repro-signature-lite" / "fixtures" / "pass" / "data.bin", "abc")
    write(
        KATAS / "K03-repro-signature-lite" / "fixtures" / "pass" / "signature.json",
        json.dumps({"data_sha256": digest, "env": "python3.10"}),
    )
    # starter data.bin as binary-ish text
    write(KATAS / "K03-repro-signature-lite" / "starter" / "data.bin", "abc")
    write(KATAS / "K03-repro-signature-lite" / "fixtures" / "fail" / "data.bin", "abc")

    # --- K04 ---
    kata(
        "K04",
        "judge-kappa-pair",
        "- C6.S1\n- C6.S2",
        """
        # K04 — Cohen kappa for two raters

        Time box: 2h.

        Implement `kappa.py` exposing `cohen_kappa(y1, y2) -> float`.
        Labels are parallel lists of strings. Grader checks known pairs.
        """,
        "Human: perfect agreement -> 1.0; chance agreement handled.",
        {"kappa.py": "def cohen_kappa(y1, y2):\n    return 0.0\n"},
        {"kappa.py": "def cohen_kappa(y1, y2):\n    return 0.0\n"},
        {
            "kappa.py": '''
            def cohen_kappa(y1, y2):
                assert len(y1) == len(y2) and y1
                labels = sorted(set(y1) | set(y2))
                n = len(y1)
                # confusion
                idx = {l: i for i, l in enumerate(labels)}
                m = [[0] * len(labels) for _ in labels]
                for a, b in zip(y1, y2):
                    m[idx[a]][idx[b]] += 1
                po = sum(m[i][i] for i in range(len(labels))) / n
                row = [sum(m[i][j] for j in range(len(labels))) for i in range(len(labels))]
                col = [sum(m[i][j] for i in range(len(labels))) for j in range(len(labels))]
                pe = sum((row[i] / n) * (col[i] / n) for i in range(len(labels)))
                if pe == 1:
                    return 1.0
                return (po - pe) / (1 - pe)
            '''
        },
        '''
        import importlib.util
        from pathlib import Path

        def _load(submission: Path):
            path = submission / "kappa.py"
            spec = importlib.util.spec_from_file_location("kappa_mod", path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod.cohen_kappa

        def grade(submission: Path) -> int:
            try:
                fn = _load(submission)
                if abs(fn(["a", "a", "b", "b"], ["a", "a", "b", "b"]) - 1.0) > 1e-6:
                    return 2
                # total disagreement on balanced binary -> kappa  -1 or low
                k = fn(["a", "a", "b", "b"], ["b", "b", "a", "a"])
                if k > -0.9:
                    return 2
                return 0
            except Exception:
                return 2
        ''',
    )

    # Continue generating remaining katas in compact form
    specs = _rest_specs()
    for spec in specs:
        kata(**spec)

    print("generated", len(list(KATAS.glob("K*"))), "katas")


def _rest_specs() -> list[dict]:
    import json as _json

    out: list[dict] = []

    out.append(
        dict(
            kid="K05",
            slug="rag-hitk-gate",
            skills="- C4.S1\n- C4.S2",
            brief="# K05 — hit@k / MRR gate\n\nTime box: 2–3h.\n\nImplement `metrics.py` with `hit_at_k(ranking, relevant, k)` and `mrr(ranking, relevant)`.\n",
            rubric="Human: ranking is ordered doc ids; relevant is a set.",
            starter_files={
                "metrics.py": "def hit_at_k(ranking, relevant, k):\n    return 0.0\n\ndef mrr(ranking, relevant):\n    return 0.0\n"
            },
            fail_files={
                "metrics.py": "def hit_at_k(ranking, relevant, k):\n    return 0.0\n\ndef mrr(ranking, relevant):\n    return 0.0\n"
            },
            pass_files={
                "metrics.py": '''
                def hit_at_k(ranking, relevant, k):
                    rel = set(relevant)
                    return 1.0 if any(x in rel for x in ranking[:k]) else 0.0

                def mrr(ranking, relevant):
                    rel = set(relevant)
                    for i, x in enumerate(ranking, 1):
                        if x in rel:
                            return 1.0 / i
                    return 0.0
                '''
            },
            grader='''
            import importlib.util
            from pathlib import Path

            def _load(submission):
                path = submission / "metrics.py"
                spec = importlib.util.spec_from_file_location("metrics_mod", path)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                return mod

            def grade(submission: Path) -> int:
                try:
                    m = _load(submission)
                    ranking = ["d1", "d2", "d3"]
                    if m.hit_at_k(ranking, ["d2"], 2) != 1.0:
                        return 2
                    if m.hit_at_k(ranking, ["d3"], 2) != 0.0:
                        return 2
                    if abs(m.mrr(ranking, ["d2"]) - 0.5) > 1e-9:
                        return 2
                    return 0
                except Exception:
                    return 2
            ''',
        )
    )

    out.append(
        dict(
            kid="K06",
            slug="retrieve-vs-generate",
            skills="- C4.S4",
            brief="# K06 — Retrieve vs generate failure\n\nTime box: 1–2h.\n\nWrite `diagnose.py` with `diagnose(retrieved_ids, relevant_ids, answer_has_hallucination: bool) -> str` returning `retrieval` | `generation` | `ok`.\n",
            rubric="If relevant not in retrieved -> retrieval; else if hallucination -> generation; else ok.",
            starter_files={"diagnose.py": "def diagnose(retrieved_ids, relevant_ids, answer_has_hallucination):\n    return 'ok'\n"},
            fail_files={"diagnose.py": "def diagnose(retrieved_ids, relevant_ids, answer_has_hallucination):\n    return 'ok'\n"},
            pass_files={
                "diagnose.py": '''
                def diagnose(retrieved_ids, relevant_ids, answer_has_hallucination):
                    retrieved = set(retrieved_ids)
                    if not set(relevant_ids).issubset(retrieved):
                        return "retrieval"
                    if answer_has_hallucination:
                        return "generation"
                    return "ok"
                '''
            },
            grader='''
            import importlib.util
            from pathlib import Path

            def grade(submission: Path) -> int:
                try:
                    path = submission / "diagnose.py"
                    spec = importlib.util.spec_from_file_location("diag", path)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    d = mod.diagnose
                    if d(["a"], ["b"], False) != "retrieval":
                        return 2
                    if d(["a", "b"], ["a"], True) != "generation":
                        return 2
                    if d(["a", "b"], ["a"], False) != "ok":
                        return 2
                    return 0
                except Exception:
                    return 2
            ''',
        )
    )

    out.append(
        dict(
            kid="K07",
            slug="agent-stop-layers",
            skills="- C5.S4\n- C5.S5",
            brief="# K07 — Stop layers on disk\n\nTime box: 1h.\n\nProvide `stop_layers.json` with keys goal, max_turns, budget, no_progress (all non-empty strings).\n",
            rubric="All four layers present.",
            starter_files={"stop_layers.json": _json.dumps({"goal": ""})},
            fail_files={"stop_layers.json": _json.dumps({"goal": "x"})},
            pass_files={
                "stop_layers.json": _json.dumps(
                    {
                        "goal": "tests green",
                        "max_turns": "5",
                        "budget": "1 USD",
                        "no_progress": "2 days",
                    }
                )
            },
            grader='''
            import json
            from pathlib import Path

            KEYS = ("goal", "max_turns", "budget", "no_progress")

            def grade(submission: Path) -> int:
                path = submission / "stop_layers.json"
                if not path.is_file():
                    return 2
                data = json.loads(path.read_text(encoding="utf-8"))
                for k in KEYS:
                    if not str(data.get(k) or "").strip():
                        return 2
                return 0
            ''',
        )
    )

    out.append(
        dict(
            kid="K08",
            slug="tool-schema-validate",
            skills="- C3.S1\n- C3.S2",
            brief="# K08 — Tool schema validate\n\nTime box: 2h.\n\nImplement `validate.py` with `validate_tool(call: dict, schema: dict) -> bool`.\nSchema: `{\"name\": str, \"required\": [str]}`. Call must match name and include required args keys.\n",
            rubric="Wrong name or missing required arg -> False.",
            starter_files={"validate.py": "def validate_tool(call, schema):\n    return True\n"},
            fail_files={"validate.py": "def validate_tool(call, schema):\n    return True\n"},
            pass_files={
                "validate.py": '''
                def validate_tool(call, schema):
                    if call.get("name") != schema.get("name"):
                        return False
                    args = call.get("args") or {}
                    for key in schema.get("required") or []:
                        if key not in args:
                            return False
                    return True
                '''
            },
            grader='''
            import importlib.util
            from pathlib import Path

            def grade(submission: Path) -> int:
                try:
                    path = submission / "validate.py"
                    spec = importlib.util.spec_from_file_location("val", path)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    schema = {"name": "search", "required": ["q"]}
                    if not mod.validate_tool({"name": "search", "args": {"q": "x"}}, schema):
                        return 2
                    if mod.validate_tool({"name": "other", "args": {"q": "x"}}, schema):
                        return 2
                    if mod.validate_tool({"name": "search", "args": {}}, schema):
                        return 2
                    return 0
                except Exception:
                    return 2
            ''',
        )
    )

    # K09-K24
    out.extend(_k09_k24())
    return out


def _k09_k24() -> list[dict]:
    import json as _json

    specs = []

    specs.append(
        dict(
            kid="K09",
            slug="structured-tool-result",
            skills="- C3.S1\n- C3.S5",
            brief="# K09 — Structured tool result\n\nTime box: 1–2h.\n\nWrite `result.json` with keys tool, args_hash, status where status is ok|error.\n",
            rubric="All keys present; status enumerated.",
            starter_files={"result.json": "{}"},
            fail_files={"result.json": _json.dumps({"tool": "x"})},
            pass_files={
                "result.json": _json.dumps(
                    {"tool": "search", "args_hash": "abc", "status": "ok"}
                )
            },
            grader='''
            import json
            from pathlib import Path

            def grade(submission: Path) -> int:
                path = submission / "result.json"
                if not path.is_file():
                    return 2
                data = json.loads(path.read_text(encoding="utf-8"))
                if not data.get("tool") or not data.get("args_hash"):
                    return 2
                if data.get("status") not in {"ok", "error"}:
                    return 2
                return 0
            ''',
        )
    )

    specs.append(
        dict(
            kid="K10",
            slug="trajectory-forbid-tool",
            skills="- C7.S4",
            brief="# K10 — Forbidden tool in trajectory\n\nTime box: 1–2h.\n\nImplement `check.py` with `has_forbidden(events, forbidden) -> bool`.\nEvents are list of `{tool: str}`.\n",
            rubric="True iff any event tool is in forbidden set.",
            starter_files={"check.py": "def has_forbidden(events, forbidden):\n    return False\n"},
            fail_files={"check.py": "def has_forbidden(events, forbidden):\n    return False\n"},
            pass_files={
                "check.py": '''
                def has_forbidden(events, forbidden):
                    bad = set(forbidden)
                    return any(e.get("tool") in bad for e in events)
                '''
            },
            grader='''
            import importlib.util
            from pathlib import Path

            def grade(submission: Path) -> int:
                try:
                    path = submission / "check.py"
                    spec = importlib.util.spec_from_file_location("chk", path)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    ev = [{"tool": "read"}, {"tool": "shell"}]
                    if not mod.has_forbidden(ev, ["shell"]):
                        return 2
                    if mod.has_forbidden(ev, ["delete"]):
                        return 2
                    return 0
                except Exception:
                    return 2
            ''',
        )
    )

    specs.append(
        dict(
            kid="K11",
            slug="faithfulness-proxy",
            skills="- C4.S5\n- C4.S8",
            brief="# K11 — Offline faithfulness proxy\n\nTime box: 2h.\n\nImplement `faithfulness.py` with `score(answer: str, context: str) -> float` in [0,1]: fraction of answer tokens (whitespace) that appear in context (casefold).\n",
            rubric="Empty answer -> 1.0; tokens not in context lower the score.",
            starter_files={"faithfulness.py": "def score(answer, context):\n    return 0.0\n"},
            fail_files={"faithfulness.py": "def score(answer, context):\n    return 0.0\n"},
            pass_files={
                "faithfulness.py": '''
                def score(answer, context):
                    toks = [t for t in answer.casefold().split() if t]
                    if not toks:
                        return 1.0
                    ctx = set(context.casefold().split())
                    return sum(1 for t in toks if t in ctx) / len(toks)
                '''
            },
            grader='''
            import importlib.util
            from pathlib import Path

            def grade(submission: Path) -> int:
                try:
                    path = submission / "faithfulness.py"
                    spec = importlib.util.spec_from_file_location("faith", path)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    if abs(mod.score("", "anything") - 1.0) > 1e-9:
                        return 2
                    if abs(mod.score("red cat", "the red ball") - 0.5) > 1e-9:
                        return 2
                    return 0
                except Exception:
                    return 2
            ''',
        )
    )

    specs.append(
        dict(
            kid="K12",
            slug="corpus-hash-freeze",
            skills="- C4.S3\n- C4.S7",
            brief="# K12 — Corpus hash freeze\n\nTime box: 1–2h.\n\nProvide `baseline.json` with `corpus_sha256` matching sha256 of `corpus.txt`.\n",
            rubric="Any corpus edit without baseline update must fail.",
            starter_files={"corpus.txt": "hello", "baseline.json": "{}"},
            fail_files={
                "corpus.txt": "hello",
                "baseline.json": _json.dumps({"corpus_sha256": "nope"}),
            },
            pass_files={},
            grader='''
            import hashlib
            import json
            from pathlib import Path

            def grade(submission: Path) -> int:
                corpus = submission / "corpus.txt"
                base = submission / "baseline.json"
                if not corpus.is_file() or not base.is_file():
                    return 2
                digest = hashlib.sha256(corpus.read_bytes()).hexdigest()
                data = json.loads(base.read_text(encoding="utf-8"))
                return 0 if data.get("corpus_sha256") == digest else 2
            ''',
        )
    )

    import hashlib as _hashlib

    d = _hashlib.sha256(b"hello").hexdigest()
    # pass files filled after kata() call via side write in main - handle here by including content
    specs[-1]["pass_files"] = {
        "corpus.txt": "hello",
        "baseline.json": _json.dumps({"corpus_sha256": d}),
    }
    specs[-1]["starter_files"]["corpus.txt"] = "hello"

    specs.append(
        dict(
            kid="K13",
            slug="drift-attribution-toy",
            skills="- C6.S5\n- C6.S6",
            brief="# K13 — Drift attribution toy\n\nTime box: 2h.\n\nImplement `attr.py` with `verdict(base_kappa, cur_kappa, live_moved: bool, drop=0.1) -> str`:\nJUDGE_DRIFT if kappa dropped by >= drop; else SYSTEM_CHANGE if live_moved; else STABLE.\n",
            rubric="Judge drift beats system change when kappa falls.",
            starter_files={"attr.py": "def verdict(base_kappa, cur_kappa, live_moved, drop=0.1):\n    return 'STABLE'\n"},
            fail_files={"attr.py": "def verdict(base_kappa, cur_kappa, live_moved, drop=0.1):\n    return 'STABLE'\n"},
            pass_files={
                "attr.py": '''
                def verdict(base_kappa, cur_kappa, live_moved, drop=0.1):
                    if base_kappa - cur_kappa >= drop:
                        return "JUDGE_DRIFT"
                    if live_moved:
                        return "SYSTEM_CHANGE"
                    return "STABLE"
                '''
            },
            grader='''
            import importlib.util
            from pathlib import Path

            def grade(submission: Path) -> int:
                try:
                    path = submission / "attr.py"
                    spec = importlib.util.spec_from_file_location("attr", path)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    v = mod.verdict
                    if v(0.9, 0.7, True) != "JUDGE_DRIFT":
                        return 2
                    if v(0.9, 0.89, True) != "SYSTEM_CHANGE":
                        return 2
                    if v(0.9, 0.89, False) != "STABLE":
                        return 2
                    return 0
                except Exception:
                    return 2
            ''',
        )
    )

    specs.append(
        dict(
            kid="K14",
            slug="journal-append-only",
            skills="- C5.S8\n- C1.S6",
            brief="# K14 — Journal append-only\n\nTime box: 1h.\n\nProvide `JOURNAL.md` containing at least one tick block with lines for gates and decision.\n",
            rubric="Must include 'gates:' and 'decision:' markers.",
            starter_files={"JOURNAL.md": "# journal\n"},
            fail_files={"JOURNAL.md": "# empty\n"},
            pass_files={
                "JOURNAL.md": "## tick\n- gates: tests=PASS\n- decision: advance\n"
            },
            grader='''
            from pathlib import Path

            def grade(submission: Path) -> int:
                path = submission / "JOURNAL.md"
                if not path.is_file():
                    return 2
                text = path.read_text(encoding="utf-8").casefold()
                if "gates:" not in text or "decision:" not in text:
                    return 2
                return 0
            ''',
        )
    )

    specs.append(
        dict(
            kid="K15",
            slug="cost-budget-cap",
            skills="- C5.S7\n- C7.S8",
            brief="# K15 — Cost budget cap\n\nTime box: 1–2h.\n\nImplement `budget.py` with `within_budget(spent: float, cap: float) -> bool`.\n",
            rubric="spent <= cap -> True.",
            starter_files={"budget.py": "def within_budget(spent, cap):\n    return True\n"},
            fail_files={"budget.py": "def within_budget(spent, cap):\n    return True\n"},
            pass_files={
                "budget.py": "def within_budget(spent, cap):\n    return float(spent) <= float(cap)\n"
            },
            grader='''
            import importlib.util
            from pathlib import Path

            def grade(submission: Path) -> int:
                try:
                    path = submission / "budget.py"
                    spec = importlib.util.spec_from_file_location("bud", path)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    if not mod.within_budget(1.0, 1.0):
                        return 2
                    if mod.within_budget(1.01, 1.0):
                        return 2
                    return 0
                except Exception:
                    return 2
            ''',
        )
    )

    specs.append(
        dict(
            kid="K16",
            slug="irreversible-checkpoint",
            skills="- C3.S8\n- C7.S1",
            brief="# K16 — Irreversible checkpoint\n\nTime box: 1h.\n\nProvide `checkpoints.json` listing irreversible actions each with `name` and `human_required: true`.\nNeed at least two entries.\n",
            rubric="Every entry must require human.",
            starter_files={"checkpoints.json": "[]"},
            fail_files={
                "checkpoints.json": _json.dumps(
                    [{"name": "deploy", "human_required": False}]
                )
            },
            pass_files={
                "checkpoints.json": _json.dumps(
                    [
                        {"name": "force-push", "human_required": True},
                        {"name": "prod-deploy", "human_required": True},
                    ]
                )
            },
            grader='''
            import json
            from pathlib import Path

            def grade(submission: Path) -> int:
                path = submission / "checkpoints.json"
                if not path.is_file():
                    return 2
                data = json.loads(path.read_text(encoding="utf-8"))
                if not isinstance(data, list) or len(data) < 2:
                    return 2
                for row in data:
                    if not row.get("name") or row.get("human_required") is not True:
                        return 2
                return 0
            ''',
        )
    )

    specs.append(
        dict(
            kid="K17",
            slug="rubric-vs-item",
            skills="- C6.S3",
            brief="# K17 — Rubric vs item ambiguity\n\nTime box: 2h.\n\nImplement `cause.py` with `cause(item_ambiguous: bool, rubric_vague: bool) -> str` returning `item` | `rubric` | `both` | `neither`.\n",
            rubric="Priority: both > item > rubric > neither.",
            starter_files={"cause.py": "def cause(item_ambiguous, rubric_vague):\n    return 'neither'\n"},
            fail_files={"cause.py": "def cause(item_ambiguous, rubric_vague):\n    return 'neither'\n"},
            pass_files={
                "cause.py": '''
                def cause(item_ambiguous, rubric_vague):
                    if item_ambiguous and rubric_vague:
                        return "both"
                    if item_ambiguous:
                        return "item"
                    if rubric_vague:
                        return "rubric"
                    return "neither"
                '''
            },
            grader='''
            import importlib.util
            from pathlib import Path

            def grade(submission: Path) -> int:
                try:
                    path = submission / "cause.py"
                    spec = importlib.util.spec_from_file_location("cause", path)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    c = mod.cause
                    if c(True, True) != "both":
                        return 2
                    if c(True, False) != "item":
                        return 2
                    if c(False, True) != "rubric":
                        return 2
                    if c(False, False) != "neither":
                        return 2
                    return 0
                except Exception:
                    return 2
            ''',
        )
    )

    specs.append(
        dict(
            kid="K18",
            slug="weighted-kappa-ordinal",
            skills="- C6.S4",
            brief="# K18 — Weighted kappa (ordinal)\n\nTime box: 3h.\n\nImplement `weighted_kappa(y1, y2, weights='linear')` for ordinal labels 0..n. Linear weights. Perfect agreement -> 1.0.\n",
            rubric="Use linear weights on sorted unique labels.",
            starter_files={"kappa.py": "def weighted_kappa(y1, y2, weights='linear'):\n    return 0.0\n"},
            fail_files={"kappa.py": "def weighted_kappa(y1, y2, weights='linear'):\n    return 0.0\n"},
            pass_files={
                "kappa.py": '''
                def weighted_kappa(y1, y2, weights="linear"):
                    assert len(y1) == len(y2) and y1
                    labels = sorted(set(y1) | set(y2))
                    idx = {l: i for i, l in enumerate(labels)}
                    k = len(labels)
                    n = len(y1)
                    o = [[0] * k for _ in range(k)]
                    for a, b in zip(y1, y2):
                        o[idx[a]][idx[b]] += 1
                    w = [[0.0] * k for _ in range(k)]
                    for i in range(k):
                        for j in range(k):
                            w[i][j] = abs(i - j) / (k - 1) if k > 1 else 0.0
                    row = [sum(o[i][j] for j in range(k)) for i in range(k)]
                    col = [sum(o[i][j] for i in range(k)) for j in range(k)]
                    e = [[row[i] * col[j] / n for j in range(k)] for i in range(k)]
                    num = sum(w[i][j] * o[i][j] for i in range(k) for j in range(k))
                    den = sum(w[i][j] * e[i][j] for i in range(k) for j in range(k))
                    if den == 0:
                        return 1.0
                    return 1.0 - num / den
                '''
            },
            grader='''
            import importlib.util
            from pathlib import Path

            def grade(submission: Path) -> int:
                try:
                    path = submission / "kappa.py"
                    spec = importlib.util.spec_from_file_location("wk", path)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    y = [0, 1, 2, 2]
                    if abs(mod.weighted_kappa(y, y) - 1.0) > 1e-6:
                        return 2
                    return 0
                except Exception:
                    return 2
            ''',
        )
    )

    specs.append(
        dict(
            kid="K19",
            slug="sentinel-gate-remap",
            skills="- C6.S6\n- C5.S6",
            brief="# K19 — Sentinel gate remap\n\nTime box: 1–2h.\n\nImplement `remap(exit_code: int) -> int`: 0->0, 3(SYSTEM_CHANGE)->0, 2(JUDGE_DRIFT)->2, else 1.\n",
            rubric="Only judge drift should redden a repair-first loop gate.",
            starter_files={"remap.py": "def remap(exit_code):\n    return exit_code\n"},
            fail_files={"remap.py": "def remap(exit_code):\n    return exit_code\n"},
            pass_files={
                "remap.py": '''
                def remap(exit_code):
                    if exit_code == 0 or exit_code == 3:
                        return 0
                    if exit_code == 2:
                        return 2
                    return 1
                '''
            },
            grader='''
            import importlib.util
            from pathlib import Path

            def grade(submission: Path) -> int:
                try:
                    path = submission / "remap.py"
                    spec = importlib.util.spec_from_file_location("rm", path)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    if mod.remap(0) != 0 or mod.remap(3) != 0:
                        return 2
                    if mod.remap(2) != 2:
                        return 2
                    if mod.remap(1) != 1:
                        return 2
                    return 0
                except Exception:
                    return 2
            ''',
        )
    )

    specs.append(
        dict(
            kid="K20",
            slug="tick-policy-repair",
            skills="- C5.S6\n- C1.S5",
            brief="# K20 — Tick policy repair-before-advance\n\nTime box: 2h.\n\nImplement `decide(gates: dict[str,bool], head: str) -> str` returning `repair:<gate>` if any gate False, else `advance:<head>`.\n",
            rubric="Any red gate blocks advance.",
            starter_files={"decide.py": "def decide(gates, head):\n    return 'advance:' + head\n"},
            fail_files={"decide.py": "def decide(gates, head):\n    return 'advance:' + head\n"},
            pass_files={
                "decide.py": '''
                def decide(gates, head):
                    for name, ok in gates.items():
                        if not ok:
                            return f"repair:{name}"
                    return f"advance:{head}"
                '''
            },
            grader='''
            import importlib.util
            from pathlib import Path

            def grade(submission: Path) -> int:
                try:
                    path = submission / "decide.py"
                    spec = importlib.util.spec_from_file_location("dec", path)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    if mod.decide({"tests": False, "lint": True}, "M1") != "repair:tests":
                        return 2
                    if mod.decide({"tests": True, "lint": True}, "M1") != "advance:M1":
                        return 2
                    return 0
                except Exception:
                    return 2
            ''',
        )
    )

    specs.append(
        dict(
            kid="K21",
            slug="absolute-paths-aci",
            skills="- C3.S7",
            brief="# K21 — Absolute paths ACI\n\nTime box: 1h.\n\nImplement `ok_path(p: str) -> bool` True only for absolute paths (POSIX `/` or Windows drive `C:\\\\`).\n",
            rubric="Relative paths must be rejected.",
            starter_files={"paths.py": "def ok_path(p):\n    return True\n"},
            fail_files={"paths.py": "def ok_path(p):\n    return True\n"},
            pass_files={
                "paths.py": '''
                from pathlib import Path

                def ok_path(p):
                    return Path(p).is_absolute()
                '''
            },
            grader='''
            import importlib.util
            from pathlib import Path

            def grade(submission: Path) -> int:
                try:
                    path = submission / "paths.py"
                    spec = importlib.util.spec_from_file_location("paths", path)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    if mod.ok_path("relative/file.txt"):
                        return 2
                    if not mod.ok_path("/tmp/x") and not mod.ok_path("C:\\\\tmp\\\\x"):
                        # at least one absolute style must work on this OS
                        if not mod.ok_path(str(Path.cwd() / "x")):
                            # Path.cwd()/x is absolute
                            return 2
                    if not mod.ok_path(str(Path.cwd() / "abs.txt")):
                        return 2
                    return 0
                except Exception:
                    return 2
            ''',
        )
    )

    specs.append(
        dict(
            kid="K22",
            slug="offline-lexical-judge",
            skills="- C4.S5",
            brief="# K22 — Offline lexical judge\n\nTime box: 2h.\n\nImplement `judge.py` with `pass_fail(answer, must_include: list[str]) -> str` returning pass if all needles appear in answer casefold else fail.\n",
            rubric="All required phrases must appear.",
            starter_files={"judge.py": "def pass_fail(answer, must_include):\n    return 'pass'\n"},
            fail_files={"judge.py": "def pass_fail(answer, must_include):\n    return 'pass'\n"},
            pass_files={
                "judge.py": '''
                def pass_fail(answer, must_include):
                    text = answer.casefold()
                    return "pass" if all(m.casefold() in text for m in must_include) else "fail"
                '''
            },
            grader='''
            import importlib.util
            from pathlib import Path

            def grade(submission: Path) -> int:
                try:
                    path = submission / "judge.py"
                    spec = importlib.util.spec_from_file_location("j", path)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    if mod.pass_fail("Hello World", ["hello"]) != "pass":
                        return 2
                    if mod.pass_fail("Hello", ["hello", "world"]) != "fail":
                        return 2
                    return 0
                except Exception:
                    return 2
            ''',
        )
    )

    specs.append(
        dict(
            kid="K23",
            slug="ci-workflow-assert",
            skills="- C7.S7\n- C1.S3",
            brief="# K23 — CI workflow assert\n\nTime box: 1h.\n\nProvide `.github/workflows/ci.yml` that contains `jobs:` and `pytest` somewhere in the file.\n",
            rubric="Minimal CI file present.",
            starter_files={".github/workflows/ci.yml": "name: x\n"},
            fail_files={".github/workflows/ci.yml": "name: x\n"},
            pass_files={
                ".github/workflows/ci.yml": "name: CI\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - run: pytest -q\n"
            },
            grader='''
            from pathlib import Path

            def grade(submission: Path) -> int:
                path = submission / ".github" / "workflows" / "ci.yml"
                if not path.is_file():
                    return 2
                text = path.read_text(encoding="utf-8").casefold()
                if "jobs:" not in text or "pytest" not in text:
                    return 2
                return 0
            ''',
        )
    )

    specs.append(
        dict(
            kid="K24",
            slug="composite-multi-failure",
            skills="- C7.S6\n- C7.S4\n- C7.S5",
            brief="# K24 — Composite multi-failure\n\nTime box: 2h.\n\nImplement `detect.py` with `failures(events, forbidden, required) -> list[str]` returning any of `forbidden_tool`, `missing_tool` that apply.\n",
            rubric="Can return both labels in one run.",
            starter_files={"detect.py": "def failures(events, forbidden, required):\n    return []\n"},
            fail_files={"detect.py": "def failures(events, forbidden, required):\n    return []\n"},
            pass_files={
                "detect.py": '''
                def failures(events, forbidden, required):
                    tools = [e.get("tool") for e in events]
                    out = []
                    if any(t in set(forbidden) for t in tools):
                        out.append("forbidden_tool")
                    if any(r not in tools for r in required):
                        out.append("missing_tool")
                    return out
                '''
            },
            grader='''
            import importlib.util
            from pathlib import Path

            def grade(submission: Path) -> int:
                try:
                    path = submission / "detect.py"
                    spec = importlib.util.spec_from_file_location("det", path)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    ev = [{"tool": "shell"}, {"tool": "read"}]
                    got = mod.failures(ev, ["shell"], ["write"])
                    if "forbidden_tool" not in got or "missing_tool" not in got:
                        return 2
                    if mod.failures([{"tool": "read"}], ["shell"], ["read"]):
                        return 2
                    return 0
                except Exception:
                    return 2
            ''',
        )
    )

    return specs


if __name__ == "__main__":
    main()
