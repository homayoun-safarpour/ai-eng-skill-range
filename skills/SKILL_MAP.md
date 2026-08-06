# Skill map — 56 nodes (7 clusters × 8)

Each skill is a named capability. Graded katas reference skill IDs in `SKILL.md`.
Progress: graded katas prove skills under a frozen grader (exit 0/2).

Interview-core path uses katas **K01–K16**. Specialty depth uses **K17–K24**.

## C1 — Production Python and CI hygiene

| ID | Skill |
| --- | --- |
| C1.S1 | Structure a small installable Python package |
| C1.S2 | Write pytest that fails closed on regressions |
| C1.S3 | Wire GitHub Actions for 3.10–3.12 |
| C1.S4 | Use exit codes as gate contracts (0 pass / 2 fail) |
| C1.S5 | Keep a human-editable markdown backlog |
| C1.S6 | Append-only journal of decisions |
| C1.S7 | Fail CI when required headings or files are missing |
| C1.S8 | Pin dependencies or document lockfile discipline |

## C2 — ML and reproducibility basics

| ID | Skill |
| --- | --- |
| C2.S1 | Hash dataset bytes for freeze checks |
| C2.S2 | Include env or lock fingerprint in a run signature |
| C2.S3 | Reproduce a train step with a fixed seed |
| C2.S4 | Define a metric floor gate |
| C2.S5 | Detect simple feature distribution drift |
| C2.S6 | Serve a model behind a health endpoint pattern |
| C2.S7 | Separate training code hash from model weights |
| C2.S8 | Document what a signature does and does not prove |

## C3 — LLM app patterns

| ID | Skill |
| --- | --- |
| C3.S1 | Validate tool call JSON against a schema |
| C3.S2 | Reject malformed structured output fail-closed |
| C3.S3 | Bound tool retries and stop runaway loops |
| C3.S4 | Separate planner output from executor side effects |
| C3.S5 | Log tool name, args hash, and result status |
| C3.S6 | Prefer scripts for deterministic work over re-prompting |
| C3.S7 | Require absolute paths in file tools |
| C3.S8 | Define irreversible actions needing human approval |

## C4 — RAG reliability

| ID | Skill |
| --- | --- |
| C4.S1 | Compute hit@k on a frozen case set |
| C4.S2 | Compute MRR on a frozen case set |
| C4.S3 | Freeze corpus content with sha256 |
| C4.S4 | Separate retrieval failure from generation failure |
| C4.S5 | Offline lexical faithfulness proxy |
| C4.S6 | Version eval cases next to the corpus |
| C4.S7 | Fail closed when corpus hash drifts |
| C4.S8 | Report honest limits of lexical judges |

## C5 — Agents and loops

| ID | Skill |
| --- | --- |
| C5.S1 | Write a five-decision Loop Contract |
| C5.S2 | Define machine-checkable done criteria |
| C5.S3 | Keep verifier independent from maker |
| C5.S4 | Layer stop conditions (goal, turns, budget, no-progress) |
| C5.S5 | Persist loop state on disk |
| C5.S6 | Prefer repair before advance when gates are red |
| C5.S7 | Cap cost or token budget per run |
| C5.S8 | Journal one bounded action per tick |

## C6 — Eval and judges

| ID | Skill |
| --- | --- |
| C6.S1 | Compute Cohen kappa for two raters |
| C6.S2 | Interpret low kappa as disagreement, not truth |
| C6.S3 | Separate item ambiguity from rubric underspecification |
| C6.S4 | Use weighted kappa for ordinal labels |
| C6.S5 | Freeze a human anchor set for drift checks |
| C6.S6 | Attribute score movement to judge vs system |
| C6.S7 | Build a tiny golden set before changing prompts |
| C6.S8 | Calibrate an automated grader against human labels |

## C7 — Harness, safety, and cost

| ID | Skill |
| --- | --- |
| C7.S1 | Checklist irreversible actions before automation |
| C7.S2 | Document sandbox / network assumptions |
| C7.S3 | Fail closed on missing baseline |
| C7.S4 | Detect forbidden tools in a trajectory |
| C7.S5 | Detect missing required tools in a trajectory |
| C7.S6 | Composite multi-failure scenario labeling |
| C7.S7 | Assert CI workflow files exist and name jobs |
| C7.S8 | Route easy vs hard work without claiming free model calls |

## Kata index (target 24)

| Kata | Skills (primary) | Path |
| --- | --- | --- |
| K01 | C5.S1 C5.S2 C1.S7 | interview-core |
| K02 | C1.S4 C5.S6 | interview-core |
| K03 | C2.S1 C2.S2 C2.S8 | interview-core |
| K04 | C6.S1 C6.S2 | interview-core |
| K05 | C4.S1 C4.S2 | interview-core |
| K06 | C4.S4 | interview-core |
| K07 | C5.S4 C5.S5 | interview-core |
| K08 | C3.S1 C3.S2 | interview-core |
| K09 | C3.S1 C3.S5 | interview-core |
| K10 | C7.S4 | interview-core |
| K11 | C4.S5 C4.S8 | interview-core |
| K12 | C4.S3 C4.S7 | interview-core |
| K13 | C6.S5 C6.S6 | interview-core |
| K14 | C5.S8 C1.S6 | interview-core |
| K15 | C5.S7 C7.S8 | interview-core |
| K16 | C3.S8 C7.S1 | interview-core |
| K17 | C6.S3 | specialty |
| K18 | C6.S4 | specialty |
| K19 | C6.S6 C5.S6 | specialty |
| K20 | C5.S6 C1.S5 | specialty |
| K21 | C3.S7 | specialty |
| K22 | C4.S5 | specialty |
| K23 | C7.S7 C1.S3 | specialty |
| K24 | C7.S6 C7.S4 C7.S5 | specialty |
