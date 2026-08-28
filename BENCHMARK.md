# Benchmark contract

## Core question

Does acquisition history leave a causal trace after the original source is unavailable and the current task relation is supplied again?

## Acquisition variable

The current benchmark uses two routes to the same functional relation:

- **examples** — demonstrations from which the relation can be inferred;
- **explicit** — the relation is stated directly.

The later task relation is the same across routes.

## Retained carrier

A fixed bridge follows the acquisition material:

> History processed. Ready.

The bridge text is identical across routes.

After acquisition, the source-history prefix is replaced with K/V state from a length-matched neutral history. Route-dependent bridge K/V remains from the real acquisition event.

The later event receives the retained bridge state without direct access to the original examples or direct instruction.

## Later event

The current task relation is supplied again during the later event.

This is a central control. The later computation does not need the old source to recover which relation is currently in force. A remaining route effect therefore concerns history left by how that same relation was acquired.

## Causal intervention

For paired runs with the same current relation and different acquisition histories, replace early bridge K/V in the recipient with bridge K/V from the opposite acquisition route.

For recipient vector `a`, unpatched opposite-route vector `b`, and intervened vector `z`, movement along the route axis is:

```text
p(a,z,b) = ((z-a) · (b-a)) / (||b-a||² + 1e-9)
```

Interpretation:

- `0` — no movement from the recipient along the route axis;
- `1` — full movement to the unpatched donor position on that axis;
- values outside `[0,1]` are possible.

Both route directions are tested and averaged within each paired episode.

## Required controls

### Same-route donor

Replace bridge K/V with an independent donor from the same acquisition route, same task content, and a different session nonce.

The reported net causal effect is:

```text
cross-route movement - matched same-route movement
```

### Source neutralisation

The source-history prefix must be replaced with neutral-history state before the later event.

### Current-content control

The current task relation must be supplied again during the later event.

### Bridge-path check

Remove later-event attention to every bridge position while leaving the current relation available in the later query.

A route difference that survives this intervention cannot be attributed to the tested bridge path.

### Tokenizer preflight

Candidate answer strings must be tested in context for every pinned model/tokenizer and task. The original confirmatory launch exposed why bare-token assumptions are unsafe.

## Frozen confirmatory tasks

### SAME / DIFFERENT

- SAME: 0 maps to 0 and 1 maps to 1.
- DIFFERENT: 0 maps to 1 and 1 maps to 0.

The current instruction is supplied again during the later event.

### DAX / WUG

The mapping is counterbalanced:

- DAX -> X, WUG -> Y;
- DAX -> Y, WUG -> X.

The mapping is acquired from examples or direct instruction and is supplied again in the later event.

## Frozen v11 arms

| Arm | Model | Task | Paired episodes | Bridge layers | Later hidden layer |
| --- | --- | --- | ---: | --- | ---: |
| Primary | Qwen2.5-3B-Instruct | SAME/DIFFERENT | 512 | 0–5 | 8 |
| Cross-model | Mistral-7B-Instruct-v0.3 | SAME/DIFFERENT | 256 | 0–4 | 7 |
| Second task | Qwen2.5-3B-Instruct | DAX/WUG | 256 | 0–5 | 8 |

The primary endpoints are net route-axis movement of:

1. the fixed later hidden state;
2. the complete next-token logit vector.

The Qwen primary arm succeeds only when both two-sided 95% confidence intervals lie above zero.

## Statistics

The frozen analysis reports:

- episode mean;
- stratified bootstrap confidence interval with 10,000 resamples;
- paired sign-flip value with 100,000 Monte Carlo draws;
- positive-effect fraction.

Answer-margin and two-token-probability endpoints are secondary. Their equivalence rules are documented in [RESULTS.md](RESULTS.md).

## What counts as a community benchmark result

A submitted model result should report at minimum:

- exact model and revision;
- tokenizer revision;
- acquisition route definitions;
- task-content balancing;
- source-neutralisation implementation;
- retained carrier;
- intervention locations;
- later outcome location;
- cross-route movement;
- same-route donor movement;
- bridge/path-removal control or an architecture-appropriate equivalent;
- random seeds;
- software versions;
- hardware.

If an architecture does not use transformer K/V state, use the same causal question with its native retained state. Document what state was removed, what state remained, and what was intervened on.

## Claim boundary

A positive benchmark result establishes a causal history effect for the tested model, task, and state intervention. It does not establish phenomenal consciousness or a unique criterion for consciousness.
