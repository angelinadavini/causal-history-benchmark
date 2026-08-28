# OLMo-2 extension protocol

This is a new model-family extension. It does not change the frozen v11
Qwen, Mistral, or DAX/WUG result.

## Question

If OLMo-2 receives the same rule through examples or a direct instruction,
does the earlier route still change later processing after the source prefix
is neutralised and the current rule is supplied again?

## Frozen setup

- Model: `allenai/OLMo-2-1124-7B-Instruct`
- Revision: `470b1fba1ae01581f270116362ee4aa1b97f4c84`
- Task: SAME/DIFFERENT
- Episodes: 256, balanced across the two rules and two new-bit values
- Seed: `20260828`
- Bridge text: `History processed. Ready.\n`
- Bridge length: five tokens at the frozen revision
- Source state: first padded history block replaced with the neutral-history cache
- Later event: the same current rule and new item are supplied in both histories
- Interchange: bridge K/V from the other route, in layers 0--5
- Later hidden outcome: layer 8, final query position
- Logit outcome: complete next-token vector at the final query position
- Control: matched same-route bridge swap from another nonce
- Path cut: later bridge attention disabled while the source remains neutralised
- Confidence interval: percentile bootstrap, 10,000 draws, seeds 20260929--20260932
- Chunk size: 32 records per `OLMO2_RECORDS_CHUNK` log line

## Counts and interpretation

The episode count is fixed before the larger run. The run is valid only if
the model loads, answer tokenisation is stable in context, the source
replacement is applied, the bridge can be moved, the same-route control runs,
the hidden and complete-logit outcomes are finite, and the bridge path cut
can be evaluated. An apparatus failure is reported as engineering failure.

If the setup passes, report the measured hidden and logit movement, controls,
path-cut values, and bootstrap intervals. Do not call this a universal model
claim, and do not infer phenomenal consciousness from this extension.

## Exact command

```text
python scripts/run_olmo2_extension.py --model allenai/OLMo-2-1124-7B-Instruct --revision 470b1fba1ae01581f270116362ee4aa1b97f4c84 --episodes 256 --seed 20260828 --patched-layers 6 --outcome-layer 8 --chunk-size 32
```
