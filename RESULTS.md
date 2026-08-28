# Confirmatory results

The frozen confirmatory prediction passed in the primary Qwen arm, the Mistral cross-model arm, and the Qwen DAX/WUG second-task arm.

## Design

The same usable relation was acquired through examples or direct instruction.

The source-history prefix was replaced with neutral-history K/V state. The current task relation was supplied again during the later event. Acquisition route remained only in the fixed bridge state.

Early bridge K/V from the opposite route was then interchanged. The matched control used a donor from the same route. Reported effects are cross-route movement minus same-route movement.

## Frozen arms

| Arm | Model | Task | Episodes |
| --- | --- | --- | ---: |
| Primary | Qwen2.5-3B-Instruct | SAME/DIFFERENT | 512 |
| Cross-model replication | Mistral-7B-Instruct-v0.3 | SAME/DIFFERENT | 256 |
| Second-task replication | Qwen2.5-3B-Instruct | DAX/WUG | 256 |

## Primary endpoints

| Arm | Outcome | Mean net movement | 95% CI | Positive episodes | Paired sign-flip p |
| --- | --- | ---: | --- | ---: | ---: |
| Qwen primary | Later hidden state | **0.68747** | [0.68661, 0.68832] | 100.0% | 0.000010 |
| Qwen primary | Complete logit vector | **0.25833** | [0.25555, 0.26109] | 100.0% | 0.000010 |
| Mistral replication | Later hidden state | **0.80099** | [0.79955, 0.80245] | 100.0% | 0.000010 |
| Mistral replication | Complete logit vector | **0.05865** | [0.05681, 0.06056] | 100.0% | 0.000010 |
| DAX/WUG replication | Later hidden state | **0.60515** | [0.60352, 0.60679] | 100.0% | 0.000010 |
| DAX/WUG replication | Complete logit vector | **0.04717** | [0.04335, 0.05106] | 89.45% | 0.000010 |

A route-axis value of one means full movement from the recipient state to the unpatched opposite-route state along that episode's route axis. Zero means no movement along that axis.

## Bridge-path intervention

Removing later-event attention to every bridge position reduced the hidden-state route distance to **0.000** in all three arms.

The complete-logit route distance also fell to **0.000** in all three arms.

Within this implementation, access to the retained bridge is necessary for the measured route difference.

## Content and wording transfer

Reference route centroids used acquisition templates 0–2 in one content mode. Evaluation used template 3 in the opposite content mode.

| Model | Unpatched route classification | Donor-route classification after interchange |
| --- | ---: | ---: |
| Qwen2.5-3B-Instruct | 83.50% | 75.59% |
| Mistral-7B-Instruct-v0.3 | 91.99% | 79.88% |

Template 3 was held out from reference-centroid estimation in the confirmatory run. It had been inspected during exploratory development, so it is not described as investigator-unseen wording.

## Answer endpoints

The answer endpoints were secondary.

| Arm | Signed margin movement, 90% CI | Two-token probability movement, 90% CI | Frozen equivalence decision |
| --- | --- | --- | --- |
| Qwen primary | 0.45166 [0.43629, 0.46694] | 0.00562 [0.00467, 0.00658] | Failed |
| Mistral replication | 0.01162 [0.01093, 0.01231] | 0.00232 [0.00216, 0.00248] | Passed |
| DAX/WUG replication | -0.04874 [-0.05872, -0.03870] | -0.01116 [-0.01320, -0.00912] | Passed |

The Qwen correct-answer margin exceeded the frozen ±0.20-logit equivalence bound. No choice-flip rule was frozen. The confirmed output claim concerns movement of the complete next-token distribution. The study does not establish a robust overt-choice effect.

## Frozen provenance

Valid Hugging Face jobs:

- Qwen primary: `6a90939f45686a1580c0f60e`
- Mistral replication: `6a9093b3984507d9db4e8d7d`
- amended Qwen DAX/WUG: `6a90c7e345686a1580c0fe2a`

Frozen manifest hashes:

- base v2: `fb42c0f7e984c8e775b55960eb5c7f9be02d6eff8944bcdb198223435764a7d2`
- secondary v2.1: `570f3119f16b32942c0bae5fdbdeb8396311a76c3bb8fed1b6eea577fc69cb54`

## Preserved failures

The public record keeps failures that affected the design:

- the verbal source-attribution instrument failed through response bias;
- learned-direction steering did not selectively alter answer logits beyond a matched random perturbation;
- a fixed untrained bridge often retained decodable information without reliably governing the next answer;
- Qwen2.5-0.5B-Instruct was below task capacity;
- one-pass sparse attention masking degraded direct-source performance and was rejected as the main apparatus;
- the first confirmatory launch was invalidated before scientific output because a tokenizer assumption failed on Mistral;
- the first DAX/WUG confirmatory attempt stopped on its first episode because appending `X` changed the query-token boundary.

These failures are not counted as scientific nulls when the apparatus failed its own controls.

## Current safe claim

> In Qwen2.5-3B-Instruct, acquisition route left a retained bridge state after source-history neutralisation. Exchanging early bridge K/V between acquisition routes causally moved a fixed later hidden state and the complete next-token logit vector toward the donor history after the current task relation was supplied again. The effect replicated in Mistral-7B-Instruct-v0.3 and in a separate DAX/WUG mapping task. Removing later-event access to the bridge eliminated the measured route difference.

The result does not establish consciousness.
