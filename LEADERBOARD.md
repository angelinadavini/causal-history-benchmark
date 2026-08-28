# Causal History Benchmark leaderboard

This page keeps results from models that have been tested with the same basic question:

> After the old teaching information is gone and the same rule is available now, does how the model learned it earlier still change what happens next?

A result belongs here only if the run shows how the original source was removed, what state was left, what state was moved, what same-history control was used, and what happened when the proposed path was cut.

## Confirmed reference results

| Model | Task | Pairs | State moved | Later measure | Net movement | After bridge cut | Status |
| --- | --- | ---: | --- | --- | ---: | ---: | --- |
| Qwen2.5-3B-Instruct | SAME/DIFFERENT | 512 | bridge K/V, layers 0–5 | hidden layer 8 | **0.68747** | distance -> 0 | frozen v11 |
| Qwen2.5-3B-Instruct | SAME/DIFFERENT | 512 | bridge K/V, layers 0–5 | full next-token logits | **0.25833** | distance -> 0 | frozen v11 |
| Mistral-7B-Instruct-v0.3 | SAME/DIFFERENT | 256 | bridge K/V, layers 0–4 | hidden layer 7 | **0.80099** | distance -> 0 | frozen v11 |
| Mistral-7B-Instruct-v0.3 | SAME/DIFFERENT | 256 | bridge K/V, layers 0–4 | full next-token logits | **0.05865** | distance -> 0 | frozen v11 |
| Qwen2.5-3B-Instruct | DAX/WUG | 256 | bridge K/V, layers 0–5 | hidden layer 8 | **0.60515** | distance -> 0 | frozen v11 |
| Qwen2.5-3B-Instruct | DAX/WUG | 256 | bridge K/V, layers 0–5 | full next-token logits | **0.04717** | distance -> 0 | frozen v11 |

## Results from other researchers

No outside replication has been accepted yet.

| Model / system | Task | State moved | Cross-history result | Same-history control | Path-cut result | Code / result | Status |
| --- | --- | --- | ---: | ---: | ---: | --- | --- |
| — | — | — | — | — | — | — | open |

## New model-family extensions

These rows are kept separate from the frozen v11 reference results. They use
the same causal-history question with a newly frozen model-specific run.

| Model | Task | Pairs | State moved | Later measure | Net movement | 95% CI | After bridge cut | Status |
| --- | --- | ---: | --- | --- | ---: | --- | ---: | --- |
| OLMo-2-1124-7B-Instruct | SAME/DIFFERENT | 256 | bridge K/V, layers 0--5 | hidden layer 8 | **0.58722** | [0.58430, 0.59009] | distance -> 0 | extension: positive hidden endpoint |
| OLMo-2-1124-7B-Instruct | SAME/DIFFERENT | 256 | bridge K/V, layers 0--5 | full next-token logits | **0.03286** | [-0.03762, 0.10720] | distance -> 0 | extension: interval includes zero |

## Multi-event correction extension

These runs add an explicit correction event before the final test. They are
kept separate from the v11 reference rows and from the one-event OLMo result.

| Model | Task | Episodes | State moved | Later measure | Net movement | 95% CI | Full cut | Status |
| --- | --- | ---: | --- | --- | ---: | --- | ---: | --- |
| Qwen2.5-3B-Instruct | SAME/DIFFERENT with correction | 256 | second bridge K/V, layers 0--5 | final hidden layer 8 | **0.00482** | [0.00016, 0.00943] | distance -> 0 | extension: positive hidden endpoint |
| Qwen2.5-3B-Instruct | SAME/DIFFERENT with correction | 256 | second bridge K/V, layers 0--5 | final full next-token logits | **-0.00852** | [-0.01125, -0.00581] | distance -> 0 | extension: no positive logit endpoint |
| OLMo-2-1124-7B-Instruct | SAME/DIFFERENT with correction | 256 | second bridge K/V, layers 0--5 | final hidden layer 8 | **0.02658** | [0.02499, 0.02816] | distance -> 0 | extension: positive hidden endpoint |
| OLMo-2-1124-7B-Instruct | SAME/DIFFERENT with correction | 256 | second bridge K/V, layers 0--5 | final full next-token logits | **-0.03626** | [-0.04480, -0.02763] | distance -> 0 | extension: no positive logit endpoint |

## Add your model

Open a pull request with:

- the exact model and revision;
- tokenizer version if relevant;
- the task;
- the two learning routes;
- how the original source was removed;
- what state was kept;
- what state was moved;
- where the later result was measured;
- cross-history result;
- same-history control;
- path-cut result;
- seeds and software versions;
- code and a machine-readable result file.

If the model passes all setup checks and shows no history effect, submit that too. A clean negative result belongs in the public record.

If the setup fails before the scientific question is tested, document the failure separately so nobody mistakes it for a negative scientific result.

## Models I especially want to see here

The strongest next additions would come from systems that are different from the two transformer families already confirmed:

- state-space models;
- recurrent language models;
- memory-augmented models;
- multimodal agents with persistent internal state;
- models with learned context compression or recurrent memory.

Those systems do not need to use K/V. Test the state that actually carries their history and keep the same causal question.
