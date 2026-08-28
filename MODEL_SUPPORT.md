# Model support

| Model | Status | Confirmed task(s) | Confirmed result |
| --- | --- | --- | --- |
| Qwen2.5-3B-Instruct | frozen primary + second-task replication | SAME/DIFFERENT; DAX/WUG | positive hidden-state and complete-logit route movement; bridge-path removal reduced route distance to zero |
| Mistral-7B-Instruct-v0.3 | frozen cross-model replication | SAME/DIFFERENT | positive hidden-state and complete-logit route movement; bridge-path removal reduced route distance to zero |
| Qwen2.5-0.5B-Instruct | development only | early task versions | below task-capacity gate; no scientific history inference |
| Phi-3.5-mini-instruct | engineering blocked in exploratory code | — | cache API incompatibility; no scientific result |

See [RESULTS.md](RESULTS.md) for exact confirmatory numbers.

## Models wanted

External replications are especially useful for:

- Gemma-family models;
- Llama-family models;
- state-space language models;
- recurrent language models;
- explicit-memory models;
- models with learned context compression;
- multimodal agents with persistent internal state.

## Adding a model

A model should enter the replication leaderboard only after:

1. the model passes task and tokenizer positive controls;
2. the original source is removed or neutralised;
3. current task content is supplied equally across histories;
4. the retained state is identified;
5. cross-route state intervention is run;
6. a matched same-route intervention is run;
7. a path-removal or architecture-appropriate carrier check is run;
8. seeds, revisions, code, and software versions are preserved.

A null result is useful when the apparatus passes its controls.
