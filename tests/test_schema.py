import pytest

from causal_history.schema import validate_result


def valid_record():
    return {
        "benchmark_version": "0.1.0",
        "model": "example/model",
        "model_revision": "abc123",
        "task": "same_different",
        "episodes": 16,
        "hidden_net_movement": 0.5,
        "logit_net_movement": 0.1,
        "hidden_cut_ratio": 0.0,
        "logit_cut_ratio": 0.0,
        "source_neutralised": True,
        "same_route_control": True,
    }


def test_valid_record_passes():
    validate_result(valid_record())


def test_missing_control_fails():
    record = valid_record()
    record["same_route_control"] = False
    with pytest.raises(ValueError):
        validate_result(record)
