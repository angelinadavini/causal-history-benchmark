from causal_history.frozen import V11_ARMS


def test_frozen_v11_values():
    assert V11_ARMS["qwen_primary"]["hidden_mean"] == 0.687469575
    assert V11_ARMS["mistral_replication"]["logit_mean"] == 0.0586511536
    assert V11_ARMS["qwen_secondary"]["hidden_cut_ratio"] == 0.0
