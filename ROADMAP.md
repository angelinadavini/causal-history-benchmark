# What comes next

The first frozen CHB result is confirmed. The next job is to make the test easy for other people to find, run, and extend.

## 1. Finish exact v11 reproduction

The public repo already has the small reusable runner and the frozen result record.

The exact v11 runner, analysis code, manifests, and public-safe result files should also live here so another researcher can reproduce the confirmed study without guessing which development script was used.

The exact reproduction command should check the frozen hashes before it runs.

## 2. Put CHB where ML researchers already look

GitHub is the code home.

The next public layer is Hugging Face:

- a public CHB benchmark dataset;
- a clear dataset card;
- `eval.yaml` so Hugging Face can recognise it as a benchmark;
- model-result files that can appear on model pages and feed the CHB leaderboard;
- a public Space that shows the result table and gives people a simple way into the benchmark.

After that, freeze a release on Zenodo so every benchmark version can be cited with a DOI.

The paper should point to the benchmark. The benchmark should remain useful without the paper.

## 3. Test more model families

The current confirmed result covers Qwen and Mistral.

The next strong tests are:

- Gemma;
- Llama-family models;
- other Qwen and Mistral sizes;
- another open model family with a different implementation.

We want to know where the effect repeats, where it gets weaker, and where it disappears when the experiment itself still works.

## 4. Test systems that do not use transformer K/V

This is one of the most important extensions.

Possible targets:

- state-space models;
- recurrent language models;
- explicit-memory systems;
- learned context-compression systems;
- multimodal agents that carry state forward.

The stored state can be different. The question stays the same: after the original source is gone and the same current information is available, does how the information entered earlier still change what happens next?

## 5. Change the learning histories

Examples versus direct instruction is only the first pair.

Other useful comparisons include:

- seeing something versus being told it;
- reaching a conclusion yourself versus being given the conclusion;
- retrieving information versus already having it in the model;
- first learning versus correction;
- different teaching sequences that end with the same usable rule.

Each test still has to make the current information the same before asking whether the earlier route changes what happens later.

## 6. Add time and interference

Test what happens when more is placed between the learning event and the later event:

- longer delays;
- unrelated material;
- competing rules;
- context compression;
- state resets;
- memory retrieval.

This tells us how long the history effect lasts and what destroys it.

## 7. Build a better source-history measure

The first verbal source question failed because the model fell into a response bias.

A new source-history measure should avoid relying on the model simply choosing between verbal labels such as “examples” and “instruction.” It should be designed so a response habit cannot look like source knowledge.

## 8. Make outside results easy to add

A researcher who runs CHB should be able to submit one result file, one reproducible script, and one short explanation.

The public leaderboard should include positive results, clean negative results, and setup failures in separate places so nobody has to guess what happened.

The goal is simple: if somebody tests a new model next year, they should have a clear place to put the result and a clear earlier result to compare it with.
