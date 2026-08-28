# Causal History Benchmark

**If a model has the same rule in front of it now, can the way it learned that rule earlier still change what it does next?**

That is what the Causal History Benchmark tests.

In one run, the model learns a rule from examples. In another, it is told the same rule directly. We remove the original examples or instruction from the stored source state. The model gets the same rule again and the same kind of new task.

At that point, the current information is the same. What differs is how the rule was learned earlier.

CHB tests whether that earlier difference is still doing anything. It moves the stored bridge state from one learning condition into the other and measures what happens later. It also blocks the later query from using the bridge. If the bridge is carrying the effect, moving it should move the later computation and blocking it should remove the difference.

## What we found

All three frozen confirmatory tests passed.

| Test | Model | Task | Episodes | Hidden-state movement | Full-logit movement |
| --- | --- | --- | ---: | ---: | ---: |
| Primary | Qwen2.5-3B-Instruct | SAME/DIFFERENT | 512 | **0.68747** [0.68661, 0.68832] | **0.25833** [0.25555, 0.26109] |
| Second model | Mistral-7B-Instruct-v0.3 | SAME/DIFFERENT | 256 | **0.80099** [0.79955, 0.80245] | **0.05865** [0.05681, 0.06056] |
| Second task | Qwen2.5-3B-Instruct | DAX/WUG | 256 | **0.60515** [0.60352, 0.60679] | **0.04717** [0.04335, 0.05106] |

The numbers show movement toward the state produced by the other learning history after subtracting the matched same-history control.

When the later query could no longer use the bridge, the measured difference fell to **zero in all three tests**, in both hidden-state and full-logit space.

The result is simple:

> The way the model learned the same information earlier changed what happened later. The original teaching information was gone. The current rule was the same. Moving the state left by the earlier learning moved the later computation. Blocking access to that state removed the difference.

CHB measures that effect. It does not assign a consciousness score.

## A separate third-family extension

An OLMo-2 run used a new frozen protocol after the three v11 tests. Its hidden
state moved **0.58722** toward the donor history (95% CI [0.58430, 0.59009])
after the same-history control, with zero movement when the bridge path was
cut. The full next-token logit movement was **0.03286** (95% CI [-0.03762,
0.10720]), so that endpoint is recorded as inconclusive. This extension does
not change the frozen v11 results. Its protocol, raw log, and result file are
in [`replications/olmo2/`](replications/olmo2/).

## A multi-event correction extension

We also ran a separate test with an explicit correction event between the
first learning event and the final test. In 256 episodes each, Qwen and OLMo
kept a small positive hidden-state history effect after the correction:

| Model | Final hidden-state net | 95% CI | Final full-logit net | 95% CI |
| --- | ---: | --- | ---: | --- |
| Qwen2.5-3B-Instruct | **0.00482** | [0.00016, 0.00943] | -0.00852 | [-0.01125, -0.00581] |
| OLMo-2-1124-7B-Instruct | **0.02658** | [0.02499, 0.02816] | -0.03626 | [-0.04480, -0.02763] |

The full retained-state cut was zero in both runs. The hidden-state endpoint
stayed above zero; the complete next-token logit endpoint did not. These are
extension results and do not change the frozen v11 study. The raw logs,
manifests, and analysis files are in
[`replications/multi_event_correction/`](replications/multi_event_correction/).

## Run it

Clone the repo:

```bash
git clone https://github.com/angelinadavini/causal-history-benchmark.git
cd causal-history-benchmark
```

Install the benchmark and tests:

```bash
pip install -e ".[test]"
pytest -q
```

For model runs:

```bash
pip install -e ".[benchmark,test]"
chb-validate
```

Run the small Qwen reference test:

```bash
python scripts/run_benchmark.py \
  --model Qwen/Qwen2.5-3B-Instruct \
  --reps 16
```

This small run uses the same core idea as the confirmed experiment. The exact v11 study used frozen model versions, seeds, wording, layer choices, analysis rules, and tokenizer checks. Those records are kept under [`confirmatory/`](confirmatory/).

## What has to be true for a CHB result to count

A positive number on its own is not enough.

1. The model must get the same rule through two different learning routes.
2. The original examples or instruction must be removed before the later test.
3. Both conditions must get the same current rule again.
4. The cross-history swap must be compared with a same-history swap.
5. The stored history state must be changed directly. Reading it with a probe is not enough.
6. The later hidden state and full next-token output must be measured.
7. The proposed path must be cut. If the effect really depends on that path, the difference should disappear or fall as predicted.

The machine-readable result format is in [`results/result_schema.json`](results/result_schema.json).

## Test your own model

The benchmark is not meant to stop with Qwen and Mistral.

You can test another transformer, a recurrent model, a state-space model, an agent, or another system with a state that can carry earlier information forward.

The exact internal state may be different. The question stays the same:

> After the old source is gone and the same information is available now, does the way the model learned it earlier still change what happens next?

A new result should include the exact model version, tokenizer, task, learning routes, source-removal method, state that was moved, where it was moved, same-history control, path check, software versions, hardware, and a machine-readable result file.

See [`QUICKSTART.md`](QUICKSTART.md) for the shortest route and [`CONTRIBUTING.md`](CONTRIBUTING.md) if you want to add a result to the public leaderboard.

## See the confirmed v11 values

```bash
chb-v11
```

This prints the frozen endpoint values, job IDs, and bridge-cut results stored with the package.

To verify the exact v11 reproduction files without downloading model weights:

```bash
python scripts/reproduce_v11.py
```

The exact frozen runners, analysis, protocols, seed manifests, and final logs are in [`confirmatory/v11/`](confirmatory/v11/). The helper checks their hashes before any model run. Use `--run` only on a GPU with access to the pinned model revisions.

## What is in this repo

- [`BENCHMARK.md`](BENCHMARK.md) — exactly what the test does and what controls are required
- [`RESULTS.md`](RESULTS.md) — the frozen v11 results, including failed and secondary endpoints
- [`QUICKSTART.md`](QUICKSTART.md) — how to run the small reference test
- [`LEADERBOARD.md`](LEADERBOARD.md) — confirmed results and future replications
- [`MODEL_SUPPORT.md`](MODEL_SUPPORT.md) — models tested so far
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — how to add a model result
- [`confirmatory/`](confirmatory/) — frozen v11 protocol records and hashes
- [`configs/`](configs/) — machine-readable definitions of the three confirmed arms
- [`replications/`](replications/) — separate OLMo and multi-event correction runs
- [`src/causal_history/`](src/causal_history/) — reusable Python code
- [`tests/`](tests/) — package tests
- [`results/confirmatory_summary.csv`](results/confirmatory_summary.csv) — frozen result table
- [`results/extensions_summary.csv`](results/extensions_summary.csv) — separate model-extension results
- [`results/result_schema.json`](results/result_schema.json) — format for new results
- [`OUTSIDE_REPRODUCTION.md`](OUTSIDE_REPRODUCTION.md) — exact files and request for an independent run

## Why I made it public

A paper can report the first result. The useful part should not end with the paper.

I built CHB so other researchers can run the same question on another model, change the kind of learning history, test longer delays, use another way of moving internal state, or see whether the effect exists outside transformer K/V state.

If you use the benchmark, extend it, or test another model, I want the result to be directly comparable with what is already here.

## Citation

Citation information is in [`CITATION.cff`](CITATION.cff).

## Author

Angelina Davini Hintsanen

## License

MIT License. See [`LICENSE`](LICENSE).
