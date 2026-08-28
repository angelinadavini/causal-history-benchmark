#!/usr/bin/env python3
"""Frozen-style OLMo-2 Causal History Benchmark extension.

This extension uses the public CHB SAME/DIFFERENT task.  The old source
prefix is neutralised, the five-token bridge is retained, and a later event
receives the same current rule in both histories.  Cross-history bridge K/V
interchange is compared with a same-history swap.  A bridge visibility cut
checks the proposed path from the retained state to the later event.

This file is an extension runner.  It does not alter the frozen v11 result.
"""

import argparse
import json
import math
import platform
import random
import sys
from dataclasses import dataclass

import torch
import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer, DynamicCache


DEFAULT_MODEL = "allenai/OLMo-2-1124-7B-Instruct"
DEFAULT_REVISION = "470b1fba1ae01581f270116362ee4aa1b97f4c84"
BRIDGE = "History processed. Ready.\n"
NEUTRAL = "cloud stone window copper river lamp paper chair"


def example_history(mode: int, nonce: str) -> str:
    cases = (
        "0 -> 0; 1 -> 1; 0 -> 0; 1 -> 1."
        if mode == 0
        else "0 -> 1; 1 -> 0; 0 -> 1; 1 -> 0."
    )
    return f"Session {nonce}. Examples: {cases}\n"


def direct_history(mode: int, nonce: str) -> str:
    rule = "SAME" if mode == 0 else "DIFFERENT"
    return f"Session {nonce}. Direct rule: {rule}.\n"


def neutral_history(nonce: str) -> str:
    return f"Session {nonce}. Earlier material was neutral: {NEUTRAL}.\n"


def clone_cache(cache):
    out = DynamicCache()
    for i, layer in enumerate(cache.layers):
        out.update(layer.keys.clone(), layer.values.clone(), i)
    return out


def projection(base: torch.Tensor, patched: torch.Tensor, donor: torch.Tensor) -> float:
    direction = donor - base
    denominator = float(torch.dot(direction, direction))
    if not math.isfinite(denominator) or denominator <= 1e-12:
        raise RuntimeError("zero or invalid route axis")
    return float(torch.dot(patched - base, direction) / denominator)


def distance(a: torch.Tensor, b: torch.Tensor) -> float:
    value = float(torch.linalg.vector_norm(b - a))
    if not math.isfinite(value):
        raise RuntimeError("non-finite distance")
    return value


@dataclass
class Runtime:
    tokenizer: object
    model: object
    pad: int
    bridge_ids: list[int]
    max_history: int
    end: int
    patched_layers: tuple[int, ...]
    outcome_layer: int

    def cache_text(self, text: str):
        raw = self.tokenizer.encode(text, add_special_tokens=False)
        if len(raw) > self.max_history:
            raise RuntimeError("history exceeds frozen padded length")
        ids = raw + [self.pad] * (self.max_history - len(raw)) + self.bridge_ids
        mask = [1] * len(raw) + [0] * (self.max_history - len(raw)) + [1] * len(self.bridge_ids)
        with torch.inference_mode():
            output = self.model(
                input_ids=torch.tensor([ids], device="cuda"),
                attention_mask=torch.tensor([mask], dtype=torch.long, device="cuda"),
                use_cache=True,
                return_dict=True,
            )
        return output.past_key_values

    def neutralize_source(self, real_cache, neutral_cache):
        out = DynamicCache()
        for i, (real, neutral) in enumerate(zip(real_cache.layers, neutral_cache.layers)):
            keys = torch.cat(
                [neutral.keys[:, :, : self.max_history, :], real.keys[:, :, self.max_history : self.end, :]],
                dim=2,
            ).clone()
            values = torch.cat(
                [neutral.values[:, :, : self.max_history, :], real.values[:, :, self.max_history : self.end, :]],
                dim=2,
            ).clone()
            out.update(keys, values, i)
        return out

    def route_cache(self, route: str, mode: int, nonce: str):
        source = example_history(mode, nonce) if route == "examples" else direct_history(mode, nonce)
        return self.neutralize_source(self.cache_text(source), self.cache_text(neutral_history(nonce)))

    def patch_bridge(self, recipient, donor):
        out = DynamicCache()
        for i, (r, d) in enumerate(zip(recipient.layers, donor.layers)):
            keys = r.keys.clone()
            values = r.values.clone()
            if i in self.patched_layers:
                keys[:, :, self.max_history : self.end, :] = d.keys[:, :, self.max_history : self.end, :]
                values[:, :, self.max_history : self.end, :] = d.values[:, :, self.max_history : self.end, :]
            out.update(keys, values, i)
        return out

    def later(self, cache, mode: int, new_bit: int, bridge_visible: bool = True):
        rule = "SAME" if mode == 0 else "DIFFERENT"
        same_answer = new_bit
        different_answer = 1 - new_bit
        query = (
            f"Current instruction: {rule}. New bit: {new_bit}. "
            f"SAME means answer {same_answer}. DIFFERENT means answer {different_answer}. "
            "Reply only 0 or 1.\nAnswer:"
        )
        query_ids = self.tokenizer.encode(query, add_special_tokens=False)
        pos = torch.arange(self.end, self.end + len(query_ids), device="cuda")
        attention = torch.ones((1, self.end + len(query_ids)), dtype=torch.long, device="cuda")
        if not bridge_visible:
            attention[:, self.max_history : self.end] = 0
        with torch.inference_mode():
            output = self.model(
                input_ids=torch.tensor([query_ids], device="cuda"),
                past_key_values=clone_cache(cache),
                attention_mask=attention,
                position_ids=pos.unsqueeze(0),
                cache_position=pos,
                use_cache=False,
                output_hidden_states=True,
                return_dict=True,
            )
        hidden = output.hidden_states[self.outcome_layer][0, -1].float().cpu()
        logits = output.logits[0, -1].float().cpu()
        return hidden, logits


