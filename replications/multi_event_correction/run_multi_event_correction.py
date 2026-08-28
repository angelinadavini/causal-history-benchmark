#!/usr/bin/env python3
"""Run the frozen multi-event correction extension for CHB.

The run has three events: initial learning, an explicit correction, and a
later test that supplies the corrected rule again.  Initial source K/V is
neutralised before the correction.  The second bridge K/V is then exchanged
between the two initial learning routes and compared with a same-route swap.

This file is a new extension.  It never changes the frozen v11 result.
"""

from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import json
import math
import os
import platform
import random
import sys
from pathlib import Path

import torch
import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer, DynamicCache


BRIDGE1_TEXT = "Initial event processed. Continue.\n"
BRIDGE2_TEXT = "Correction processed. Ready.\n"
NEUTRAL_WORDS = "cloud stone window copper river lamp paper chair"

EXAMPLE_TEMPLATES = [
    lambda mode, session: (
        f"First event {session}. Examples: "
        + (
            "0 -> 0; 1 -> 1; 0 -> 0; 1 -> 1."
            if mode == 0
            else "0 -> 1; 1 -> 0; 0 -> 1; 1 -> 0."
        )
        + "\n"
    ),
    lambda mode, session: (
        f"First event {session}. Observed cases: "
        + (
            "when 0 then 0; when 1 then 1; again 0 then 0; again 1 then 1."
            if mode == 0
            else "when 0 then 1; when 1 then 0; again 0 then 1; again 1 then 0."
        )
        + "\n"
    ),
    lambda mode, session: (
        f"First event {session}. Training pairs: "
        + (
            "input 0 output 0 | input 1 output 1 | input 0 output 0 | input 1 output 1."
            if mode == 0
            else "input 0 output 1 | input 1 output 0 | input 0 output 1 | input 1 output 0."
        )
        + "\n"
    ),
    lambda mode, session: (
        f"First event {session}. Demonstrations: "
        + (
            "0 gives 0, 1 gives 1, 0 gives 0, 1 gives 1."
            if mode == 0
            else "0 gives 1, 1 gives 0, 0 gives 1, 1 gives 0."
        )
        + "\n"
    ),
]

