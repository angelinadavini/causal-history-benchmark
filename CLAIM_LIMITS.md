# What the v11 result shows

The frozen v11 study supports this result:

> The way the model learned the same information earlier changed what happened later. The original teaching state was removed. The same current rule was supplied again. Moving the bridge state left by one learning history into the other condition moved both a later hidden state and the complete next-token output toward the history that supplied the bridge. The result replicated in Mistral and in a second DAX/WUG task. When the later query could no longer use the bridge, the measured history difference disappeared.

That is the result CHB is built to test in other models.

## Where the current evidence stops

The confirmed study used two decoder-only transformer families and two controlled relation tasks.

It did not test:

- every language model;
- non-transformer architectures;
- unrestricted delays or long chains of intervening events;
- whether bridge K/V is comparable to any specific human neural state.

The answer endpoint also has a clear limit. In the primary Qwen arm, the correct-answer margin moved 0.45166 logits toward the donor history, with a 90% CI of [0.43629, 0.46694]. That failed the frozen ±0.20-logit equivalence rule. No choice-flip rule was frozen. The confirmed output result is therefore movement of the complete next-token distribution, not a robust overt-choice claim.

The attempted verbal source question also failed because the model showed a strong response bias. CHB does not use that measure as evidence of source attribution.

## What CHB is new for

Earlier work already showed that models can keep information in K/V state, that prompt history can affect answers, that internal state can reveal where information came from, that task directions can be found and moved, and that models can sometimes report information about their own processing.

CHB tests a different sequence in one controlled experiment:

```text
same rule
-> learned in two different ways
-> original source state removed
-> same current rule supplied again
-> retained bridge state moved between learning histories
-> later hidden state and full output move toward the donor history
-> bridge access removed
-> measured history difference disappears
```

That sequence is the contribution.

## Consciousness

CHB does not produce a consciousness score.

The benchmark can be used in research on AI consciousness because the experiment asks whether what happened earlier can change the state from which something later is processed. Any stronger consciousness claim has to come from the theory and evidence being tested around that result, not from a CHB number by itself.
