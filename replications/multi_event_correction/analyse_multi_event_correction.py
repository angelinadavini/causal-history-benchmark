#!/usr/bin/env python3
"""Recompute the frozen multi-event correction extension from a raw log."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def bootstrap_mean(values: list[float], seed: int, draws: int = 10000) -> dict[str, object]:
    rng = random.Random(seed)
    n = len(values)
    means = [
        sum(values[rng.randrange(n)] for _ in range(n)) / n
        for _ in range(draws)
    ]
    means.sort()
    return {
        "mean": sum(values) / n,
        "ci95": [means[int(0.025 * draws)], means[int(0.975 * draws) - 1]],
    }


def parse_log(path: Path) -> tuple[dict, list[dict], dict]:
    metadata = None
    result = None
    records: list[dict] = []
    chunks: list[list[dict]] = []
    pending_chunk: str | None = None

    def finish_chunk() -> None:
        nonlocal pending_chunk
        if pending_chunk is not None:
            chunks.append(json.loads(pending_chunk))
            pending_chunk = None

    # The Jobs log service wraps very long stdout lines at 16 KB.  A record
    # chunk can therefore arrive as two physical lines.  Join continuation
    # text before decoding it; the raw log file itself remains unchanged.
    for line in path.read_text(encoding="utf-8").split("\n"):
        line = line.rstrip("\r")
        if line.startswith("CORRECTION_METADATA "):
            finish_chunk()
            metadata = json.loads(line.split(" ", 1)[1])
        elif line.startswith("CORRECTION_RECORDS_CHUNK "):
            finish_chunk()
            pending_chunk = line.split(" ", 1)[1]
        elif line.startswith("CORRECTION_RESULT "):
            finish_chunk()
            result = json.loads(line.split(" ", 1)[1])
        elif pending_chunk is not None:
            pending_chunk += line
    finish_chunk()
    if metadata is None:
        raise ValueError("raw log has no CORRECTION_METADATA line")
    if result is None:
        raise ValueError("raw log has no CORRECTION_RESULT line")
    for chunk in chunks:
        records.extend(chunk)
    if not records:
        raise ValueError("raw log has no correction records")
    return metadata, records, result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("log", type=Path)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--runner", type=Path, required=True)
    parser.add_argument("--protocol", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    metadata, records, reported = parse_log(args.log)
    expected_manifest_hash = sha256_file(args.manifest)
    if metadata.get("manifest_sha256") != expected_manifest_hash:
        raise ValueError("manifest hash in raw log does not match the supplied manifest")
    if metadata.get("runner_sha256") != manifest.get("runner_sha256"):
        raise ValueError("runner hash in raw log does not match the manifest")
    if sha256_file(args.runner) != manifest.get("runner_sha256"):
        raise ValueError("runner file does not match the manifest")
    if sha256_file(args.protocol) != manifest.get("protocol_sha256"):
        raise ValueError("protocol file does not match the manifest")
    if metadata.get("run_kind") != "frozen_extension":
        raise ValueError("the supplied log is not a frozen extension run")
    if len(records) != manifest["episodes"]:
        raise ValueError(f"expected {manifest['episodes']} records, found {len(records)}")
    episodes = [int(row["episode"]) for row in records]
    if sorted(episodes) != list(range(manifest["episodes"])):
        raise ValueError("episode records are missing, duplicated, or out of order")

    hidden_net = [float(row["net_hidden"]) for row in records]
    logit_net = [float(row["net_logit"]) for row in records]
    hidden_full_cut = [float(row["hidden_full_cut_distance"]) for row in records]
    logit_full_cut = [float(row["logit_full_cut_distance"]) for row in records]
    hidden_b2_cut = [float(row["hidden_second_bridge_cut_distance"]) for row in records]
    logit_b2_cut = [float(row["logit_second_bridge_cut_distance"]) for row in records]
    tolerance = 1e-6
    analysis = {
        "analysis_version": "chb-multi-event-correction-analysis-v1",
        "manifest_sha256": expected_manifest_hash,
        "runner_sha256": manifest["runner_sha256"],
        "protocol_sha256": manifest["protocol_sha256"],
        "model": manifest["model"],
        "revision": manifest["revision"],
        "task": manifest["task"],
        "episodes": len(records),
        "hidden_net": bootstrap_mean(hidden_net, int(manifest["seed"]) + 101),
        "logit_net": bootstrap_mean(logit_net, int(manifest["seed"]) + 102),
        "hidden_positive_fraction": sum(value > 0 for value in hidden_net) / len(records),
        "logit_positive_fraction": sum(value > 0 for value in logit_net) / len(records),
        "hidden_route_distance_after_correction_mean": sum(
            float(row["hidden_route_distance_after_correction"]) for row in records
        )
        / len(records),
        "logit_route_distance_after_correction_mean": sum(
            float(row["logit_route_distance_after_correction"]) for row in records
        )
        / len(records),
        "hidden_full_cut_distance_mean": sum(hidden_full_cut) / len(records),
        "logit_full_cut_distance_mean": sum(logit_full_cut) / len(records),
        "hidden_second_bridge_cut_distance_mean": sum(hidden_b2_cut) / len(records),
        "logit_second_bridge_cut_distance_mean": sum(logit_b2_cut) / len(records),
        "full_cut_hidden_zero": all(abs(value) <= tolerance for value in hidden_full_cut),
        "full_cut_logit_zero": all(abs(value) <= tolerance for value in logit_full_cut),
        "reported_result_matches": reported.get("hidden_net") == bootstrap_mean(hidden_net, int(manifest["seed"]) + 101)
        and reported.get("logit_net") == bootstrap_mean(logit_net, int(manifest["seed"]) + 102),
        "status": "analysed",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(analysis, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(analysis, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
