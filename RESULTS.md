# Current development results

These results are exploratory development results. They are preserved publicly for auditability and will not be treated as confirmatory evidence until the final protocol is frozen and rerun on fresh seeds.

## Qwen2.5-3B-Instruct

### Held-out template route test

A route direction was learned from three example/direct-instruction templates and tested on a fourth held-out template.

The original source prefix was neutralized. The same fixed bridge tokens remained. The current SAME/DIFFERENT instruction was supplied again during the later event.

Later hidden-state route classification:

| Later layer | Baseline route identification | Learned route intervention -> donor | Matched random -> donor |
|---|---:|---:|---:|
| 8 | 96.9% | 100.0% | 0.0% |
| 18 | 99.2% | 53.1% | 25.0% |
| 28 | 99.2% | 29.7% | 6.3% |
| 36 | 98.4% | 28.9% | 8.6% |

The strongest causal effect appears early in processing of the later event.

### Strict cross-content test

The route direction was learned within one content mode only and tested on the opposite content mode using the held-out surface template. Twenty random controls were used.

At layer 8:

- train SAME, test DIFFERENT: donor-route steering = **100%**; mean random donor rate = **14.3%**;
- train DIFFERENT, test SAME: donor-route steering = **100%**; mean random donor rate = **8.0%**.

This test reduces the possibility that the direction is only encoding the specific SAME/DIFFERENT task content.

### Direct interchange localization

Bridge K/V state was swapped one early layer at a time and cumulatively. Outcome was measured at later layer 8.

| Patched bridge state | Cross-route projection | Same-route control |
|---|---:|---:|
| layer 1 | 0.008 | 0.0006 |
| layer 2 | 0.102 | 0.0006 |
| layer 3 | 0.358 | 0.0008 |
| layer 4 | 0.139 | 0.0005 |
| layer 5 | 0.038 | 0.0003 |
| cumulative 0-3 | 0.468 | 0.0011 |
| cumulative 0-4 | 0.608 | 0.0007 |
| cumulative 0-5 | **0.646** | **0.0009** |

For cumulative layers 0-2 through 0-5, all 64 pairs moved in the cross-route direction.

### Second task: DAX / WUG mapping

A second task used arbitrary DAX/WUG mappings with X/Y outputs. The source prefix was neutralized and the current mapping was supplied again during the later event.

On 64 pairs:

- cross-route projection: **0.569**;
- same-route control: **0.0013**;
- cross-route positive direction: **64/64**;
- mean later route-state distance: **1.179**.

This is an independent task-level replication inside the same Qwen model.

## Mistral-7B-Instruct-v0.3

A first cross-model replication used 4-bit NF4 quantization on Mistral-7B-Instruct-v0.3.

Bridge K/V state from layers 0-4 was swapped between example-history and direct-history runs. The later event was measured at layer 7.

On 64 pairs:

- mean cross-route projection: **0.809**;
- median cross-route projection: **0.809**;
- same-route control: **0.031**;
- cross-route positive direction: **64/64**;
- mean relative distance from patched state to donor target: **0.385**.

This result shows the effect is not confined to Qwen2.5-3B-Instruct.

A full-precision Mistral replication was queued later and did not complete; the public claim currently rests on the completed 4-bit Mistral development run.

## Earlier state-retention result

In a separate probe experiment using Qwen2.5-3B-Instruct, a random five-digit code appeared before a fixed bridge. Linear probes were trained only on K/V state from the final bridge token.

Ten-way chance was 10% per digit.

Best layer mean digit accuracy: **57.7%**.

Individual digit accuracies at layer 34:

- 80.0%;
- 60.0%;
- 36.7%;
- 43.3%;
- 68.3%.

One digit reached 95% at layer 35.

This result is used only to show that source information can remain decodable in downstream state. KV information persistence itself is already established in prior work and is not a novelty claim of this benchmark.

## Failed development tests preserved on purpose

Several tests failed and changed the design:

- Qwen2.5-0.5B-Instruct was below task capacity.
- One-pass sparse attention masks degraded direct-source performance and were rejected as the primary design.
- Fixed untrained bridge states often retained decodable information without reliably controlling later answers.
- A later source-report question showed a severe response bias and is not currently used as evidence.
- Several relational and parity tasks failed positive controls and were rejected before hypothesis interpretation.

These failures are part of the benchmark development record because they prevent apparatus failures from being mistaken for scientific null results.

## Current safe claim

The current development evidence supports this statement:

> In the tested decoder-only language models, acquisition route can leave a retained state that survives removal of the original source state and causally changes the internal processing of a later event, even when the current task information is supplied again.

This statement remains development-level until the confirmatory protocol is frozen and rerun.
