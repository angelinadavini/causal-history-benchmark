# Add a model result

The most useful contribution is simple: run the same question on another model and show exactly what happened.

## Keep the question the same

Before you run anything, read [`BENCHMARK.md`](BENCHMARK.md).

CHB asks:

> After the old teaching information is gone and the same rule is available now, does the way the model learned that rule earlier still change what happens next?

You can change the model, task, internal state, or intervention method. Do not quietly change the question.

## Save enough for someone else to check your run

Keep:

- model name and exact revision;
- tokenizer revision;
- software versions;
- hardware;
- the two learning conditions;
- the later task;
- random seeds;
- how you removed the original teaching state;
- what state remained;
- what state you moved or changed;
- where you measured the later result;
- cross-history result;
- same-history control;
- path-cut result;
- anything that failed or had to be changed.

## Make sure the setup works before calling a result negative

A model can fail because the experiment is broken.

Check that:

- the model can do the later task;
- the tokenizer produces the answer boundaries you expect;
- the state you want to move actually exists;
- source removal works;
- the later task still has the current rule it needs.

If one of those checks fails, report the setup failure. Do not call it evidence that the model lacks the effect.

## What to add to the repo

Use this layout:

```text
replications/<short-model-name>/README.md
replications/<short-model-name>/result.json
replications/<short-model-name>/run.py
```

Then add one row to [`LEADERBOARD.md`](LEADERBOARD.md).

The README should explain the run in normal language. The JSON should contain the exact values. The script should be enough for another researcher to see how the result was produced.

## Negative results are useful

If the setup worked and the history effect was absent, submit it.

A clean negative result on another model or architecture is useful. It tells us where the effect does and does not appear.

If the setup itself failed, document that too. Somebody else may be able to fix it instead of wasting time on the same problem.
