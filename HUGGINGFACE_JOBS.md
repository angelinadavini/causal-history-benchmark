# Hugging Face compute provenance

This file records development jobs that materially changed the benchmark design or support results currently described in the repository.

The full research ledger contains additional failed engineering runs.

## Key jobs

| Job ID | Model | Purpose | Result |
|---|---|---|---|
| `6a9036e9984507d9db4e817c` | Qwen2.5-3B-Instruct | bridge-only cache smoke | infrastructure timeout; no scientific result |
| `6a903a4045686a1580c0e4d3` | Qwen2.5-3B-Instruct | rebuild cache with bridge K/V only | passed; physical source removal is technically possible |
| `6a903ac4984507d9db4e8213` | Qwen2.5-3B-Instruct | two-pass explicit mapping after source removal | behavior gate failed |
| `6a903b89984507d9db4e8234` | Qwen2.5-3B-Instruct | in-place source masking | behavior gate failed |
| `6a903c6845686a1580c0e547` | Qwen2.5-3B-Instruct | passcode decoding from fixed bridge K/V | strong decodability; best mean digit accuracy 57.7% vs 10% chance |
| `6a906660984507d9db4e8881` | Qwen2.5-3B-Instruct | strict cross-content held-out route intervention | layer-8 donor steering 100% in both cross-content directions; 20 matched random controls far weaker |
| `6a90673d984507d9db4e8897` | Qwen2.5-3B-Instruct | early-layer interchange localization | cumulative layers 0-5 moved later layer-8 state 0.646 toward donor; same-route control 0.0009 |
| `6a90672845686a1580c0edd4` | Mistral-7B-Instruct-v0.3, 4-bit NF4 | cross-model interchange | mean donor projection 0.809; same-route control 0.031; 64/64 positive |
| `6a9068c4984507d9db4e88ca` | Qwen2.5-3B-Instruct | second task, DAX/WUG mapping | mean donor projection 0.569; same-route control 0.0013; 64/64 positive |
| `6a90672845686a1580c0edd2` | Phi-3.5-mini-instruct | attempted cross-model replication | Transformers/DynamicCache compatibility error; no scientific result |
| `6a90712345686a1580c0f0d3` | Mistral-7B-Instruct-v0.3 fp16 | full-precision replication | canceled before result |
| `6a907a77984507d9db4e8bc2` | Qwen2.5-3B-Instruct | logit-level mediation follow-up | launched after the current documented internal-state result; inspect job record before treating as evidence |

## Why failed jobs are listed

A failed compute job and a failed scientific test are different things.

Infrastructure errors are recorded so they cannot later be mistaken for null findings. Tasks that fail their own positive-control gate are also preserved and excluded from hypothesis interpretation.

## Reproducibility plan

The final release will replace this development table with:

- frozen experiment scripts;
- exact model revisions;
- package versions;
- hardware configuration;
- random seeds;
- prompt templates;
- intervention layers;
- raw per-trial outputs;
- analysis code;
- hashes for released result files.
