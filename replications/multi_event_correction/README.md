# Multi-event correction extension

This extension asks one extra question:

After the model learns a rule, can a later correction remove the effect of how
the rule was first learned?

The model first learns SAME or DIFFERENT from examples or a direct instruction.
The original source state is then neutralised. A later event reverses the rule.
The corrected rule is supplied again in a final event with a new item.

The state after the correction is exchanged between the two initial learning
routes. A same-route exchange is the control. The final hidden state and the
complete next-token logit vector are measured. The run also cuts access to all
post-source positions and to the second bridge alone.

This is a new extension. It does not change the frozen v11 results.

The frozen protocol is [`MULTI_EVENT_CORRECTION_PROTOCOL_v1.md`](MULTI_EVENT_CORRECTION_PROTOCOL_v1.md).
The Qwen manifest is [`MULTI_EVENT_CORRECTION_MANIFEST_QWEN_v1.json`](MULTI_EVENT_CORRECTION_MANIFEST_QWEN_v1.json).
The runner and analysis file are kept beside it for exact reproduction.

## Results

Both 256-episode runs completed. The raw logs contain all eight record chunks
per run. The manifest, runner, and protocol hashes passed the analysis checks.

| Model | Later hidden-state net movement | 95% CI | Full-logit net movement | 95% CI | Full retained-state cut |
| --- | ---: | --- | ---: | --- | ---: |
| Qwen2.5-3B-Instruct | 0.00482 | [0.00016, 0.00943] | -0.00852 | [-0.01125, -0.00581] | 0.00000 |
| OLMo-2-1124-7B-Instruct | 0.02658 | [0.02499, 0.02816] | -0.03626 | [-0.04480, -0.02763] | 0.00000 |

The hidden-state endpoint stayed above zero after one correction event in both
runs. The full next-token logit endpoint moved in the negative direction in
both runs. The second-bridge cut remained available in the raw records; these
results do not show that the first learning route survives correction in the
full output distribution.

The Qwen raw log and result are in
[`MULTI_EVENT_CORRECTION_QWEN_JOB_6a918c7b45686a1580c119b0_RAW_FINAL.log`](MULTI_EVENT_CORRECTION_QWEN_JOB_6a918c7b45686a1580c119b0_RAW_FINAL.log)
and [`MULTI_EVENT_CORRECTION_QWEN_RESULT.json`](MULTI_EVENT_CORRECTION_QWEN_RESULT.json).
The OLMo raw log and result are in
[`MULTI_EVENT_CORRECTION_OLMO2_JOB_6a918db2984507d9db4e9dbc_RAW_FINAL.log`](MULTI_EVENT_CORRECTION_OLMO2_JOB_6a918db2984507d9db4e9dbc_RAW_FINAL.log)
and [`MULTI_EVENT_CORRECTION_OLMO2_RESULT.json`](MULTI_EVENT_CORRECTION_OLMO2_RESULT.json).
