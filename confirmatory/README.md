# The frozen v11 experiment

This folder records exactly which confirmatory runs count as the v11 result and why.

## The three valid jobs

- Qwen primary: `6a90939f45686a1580c0f60e`
- Mistral replication: `6a9093b3984507d9db4e8d7d`
- amended Qwen DAX/WUG: `6a90c7e345686a1580c0fe2a`

## Frozen hashes

Base v2 manifest:

```text
fb42c0f7e984c8e775b55960eb5c7f9be02d6eff8944bcdb198223435764a7d2
```

DAX/WUG v2.1 manifest:

```text
570f3119f16b32942c0bae5fdbdeb8396311a76c3bb8fed1b6eea577fc69cb54
```

These hashes identify the seeds and frozen protocol used for the confirmed study.

## Software used for the frozen runs

```text
transformers==5.13.0
sentencepiece==0.2.1
accelerate==1.10.1
```

## Why there is a v2.1

The first confirmatory launch had a tokenizer problem. Mistral did not handle the answer labels the way the code assumed.

That problem was found before scientific output was inspected. The related Qwen jobs were cancelled unread.

The repaired v2 launch completed the Qwen primary and Mistral runs. The DAX/WUG run then stopped on its first episode because adding `X` changed the query-token boundary.

A tokenizer-only check tested `0`, `1`, `X`, and `Y` across both tokenizers and every task condition. The DAX/WUG prompt was repaired with one newline after `Answer:`. New DAX/WUG seeds and the amendment were frozen before the completed Qwen and Mistral scientific outputs were opened.

That repaired secondary run is v2.1.

## Results

See:

- [`../RESULTS.md`](../RESULTS.md) for the human-readable result;
- [`../results/confirmatory_summary.csv`](../results/confirmatory_summary.csv) for the machine-readable endpoint table.

## Quick run versus exact reproduction

`scripts/reference_interchange.py` is the small public test. It is useful for trying the method on a compatible model.

The exact v11 runners, analysis code, manifests, protocols, and final logs are in [`v11/`](v11/). The packages there are unchanged copies of the files used for the frozen study.

To verify the package locks without downloading model weights:

```bash
python scripts/reproduce_v11.py
```

To run the frozen experiment on a GPU, after checking model access and installing the pinned requirements:

```bash
python scripts/reproduce_v11.py --run --output v11-reproduction-output
```

The helper checks every recorded file hash before it starts. It writes new logs to the chosen output directory and never overwrites the published results.
