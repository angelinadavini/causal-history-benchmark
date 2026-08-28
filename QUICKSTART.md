# Quickstart

## 1. Install

A CUDA-capable GPU is recommended.

```bash
git clone https://github.com/angelinadavini/causal-history-benchmark.git
cd causal-history-benchmark
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Run the compact Qwen reference experiment

```bash
python scripts/reference_interchange.py \
  --model Qwen/Qwen2.5-3B-Instruct \
  --reps 16 \
  --patched-layers 6 \
  --outcome-layer 8
```

The script prints JSON containing:

- `n_pairs` — paired episodes tested;
- `bridge_tokens` — number of fixed bridge tokens;
- `patched_layers` — bridge K/V layers interchanged;
- `outcome_layer` — later hidden layer measured;
- `cross_projection_mean` — movement caused by the opposite-route donor;
- `same_route_control_mean` — movement caused by a matched donor from the same route;
- `cross_positive_fraction` — fraction of pairs moving in the predicted direction.

The useful comparison is the cross-route intervention against the same-route control.

## 3. Understand the manipulation

The reference task has two routes to the same SAME/DIFFERENT relation.

```text
examples history ---------> fixed bridge
                                |
direct instruction -------> fixed bridge
                                |
source prefix replaced by neutral state
                                |
current relation supplied again
                                |
new event
```

The benchmark then swaps early bridge K/V between the two histories and measures the later event.

The source prefix has already been neutralised, and the later query already states the current relation. The intervention therefore asks whether acquisition route remains causally active beyond the current task content.

## 4. Run another compatible decoder model

Start with the same script:

```bash
python scripts/reference_interchange.py --model YOUR_MODEL_ID
```

Before interpreting a result, check:

- the model supports `DynamicCache` or adapt the cache code explicitly;
- the model solves the later task under both routes;
- bridge token boundaries are correct for its tokenizer;
- the chosen later layer exists;
- the source-neutralisation step works as intended;
- same-route replacement remains a small control;
- answer strings are tokenised correctly in context.

Model-specific layer choices should be fixed before a confirmatory run.

## 5. Submit a replication

Open a pull request that adds one row to [LEADERBOARD.md](LEADERBOARD.md) and includes a reproducible result file.

Use a compact JSON record such as:

```json
{
  "model": "author/model",
  "model_revision": "commit-or-tag",
  "task": "SAME_DIFFERENT",
  "n_pairs": 256,
  "retained_state": "bridge KV",
  "intervention": "opposite-route interchange",
  "cross_route_movement": 0.42,
  "same_route_control": 0.01,
  "path_removal_ratio": 0.00,
  "software": {
    "transformers": "5.13.0"
  }
}
```

Include the exact runner or patch used for that architecture.

## 6. Non-K/V architectures

The benchmark question is broader than transformer cache state.

For a recurrent network, state-space model, memory-augmented model, or agent, identify the native state that carries earlier history. Remove the original source, supply the current relation again, intervene on the retained state, and test the later event.

The state object may change. The causal contract in [BENCHMARK.md](BENCHMARK.md) should remain explicit.
