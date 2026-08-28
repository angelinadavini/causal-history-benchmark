---
license: mit
pretty_name: Causal History Benchmark
tags:
- benchmark
- language-models
- causal-intervention
- mechanistic-interpretability
- ai-consciousness
- reproducibility
task_categories:
- text-generation
---

# Causal History Benchmark

**If a model has the same rule in front of it now, can the way it learned that rule earlier still change what it does next?**

CHB tests that question.

The model learns the same rule from examples or from a direct instruction. The original teaching state is removed. The same rule is supplied again during a later task. We then move the stored bridge state between the two learning histories and measure what changes later.

The test also cuts access to the bridge. If the later difference depends on that stored history state, the difference should disappear when the bridge can no longer be used.

## Confirmed v11 results

| Model | Task | Episodes | Hidden-state movement | Full-logit movement | After bridge cut |
| --- | --- | ---: | ---: | ---: | --- |
| Qwen2.5-3B-Instruct | SAME/DIFFERENT | 512 | 0.68747 | 0.25833 | distance -> 0 |
| Mistral-7B-Instruct-v0.3 | SAME/DIFFERENT | 256 | 0.80099 | 0.05865 | distance -> 0 |
| Qwen2.5-3B-Instruct | DAX/WUG | 256 | 0.60515 | 0.04717 | distance -> 0 |

The full confidence intervals and frozen job record are in the public GitHub repository.

## Separate OLMo-2 extension

The later OLMo-2 extension is recorded separately from the frozen v11 table.
Its hidden-state movement was 0.58722 (95% CI [0.58430, 0.59009]) after the
same-history control. Its full-logit movement was 0.03286 (95% CI [-0.03762,
0.10720]), so that endpoint is inconclusive. Both bridge-cut distances were
zero. The raw log and all 256 records are linked from the GitHub repository.

## Multi-event correction extension

An extra run inserted an explicit correction event before the final test. The
final hidden-state net movement was 0.00482 (95% CI [0.00016, 0.00943]) for
Qwen and 0.02658 (95% CI [0.02499, 0.02816]) for OLMo. The final full-logit net
was -0.00852 (95% CI [-0.01125, -0.00581]) for Qwen and -0.03626 (95% CI
[-0.04480, -0.02763]) for OLMo. The full retained-state cut was zero in both
runs. These extension results are kept separate from the frozen v11 table.

## The result

> The way the model learned the same information earlier changed what happened later. The original teaching state was gone. The same current rule was supplied again. Moving the state left by the earlier learning moved the later computation. Blocking access to that state removed the difference.

CHB measures this causal-history effect. It does not assign a consciousness score.

## Use the benchmark

Code, frozen results, controls, and contribution instructions:

https://github.com/angelinadavini/causal-history-benchmark

Small public reference run:

```bash
git clone https://github.com/angelinadavini/causal-history-benchmark.git
cd causal-history-benchmark
pip install -e ".[benchmark,test]"
python scripts/run_benchmark.py --model Qwen/Qwen2.5-3B-Instruct --reps 16
```

## Add a model

I want this benchmark to grow beyond the two model families already tested.

If you run CHB on another model, save the exact model version, tokenizer, learning conditions, source-removal method, state intervention, same-history control, path-cut result, software, hardware, and machine-readable result file.

Clean negative results are useful too.

## Author

Angelina Davini Hintsanen
