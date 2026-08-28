from __future__ import annotations

import json
import platform

from . import __version__
from .frozen import V11_ARMS


def show_v11() -> None:
    print(json.dumps({"benchmark_version": __version__, "v11": V11_ARMS}, indent=2, sort_keys=True))


def validate_install() -> None:
    report = {"causal_history": __version__, "python": platform.python_version()}
    try:
        import torch
        report["torch"] = torch.__version__
        report["cuda_available"] = bool(torch.cuda.is_available())
    except Exception as exc:
        report["torch"] = None
        report["torch_error"] = str(exc)
    try:
        import transformers
        report["transformers"] = transformers.__version__
    except Exception as exc:
        report["transformers"] = None
        report["transformers_error"] = str(exc)
    print(json.dumps(report, indent=2, sort_keys=True))
