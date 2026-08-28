"""Frozen v11 confirmatory summary.

These constants are a machine-readable copy of the v11 checkpoint. They are
not recomputed from exploratory runs.
"""

V11_ARMS = {
    "qwen_primary": {
        "model": "Qwen/Qwen2.5-3B-Instruct",
        "task": "same_different",
        "episodes": 512,
        "hidden_mean": 0.687469575,
        "hidden_ci95": [0.6866143062, 0.6883246779],
        "logit_mean": 0.2583306524,
        "logit_ci95": [0.2555484079, 0.2610885156],
        "hidden_cut_ratio": 0.0,
        "logit_cut_ratio": 0.0,
        "job_id": "6a90939f45686a1580c0f60e",
    },
    "mistral_replication": {
        "model": "mistralai/Mistral-7B-Instruct-v0.3",
        "task": "same_different",
        "episodes": 256,
        "hidden_mean": 0.8009862129,
        "hidden_ci95": [0.7995546236, 0.802449715],
        "logit_mean": 0.0586511536,
        "logit_ci95": [0.0568064663, 0.0605615105],
        "hidden_cut_ratio": 0.0,
        "logit_cut_ratio": 0.0,
        "job_id": "6a9093b3984507d9db4e8d7d",
    },
    "qwen_secondary": {
        "model": "Qwen/Qwen2.5-3B-Instruct",
        "task": "dax_wug",
        "episodes": 256,
        "hidden_mean": 0.6051466105,
        "hidden_ci95": [0.6035211896, 0.6067949519],
        "logit_mean": 0.0471712814,
        "logit_ci95": [0.0433458042, 0.0510640598],
        "hidden_cut_ratio": 0.0,
        "logit_cut_ratio": 0.0,
        "job_id": "6a90c7e345686a1580c0fe2a",
    },
}

BASE_V2_MANIFEST_SHA256 = "fb42c0f7e984c8e775b55960eb5c7f9be02d6eff8944bcdb198223435764a7d2"
SECONDARY_V2_1_MANIFEST_SHA256 = "570f3119f16b32942c0bae5fdbdeb8396311a76c3bb8fed1b6eea577fc69cb54"
