# OLMo-2 extension

This folder records a third-family extension of the frozen v11 benchmark.
The v11 Qwen, Mistral, and DAX/WUG numbers are unchanged.

The pinned model is `allenai/OLMo-2-1124-7B-Instruct` at revision
`470b1fba1ae01581f270116362ee4aa1b97f4c84`. The five-token bridge and the
source-neutralisation test passed in the four-episode GPU smoke run recorded
in `OLMO2_SMOKE_JOB_6a916c9745686a1580c11556.log`.

The larger run used the settings in `OLMO2_EXTENSION_MANIFEST.json`, which
were frozen before launch. The final log and machine-readable result are
included here.

The hidden-state movement was **0.58722** (95% CI [0.58430, 0.59009]) after
the same-history control. All 256 episode values were positive. The bridge
cut gave zero hidden-state distance.

The full next-token logit movement was **0.03286** (95% CI [-0.03762,
0.10720]) after the same-history control. Its interval includes zero, so this
endpoint is not treated as a positive result. The bridge cut gave zero logit
distance.

This extension therefore gives a positive hidden-state result and an
inconclusive full-logit result. It is a new extension result, not an update to
the frozen v11 numbers. The raw final log contains all eight
`OLMO2_RECORDS_CHUNK` lines.

- Job: `6a916eeb45686a1580c115a9`
- Raw log: `OLMO2_EXTENSION_JOB_6a916eeb45686a1580c115a9_RAW_FINAL.log`
- Result: `OLMO2_RESULT.json`

This extension tests the same causal-history question as CHB. It is not a
consciousness test and cannot establish phenomenal experience.
