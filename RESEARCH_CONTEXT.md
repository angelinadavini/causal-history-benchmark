# Where CHB fits

CHB came from a simple question: if the same information is available now, can the way it entered earlier still change what a model does next?

Several research areas already answer nearby questions. CHB was built to test the part that was still missing.

## What earlier ML work had already shown

### Information can remain after the original text is gone

MEMENTO showed that information from removed reasoning blocks can survive in later K/V state and still affect later computation.

So CHB does not claim that it discovered K/V persistence.

### A model can carry signs of where information came from

Work on source provenance, retrieved context, and computational reality monitoring shows that information learned or retrieved in different ways can leave different internal patterns.

So simply finding a history signature inside a model is also not enough for the CHB claim.

### Internal task information can be moved

Function-vector, activation-patching, interchange-intervention, and causal-abstraction work shows that internal model state can be changed directly and that the change can alter later computation.

CHB uses that kind of causal test on learning history.

### Being able to read information from a state does not mean the model uses it

A probe may decode something that has little or no effect on the next computation.

That is why CHB does not stop when learning history can be decoded. The state has to be changed, and the later computation has to move with it.

## Why consciousness research led to this question

Human consciousness research separates things that happen at different times: an event, later attention, later interpretation, introspection, decision, report, and memory.

That timing created the machine question behind CHB. If something that happens earlier changes the system, a later event may occur in a system that has already been changed by what came before.

The benchmark asks whether current AI can show that part of the sequence in a controlled causal test.

The confirmed result says that the tested models can: how the same information was learned earlier changed the state used during later processing, even after the original source was removed and the same current rule was supplied again.

How that result should be used inside a theory of consciousness is a separate scientific argument. CHB gives researchers a machine result they can compare with those theories instead of relying only on what a model says about itself.

## Why the repo is public

The paper is one account of the work. The benchmark is the reusable part.

This repository is meant to let other researchers test the same question, challenge the result, add models, change the intervention, and show where the effect does or does not hold.