def bootstrap_mean(values: list[float], seed: int, draws: int = 10000):
    rng = random.Random(seed)
    n = len(values)
    means = []
    for _ in range(draws):
        means.append(sum(values[rng.randrange(n)] for _ in range(n)) / n)
    means.sort()
    return {
        "mean": sum(values) / n,
        "ci95": [means[int(0.025 * draws)], means[int(0.975 * draws) - 1]],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--revision", default=DEFAULT_REVISION)
    parser.add_argument("--episodes", type=int, default=256)
    parser.add_argument("--seed", type=int, default=20260828)
    parser.add_argument("--patched-layers", type=int, default=6)
    parser.add_argument("--outcome-layer", type=int, default=8)
    parser.add_argument("--chunk-size", type=int, default=32)
    args = parser.parse_args()
    if args.episodes <= 0 or args.episodes % 4:
        raise SystemExit("episodes must be a positive multiple of four")

    tokenizer = AutoTokenizer.from_pretrained(args.model, revision=args.revision)
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        revision=args.revision,
        dtype=torch.float16,
        attn_implementation="sdpa",
        low_cpu_mem_usage=True,
        device_map="cuda",
    ).eval()
    pad = tokenizer.eos_token_id
    bridge_ids = tokenizer.encode(BRIDGE, add_special_tokens=False)
    if len(bridge_ids) != 5:
        raise RuntimeError(f"bridge token count changed: {len(bridge_ids)}")

    probe = "0 0 0 0"
    lengths = [
        len(tokenizer.encode(example_history(mode, probe), add_special_tokens=False))
        for mode in (0, 1)
    ] + [
        len(tokenizer.encode(direct_history(mode, probe), add_special_tokens=False))
        for mode in (0, 1)
    ] + [len(tokenizer.encode(neutral_history(probe), add_special_tokens=False))]
    max_history = max(lengths)
    runtime = Runtime(
        tokenizer=tokenizer,
        model=model,
        pad=pad,
        bridge_ids=bridge_ids,
        max_history=max_history,
        end=max_history + len(bridge_ids),
        patched_layers=tuple(range(args.patched_layers)),
        outcome_layer=args.outcome_layer,
    )
    metadata = {
        "model": args.model,
        "revision": args.revision,
        "transformers": transformers.__version__,
        "torch": torch.__version__,
        "gpu": torch.cuda.get_device_name(0),
        "cache_type": type(runtime.cache_text(neutral_history(probe))).__name__,
        "layers": getattr(model.config, "num_hidden_layers", None),
        "hidden_size": getattr(model.config, "hidden_size", None),
        "bridge_ids": bridge_ids,
        "bridge_tokens": len(bridge_ids),
        "max_history": max_history,
        "patched_layers": list(runtime.patched_layers),
        "outcome_layer": args.outcome_layer,
        "episodes": args.episodes,
        "seed": args.seed,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
    }
    print("OLMO2_METADATA " + json.dumps(metadata, sort_keys=True), flush=True)

    rng = random.Random(args.seed)
    rows = []
    for episode in range(args.episodes):
        mode = (episode // 2) % 2
        new_bit = episode % 2
        nonce1 = " ".join(str(rng.randrange(10)) for _ in range(4))
        nonce2 = " ".join(str(rng.randrange(10)) for _ in range(4))
        examples = runtime.route_cache("examples", mode, nonce1)
        direct = runtime.route_cache("direct", mode, nonce1)
        examples_control = runtime.route_cache("examples", mode, nonce2)
        direct_control = runtime.route_cache("direct", mode, nonce2)

        h_examples, l_examples = runtime.later(examples, mode, new_bit)
        h_direct, l_direct = runtime.later(direct, mode, new_bit)
        h_ex_to_direct, l_ex_to_direct = runtime.later(runtime.patch_bridge(examples, direct), mode, new_bit)
        h_direct_to_ex, l_direct_to_ex = runtime.later(runtime.patch_bridge(direct, examples), mode, new_bit)
        h_ex_same, l_ex_same = runtime.later(runtime.patch_bridge(examples, examples_control), mode, new_bit)
        h_direct_same, l_direct_same = runtime.later(runtime.patch_bridge(direct, direct_control), mode, new_bit)
        h_examples_cut, l_examples_cut = runtime.later(examples, mode, new_bit, bridge_visible=False)
        h_direct_cut, l_direct_cut = runtime.later(direct, mode, new_bit, bridge_visible=False)

        hidden_cross = (
            projection(h_examples, h_ex_to_direct, h_direct)
            + projection(h_direct, h_direct_to_ex, h_examples)
        ) / 2
        hidden_same = (
            projection(h_examples, h_ex_same, h_direct)
            + projection(h_direct, h_direct_same, h_examples)
        ) / 2
        logit_cross = (
            projection(l_examples, l_ex_to_direct, l_direct)
            + projection(l_direct, l_direct_to_ex, l_examples)
        ) / 2
        logit_same = (
            projection(l_examples, l_ex_same, l_direct)
            + projection(l_direct, l_direct_same, l_examples)
        ) / 2
        row = {
            "episode": episode,
            "mode": mode,
            "bit": new_bit,
            "hidden_cross": hidden_cross,
            "hidden_same": hidden_same,
            "hidden_net": hidden_cross - hidden_same,
            "logit_cross": logit_cross,
            "logit_same": logit_same,
            "logit_net": logit_cross - logit_same,
            "hidden_route_distance": distance(h_examples, h_direct),
            "logit_route_distance": distance(l_examples, l_direct),
            "hidden_cut_distance": distance(h_examples_cut, h_direct_cut),
            "logit_cut_distance": distance(l_examples_cut, l_direct_cut),
        }
        rows.append(row)
        if len(rows) % args.chunk_size == 0:
            start = len(rows) - args.chunk_size
            print(
                "OLMO2_RECORDS_CHUNK "
                + json.dumps(rows[start:], separators=(",", ":"), sort_keys=True),
                flush=True,
            )

    hidden_net = [r["hidden_net"] for r in rows]
    logit_net = [r["logit_net"] for r in rows]
    hidden_cross = [r["hidden_cross"] for r in rows]
    logit_cross = [r["logit_cross"] for r in rows]
    summary = {
        **metadata,
        "status": "completed",
        "hidden_cross": bootstrap_mean(hidden_cross, args.seed + 101),
        "hidden_net": bootstrap_mean(hidden_net, args.seed + 102),
        "logit_cross": bootstrap_mean(logit_cross, args.seed + 103),
        "logit_net": bootstrap_mean(logit_net, args.seed + 104),
        "hidden_same_mean": sum(r["hidden_same"] for r in rows) / len(rows),
        "logit_same_mean": sum(r["logit_same"] for r in rows) / len(rows),
        "hidden_cut_mean": sum(r["hidden_cut_distance"] for r in rows) / len(rows),
        "logit_cut_mean": sum(r["logit_cut_distance"] for r in rows) / len(rows),
        "cross_positive_fraction_hidden": sum(x > 0 for x in hidden_net) / len(rows),
        "cross_positive_fraction_logit": sum(x > 0 for x in logit_net) / len(rows),
    }
    print("OLMO2_RESULT " + json.dumps(summary, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
