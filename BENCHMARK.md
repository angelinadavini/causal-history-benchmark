# Benchmark specification

## Core question

Does acquisition history leave a causal trace after the original source is unavailable and the current task information is supplied again?

## Acquisition variable

Current development work uses two routes:

- **examples** — the model receives demonstrations from which the rule can be inferred;
- **explicit** — the model receives the same rule directly.

The current task content is matched across routes.

## Retained state

A fixed bridge follows the acquisition material:

> History processed. Ready.

The bridge text is identical across routes.

After the acquisition pass, the source-prefix K/V state is replaced with a neutral control prefix. The bridge K/V state remains from the original acquisition history. The later event therefore receives the retained bridge state without direct access to the original source state.

## Later event

The later event supplies the current task information again. This prevents a route effect from being explained by one route simply retaining more usable task content than the other.

The later event is then measured before any source-report question.

## Primary measurements

### 1. Route decodability

Can a classifier identify the earlier acquisition route from the later hidden state?

Decodability is evidence that route information is present. It is not sufficient for a causal claim.

### 2. Interchange intervention

Take paired runs with the same current task content and different acquisition histories.

Replace bridge K/V state from selected layers in the recipient with bridge K/V state from the donor route.

Measure how far the recipient's later state moves toward the donor-route state.

For recipient state `y_r`, donor state `y_d`, and patched state `y_p`, the route-axis projection is:

```text
projection = ((y_p - y_r) · (y_d - y_r)) / ||y_d - y_r||²
```

Interpretation:

- 0: no movement toward donor;
- 1: reaches donor position on that route axis;
- values above or below this range are possible.

### 3. Same-route control

Swap bridge K/V state between two runs from the same acquisition route using different random session material.

A large cross-route movement together with a near-zero same-route movement supports a route-specific causal effect.

### 4. Random-direction control

Where a learned route direction is used, compare it with random directions of the same norm.

### 5. Held-out wording

Learn a route direction from several surface templates and evaluate it on a held-out template.

This tests whether the effect generalizes beyond one exact phrasing.

## Current development tasks

### SAME / DIFFERENT

Two content modes are used:

- SAME: input 0 maps to 0 and input 1 maps to 1;
- DIFFERENT: input 0 maps to 1 and input 1 maps to 0.

The route variable is examples versus direct instruction.

The current instruction is supplied again during the later event.

### DAX / WUG

An arbitrary mapping uses two symbols and two output labels:

- DAX -> X, WUG -> Y;
- or the reversed mapping.

The mapping is acquired from examples or direct instruction. The current mapping is supplied again during the later event.

## Required controls before a confirmatory claim

- fresh untouched seeds;
- frozen prompt templates;
- frozen intervention layers;
- frozen outcome layers;
- frozen statistics and equivalence bounds;
- at least two model families;
- more than one task family;
- same-route state swaps;
- random or norm-matched intervention controls;
- surface-template holdout;
- current task information supplied equally across histories;
- source-prefix neutralization verified;
- output-token calibration;
- model-specific tokenizer checks.

## Planned extensions

- Gemma / Llama-family replication;
- state-space or recurrent architecture comparison;
- finer layer and token localization;
- K-only versus V-only interventions;
- bridge-token ablations;
- output/logit mediation;
- source attribution with a bias-resistant measure;
- benchmark dataset release on Hugging Face.
