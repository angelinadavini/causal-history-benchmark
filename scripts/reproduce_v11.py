#!/usr/bin/env python3
"""Verify and run the public v11 reproduction package.

The frozen experiment is kept in the downloadable packages under
``confirmatory/v11``.  This helper checks the manifest locks and the file
hashes before it runs anything.  It never changes the frozen files.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_DIR = ROOT / "confirmatory" / "v11"
BASE_LOCK = "fb42c0f7e984c8e775b55960eb5c7f9be02d6eff8944bcdb198223435764a7d2"
SECONDARY_LOCK = "570f3119f16b32942c0bae5fdbdeb8396311a76c3bb8fed1b6eea577fc69cb54"


def canonical_manifest_hash(path: Path) -> str:
    data = json.loads(path.read_text(encoding="utf-8"))
    declared = data.pop("manifest_sha256", None)
    canonical = json.dumps(data, sort_keys=True, separators=(",", ":")).encode()
    actual = hashlib.sha256(canonical).hexdigest()
    if actual != declared:
        raise RuntimeError(f"manifest hash mismatch: {path} ({actual} != {declared})")
    return actual


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_tree(root: Path) -> None:
    base = root / "base" / "CONFIRMATORY_SEED_MANIFEST_v2.json"
    secondary = root / "secondary" / "CONFIRMATORY_SECONDARY_SEED_MANIFEST_v2_1.json"
    if canonical_manifest_hash(base) != BASE_LOCK:
        raise RuntimeError("base v2 manifest lock does not match the frozen lock")
    if canonical_manifest_hash(secondary) != SECONDARY_LOCK:
        raise RuntimeError("secondary v2.1 manifest lock does not match the frozen lock")

    base_data = json.loads(base.read_text(encoding="utf-8"))
    for field, relative in {
        "protocol_sha256": "base/CONFIRMATORY_PROTOCOL_v2.md",
        "runner_sha256": "base/confirmatory_runner.py",
        "analysis_sha256": "base/analyse_confirmatory.py",
        "requirements_sha256": "base/requirements-confirmatory.txt",
    }.items():
        actual = file_hash(root / relative)
        if actual != base_data[field]:
            raise RuntimeError(f"base {field} mismatch: {actual} != {base_data[field]}")

    secondary_data = json.loads(secondary.read_text(encoding="utf-8"))
    for field, relative in {
        "protocol_sha256": "secondary/SECONDARY_AMENDMENT_PROTOCOL_v2_1.md",
        "runner_sha256": "secondary/confirmatory_secondary_runner_v2_1.py",
        "analysis_sha256": "secondary/analyse_confirmatory_v2_1.py",
        "requirements_sha256": "secondary/requirements-confirmatory.txt",
    }.items():
        actual = file_hash(root / relative)
        if actual != secondary_data[field]:
            raise RuntimeError(
                f"secondary {field} mismatch: {actual} != {secondary_data[field]}"
            )
    print("Frozen v2 and v2.1 locks and file hashes verified.")


def extract_packages(destination: Path) -> Path:
    base_zip = PACKAGE_DIR / "AI_Consciousness_Confirmatory_Freeze_v2.zip"
    secondary_zip = PACKAGE_DIR / "AI_Consciousness_Confirmatory_Secondary_Amendment_v2_1.zip"
    if not base_zip.exists() or not secondary_zip.exists():
        raise FileNotFoundError("the frozen v11 packages are missing from confirmatory/v11")
    base_root = destination / "base"
    secondary_root = destination / "secondary"
    base_root.mkdir(parents=True)
    secondary_root.mkdir(parents=True)
    with zipfile.ZipFile(base_zip) as archive:
        archive.extractall(base_root)
    with zipfile.ZipFile(secondary_zip) as archive:
        archive.extractall(secondary_root)
    # The archives have one top-level folder each.
    base_folder = next(base_root.iterdir())
    secondary_folder = next(secondary_root.iterdir())
    normalized = destination / "normalized"
    (normalized / "base").mkdir(parents=True)
    (normalized / "secondary").mkdir(parents=True)
    for source in base_folder.iterdir():
        source.rename(normalized / "base" / source.name)
    for source in secondary_folder.iterdir():
        source.rename(normalized / "secondary" / source.name)
    return normalized


def run(args: argparse.Namespace) -> None:
    with tempfile.TemporaryDirectory(prefix="chb-v11-") as temporary:
        extracted = extract_packages(Path(temporary))
        verify_tree(extracted)
        if not args.run:
            print("Verification complete. Add --run to execute the frozen runners.")
            return
        output = Path(args.output).resolve()
        output.mkdir(parents=True, exist_ok=True)
        base = extracted / "base"
        secondary = extracted / "secondary"
        manifest = base / "CONFIRMATORY_SEED_MANIFEST_v2.json"
        secondary_manifest = secondary / "CONFIRMATORY_SECONDARY_SEED_MANIFEST_v2_1.json"
        commands = {
            "qwen_primary": ["qwen_primary", str(manifest)],
            "mistral_replication": ["mistral_replication", str(manifest)],
            "qwen_secondary": ["qwen_secondary", str(secondary_manifest)],
        }
        for arm, (name, seed_manifest) in commands.items():
            runner = base / "confirmatory_runner.py" if arm != "qwen_secondary" else secondary / "confirmatory_secondary_runner_v2_1.py"
            log_path = output / f"{arm}.log"
            with log_path.open("w", encoding="utf-8") as log:
                subprocess.run(
                    [sys.executable, str(runner), "--arm", name, "--seed-manifest", seed_manifest],
                    stdout=log,
                    stderr=subprocess.STDOUT,
                    check=True,
                )
        analysis = output / "confirmatory_analysis_v2_1.json"
        subprocess.run(
            [
                sys.executable,
                str(secondary / "analyse_confirmatory_v2_1.py"),
                str(output / "qwen_primary.log"),
                str(output / "mistral_replication.log"),
                str(output / "qwen_secondary.log"),
                "--base-seed-manifest",
                str(manifest),
                "--secondary-seed-manifest",
                str(secondary_manifest),
                "--output",
                str(analysis),
            ],
            check=True,
        )
        print(f"Analysis written to {analysis}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true", help="run the frozen model jobs after verification")
    parser.add_argument("--output", default="v11-reproduction-output", help="directory for logs and analysis")
    run(parser.parse_args())


if __name__ == "__main__":
    main()
