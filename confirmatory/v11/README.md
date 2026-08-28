# Exact v11 reproduction

The small runner in `scripts/reference_interchange.py` is useful for trying CHB on a compatible model. It is not the code that produced the frozen v11 numbers.

This folder contains the two frozen code packages used for that study:

- `AI_Consciousness_Confirmatory_Freeze_v2.zip` contains the Qwen primary and Mistral replication runner, analysis, protocol, requirements, and seed manifest.
- `AI_Consciousness_Confirmatory_Secondary_Amendment_v2_1.zip` contains the repaired Qwen DAX/WUG runner, analysis, protocol, requirements, and secondary seed manifest.
- `AI_Consciousness_Confirmatory_Results_v2_1.zip` contains the final logs, every packed record chunk, the analysis output, and the result summary.

The packages are kept unchanged. The manifest locks are:

```text
base v2:      fb42c0f7e984c8e775b55960eb5c7f9be02d6eff8944bcdb198223435764a7d2
secondary v2.1: 570f3119f16b32942c0bae5fdbdeb8396311a76c3bb8fed1b6eea577fc69cb54
```

Check the package locks without downloading model weights:

```bash
python scripts/reproduce_v11.py
```

Run the full reproduction only on a GPU with access to the pinned model revisions:

```bash
python scripts/reproduce_v11.py --run --output v11-reproduction-output
```

The script verifies the manifest, protocol, runner, analysis, and requirements hashes before it starts. It writes raw runner logs and the joint analysis to the chosen output directory. The run is separate from the published v11 results and never overwrites them.

The public result is the causal movement of the later hidden state and the complete next-token logit vector after cross-history bridge replacement and subtraction of the same-history control. It is not a consciousness score.
