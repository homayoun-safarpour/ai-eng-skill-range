# K01 walkthrough (under 10 minutes)

Offline loop-contract kata. No API. No GPU.

## 1. Install

```bash
git clone https://github.com/homayoun-safarpour/ai-eng-skill-range
cd ai-eng-skill-range
pip install -e ".[dev]"
skillrange list
```

## 2. Grade the known-pass fixture (expect exit 0)

```bash
skillrange grade K01 --submission katas/K01-loop-contract/fixtures/pass
echo Exit: $?
```

On Windows PowerShell: `$LASTEXITCODE` should be `0`.

## 3. Grade the known-fail fixture (expect exit 2)

```bash
skillrange grade K01 --submission katas/K01-loop-contract/fixtures/fail
echo Exit: $?
```

Expect exit `2`. That is the gate contract, not a crash.

## 4. Try the starter (usually exit 2 until filled)

```bash
cp -r katas/K01-loop-contract/starter /tmp/k01
# edit /tmp/k01 until required LOOP_CONTRACT headings exist
skillrange grade K01 --submission /tmp/k01
```

## What you just proved

A frozen grader can dogfood pass and fail without reading chat. Same pattern as CI on this repo.

Next: [SKILL_MAP.md](../skills/SKILL_MAP.md) for K02+. Reliability limits: [../docs/RELIABILITY_CARD.md](../docs/RELIABILITY_CARD.md).
