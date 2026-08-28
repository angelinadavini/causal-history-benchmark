# Claim limits

## Supported by the frozen v11 confirmatory study

The evidence supports this claim:

> In Qwen2.5-3B-Instruct, acquisition route left a retained bridge state after source-history neutralisation. Exchanging early bridge K/V between acquisition routes causally moved both a fixed later hidden state and the complete next-token logit vector toward the donor history after the current task relation was supplied again. The effect replicated in Mistral-7B-Instruct-v0.3 and in a separate DAX/WUG mapping task.

The bridge-path intervention supports a carrier claim inside this implementation: the measured route difference disappeared when later tokens could not attend to the bridge.

The SAME/DIFFERENT results also support transfer across task-content mode and evaluation wording at the fixed hidden layer. The evaluation wording was held out from confirmatory centroid estimation and had been inspected during development.

## Unsupported

Do not use this benchmark result to claim:

- consciousness;
- sentience;
- phenomenal experience;
- subjective continuity;
- a unique criterion for consciousness;
- a general result for every language model or artificial system;
- a robust overt-choice effect;
- valid verbal source attribution;
- equivalence between transformer bridge K/V and human experience;
- independence from transformer K/V architecture;
- persistence across unrestricted delays or intervening events;
- investigator-unseen wording.

## Answer endpoint

The Qwen primary correct-answer margin moved 0.45166 logits toward the donor, with a 90% CI of [0.43629, 0.46694]. That interval lies outside the frozen ±0.20-logit equivalence bound.

The two-token probability movement was 0.00562 [0.00467, 0.00658], inside its ±0.05 bound.

No choice-flip rule was frozen. State only that the complete output distribution moved and that the Qwen secondary margin endpoint was not negligible under the frozen rule.

Mistral and DAX/WUG met both answer-endpoint equivalence rules.

## Prior-work boundary

The benchmark does not claim discovery of:

- K/V leakage after text removal;
- generic prompt-history effects;
- decodability of retained state;
- task or function vectors;
- machine introspection;
- source-provenance signatures;
- temporal continuity as a proposed AI-consciousness requirement;
- consciousness-theory indicators for AI.

The contribution is the controlled causal sequence:

```text
same usable relation
-> different acquisition route
-> source prefix neutralised
-> current relation supplied again
-> retained bridge state interchanged
-> later hidden state and full logit distribution move toward donor history
-> bridge access removed and route difference disappears
```

## Community extensions

A result from another model or architecture inherits only the claim supported by its own controls. A replication should not be described as a consciousness result unless an independent validated consciousness criterion exists. This repository currently contains no such criterion.
