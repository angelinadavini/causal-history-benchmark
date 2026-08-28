from __future__ import annotations

REQUIRED_RESULT_FIELDS = {
    "benchmark_version",
    "model",
    "model_revision",
    "task",
    "episodes",
    "hidden_net_movement",
    "logit_net_movement",
    "hidden_cut_ratio",
    "logit_cut_ratio",
    "source_neutralised",
    "same_route_control",
}


def validate_result(record: dict) -> None:
    missing = sorted(REQUIRED_RESULT_FIELDS - set(record))
    if missing:
        raise ValueError(f"missing required result fields: {', '.join(missing)}")
    if not isinstance(record["episodes"], int) or record["episodes"] <= 0:
        raise ValueError("episodes must be a positive integer")
    for key in ("hidden_net_movement", "logit_net_movement", "hidden_cut_ratio", "logit_cut_ratio"):
        if not isinstance(record[key], (int, float)):
            raise ValueError(f"{key} must be numeric")
    for key in ("source_neutralised", "same_route_control"):
        if record[key] is not True:
            raise ValueError(f"{key} must be true for a benchmark-valid result")
