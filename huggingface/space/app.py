import gradio as gr

RESULTS = [
    ["Qwen2.5-3B-Instruct", "SAME/DIFFERENT", 512, "0.68747 [0.68661, 0.68832]", "0.25833 [0.25555, 0.26109]", "0"],
    ["Mistral-7B-Instruct-v0.3", "SAME/DIFFERENT", 256, "0.80099 [0.79955, 0.80245]", "0.05865 [0.05681, 0.06056]", "0"],
    ["Qwen2.5-3B-Instruct", "DAX/WUG", 256, "0.60515 [0.60352, 0.60679]", "0.04717 [0.04335, 0.05106]", "0"],
]

EXTENSION_RESULTS = [
    ["OLMo-2-1124-7B-Instruct", "SAME/DIFFERENT", 256, "0.58722 [0.58430, 0.59009]", "0.03286 [-0.03762, 0.10720]", "0"],
]

with gr.Blocks(title="Causal History Benchmark") as demo:
    gr.Markdown(
        """
# Causal History Benchmark

**If a model has the same rule in front of it now, can the way it learned that rule earlier still change what it does next?**

That is what CHB tests.

The model learns the same rule from examples or from a direct instruction. The original teaching state is removed. The same rule is supplied again. We move the stored bridge state between the two learning histories and measure what changes later.

The confirmed result is simple: **how the rule was learned earlier still changed the later computation. Moving the stored history state moved the later hidden state and full next-token output. Blocking access to the bridge removed the measured difference.**
"""
    )

    gr.Dataframe(
        headers=[
            "Model",
            "Task",
            "Episodes",
            "Hidden-state movement",
            "Full-logit movement",
            "Distance after bridge cut",
        ],
        value=RESULTS,
        interactive=False,
        label="Frozen v11 results",
    )

    gr.Markdown("## Separate OLMo-2 extension\n\nThe hidden-state endpoint was positive. The full-logit interval includes zero, so it is recorded as inconclusive. This extension does not change the frozen v11 results.")
    gr.Dataframe(
        headers=[
            "Model",
            "Task",
            "Episodes",
            "Hidden-state movement",
            "Full-logit movement",
            "Distance after bridge cut",
        ],
        value=EXTENSION_RESULTS,
        interactive=False,
        label="Separate extension result",
    )

    gr.Markdown(
        """
## Run it yourself

```bash
git clone https://github.com/angelinadavini/causal-history-benchmark.git
cd causal-history-benchmark
pip install -e ".[benchmark,test]"
python scripts/run_benchmark.py --model Qwen/Qwen2.5-3B-Instruct --reps 16
```

**GitHub:** https://github.com/angelinadavini/causal-history-benchmark

The benchmark is public so other researchers can test more models, add clean negative results, change the intervention, and see where the effect does or does not hold.

**Author:** Angelina Davini Hintsanen
"""
    )

if __name__ == "__main__":
    demo.launch()
