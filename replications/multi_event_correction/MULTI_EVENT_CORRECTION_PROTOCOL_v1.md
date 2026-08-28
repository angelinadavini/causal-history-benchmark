# Multi-event correction test, version 1

## Question

After a model learns a rule, can a later correction event remove the effect of
how that rule was first learned?

The test keeps the current rule the same at the final event. It asks whether
the first learning route still changes the state from which that final event is
processed.

## Event sequence

Each episode has three events.

1. **Initial learning.** The model receives the SAME or DIFFERENT rule through
   examples or through a direct instruction.
2. **Correction.** The rule is reversed in a later event. The correction text is
   the same for the examples and direct-instruction histories within each rule
   condition.
3. **Final test.** The corrected rule is supplied again with a new binary item.
   The answer mapping is therefore the same at the time of measurement.

The initial source is neutralised before the correction event. The first bridge
state is kept while the correction is processed. A second fixed bridge follows
the correction.

## Causal intervention

The primary intervention moves the second bridge K/V state from one initial
learning route into the other route. The second bridge is the state produced
after the correction event. A same-route bridge swap is the control.

The later hidden state and the complete next-token logit vector are measured at
the final test.

## Path controls

Two path checks are recorded.

- **Full retained-state cut:** the later test cannot attend to the first bridge,
  the correction event, or the second bridge. The source positions contain the
  same neutral K/V state in both histories. The history difference should fall
  to zero.
- **Second-bridge-only cut:** the later test cannot attend to the second bridge
  while the first bridge and correction positions remain visible. This records
  whether the final bridge is the only route that carries the difference.

## Frozen task and text

The task is SAME/DIFFERENT. Four initial wording forms are balanced across
episodes. The direct and example forms use the same rule content within an
episode. The correction is explicit and reverses the initial rule.

The final event says the corrected rule again and supplies a new bit. The
candidate answer strings `0` and `1` are checked in the full prompt context
before any episode is run. The run stops if adding either answer changes the
query-token prefix.

The two visible bridges are fixed text. Their token counts, the padded source
length, the padded correction length, the patched layers, and the outcome layer
are recorded in the run metadata.

## Primary endpoint and controls

For each episode, route-axis movement is calculated in the same way as the
frozen CHB test:

```text
p(a,z,b) = ((z-a) · (b-a)) / (||b-a||² + 1e-9)
```

The cross-history value averages both swap directions. The same-history value
does the same for matched swaps. The reported net value is cross-history minus
same-history movement.

The primary endpoint is net movement of the final hidden state toward the
donor history. Net movement of the complete next-token logit vector is a second
endpoint. The full retained-state cut is required to remove the measured route
difference.

## Frozen decision rules

The protocol is an extension of CHB, not a replacement for the v11 study.

- A positive hidden-state result requires a 95% bootstrap interval for the net
  movement to lie above zero.
- The complete-logit result is reported with its interval and is not converted
  into an overt-choice claim.
- A full retained-state cut must reduce both route distances to zero within
  floating-point tolerance. A failure is recorded as a path-control failure.
- Any tokenizer, cache, model-loading, or task-setup failure is an engineering
  failure. It is not a negative scientific result.

## Scope

This test asks whether an initial learning route remains causally operative
after one explicit correction event. It does not test lasting weight updates,
unrestricted delays, sessions, or phenomenal consciousness.

The test is run first on the pinned Qwen2.5-3B-Instruct model. A separate OLMo-2
run may use the same frozen protocol with its own model manifest. Each model is
reported as a new extension and cannot change the frozen v11 values.
