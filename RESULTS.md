# Confirmed results

The frozen v11 study passed in Qwen, replicated in Mistral, and replicated again on a second DAX/WUG task.

## What was tested

The model learned the same rule in two ways: from examples or from a direct instruction.

Before the later test, the K/V state for the original teaching material was replaced with matched neutral K/V. The same rule was then supplied again during the later event. The only state left that still depended on how the rule had been learned was the fixed bridge.

We moved the bridge K/V from one learning history into the other condition and measured what happened later. Each cross-history swap was compared with a matched same-history swap.

The reported effect is:

```text
cross-history movement - same-history movement
```

## The three frozen tests

| Test | Model | Task | Episodes |
| --- | --- | --- | ---: |
| Primary | Qwen2.5-3B-Instruct | SAME/DIFFERENT | 512 |
| Second model | Mistral-7B-Instruct-v0.3 | SAME/DIFFERENT | 256 |
| Second task | Qwen2.5-3B-Instruct | DAX/WUG | 256 |

## Main results

| Test | Measure | Mean movement | 95% CI | Positive episodes | Sign-flip p |
| --- | --- | ---: | --- | ---: | ---: |
| Qwen primary | Later hidden state | **0.68747** | [0.68661, 0.68832] | 100.0% | 0.000010 |
| Qwen primary | Full next-token logits | **0.25833** | [0.25555, 0.26109] | 100.0% | 0.000010 |
| Mistral | Later hidden state | **0.80099** | [0.79955, 0.80245] | 100.0% | 0.000010 |
| Mistral | Full next-token logits | **0.05865** | [0.05681, 0.06056] | 100.0% | 0.000010 |
| DAX/WUG | Later hidden state | **0.60515** | [0.60352, 0.60679] | 100.0% | 0.000010 |
| DAX/WUG | Full next-token logits | **0.04717** | [0.04335, 0.05106] | 89.45% | 0.000010 |

A value of `1` would mean that the patched result moved all the way to the unpatched state produced by the other learning history along that episode's history axis. A value of `0` means no movement along that axis.

All six frozen primary endpoints passed.

## What happened when the bridge was cut

We blocked the later event from attending to every bridge position.

The hidden-state history distance fell to **0.000** in Qwen, Mistral, and DAX/WUG.

The full-logit history distance also fell to **0.000** in all three tests.

So in this setup, the later difference depended on access to the bridge.

## Wording and rule-content check

The reference centroids were built from templates 0–2 in one rule-content condition. Template 3 was tested with the opposite rule content.

| Model | History classification before patch | Donor-history classification after patch |
| --- | ---: | ---: |
| Qwen2.5-3B-Instruct | 83.50% | 75.59% |
| Mistral-7B-Instruct-v0.3 | 91.99% | 79.88% |

Template 3 was not used to build the confirmatory centroids. It had been seen during earlier development, so it is not described as completely unseen wording.

## Answer-level measures

These were secondary measures.

| Test | Correct-answer margin movement, 90% CI | Two-token probability movement, 90% CI | Frozen equivalence result |
| --- | --- | --- | --- |
| Qwen primary | 0.45166 [0.43629, 0.46694] | 0.00562 [0.00467, 0.00658] | Failed |
| Mistral | 0.01162 [0.01093, 0.01231] | 0.00232 [0.00216, 0.00248] | Passed |
| DAX/WUG | -0.04874 [-0.05872, -0.03870] | -0.01116 [-0.01320, -0.00912] | Passed |

The Qwen correct-answer margin was outside the frozen ±0.20-logit equivalence range. No choice-flip rule had been frozen. The confirmed output result is therefore about movement of the complete next-token distribution. It is not a robust overt-choice result.

## Frozen job record

Valid Hugging Face jobs:

- Qwen primary: `6a90939f45686a1580c0f60e`
- Mistral replication: `6a9093b3984507d9db4e8d7d`
- amended Qwen DAX/WUG: `6a90c7e345686a1580c0fe2a`

