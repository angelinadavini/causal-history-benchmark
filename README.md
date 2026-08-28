# Causal History Benchmark

**Does the way a model learned the same information leave a causal trace that changes what the model does later?**

The Causal History Benchmark is a mechanistic benchmark for testing acquisition history in language models.

Two runs end with the same usable task relation. One model history learned that relation from examples. The other received it directly. The original source-history state is then replaced with neutral state. The current relation is supplied again during a later event. A short fixed bridge is the only route-dependent state left from the earlier event.

The benchmark asks whether changing that retained bridge state changes the later computation.

## Confirmed result

The frozen confirmatory study passed in three arms:

| Arm | Model | Task | Episodes | Later hidden-state movement | Complete-logit movement |
| --- | --- | --- | ---: | ---: | ---: |
| Primary | Qwen2.5-3B-Instruct | SAME/DIFFERENT | 512 | **0.68747** [0.68661, 0.68832] | **0.25833** [0.25555, 0.26109] |
| Cross-model | Mistral-7B-Instruct-v0.3 | SAME/DIFFERENT | 256 | **0.80099** [0.79955, 0.80245] | **0.05865** [0.05681, 0.06056] |
| Second task | Qwen2.5-3B-Instruct | DAX/WUG | 256 | **0.60515** [0.60352, 0.60679] | **0.04717** [0.04335, 0.05106] |

Values are net recipient-to-donor route-axis movement after subtracting the matched same-route donor control. Every hidden-state endpoint was positive in every episode. The full-logit endpoint was positive in every Qwen primary and Mistral episode and in 89.45% of DAX/WUG episodes.

Removing later-event attention to the bridge reduced the measured route distance to **zero in every confirmatory arm**.

The confirmed machine claim is simple:

> Acquisition route can remain as a causal machine state after the original source state is neutralised and the current relation is supplied again. Interchanging that retained state changes a later hidden representation and the complete next-token output distribution.

The result does not establish consciousness.

## Run the benchmark

Clone the repository and install the pinned dependencies:

```bash
git clone https://github.com/angelinadavini/causal-history-benchmark.git
cd causal-history-benchmark
pip install -r requirements.txt
```

Run the compact reference experiment on Qwen:

```bash
python scripts/reference_interchange.py --model Qwen/Qwen2.5-3B-Instruct --reps 16
```

The reference script tests the core intervention with source-prefix neutralisation, bridge K/V interchange, a later event with current task information supplied again, and a same-route donor control.

See [QUICKSTART.md](QUICKSTART.md) for the result fields and how to test another compatible decoder model.

## Add your model

The benchmark is meant to be run on other models and architectures. If you test a model, open a pull request with:

- model name and exact revision;
- tokenizer revision;
- task and acquisition routes;
- bridge definition;
- intervention layers and outcome layer;
- cross-route and same-route movement;
- source-neutralisation check;
- hardware and software versions.

Results that satisfy the benchmark controls can be added to [LEADERBOARD.md](LEADERBOARD.md).

## What is being measured

The benchmark keeps several questions separate:

- Does earlier information remain in state?
- Is that state used by later computation?
- Does acquisition route remain after current task content is supplied again?
- Does changing the route-specific state change a later event?
- Does the effect disappear when the later event loses access to the retained carrier?
- Does the result replicate across tasks, models, wording, delays, and architectures?

A probe that decodes route information is not enough. The central benchmark result requires a causal intervention.

## Benchmark structure

```text
same relation
    |
    +-- learned from examples
    |
    +-- supplied directly
            |
            v
fixed bridge state
            |
source-history prefix replaced by neutral K/V
            |
            v
current relation supplied again in a later event
            |
            v
measure later hidden state + complete logits
            |
            v
interchange retained bridge state across routes
            |
            v
does the later computation move toward donor history?
```

## Repository map

- [BENCHMARK.md](BENCHMARK.md) — benchmark contract and required controls
- [RESULTS.md](RESULTS.md) — frozen confirmatory results and preserved failures
- [QUICKSTART.md](QUICKSTART.md) — run the reference implementation
- [LEADERBOARD.md](LEADERBOARD.md) — community replication table
- [CONTRIBUTING.md](CONTRIBUTING.md) — how to submit a model result
- [CLAIM_LIMITS.md](CLAIM_LIMITS.md) — exact supported and unsupported claims
- [scripts/reference_interchange.py](scripts/reference_interchange.py) — compact runnable experiment
- [results/confirmatory_summary.csv](results/confirmatory_summary.csv) — machine-readable v11 endpoint summary

## Why this exists independently of a paper

A paper is one report of the benchmark. The benchmark itself is meant to be reused.

A model developer can run it on a new model. A mechanistic-interpretability researcher can replace the K/V intervention with another causal method. A memory-system researcher can test longer delays. A state-space or recurrent-model researcher can ask whether the same history effect appears outside transformer K/V state.

That makes the useful object the test and its controls, not a single publication.

## Claim boundary

The current confirmatory evidence covers two decoder-only transformer families and two synthetic relation tasks. It does not establish phenomenal consciousness, sentience, subjective continuity, a unique consciousness criterion, valid verbal source attribution, a robust overt-choice effect, or generality across architectures.

## Citation

GitHub exposes the repository citation through [CITATION.cff](CITATION.cff). Please cite the benchmark if you use its task, intervention, controls, or results.

## Author

Angelina Davini Hintsanen

## License

MIT License. See [LICENSE](LICENSE).