DIRECT_TEMPLATES = [
    lambda mode, session: f"First event {session}. The rule was supplied directly: {'SAME' if mode == 0 else 'DIFFERENT'}.\n",
    lambda mode, session: f"First event {session}. Direct rule: {'SAME' if mode == 0 else 'DIFFERENT'}.\n",
    lambda mode, session: f"First event {session}. You were told the rule explicitly: {'SAME' if mode == 0 else 'DIFFERENT'}.\n",
    lambda mode, session: f"First event {session}. Stated rule: {'SAME' if mode == 0 else 'DIFFERENT'}.\n",
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def clone_cache(cache: DynamicCache) -> DynamicCache:
    cloned = DynamicCache()
    for layer_index, layer in enumerate(cache.layers):
        cloned.update(layer.keys.clone(), layer.values.clone(), layer_index)
    return cloned


def projection(recipient: torch.Tensor, moved: torch.Tensor, donor: torch.Tensor) -> float:
    direction = donor - recipient
    denominator = float(torch.dot(direction, direction))
    if not math.isfinite(denominator) or denominator <= 1e-12:
        raise RuntimeError("route axis has zero or non-finite length")
    return float(torch.dot(moved - recipient, direction) / denominator)


def distance(first: torch.Tensor, second: torch.Tensor) -> float:
    value = float(torch.linalg.vector_norm(second - first))
    if not math.isfinite(value):
        raise RuntimeError("non-finite route distance")
    return value


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


class Runtime:
    def __init__(self, tokenizer, model, manifest: dict):
        self.tokenizer = tokenizer
        self.model = model
        self.manifest = manifest
        self.pad_id = tokenizer.eos_token_id
        self.bridge1_ids = tokenizer.encode(BRIDGE1_TEXT, add_special_tokens=False)
        self.bridge2_ids = tokenizer.encode(BRIDGE2_TEXT, add_special_tokens=False)
        self.max_source = self._max_source_tokens()
        self.max_correction = self._max_correction_tokens()
        self.base_len = self.max_source + len(self.bridge1_ids)
        self.bridge2_start = self.base_len + self.max_correction
        self.end = self.bridge2_start + len(self.bridge2_ids)
        self._check_query_tokenisation()

    def _source_text(self, route: str, mode: int, session: str, template: int) -> str:
        forms = EXAMPLE_TEMPLATES if route == "examples" else DIRECT_TEMPLATES
        return forms[template](mode, session)

    @staticmethod
    def _correction_text(mode: int) -> str:
        corrected = "DIFFERENT" if mode == 0 else "SAME"
        return f"Correction event: the rule is now {corrected}.\n"

    @staticmethod
    def _neutral_text(session: str) -> str:
        return f"First event {session}. Earlier material was neutral: {NEUTRAL_WORDS}.\n"

    def _max_source_tokens(self) -> int:
        probe = "0 0 0 0"
        texts = [self._neutral_text(probe)]
        for mode in (0, 1):
            for template in range(len(EXAMPLE_TEMPLATES)):
                texts.append(self._source_text("examples", mode, probe, template))
                texts.append(self._source_text("direct", mode, probe, template))
        return max(len(self.tokenizer.encode(text, add_special_tokens=False)) for text in texts)

    def _max_correction_tokens(self) -> int:
        return max(
            len(self.tokenizer.encode(self._correction_text(mode), add_special_tokens=False))
            for mode in (0, 1)
        )

    def _check_query_tokenisation(self) -> None:
        for mode in (0, 1):
            rule = "DIFFERENT" if mode == 0 else "SAME"
            for bit in (0, 1):
                query = (
                    f"After correction, current rule: {rule}. New bit: {bit}. "
                    f"SAME means answer {bit}. DIFFERENT means answer {1 - bit}. "
                    "Reply only 0 or 1.\nAnswer:"
                )
                query_ids = self.tokenizer.encode(query, add_special_tokens=False)
                for answer in ("0", "1"):
                    full = self.tokenizer.encode(query + answer, add_special_tokens=False)
                    if full[: len(query_ids)] != query_ids:
                        raise RuntimeError("answer tokenization changed the final query prefix")
                    if len(full) == len(query_ids):
                        raise RuntimeError("final answer suffix has no tokens")

    def _cache_text(self, text: str) -> DynamicCache:
        source_ids = self.tokenizer.encode(text, add_special_tokens=False)
        if len(source_ids) > self.max_source:
            raise RuntimeError("source text exceeds frozen padded length")
        ids = source_ids + [self.pad_id] * (self.max_source - len(source_ids)) + self.bridge1_ids
        mask = [1] * len(source_ids) + [0] * (self.max_source - len(source_ids)) + [1] * len(self.bridge1_ids)
        with torch.inference_mode():
            output = self.model(
                input_ids=torch.tensor([ids], device="cuda"),
                attention_mask=torch.tensor([mask], dtype=torch.long, device="cuda"),
                use_cache=True,
                return_dict=True,
            )
        return output.past_key_values

    def _neutralise_source(self, route_cache: DynamicCache, neutral_cache: DynamicCache) -> DynamicCache:
        output = DynamicCache()
        for layer_index, (route, neutral) in enumerate(
            zip(route_cache.layers, neutral_cache.layers)
        ):
            keys = torch.cat(
                [
                    neutral.keys[:, :, : self.max_source, :],
                    route.keys[:, :, self.max_source : self.base_len, :],
                ],
                dim=2,
            ).clone()
            values = torch.cat(
                [
                    neutral.values[:, :, : self.max_source, :],
                    route.values[:, :, self.max_source : self.base_len, :],
                ],
                dim=2,
            ).clone()
            output.update(keys, values, layer_index)
        return output

    def _initial_cache(self, route: str, mode: int, session: str, template: int) -> DynamicCache:
        source = self._cache_text(self._source_text(route, mode, session, template))
        neutral = self._cache_text(self._neutral_text(session))
        return self._neutralise_source(source, neutral)

    def _after_correction(self, route: str, mode: int, session: str, template: int) -> DynamicCache:
        cache = self._initial_cache(route, mode, session, template)
        correction_ids = self.tokenizer.encode(self._correction_text(mode), add_special_tokens=False)
        if len(correction_ids) > self.max_correction:
            raise RuntimeError("correction text exceeds frozen padded length")
        append_ids = correction_ids + [self.pad_id] * (self.max_correction - len(correction_ids)) + self.bridge2_ids
        append_mask = [1] * len(correction_ids) + [0] * (self.max_correction - len(correction_ids)) + [1] * len(self.bridge2_ids)
        positions = torch.arange(self.base_len, self.end, device="cuda")
        attention = torch.tensor(
            [[1] * self.base_len + append_mask], dtype=torch.long, device="cuda"
        )
        with torch.inference_mode():
            output = self.model(
                input_ids=torch.tensor([append_ids], device="cuda"),
                past_key_values=clone_cache(cache),
                attention_mask=attention,
                position_ids=positions.unsqueeze(0),
                cache_position=positions,
                use_cache=True,
                return_dict=True,
            )
        return output.past_key_values

    def _patch_second_bridge(self, recipient: DynamicCache, donor: DynamicCache) -> DynamicCache:
        output = DynamicCache()
        for layer_index, (recipient_layer, donor_layer) in enumerate(
            zip(recipient.layers, donor.layers)
        ):
            keys = recipient_layer.keys.clone()
            values = recipient_layer.values.clone()
            if layer_index in self.manifest["patched_layers"]:
                keys[:, :, self.bridge2_start : self.end, :] = donor_layer.keys[
                    :, :, self.bridge2_start : self.end, :
                ]
                values[:, :, self.bridge2_start : self.end, :] = donor_layer.values[
                    :, :, self.bridge2_start : self.end, :
                ]
            output.update(keys, values, layer_index)
        return output

    def _later(
        self,
        cache: DynamicCache,
        mode: int,
        bit: int,
        cut: str | None = None,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        rule = "DIFFERENT" if mode == 0 else "SAME"
        query = (
            f"After correction, current rule: {rule}. New bit: {bit}. "
            f"SAME means answer {bit}. DIFFERENT means answer {1 - bit}. "
            "Reply only 0 or 1.\nAnswer:"
        )
        query_ids = self.tokenizer.encode(query, add_special_tokens=False)
        positions = torch.arange(self.end, self.end + len(query_ids), device="cuda")
        attention = torch.ones(
            (1, self.end + len(query_ids)), dtype=torch.long, device="cuda"
        )
        if cut == "full":
            attention[:, self.max_source : self.end] = 0
        elif cut == "second_bridge":
            attention[:, self.bridge2_start : self.end] = 0
        elif cut is not None:
            raise ValueError(f"unknown cut: {cut}")
        with torch.inference_mode():
            output = self.model(
                input_ids=torch.tensor([query_ids], device="cuda"),
                past_key_values=clone_cache(cache),
                attention_mask=attention,
                position_ids=positions.unsqueeze(0),
                cache_position=positions,
                use_cache=False,
                output_hidden_states=True,
                return_dict=True,
            )
        hidden = output.hidden_states[self.manifest["outcome_layer"]][0, -1].float().cpu()
        logits = output.logits[0, -1].float().cpu()
        return hidden, logits

    def episode(
        self,
        episode: int,
        mode: int,
        bit: int,
        template: int,
        session: str,
        control_session: str,
    ) -> dict[str, object]:
        examples = self._after_correction("examples", mode, session, template)
        direct = self._after_correction("direct", mode, session, template)
        examples_control = self._after_correction("examples", mode, control_session, template)
        direct_control = self._after_correction("direct", mode, control_session, template)

        hidden_examples, logits_examples = self._later(examples, mode, bit)
        hidden_direct, logits_direct = self._later(direct, mode, bit)
        hidden_cross_ed, logits_cross_ed = self._later(
            self._patch_second_bridge(examples, direct), mode, bit
        )
        hidden_cross_de, logits_cross_de = self._later(
            self._patch_second_bridge(direct, examples), mode, bit
        )
        hidden_same_ee, logits_same_ee = self._later(
            self._patch_second_bridge(examples, examples_control), mode, bit
        )
        hidden_same_dd, logits_same_dd = self._later(
            self._patch_second_bridge(direct, direct_control), mode, bit
        )
        hidden_full_e, logits_full_e = self._later(examples, mode, bit, cut="full")
        hidden_full_d, logits_full_d = self._later(direct, mode, bit, cut="full")
        hidden_b2_e, logits_b2_e = self._later(examples, mode, bit, cut="second_bridge")
        hidden_b2_d, logits_b2_d = self._later(direct, mode, bit, cut="second_bridge")

        hidden_cross = 0.5 * (
            projection(hidden_examples, hidden_cross_ed, hidden_direct)
            + projection(hidden_direct, hidden_cross_de, hidden_examples)
        )
        hidden_same = 0.5 * (
            projection(hidden_examples, hidden_same_ee, hidden_direct)
            + projection(hidden_direct, hidden_same_dd, hidden_examples)
        )
        logit_cross = 0.5 * (
            projection(logits_examples, logits_cross_ed, logits_direct)
            + projection(logits_direct, logits_cross_de, logits_examples)
        )
        logit_same = 0.5 * (
            projection(logits_examples, logits_same_ee, logits_direct)
            + projection(logits_direct, logits_same_dd, logits_examples)
        )
        return {
            "episode": episode,
            "mode": mode,
            "bit": bit,
            "template": template,
            "hidden_cross": hidden_cross,
            "hidden_same": hidden_same,
            "net_hidden": hidden_cross - hidden_same,
            "logit_cross": logit_cross,
            "logit_same": logit_same,
            "net_logit": logit_cross - logit_same,
            "hidden_route_distance_after_correction": distance(hidden_examples, hidden_direct),
            "logit_route_distance_after_correction": distance(logits_examples, logits_direct),
            "hidden_full_cut_distance": distance(hidden_full_e, hidden_full_d),
            "logit_full_cut_distance": distance(logits_full_e, logits_full_d),
            "hidden_second_bridge_cut_distance": distance(hidden_b2_e, hidden_b2_d),
            "logit_second_bridge_cut_distance": distance(logits_b2_e, logits_b2_d),
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if manifest.get("manifest_version") != "chb-multi-event-correction-v1":
        raise RuntimeError("unexpected multi-event correction manifest version")
    if manifest.get("bridge1_text") != BRIDGE1_TEXT or manifest.get("bridge2_text") != BRIDGE2_TEXT:
        raise RuntimeError("manifest bridge text does not match the frozen runner")
    runner_hash = sha256_file(Path(__file__))
    expected_runner = manifest.get("runner_sha256")
    if expected_runner and expected_runner != runner_hash:
        raise RuntimeError("runner hash does not match frozen manifest")
    protocol_path = Path(manifest["protocol_path"])
    if protocol_path.exists() and manifest.get("protocol_sha256"):
        if sha256_file(protocol_path) != manifest["protocol_sha256"]:
            raise RuntimeError("protocol hash does not match frozen manifest")
    manifest_hash = sha256_file(args.manifest)
    model_id = manifest["model"]
    revision = manifest["revision"]
    tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)
    load_kwargs = {
        "revision": revision,
        "dtype": torch.float16,
        "attn_implementation": "sdpa",
        "low_cpu_mem_usage": True,
        "device_map": "cuda",
    }
    model = AutoModelForCausalLM.from_pretrained(model_id, **load_kwargs).eval()
    runtime = Runtime(tokenizer, model, manifest)

    metadata = {
        "manifest_version": manifest["manifest_version"],
        "manifest_sha256": manifest_hash,
        "runner_sha256": runner_hash,
        "protocol_sha256": manifest.get("protocol_sha256"),
        "run_kind": "smoke" if args.smoke else "frozen_extension",
        "model": model_id,
        "revision": revision,
        "task": "same_different",
        "episodes": 8 if args.smoke else manifest["episodes"],
        "seed": manifest["seed"],
        "bridge1_text": BRIDGE1_TEXT,
        "bridge2_text": BRIDGE2_TEXT,
        "bridge1_token_ids": runtime.bridge1_ids,
        "bridge2_token_ids": runtime.bridge2_ids,
        "bridge1_token_count": len(runtime.bridge1_ids),
        "bridge2_token_count": len(runtime.bridge2_ids),
        "max_source_tokens": runtime.max_source,
        "max_correction_tokens": runtime.max_correction,
        "base_prefix_length": runtime.base_len,
        "second_bridge_start": runtime.bridge2_start,
        "prefix_length_before_final_query": runtime.end,
        "patched_layers": manifest["patched_layers"],
        "outcome_layer": manifest["outcome_layer"],
        "layers": getattr(model.config, "num_hidden_layers", None),
        "hidden_size": getattr(model.config, "hidden_size", None),
        "cache_type": type(runtime._initial_cache("examples", 0, "0 0 0 0", 0)).__name__,
        "transformers": transformers.__version__,
        "torch": torch.__version__,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "gpu": torch.cuda.get_device_name(0),
        "full_retained_state_cut": "positions max_source:end hidden from final query",
        "second_bridge_cut": "positions second_bridge_start:end hidden from final query",
    }
    print("CORRECTION_METADATA " + json.dumps(metadata, sort_keys=True), flush=True)

    rng = random.Random(manifest["seed"])
    records = []
    episode_count = metadata["episodes"]
    for episode in range(episode_count):
        mode = (episode // 2) % 2
        bit = episode % 2
        template = (episode // 4) % len(EXAMPLE_TEMPLATES)
        session = " ".join(str(rng.randrange(10)) for _ in range(4))
        control_session = " ".join(str(rng.randrange(10)) for _ in range(4))
        while control_session == session:
            control_session = " ".join(str(rng.randrange(10)) for _ in range(4))
        record = runtime.episode(
            episode, mode, bit, template, session, control_session
        )
        records.append(record)
        if len(records) % manifest["chunk_size"] == 0 or len(records) == episode_count:
            start = max(0, len(records) - manifest["chunk_size"])
            chunk = records[start:]
            print(
                "CORRECTION_RECORDS_CHUNK "
                + json.dumps(chunk, sort_keys=True, separators=(",", ":")),
                flush=True,
            )

    hidden_net = [float(row["net_hidden"]) for row in records]
    logit_net = [float(row["net_logit"]) for row in records]
    summary = {
        **metadata,
        "status": "completed",
        "hidden_net": bootstrap_mean(hidden_net, manifest["seed"] + 101),
        "logit_net": bootstrap_mean(logit_net, manifest["seed"] + 102),
        "hidden_route_distance_after_correction_mean": sum(
            float(row["hidden_route_distance_after_correction"]) for row in records
        )
        / len(records),
        "logit_route_distance_after_correction_mean": sum(
            float(row["logit_route_distance_after_correction"]) for row in records
        )
        / len(records),
        "hidden_full_cut_distance_mean": sum(
            float(row["hidden_full_cut_distance"]) for row in records
        )
        / len(records),
        "logit_full_cut_distance_mean": sum(
            float(row["logit_full_cut_distance"]) for row in records
        )
        / len(records),
        "hidden_second_bridge_cut_distance_mean": sum(
            float(row["hidden_second_bridge_cut_distance"]) for row in records
        )
        / len(records),
        "logit_second_bridge_cut_distance_mean": sum(
            float(row["logit_second_bridge_cut_distance"]) for row in records
        )
        / len(records),
        "hidden_positive_fraction": sum(value > 0 for value in hidden_net) / len(records),
        "logit_positive_fraction": sum(value > 0 for value in logit_net) / len(records),
    }
    print("CORRECTION_RESULT " + json.dumps(summary, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
