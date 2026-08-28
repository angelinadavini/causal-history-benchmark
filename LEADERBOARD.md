# Causal History Benchmark leaderboard

This table is for reproducible model and architecture replications.

A row belongs here only when the submission documents source removal or neutralisation, the retained state, the cross-route intervention, and a matched control.

## Confirmed reference results

| Model | Task | Pairs | Retained state | Later outcome | Net causal movement | Path-removal result | Status |
| --- | --- | ---: | --- | --- | ---: | ---: | --- |
| Qwen2.5-3B-Instruct | SAME/DIFFERENT | 512 | bridge K/V, layers 0–5 | hidden layer 8 | **0.68747** | route distance -> 0 | frozen confirmatory |
| Qwen2.5-3B-Instruct | SAME/DIFFERENT | 512 | bridge K/V, layers 0–5 | complete next-token logits | **0.25833** | route distance -> 0 | frozen confirmatory |
| Mistral-7B-Instruct-v0.3 | SAME/DIFFERENT | 256 | bridge K/V, layers 0–4 | hidden layer 7 | **0.80099** | route distance -> 0 | frozen confirmatory |
| Mistral-7B-Instruct-v0.3 | SAME/DIFFERENT | 256 | bridge K/V, layers 0–4 | complete next-token logits | **0.05865** | route distance -> 0 | frozen confirmatory |
| Qwen2.5-3B-Instruct | DAX/WUG | 256 | bridge K/V, layers 0–5 | hidden layer 8 | **0.60515** | route distance -> 0 | frozen confirmatory |
| Qwen2.5-3B-Instruct | DAX/WUG | 256 | bridge K/V, layers 0–5 | complete next-token logits | **0.04717** | route distance -> 0 | frozen confirmatory |

## Community results

No external replication has been accepted yet.

| Model / system | Architecture | Task | Retained state | Cross-route effect | Same-route control | Path-removal control | Code / result | Status |
| --- | --- | --- | --- | ---: | ---: | ---: | --- | --- |
| — | — | — | — | — | — | — | — | open |

## Submit a result

Open a pull request with:

1. an exact model ID and revision;
2. tokenizer revision where relevant;
3. task definition;
4. acquisition routes;
5. source-removal or neutralisation method;
6. retained state definition;
7. intervention locations;
8. same-route donor control;
9. path-removal or architecture-appropriate carrier check;
10. seed and software manifest;
11. a machine-readable result file;
12. code needed to reproduce the row.

Results that fail a positive control are still useful and may be documented in a separate failure table, though they will not be counted as evidence against causal history unless the apparatus itself worked.

## Architecture challenge

The most valuable replications now are systems whose continuing state is not transformer K/V:

- state-space models;
- recurrent language models;
- memory-augmented models;
- multimodal agents with persistent internal state;
- models with explicit learned compression or recurrent memory.

For those systems, preserve the benchmark question and replace the carrier intervention with the native state object.
