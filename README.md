# Causal History Benchmark

**Does the way a model learned something leave a causal trace that changes later processing?**

The Causal History Benchmark tests whether the same usable information, acquired through different routes, leaves different retained states inside a language model.

The first experiments compare two acquisition histories:

- learning a rule from examples;
- receiving the same rule directly.

After acquisition, the original source state is replaced with neutral state. A short fixed bridge remains:

> History processed. Ready.

The current rule is supplied again during the later task. This makes the later task solvable without recovering the old source. We then ask whether the earlier acquisition route still changes the model's internal processing of the new event.

## What the current experiments show

Development experiments currently support four findings.

1. **Acquisition route remains recoverable after the original source state is neutralized.** In Qwen2.5-3B-Instruct, later hidden states identify whether the earlier rule came from examples or direct instruction with high accuracy in early and middle processing layers.

2. **The retained route state has a causal effect on later processing.** Replacing bridge K/V state from one route with bridge K/V state from the other moves the later hidden state toward the donor route.

3. **The effect survives surface changes.** A direction learned from three acquisition templates transfers to a held-out fourth template. In the strongest Qwen development test, the donor-route intervention moved 100% of layer-8 cases toward the donor history while matched random directions were far weaker.

4. **The effect appears in more than one model family.** In Mistral-7B-Instruct-v0.3, replacing early bridge K/V state moved the later layer-7 state **0.809** of the way toward the donor route on average. A same-route control moved it **0.031**. All 64 cross-route pairs moved in the predicted direction.

A second Qwen task using arbitrary DAX/WUG mappings also replicated the causal effect:

- cross-route movement: **0.569**;
- same-route control: **0.0013**;
- positive direction: **64/64 pairs**.

These are development results. Confirmatory runs with frozen seeds, analysis, models, and intervention choices are still required.

## What this benchmark measures

The benchmark separates several questions that are often collapsed into "memory":

- Is information present in the retained state?
- Can the model use that information?
- Does the route by which the information entered remain represented?
- Does that route-specific state causally change a later event?
- Does the effect survive after the original source is unavailable?
- Does the effect generalize across tasks, wording, models, and architectures?

## What this project does not claim

This project does not provide a consciousness detector.

A causal history effect in a language model does not establish phenomenal consciousness. The benchmark measures a machine property that can be compared with established work on human conscious processing, memory, report, and source attribution.

## Current benchmark structure

```text
acquisition route
    |
    +-- examples
    |
    +-- direct instruction
            |
            v
fixed bridge state
            |
original source state neutralized
            |
            v
new event with current task information supplied again
            |
            v
measure later hidden state / logits
            |
            v
intervene on retained bridge state
```

The key causal question is whether changing only the retained route-specific state changes later processing while current task content is held fixed.

## Repository map

- [`BENCHMARK.md`](BENCHMARK.md) — benchmark definition and controls
- [`RESULTS.md`](RESULTS.md) — current development results
- [`HUGGINGFACE_JOBS.md`](HUGGINGFACE_JOBS.md) — compute-job provenance
- [`CLAIM_LIMITS.md`](CLAIM_LIMITS.md) — what the results support and what they do not
- [`ROADMAP.md`](ROADMAP.md) — confirmatory and cross-model plan
- [`scripts/`](scripts/) — reference experiment code

## Status

**Development / pre-confirmatory.**

The repository is public so the research record, benchmark design, failures, and code remain visible as the project develops. A later blinded conference submission will use a separate anonymous artifact and will not point reviewers to this named repository during review.

## Author

Angelina Davini Hintsanen

## License

Code: MIT License. See [`LICENSE`](LICENSE).

Research results and documentation may be cited with the repository URL until a versioned archival DOI is issued.
