# K12 : Corpus hash freeze

Time box: 1–2h.

Provide `baseline.json` with `corpus_sha256` matching sha256 of `corpus.txt`.

## Common fail

Hand-writing a guessed hash fails. Hash corpus.txt with sha256 hex digest into corpus_sha256.

## Example fill

`ash
sha256sum corpus.txt
# put the hex digest in baseline.json as corpus_sha256
`

