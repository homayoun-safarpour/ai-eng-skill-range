# ai-eng-skill-range

**Talking about LLM and ML engineering skills is cheap. This range turns fifty-six named skills into twenty-four small katas you can fill, grade with exit codes, and fork.**

[![CI](https://github.com/homayoun-safarpour/ai-eng-skill-range/actions/workflows/ci.yml/badge.svg)](https://github.com/homayoun-safarpour/ai-eng-skill-range/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Progress](https://img.shields.io/badge/katas-24%2F24-green)

## Use this when

| Situation | Use this? |
| --- | --- |
| You want graded practice for eval, RAG, agents, repro, and harness skills | Yes |
| You want a frozen grader (exit 0/2) an org or bot can run | Yes |
| You want a 500-lesson curriculum from math to swarms | No — see other roadmaps; this is a kata range |
| You want a runtime agent framework | No |

## Quickstart

```bash
git clone https://github.com/homayoun-safarpour/ai-eng-skill-range
cd ai-eng-skill-range
pip install -e ".[dev]"
skillrange list
# attempt a kata: copy starter, edit, grade
cp -r katas/K01-loop-contract/starter /tmp/k01
# edit /tmp/k01 ...
skillrange grade K01 --submission /tmp/k01
# expect exit 2 until the contract headings are complete
skillrange grade K01 --submission katas/K01-loop-contract/fixtures/pass
```

## Skill map and paths

- Full map (56 skills): [`skills/SKILL_MAP.md`](skills/SKILL_MAP.md)
- Interview-core katas: **K01–K16**
- Specialty (eval/trust/harness depth): **K17–K24**
- Companion contract guide: [agent-loop-field-guide](https://github.com/homayoun-safarpour/agent-loop-field-guide)

## How grading works

Each kata ships `grader/run.py` with `grade(submission: Path) -> int` returning **0** (pass) or **2** (fail). CI dogfoods `fixtures/fail` (must exit 2) and `fixtures/pass` (must exit 0). Default path is offline and deterministic — no paid API, no GPU.

## Progress

**24 / 24 katas shipped.** Graded expansion stopped; new katas only when hire-signal gaps appear.

## Author

Homayoun Safarpour · [LinkedIn](https://www.linkedin.com/in/homayoun-safarpour/)

## License

MIT
