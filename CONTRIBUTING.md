# Contributing a replication

The main contribution this repository wants is a clean attempt to run the causal-history test on another model or architecture.

## Before running

Read [BENCHMARK.md](BENCHMARK.md). Keep the scientific question fixed:

> After the same usable relation is acquired through different routes, does route-dependent retained state causally change a later event once the original source is unavailable and the current relation is supplied again?

Do not begin with a consciousness label. Measure the machine state first.

## Minimum experiment record

Please preserve:

- model ID and exact revision;
- tokenizer revision;
- software versions;
- hardware;
- acquisition prompts or generator;
- later-event prompt or generator;
- random seeds;
- source-removal or neutralisation method;
- retained state object;
- intervention locations;
- outcome location;
- cross-route donor result;
- matched same-route donor result;
- path-removal result;
- failures and deviations.

## Positive controls

A failed later-history test is interpretable only when the apparatus itself works.

Check that the model can solve the current task, the intervention state exists, the later event can use the required current information, and the model/tokenizer handles the answer format correctly.

If these controls fail, report an engineering failure instead of a scientific null.

## Pull request layout

Add:

```text
replications/<short-model-name>/README.md
replications/<short-model-name>/result.json
replications/<short-model-name>/run.py
```

Then add one row to [LEADERBOARD.md](LEADERBOARD.md).

The result JSON should identify every quantity needed to understand the leaderboard row.

## Claims

Describe what the intervention establishes in the tested system. Do not convert a causal-history result into a claim of consciousness, sentience, or phenomenal experience.

## Failed replications

Failed replications are welcome when the controls passed. A clean null on a new architecture is scientifically useful.

If the apparatus failed, document the failure clearly so another researcher does not repeat it.
