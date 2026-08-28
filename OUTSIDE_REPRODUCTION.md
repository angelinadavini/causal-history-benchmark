# Outside reproduction

CHB needs results from people who did not build the original run.

The easiest first check is the exact v11 Qwen arm. It uses the pinned model
revision, frozen seeds, frozen wording, and the archived analysis. The files
and hash check are in [`confirmatory/v11/`](confirmatory/v11/).

```bash
git clone https://github.com/angelinadavini/causal-history-benchmark.git
cd causal-history-benchmark
pip install -e ".[benchmark]"
python scripts/reproduce_v11.py
```

The command above checks the files without downloading model weights. To run
the full arm on a GPU:

```bash
python scripts/reproduce_v11.py --run --output v11-reproduction-output
```

Please report:

- model and exact revision;
- tokenizer and software versions;
- hardware;
- whether every setup check passed;
- the hidden-state and full-logit results;
- same-history control;
- bridge-cut result;
- the raw log and analysis file.

An outside result can be positive, negative, or an engineering failure. A
broken setup should be labelled as a setup failure. It should not be treated as
evidence that the history effect is absent.

If you run the test, open an issue or pull request and include the files listed
above. A short note explaining what you changed is enough.

## Copy-and-send request

> Would you be willing to run the exact Qwen v11 reproduction from the Causal
> History Benchmark repository? The run tests whether the way the same rule was
> learned earlier still changes later processing after the old source is
> removed. The repository contains the frozen runner, seeds, hashes, and
> analysis. Please report the raw log, the final analysis, the same-history
> control, and the bridge-cut result. A failed setup is useful too if the error
> is recorded clearly.
