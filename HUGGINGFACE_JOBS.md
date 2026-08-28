# Hugging Face compute provenance

The benchmark was developed and confirmed through remote Hugging Face Jobs. This file keeps the main scientific job IDs separate from engineering failures.

## Frozen confirmatory jobs

| Arm | Job ID | Model | Task | Status |
| --- | --- | --- | --- | --- |
| Primary | `6a90939f45686a1580c0f60e` | Qwen2.5-3B-Instruct | SAME/DIFFERENT | valid confirmatory |
| Cross-model replication | `6a9093b3984507d9db4e8d7d` | Mistral-7B-Instruct-v0.3 | SAME/DIFFERENT | valid confirmatory |
| Second-task replication | `6a90c7e345686a1580c0fe2a` | Qwen2.5-3B-Instruct | DAX/WUG | valid amended confirmatory |

Frozen manifest hashes:

- base v2: `fb42c0f7e984c8e775b55960eb5c7f9be02d6eff8944bcdb198223435764a7d2`
- secondary v2.1: `570f3119f16b32942c0bae5fdbdeb8396311a76c3bb8fed1b6eea577fc69cb54`

The second-task amendment was frozen before completed confirmatory scientific outputs were opened.

## Important development jobs

| Job ID | Model | Purpose | Result |
| --- | --- | --- | --- |
| `6a9036e9984507d9db4e817c` | Qwen2.5-3B-Instruct | bridge-only cache smoke | infrastructure timeout; no scientific result |
| `6a903a4045686a1580c0e4d3` | Qwen2.5-3B-Instruct | rebuild cache with bridge K/V only | passed; physical source removal technically possible |
| `6a903c6845686a1580c0e547` | Qwen2.5-3B-Instruct | passcode decoding from fixed bridge K/V | source information strongly decodable from retained state |
| `6a906660984507d9db4e8881` | Qwen2.5-3B-Instruct | strict cross-content development intervention | supported history-state transfer across content modes |
| `6a90673d984507d9db4e8897` | Qwen2.5-3B-Instruct | early-layer localization | identified strong cumulative early bridge effect |
| `6a90672845686a1580c0edd4` | Mistral-7B-Instruct-v0.3 | development cross-model interchange | positive development replication |
| `6a9068c4984507d9db4e88ca` | Qwen2.5-3B-Instruct | development DAX/WUG task | positive second-task development result |
| `6a90672845686a1580c0edd2` | Phi-3.5-mini-instruct | attempted replication | cache API incompatibility; no scientific result |
| `6a90712345686a1580c0f0d3` | Mistral-7B-Instruct-v0.3 | queued full-precision exploratory run | cancelled before result |

## Invalidated confirmatory attempts

Confirmatory v1 was invalidated before scientific output was inspected because the Mistral tokenizer failed a bare-label assumption. The related Qwen v1 jobs were cancelled unread.

Confirmatory v2 then completed Qwen and Mistral. The DAX/WUG arm stopped on its first episode because appending `X` changed the query-token boundary. A tokenizer-only preflight tested the candidate strings across both pinned tokenizers and all task cells. A one-newline amendment and fresh secondary seeds were frozen before sealed outputs were opened.

These engineering events are preserved so they cannot be mistaken for scientific nulls or silently removed from the history of the benchmark.

## Cost discipline

Development jobs were stopped when an apparatus gate failed. Larger models were not run merely to rescue a weak setup. The public benchmark keeps those failures because they are useful to anyone porting the experiment to another model.
