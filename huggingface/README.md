# Hugging Face release files

This folder contains the files for the public Hugging Face version of CHB.

The goal is simple: somebody who searches Hugging Face for benchmarks should be able to find CHB, see the confirmed results, open the code, and test another model.

## Dataset repo

`dataset/` contains the dataset card and `eval.yaml` for a public benchmark repo under:

`angelinadavini/causal-history-benchmark`

Hugging Face currently requires benchmark evaluation frameworks to be on its maintained framework list before `eval.yaml` can be registered. CHB is a new framework, so `causal-history-benchmark` needs to be added to that list before the benchmark can receive the official Hub benchmark leaderboard treatment.

The dataset can still be public before that registration step.

## Space

`space/` contains a small public front page for the benchmark.

It shows:

- the question CHB asks;
- the three frozen v11 results;
- the separate OLMo-2 extension result and its uncertainty;
- the separate multi-event correction results and their uncertainty;
- the bridge-cut result;
- the command to run the public reference test;
- the GitHub link;
- the author name.

The Space does not need a paid GPU because it is a public entry point and result viewer, not the place where 3B and 7B model experiments are run.

The expensive model runs belong in reproducible jobs. The public Space belongs on free CPU.
