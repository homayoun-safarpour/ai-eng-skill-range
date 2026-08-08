# Examples

Offline grader dogfood (no API, no GPU).

| Path | Expect |
| --- | --- |
| [K01_walkthrough.md](K01_walkthrough.md) | Clone → install → grade pass (0) → grade fail (2) |
| [../katas/K01-loop-contract/fixtures/pass](../katas/K01-loop-contract/fixtures/pass) | `skillrange grade K01 --submission ...` exits **0** |
| [../katas/K01-loop-contract/fixtures/fail](../katas/K01-loop-contract/fixtures/fail) | same command exits **2** |
| [../katas/K01-loop-contract/starter](../katas/K01-loop-contract/starter) | incomplete starter (grade until exit 0) |

```bash
pip install -e ".[dev]"
skillrange grade K01 --submission katas/K01-loop-contract/fixtures/pass
skillrange grade K01 --submission katas/K01-loop-contract/fixtures/fail
```

Reliability limits: [../docs/RELIABILITY_CARD.md](../docs/RELIABILITY_CARD.md).
