# Roadmap

## 1. Freeze the confirmatory benchmark

Before the main confirmatory run:

- freeze acquisition templates;
- freeze task families;
- freeze model list;
- freeze bridge text;
- freeze intervention layers and outcome layers;
- freeze exclusion rules;
- freeze statistics and equivalence bounds;
- generate fresh untouched random seeds.

Development runs already influenced design choices. They will remain development data.

## 2. Confirm Qwen result on fresh seeds

Primary confirmatory checks:

- SAME/DIFFERENT task;
- DAX/WUG mapping task;
- held-out surface wording;
- cross-route interchange;
- same-route control;
- norm-matched random control;
- output/logit mediation;
- finer layer localization.

## 3. Cross-model replication

Target at least three independent model families where technically practical:

- Qwen;
- Mistral;
- Gemma or Llama-family model.

Quantized and full-precision runs should be distinguished explicitly.

## 4. Architecture comparison

The longer-term benchmark should compare different ways of carrying history:

- standard decoder-only Transformer K/V state;
- recurrent or state-space models;
- memory-augmented systems;
- trained compression systems such as memento-style architectures.

The question is whether route-specific causal history behaves differently when a system has a stronger built-in mechanism for carrying state forward.

## 5. Source attribution

The first verbal source-report test showed a strong answer bias and is rejected as evidence.

A better measure should:

- counterbalance source labels;
- avoid obvious semantic priors such as "examples" versus "rule";
- use forced-choice token calibration;
- measure source judgement after the later-event measure;
- test whether source judgement tracks the objectively manipulated history.

## 6. Public benchmark package

Planned release artifacts:

- Hugging Face dataset with generated benchmark episodes;
- dataset card;
- exact experiment configs;
- model-support table;
- frozen result files;
- reproducibility scripts;
- tagged GitHub release;
- archival DOI.

## 7. Paper boundary

The conference paper should stay short.

The main text should carry:

- the contribution;
- why it matters;
- nearest prior work;
- exact experimental logic;
- decisive results;
- limits of inference.

The public repository should carry the larger research trail, failed tests, extended controls, code, and full benchmark documentation.
