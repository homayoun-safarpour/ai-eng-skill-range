# K19 : Sentinel gate remap

Time box: 1–2h.

Implement `remap(exit_code: int) -> int`: 0->0, 3(SYSTEM_CHANGE)->0, 2(JUDGE_DRIFT)->2, else 1.

## Common fail

Mapping SYSTEM_CHANGE (3) to 2 fails. Remap: 0->0, 3->0, 2->2, else 1.

## Example fill

`python
remap(0)  # 0  PASS / STABLE path
remap(3)  # 0  SYSTEM_CHANGE must not red-gate the loop
remap(2)  # 2  JUDGE_DRIFT stays a hard fail
remap(1)  # 1  ERROR
`

