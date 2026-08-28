# Model support

| Model | Status | Precision | Result |
|---|---|---|---|
| Qwen2.5-0.5B-Instruct | development only | fp16 | below task-capacity gate on early benchmark versions |
| Qwen2.5-3B-Instruct | working reference model | fp16 | causal route-state effects reproduced across two tasks; early-layer localization completed |
| Mistral-7B-Instruct-v0.3 | working replication | 4-bit NF4 | cross-route bridge swap moved later state 0.809 toward donor route vs 0.031 same-route control |
| Mistral-7B-Instruct-v0.3 | pending full-precision replication | fp16 | queued attempt canceled before a result |
| Phi-3.5-mini-instruct | engineering blocked | fp16 | DynamicCache compatibility failure in current environment; no scientific result |

## Adding a model

A model should not be listed as a scientific replication until:

1. the model can run the task and positive controls;
2. source-prefix neutralization is verified;
3. paired example/direct histories are generated with matched current content;
4. same-route swaps are run;
5. cross-route state swaps are run;
6. the later-event effect is measured before any source-report question;
7. all tokenizer and output-label assumptions are checked.

Quantized runs should be labelled as quantized. They are useful replication evidence and should not silently stand in for a full-precision result.
