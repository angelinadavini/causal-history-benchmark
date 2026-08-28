#!/usr/bin/env python3
"""Reference causal-history interchange experiment.

Development reference implementation for Qwen2.5-3B-Instruct.

The experiment compares two acquisition routes for the same SAME/DIFFERENT
rule. The original source-prefix K/V state is replaced with neutral state.
The fixed bridge keeps its route-conditioned K/V state. The current rule is
supplied again during the later event.

Cross-route bridge K/V is then transplanted and the later hidden state is
measured along the paired route axis. Same-route swaps are the primary control.

This script is provided for transparency. Confirmatory benchmark scripts will
use frozen seeds, templates, model revisions, and analysis choices.
"""

import argparse
import json
import random
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, DynamicCache

BRIDGE = "History processed. Ready.\n"


def example_history(mode: int, nonce: str) -> str:
    cases = (
        "0 gives 0, 1 gives 1, 0 gives 0, 1 gives 1."
        if mode == 0
        else "0 gives 1, 1 gives 0, 0 gives 1, 1 gives 0."
    )
    return f"Session {nonce}. Demonstrations: {cases}\n"


def explicit_history(mode: int, nonce: str) -> str:
    rule = "SAME" if mode == 0 else "DIFFERENT"
    return f"Session {nonce}. Stated instruction: {rule}.\n"


def neutral_history(nonce: str) -> str:
    return (
        f"Session {nonce}. Earlier material was neutral: "
        "cloud stone window copper river lamp paper chair.\n"
    )


def clone_cache(cache):
    out = DynamicCache()
    for i, layer in enumerate(cache.layers):
        out.update(layer.keys.clone(), layer.values.clone(), i)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen2.5-3B-Instruct")
    ap.add_argument("--reps", type=int, default=16)
    ap.add_argument("--seed", type=int, default=2026082752)
    ap.add_argument("--patched-layers", type=int, default=6,
                    help="Patch bridge K/V in layers 0..N-1")
    ap.add_argument("--outcome-layer", type=int, default=8)
    args = ap.parse_args()

    rng = random.Random(args.seed)
    tok = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        dtype=torch.float16,
        attn_implementation="sdpa",
    ).cuda().eval()

    pad = tok.eos_token_id
    bridge_ids = tok.encode(BRIDGE, add_special_tokens=False)

    candidates = []
    for mode in (0, 1):
        for fn in (example_history, explicit_history):
            candidates.append(len(tok.encode(fn(mode, "0 0 0 0"), add_special_tokens=False)))
    candidates.append(len(tok.encode(neutral_history("0 0 0 0"), add_special_tokens=False)))
    max_history = max(candidates)
    end = max_history + len(bridge_ids)

    def run_prefix(text):
        hist = tok.encode(text, add_special_tokens=False)
        filler = [pad] * (max_history - len(hist))
        ids = hist + filler + bridge_ids
        mask = [1] * len(hist) + [0] * len(filler) + [1] * len(bridge_ids)
        with torch.inference_mode():
            return model(
                input_ids=torch.tensor([ids], device="cuda"),
                attention_mask=torch.tensor([mask], device="cuda"),
                use_cache=True,
                return_dict=True,
            ).past_key_values

    def neutralize_source(real_cache, neutral_cache):
        out = DynamicCache()
        for i, (real, neutral) in enumerate(zip(real_cache.layers, neutral_cache.layers)):
            keys = torch.cat([
                neutral.keys[:, :, :max_history, :],
                real.keys[:, :, max_history:end, :],
            ], dim=2).clone()
            values = torch.cat([
                neutral.values[:, :, :max_history, :],
                real.values[:, :, max_history:end, :],
            ], dim=2).clone()
            out.update(keys, values, i)
        return out

    def route_cache(route, mode, nonce):
        source = example_history(mode, nonce) if route == "examples" else explicit_history(mode, nonce)
        return neutralize_source(run_prefix(source), run_prefix(neutral_history(nonce)))

    def patch_bridge(recipient, donor):
        out = DynamicCache()
        selected = set(range(args.patched_layers))
        for i, (r, d) in enumerate(zip(recipient.layers, donor.layers)):
            keys = r.keys.clone()
            values = r.values.clone()
            if i in selected:
                keys[:, :, max_history:end, :] = d.keys[:, :, max_history:end, :]
                values[:, :, max_history:end, :] = d.values[:, :, max_history:end, :]
            out.update(keys, values, i)
        return out

    def later_state(cache, mode, new_bit):
        rule = "SAME" if mode == 0 else "DIFFERENT"
        target_same = new_bit
        target_diff = 1 - new_bit
        query = (
            f"Current instruction: {rule}. New bit: {new_bit}. "
            f"SAME means answer {target_same}. DIFFERENT means answer {target_diff}. "
            "Reply only 0 or 1.\nAnswer:"
        )
        qids = tok.encode(query, add_special_tokens=False)
        pos = torch.arange(end, end + len(qids), device="cuda")
        mask = torch.ones((1, end + len(qids)), dtype=torch.long, device="cuda")
        with torch.inference_mode():
            out = model(
                input_ids=torch.tensor([qids], device="cuda"),
                past_key_values=clone_cache(cache),
                attention_mask=mask,
                position_ids=pos.unsqueeze(0),
                cache_position=pos,
                use_cache=False,
                output_hidden_states=True,
                return_dict=True,
            )
        return out.hidden_states[args.outcome_layer][0, -1].float().cpu()

    def projection(base, patched, donor):
        direction = donor - base
        return float(torch.dot(patched - base, direction) / (torch.dot(direction, direction) + 1e-9))

    rows = []
    for mode in (0, 1):
        for new_bit in (0, 1):
            for _ in range(args.reps):
                nonce1 = " ".join(str(rng.randrange(10)) for _ in range(4))
                nonce2 = " ".join(str(rng.randrange(10)) for _ in range(4))

                ex = route_cache("examples", mode, nonce1)
                direct = route_cache("explicit", mode, nonce1)
                ex_control = route_cache("examples", mode, nonce2)
                direct_control = route_cache("explicit", mode, nonce2)

                y_ex = later_state(ex, mode, new_bit)
                y_direct = later_state(direct, mode, new_bit)

                ex_to_direct = later_state(patch_bridge(ex, direct), mode, new_bit)
                direct_to_ex = later_state(patch_bridge(direct, ex), mode, new_bit)
                ex_same = later_state(patch_bridge(ex, ex_control), mode, new_bit)
                direct_same = later_state(patch_bridge(direct, direct_control), mode, new_bit)

                cross = (
                    projection(y_ex, ex_to_direct, y_direct)
                    + projection(y_direct, direct_to_ex, y_ex)
                ) / 2
                same = (
                    projection(y_ex, ex_same, y_direct)
                    + projection(y_direct, direct_same, y_ex)
                ) / 2
                rows.append({"cross": cross, "same": same})

    mean_cross = sum(r["cross"] for r in rows) / len(rows)
    mean_same = sum(r["same"] for r in rows) / len(rows)
    result = {
        "model": args.model,
        "n_pairs": len(rows),
        "bridge_tokens": len(bridge_ids),
        "patched_layers": list(range(args.patched_layers)),
        "outcome_layer": args.outcome_layer,
        "cross_projection_mean": mean_cross,
        "same_route_control_mean": mean_same,
        "cross_positive_fraction": sum(r["cross"] > 0 for r in rows) / len(rows),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
