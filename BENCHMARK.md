# What the Causal History Benchmark tests

## The question

A model can know the same rule now and still have reached that point in different ways.

CHB asks:

> After the original teaching information is gone and the same rule is supplied again, does the way the model learned it earlier still change what happens next?

## The two learning routes

The current benchmark uses two ways of learning the same rule:

- **examples** — the model works out the rule from demonstrations;
- **direct instruction** — the rule is stated plainly.

The rule itself is matched. The difference is how the model got it.

## What remains after learning

Both learning conditions end with the same short bridge text:

> History processed. Ready.

The words are identical in both conditions. The internal state attached to those words may differ because the model reached them through different learning histories.

Before the later test, the K/V state for the original examples or instruction is replaced with K/V from a matched neutral history. The bridge state from the real learning event is kept.

So the model cannot simply reread the original teaching material.

## The later test

The rule is stated again during the later event.

This means both conditions know the same rule at the time we measure them.

If they still differ, the difference cannot be explained by one condition having the rule and the other not having it.

## The causal test

We take the bridge K/V from one learning history and put it into the other condition.

Then we measure a later hidden state and the full next-token logit vector.

If the bridge carries a causal effect of the earlier learning history, moving that bridge state should move the later computation toward the condition it came from.

For a recipient vector `a`, the unpatched opposite-history vector `b`, and the result after the bridge swap `z`, movement is measured as:

```text
p(a,z,b) = ((z-a) · (b-a)) / (||b-a||² + 1e-9)
```

A value of `0` means no movement toward the opposite history along that axis.

A value of `1` means full movement to the unpatched opposite-history position on that axis.

Values below 0 or above 1 are possible.

We test both directions and average them within each paired episode.

## The controls

### Same-history swap

A bridge swap can change a model simply because state was replaced.

So each cross-history swap is compared with a swap from another run that learned the rule in the same way.

The reported net effect is:

```text
cross-history movement - same-history movement
```

### Remove the original source

The original examples or instruction are replaced with neutral K/V before the later test.

The later result therefore cannot come from directly rereading the original source state.

### Give the rule again

The same rule is supplied again during the later event.

The test is therefore about whether the earlier learning history still changes the model after the current rule has been made the same.

### Cut access to the bridge

We also stop the later event from attending to the bridge positions.

If the measured history difference depends on that bridge, cutting access should remove or sharply reduce the difference.

In all three frozen v11 confirmatory tests, the measured hidden-state and full-logit route distance fell to zero when bridge access was removed.

### Check tokenisation before running

Answer strings can split differently across tokenizers and prompt contexts.

That caused an invalid first confirmatory launch. The frozen protocol therefore checks candidate answers in context before a scientific run begins.

## The two tasks used in v11

### SAME / DIFFERENT

- SAME: 0 maps to 0 and 1 maps to 1.
- DIFFERENT: 0 maps to 1 and 1 maps to 0.

The current SAME or DIFFERENT rule is stated again during the later event.

### DAX / WUG

The mapping is counterbalanced:

- DAX -> X, WUG -> Y;
- DAX -> Y, WUG -> X.

The mapping is learned from examples or direct instruction and is stated again during the later event.

## The frozen v11 tests

| Test | Model | Task | Paired episodes | Bridge layers moved | Later hidden layer |
| --- | --- | --- | ---: | --- | ---: |
| Primary | Qwen2.5-3B-Instruct | SAME/DIFFERENT | 512 | 0–5 | 8 |
| Second model | Mistral-7B-Instruct-v0.3 | SAME/DIFFERENT | 256 | 0–4 | 7 |
| Second task | Qwen2.5-3B-Instruct | DAX/WUG | 256 | 0–5 | 8 |

The two main outcomes are movement of:

1. the later hidden state;
2. the complete next-token logit vector.

For the primary Qwen test, both frozen 95% confidence intervals had to be above zero.

## Statistics used in the frozen study

The frozen analysis reports:

- the mean across episodes;
- a stratified bootstrap 95% confidence interval using 10,000 resamples;
- a paired sign-flip value using 100,000 Monte Carlo draws;
- the fraction of episodes with a positive effect.

The answer-margin and two-token probability measures were secondary. Their frozen results are kept in [`RESULTS.md`](RESULTS.md).

## If you test another model

Report enough information for another researcher to understand exactly what you did:

- model and exact revision;
- tokenizer revision;
- the two learning routes;
- how task content was balanced;
- how the original source was removed;
- what state remained;
- what state you moved or changed;
- where you measured the later result;
- cross-history movement;
- same-history movement;
- the path-cut result or the closest equivalent for that architecture;
- random seeds;
- software versions;
- hardware.

A model does not need transformer K/V state to be tested with CHB. If it carries history in another kind of state, use that state and keep the same causal question.