Frozen manifest hashes:

- base v2: `fb42c0f7e984c8e775b55960eb5c7f9be02d6eff8944bcdb198223435764a7d2`
- secondary v2.1: `570f3119f16b32942c0bae5fdbdeb8396311a76c3bb8fed1b6eea577fc69cb54`

## Failed attempts kept in the record

These are kept because they changed how the final experiment was built:

- the verbal source question failed because the model fell into a response bias;
- learned-direction steering did not move answer logits more selectively than a matched random change;
- a fixed untrained bridge could store readable information without reliably controlling the next answer;
- Qwen2.5-0.5B-Instruct could not reliably do the task;
- one sparse-attention masking setup damaged normal task performance and was dropped;
- the first confirmatory launch was stopped before scientific output was inspected because a tokenizer assumption failed on Mistral;
- the first DAX/WUG confirmatory attempt stopped on its first episode because adding `X` changed the query-token boundary.

An apparatus failure is not counted as evidence for or against the scientific claim.

## Third-family extension: OLMo-2

This is a new extension result. It does not change the frozen v11 values
above.

The run used `allenai/OLMo-2-1124-7B-Instruct` at revision
`470b1fba1ae01581f270116362ee4aa1b97f4c84`, with 256 episodes of the
SAME/DIFFERENT task. The source state was neutralised, the same current rule
was supplied again, and bridge K/V from the other learning history was moved
at layers 0--5. A same-history swap was the control. The later hidden state was
measured at layer 8, along with the complete next-token logit vector.

| Measure | Cross-history movement | Same-history control | Net movement | 95% CI for net | Bridge cut |
| --- | ---: | ---: | ---: | --- | ---: |
| Later hidden state | 0.58816 | 0.00095 | **0.58722** | [0.58430, 0.59009] | 0.00000 |
| Complete next-token logits | 0.03700 | 0.00414 | **0.03286** | [-0.03762, 0.10720] | 0.00000 |

All 256 hidden-state net values were positive. The logit net was positive in
119 of 256 episodes (46.48%). The hidden-state result is positive under the
frozen extension analysis. The full-logit endpoint is inconclusive because
its interval includes zero. The complete raw log and every episode record are
in [`replications/olmo2/`](replications/olmo2/).

## The result in plain English

> The way the model learned the same information earlier changed what happened later. The original source state had been removed and the same current rule had been supplied again. Moving the bridge state left by one learning history into the other condition moved both a later hidden state and the complete next-token output toward the history that supplied the bridge. The result replicated in another model family and another task. When the bridge could no longer be used, the measured history difference disappeared.

## Multi-event correction extension

This separate extension asks what remains after a later event explicitly
reverses the first rule. The model learns SAME or DIFFERENT from examples or a
direct instruction, the original source state is neutralised, and a correction
event reverses the rule. The corrected rule is supplied again in the final
event. The second bridge state is exchanged across histories, with a
same-history exchange as the control.

| Model | Episodes | Final hidden-state net | 95% CI | Final full-logit net | 95% CI | Full retained-state cut |
| --- | ---: | ---: | --- | ---: | --- | ---: |
| Qwen2.5-3B-Instruct | 256 | 0.00482 | [0.00016, 0.00943] | -0.00852 | [-0.01125, -0.00581] | 0.00000 |
| OLMo-2-1124-7B-Instruct | 256 | 0.02658 | [0.02499, 0.02816] | -0.03626 | [-0.04480, -0.02763] | 0.00000 |

The final hidden-state endpoint stayed above zero in both runs. The complete
next-token logit endpoint moved below zero in both runs. The correction test
therefore gives a small retained hidden-state effect under this protocol and
does not give a positive full-logit result. It is an extension and does not
change the frozen v11 values. Full records, raw logs, manifests, and the
analysis files are in
[`replications/multi_event_correction/`](replications/multi_event_correction/).
