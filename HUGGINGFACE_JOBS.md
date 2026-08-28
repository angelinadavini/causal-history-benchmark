# Hugging Face job record

The experiments were run through Hugging Face Jobs. This page keeps the successful scientific runs separate from jobs that failed for engineering reasons.

## The three confirmed jobs

| Test | Job ID | Model | Task | Result |
| --- | --- | --- | --- | --- |
| Primary | `6a90939f45686a1580c0f60e` | Qwen2.5-3B-Instruct | SAME/DIFFERENT | valid confirmed run |
| Second model | `6a9093b3984507d9db4e8d7d` | Mistral-7B-Instruct-v0.3 | SAME/DIFFERENT | valid confirmed run |
| Second task | `6a90c7e345686a1580c0fe2a` | Qwen2.5-3B-Instruct | DAX/WUG | valid amended confirmed run |

Frozen manifest hashes:

- base v2: `fb42c0f7e984c8e775b55960eb5c7f9be02d6eff8944bcdb198223435764a7d2`
- secondary v2.1: `570f3119f16b32942c0bae5fdbdeb8396311a76c3bb8fed1b6eea577fc69cb54`

The DAX/WUG amendment and its new seeds were frozen before the completed Qwen and Mistral scientific results were opened.

## Development jobs that changed the experiment

| Job ID | Model | What it tested | What happened |
| --- | --- | --- | --- |
| `6a9036e9984507d9db4e817c` | Qwen2.5-3B-Instruct | bridge-only cache smoke test | timed out while loading; no scientific result |
| `6a903a4045686a1580c0e4d3` | Qwen2.5-3B-Instruct | whether a cache could be rebuilt with only bridge K/V | worked; physical source removal was technically possible |
| `6a903c6845686a1580c0e547` | Qwen2.5-3B-Instruct | whether removed source information could still be read from bridge K/V | yes; the bridge retained readable information |
| `6a906660984507d9db4e8881` | Qwen2.5-3B-Instruct | transfer across rule content | positive development result |
| `6a90673d984507d9db4e8897` | Qwen2.5-3B-Instruct | where the strongest early bridge effect appeared | strong cumulative early-layer effect |
| `6a90672845686a1580c0edd4` | Mistral-7B-Instruct-v0.3 | second-model bridge swap | positive development result |
| `6a9068c4984507d9db4e88ca` | Qwen2.5-3B-Instruct | DAX/WUG second task | positive development result |
| `6a90672845686a1580c0edd2` | Phi-3.5-mini-instruct | attempted second-model run | cache API failed before the scientific test |
| `6a90712345686a1580c0f0d3` | Mistral-7B-Instruct-v0.3 | full-precision exploratory run | cancelled before a result |

## Why the first confirmatory launch was thrown out

The first confirmatory launch assumed that answer labels would tokenize the same way across models. Mistral broke that assumption.

The problem was caught before scientific output was inspected. The related Qwen jobs were cancelled unread.

The next launch fixed answer-token handling. Qwen and Mistral completed. The DAX/WUG arm then stopped on its first episode because adding `X` changed the query-token boundary.

A tokenizer-only check was run across both tokenizers and all task cells. One newline was added after `Answer:` for DAX/WUG. New secondary seeds and the amendment were frozen before the completed scientific logs were opened.

These details stay public so nobody has to guess which jobs count and which do not.

## Why some jobs were stopped early

GPU time costs money. A larger or longer run was not used to rescue a setup that had already failed its own checks.

When the task, tokenizer, cache, or intervention was broken, the job was stopped and fixed before more compute was spent.
