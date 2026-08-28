# Causal History Benchmark

**Does learning the same information in a different way leave a state that changes what a model does later?**

The Causal History Benchmark (CHB) tests that question directly.

A model gets the same rule in two ways: from examples or from a direct instruction. The original examples or instruction are removed from the stored source state. The rule is supplied again during a later event, so the model has the same current task information in both conditions. A short fixed bridge is the only state left that depends on how the rule was learned earlier.

CHB moves that bridge state between the two learning conditions and measures what changes later. It also blocks later access to the bridge. A valid result therefore has to show more than a readable history signature: changing the retained state must change later processing, and the path check must behave as predicted.

## Confirmed v11 result

All three frozen confirmatory arms passed.

| Arm | Model | Task | Episodes | Hidden-state movement | Full-logit movement |
| --- | --- | --- | ---: | ---: | ---: |
| Primary | Qwen2.5-3B-Instruct | SAME/DIFFERENT | 512 | **0.68747** [0.68661, 0.68832] | **0.25833** [0.25555, 0.26109] |
| Cross-model | Mistral-7B-Instruct-v0.3 | SAME/DIFFERENT | 256 | **0.80099** [0.79955, 0.80245] | **0.05865** [0.05681, 0.06056] |
| Second task | Qwen2.5-3B-Instruct | DAX/WUG | 256 | **0.60515** [0.60352, 0.60679] | **0.04717** [0.04335, 0.05106] |

The reported value is movement toward the opposite learning history after subtracting the matched same-history control. Removing later access to the bridge reduced the measured route distance to **zero in hidden-state and full-logit space in all three arms**.

The machine result is:

> How the same information was learned earlier remained in a retained bridge state after the original source state was neutralised. Moving that state changed a later hidden state and the complete next-token output distribution after the current rule was supplied again. The result replicated in another model family and another task. Blocking later access to the bridge removed the measured history difference.

CHB measures this causal-history effect. It is not a consciousness score.

## Install

For the benchmark utilities and tests:

```bash
git clone https://github.com/angelinadavini/causal-history-benchmark.git
cd causal-history-benchmark
pip install -e ".[test]"
pytest -q
```

For model runs:

```bash
pip install -e ".[benchmark,test]"
chb-validate
```

The general benchmark package keeps the public API separate from the exact frozen confirmatory environment. The pinned v11 software record is preserved under `confirmatory/`.

## Run a small reference test

The compact public runner implements source neutralisation, bridge K/V interchange, current-rule resupply, and the matched same-history control.

```bash
python scripts/run_benchmark.py \
  --model Qwen/Qwen2.5-3B-Instruct \
  --reps 16
```

This is the small reusable reference test. The frozen v11 result used prespecified model revisions, seeds, episode counts, task wording, intervention layers, analysis rules, and tokenizer checks recorded in the confirmatory archive.

## What a benchmark-valid result needs

A submitted result should report all of these:

1. **Same information, different learning route.** The target relation must be matched across the two acquisition conditions.
2. **Original source neutralised.** The later effect cannot depend on directly rereading the original examples or instruction.
3. **Current information supplied again.** Both conditions receive the same usable task information during the later event.
4. **Matched same-route control.** Cross-route movement is compared with a donor from the same route.
5. **Causal state intervention.** Decoding route information is not enough. The retained state must be changed directly.
6. **Later hidden-state and output measurement.** CHB reports movement in a fixed later hidden state and the complete next-token logit vector.
7. **Path check.** Later access to the proposed carrier is removed to test whether the measured history difference depends on that path.

The machine-readable result contract is in [`results/result_schema.json`](results/result_schema.json).

## Frozen v11 values from Python

```bash
chb-v11
```

The package exposes the exact v11 endpoint values, job IDs, and path-check values used in the public result record.

## Add another model

CHB is intended to grow beyond Qwen and Mistral. A new model result should include:

- exact model and revision;
- tokenizer and software versions;
- task and acquisition routes;
- source-neutralisation method;
- bridge or other retained carrier definition;
- intervention layers or state location;
- outcome location;
- cross-route movement;
- same-route control movement;
- path-check result;
- hardware;
- complete machine-readable result file.

The current result schema is architecture-aware without treating transformer K/V as the only possible carrier. A recurrent model, state-space model, or another architecture can use a different state intervention if it answers the same causal question and reports the required controls.

## Repository map

- [`BENCHMARK.md`](BENCHMARK.md) — benchmark contract and required controls
- [`RESULTS.md`](RESULTS.md) — frozen v11 results and preserved failures
- [`QUICKSTART.md`](QUICKSTART.md) — compact runner instructions
- [`LEADERBOARD.md`](LEADERBOARD.md) — confirmed and community model results
- [`MODEL_SUPPORT.md`](MODEL_SUPPORT.md) — current model support
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — how to submit a replication
- [`confirmatory/`](confirmatory/) — frozen protocol provenance
- [`configs/`](configs/) — machine-readable confirmatory arm definitions
- [`src/causal_history/`](src/causal_history/) — reusable metric, task, schema, and v11 utilities
- [`scripts/reference_interchange.py`](scripts/reference_interchange.py) — compact model experiment
- [`tests/`](tests/) — benchmark utility tests
- [`results/confirmatory_summary.csv`](results/confirmatory_summary.csv) — frozen endpoint table
- [`results/result_schema.json`](results/result_schema.json) — result submission schema

## Why this exists independently of a paper

A paper reports one use of the method. The benchmark is meant to be run again.

Researchers can test another model, replace K/V interchange with another causal intervention, add longer delays, use different acquisition histories, or ask whether the same effect appears outside decoder-only transformers. Future results can be compared against the same experimental question and control structure.

## Citation

GitHub exposes the repository citation through [`CITATION.cff`](CITATION.cff).

## Author

Angelina Davini Hintsanen

## License

MIT License. See [`LICENSE`](LICENSE).
