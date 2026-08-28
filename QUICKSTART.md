# Quickstart

This is the shortest way to run the public reference test.

## 1. Install it

A CUDA-capable GPU is recommended.

```bash
git clone https://github.com/angelinadavini/causal-history-benchmark.git
cd causal-history-benchmark
python -m venv .venv
source .venv/bin/activate
pip install -e ".[benchmark,test]"
```

Check that the package is installed:

```bash
chb-validate
```

## 2. Run the small Qwen test

```bash
python scripts/run_benchmark.py \
  --model Qwen/Qwen2.5-3B-Instruct \
  --reps 16
```

What the script does:

1. The model learns the same rule from examples or from a direct instruction.
2. The original teaching state is replaced with neutral state.
3. The rule is given again during the later task.
4. The bridge state is moved between the two learning conditions.
5. A same-history swap is run as the control.
6. The script measures how far the later hidden state moves toward the other learning history.

The output is JSON so it can be saved, compared, or added to a larger benchmark run.

The main fields are:

- `cross_projection_mean` — how far the later state moved after a bridge state from the other learning history was inserted;
- `same_route_control_mean` — how far it moved after a bridge state from the same learning history was inserted;
- `cross_positive_fraction` — how often the cross-history swap moved in the predicted direction.

The cross-history result should be judged against the same-history control.

## 3. See the frozen v11 numbers

```bash
chb-v11
```

This prints the three confirmed v11 arms, their endpoint values, job IDs, and bridge-cut results.

The small public run is for trying the method. The frozen v11 study used fixed seeds, model versions, wording, layer choices, tokenizer checks, and analysis rules recorded under [`confirmatory/`](confirmatory/).

## 4. Try another model

Start with:

```bash
python scripts/run_benchmark.py --model YOUR_MODEL_ID
```

Before you trust the result, check these things:

- the model can run the later task;
- the tokenizer keeps the prompt and answer boundaries you expect;
- the source-removal step actually removes the original teaching state;
- the state you plan to move exists where you think it does;
- the later layer or state you want to measure exists;
- the same-history swap stays small enough to act as a useful control.

If the model does not use transformer K/V state, change the intervention to the kind of state that model actually carries forward. Keep the experimental question the same.

## 5. Add your result

If you run CHB on another model, save enough information for somebody else to reproduce it.

At minimum include:

```json
{
  "model": "author/model",
  "model_revision": "commit-or-tag",
  "task": "SAME_DIFFERENT",
  "n_pairs": 256,
  "retained_state": "bridge KV",
  "intervention": "cross-history bridge swap",
  "cross_route_movement": 0.42,
  "same_route_control": 0.01,
  "path_removal_ratio": 0.00,
  "software": {
    "transformers": "5.13.0"
  }
}
```

Add the exact script or patch you used for that model.

Open a pull request with the result file and a new row for [`LEADERBOARD.md`](LEADERBOARD.md).

## The experiment in one picture

```text
same rule
   |
   +-- learned from examples
   |
   +-- stated directly
             |
             v
       same bridge text
             |
   original source removed
             |
       same rule given again
             |
             v
      move bridge state
             |
             v
   measure what changes later
```

That is CHB. The rest of the repository exists to make this comparison controlled, repeatable, and easy to extend.
