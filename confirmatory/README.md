# Frozen confirmatory benchmark v2.1

This directory records the frozen confirmatory provenance used by the v11 result.

## Valid scientific jobs

- Qwen primary: `6a90939f45686a1580c0f60e`
- Mistral replication: `6a9093b3984507d9db4e8d7d`
- amended Qwen DAX/WUG: `6a90c7e345686a1580c0fe2a`

## Frozen hashes

Base v2 manifest:

```text
fb42c0f7e984c8e775b55960eb5c7f9be02d6eff8944bcdb198223435764a7d2
```

Secondary v2.1 manifest:

```text
570f3119f16b32942c0bae5fdbdeb8396311a76c3bb8fed1b6eea577fc69cb54
```

The base v2 manifest records frozen episode, reference, bootstrap, and randomisation seeds for the primary Qwen, Mistral replication, and original secondary arms.

The secondary v2.1 manifest records fresh secondary seeds after the tokenizer-only amendment.

## Package versions

The frozen confirmatory requirements were:

```text
transformers==5.13.0
sentencepiece==0.2.1
accelerate==1.10.1
```

## Why v2.1 exists

The original confirmatory launch was invalidated before scientific output was inspected because a bare-label tokenizer assumption failed for Mistral.

A repaired v2 launch completed the Qwen primary and Mistral arms. The DAX/WUG arm then stopped on its first episode because adding `X` changed the query-token boundary.

A tokenizer-only preflight checked `0`, `1`, `X`, and `Y` in every task cell for both pinned tokenizers. The DAX/WUG later query received one added newline after `Answer:`. The amendment and fresh secondary seeds were frozen before the completed Qwen and Mistral scientific outputs were opened.

## Result summary

See:

- [../RESULTS.md](../RESULTS.md)
- [../results/confirmatory_summary.csv](../results/confirmatory_summary.csv)

## Public reproduction

The compact public runner in `scripts/reference_interchange.py` implements the core causal manipulation for reuse on compatible models.

The repository will keep the exact frozen confirmatory runners and complete raw result package as a versioned archival artifact. The manifest hashes above identify the frozen protocol state independently of later benchmark extensions.
