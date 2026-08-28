# Models tested so far

| Model | What happened | Task(s) |
| --- | --- | --- |
| Qwen2.5-3B-Instruct | Confirmed. Moving the bridge state moved both a later hidden state and the full next-token output. Cutting bridge access removed the measured history difference. | SAME/DIFFERENT; DAX/WUG |
| Mistral-7B-Instruct-v0.3 | Confirmed. The same pattern appeared in a second model family. Cutting bridge access removed the measured history difference. | SAME/DIFFERENT |
| Qwen2.5-0.5B-Instruct | The model did not pass the task-performance check used during development, so no history conclusion was drawn from it. | early task versions |
| Phi-3.5-mini-instruct | The exploratory code hit a cache API incompatibility before the scientific test ran. | — |

Exact confirmed numbers are in [`RESULTS.md`](RESULTS.md).

## Models I want to see tested next

The most useful next tests are models that tell us whether the result travels beyond the systems already used:

- Gemma models;
- Llama-family models;
- other Qwen and Mistral sizes;
- state-space language models;
- recurrent language models;
- models with explicit memory;
- models that learn to compress earlier context;
- multimodal agents that keep internal state across events.

## What a new model has to show

Before a result goes on the leaderboard, the run should show that:

1. the model can do the task;
2. the tokenizer behaves as expected;
3. the original teaching state was removed or neutralised;
4. the same current rule was supplied in both learning conditions;
5. the retained history state was changed directly;
6. the cross-history change was compared with a same-history control;
7. the path carrying the effect was cut or tested in the closest equivalent way for that model;
8. seeds, model versions, software, and code were saved.

A clean negative result is useful. A broken setup is a setup problem, not evidence that the effect is absent.
