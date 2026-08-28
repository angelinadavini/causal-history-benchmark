# Roadmap

The first frozen confirmatory benchmark has passed. The priority now is reuse, independent replication, and architecture coverage.

## 1. Make the benchmark easy to run

Current public pieces:

- benchmark contract;
- compact Qwen reference implementation;
- confirmed Qwen and Mistral results;
- machine-readable confirmatory summary;
- quickstart;
- contribution guide;
- public replication leaderboard.

Next packaging work:

- publish the exact frozen confirmatory runners and manifests;
- add a small command-line wrapper that writes a standard result JSON;
- add automated preflight checks for token boundaries and supported cache APIs;
- add a reproducible environment container.

## 2. Independent model-family replications

High-value targets:

- Gemma;
- Llama-family models;
- additional Qwen and Mistral sizes;
- other open decoder-only models.

The main goal is to learn where the effect replicates, where it weakens, and where it fails under working controls.

## 3. Leave transformer K/V

The strongest extension is an architecture whose continuing state is not transformer K/V.

Targets include:

- state-space language models;
- recurrent language models;
- explicit-memory systems;
- trained context-compression systems;
- multimodal agents with persistent internal state.

The state object can change. The causal question stays the same.

## 4. New acquisition histories

Examples versus direct instruction is the first controlled route pair.

Future benchmark modules can test:

- observation versus explicit instruction;
- self-generated inference versus supplied conclusion;
- retrieved context versus internally learned relation;
- correction versus first acquisition;
- demonstration sequence variants that end with the same usable rule.

Each module must preserve a clean current-content control.

## 5. Time and interference

Test whether route-dependent causal history survives:

- longer token delays;
- unrelated intervening events;
- competing relations;
- context compression;
- state resets;
- memory retrieval boundaries.

## 6. Source attribution

The first verbal source-report instrument failed through response bias and is excluded.

A replacement should use bias-resistant response coding, tokenizer preflight, counterbalanced labels, and measurement after the later-event endpoint.

## 7. Public distribution

The repository should remain the canonical development home.

Planned distribution layers:

- Hugging Face benchmark dataset and dataset card;
- standard model-result JSON files;
- tagged GitHub releases;
- archival DOI for frozen benchmark versions;
- community leaderboard linked to reproducible code.

The aim is for researchers to run the benchmark without needing the paper.

## 8. Publication

Conference publication remains useful for peer review and formal argument. The benchmark should remain usable even if a reader never opens the paper.
