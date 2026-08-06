# Interview talking points : ai-eng-skill-range

Five CLI-backed points for a technical screen (no resume recap).

- **`skillrange list`** : prints all kata ids (K01–K24); use it to pick interview-core katas K01–K16 before specialty eval/trust depth.
- **`skillrange grade K01 --submission katas/K01-loop-contract/starter`** : unfinished starter exits **2**; the grader checks Loop Contract headings the same way a bot would gate a hire take-home.
- **`skillrange grade K01 --submission katas/K01-loop-contract/fixtures/pass`** : reference pass exits **0**; CI dogfoods the same pair on every kata (`fixtures/fail` must stay **2**).
- **`skillrange grade K05-rag-hitk-gate --submission <your_dir>`** : offline retrieval metric kata; no API key, only files under `--submission`.
- **`skillrange grade K02-exit-code-gate --submission katas/K02-exit-code-gate/fixtures/pass`** : encodes the stack-wide rule that gates speak exit codes (0 pass, 2 fail), matching trace-gate, rag-eval, and drift-sentinel contracts.
