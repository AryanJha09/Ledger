"""Config-driven, resumable experiment runner.

    python -m ledger2.runner --config configs/main.yaml

For every (model, domain, prompt, case, sample) it stores one JSON line with
the full raw response, parse status, generation options, model digest,
Ollama version, hardware and code revision. Re-running the same command
skips records that already exist, so an interrupted run can be resumed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import yaml

from . import dataset as ds
from .domains import get_domain
from .ollama_client import OllamaClient
from .parsing import parse
from .prompts import render


def _git_rev() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True,
                                       stderr=subprocess.DEVNULL).strip()
    except Exception:
        return "unknown"


def hardware() -> dict:
    info = {"platform": platform.platform(), "machine": platform.machine(),
            "processor": platform.processor(), "python": platform.python_version()}
    try:
        gpu = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader"],
            text=True, stderr=subprocess.DEVNULL, timeout=10).strip()
        info["gpu"] = gpu
    except Exception:
        info["gpu"] = None
    return info


def _sha(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def _existing_ids(path: Path) -> set:
    if not path.exists():
        return set()
    with path.open(encoding="utf-8") as f:
        return {json.loads(line)["run_id"] for line in f if line.strip()}


def run(config_path: Path, dry_run: bool = False, limit: int | None = None):
    cfg = yaml.safe_load(Path(config_path).read_text())
    out_dir = Path(cfg["output_dir"])
    out_dir.mkdir(parents=True, exist_ok=True)
    client = None if dry_run else OllamaClient(timeout=cfg.get("timeout_seconds", 300))
    env = {
        "ollama_version": None if dry_run else client.version(),
        "hardware": hardware(),
        "code_revision": _git_rev(),
        "config_file": str(config_path),
        "config_sha": _sha(Path(config_path).read_text()),
    }
    (out_dir / "environment.json").write_text(json.dumps(env, indent=2))

    # Datasets are generated deterministically and stored next to the logs.
    datasets = {}
    for d in cfg["domains"]:
        cases = ds.build(d["key"], d["n_per_condition"], cfg["dataset_seed"])
        h = ds.write(cases, out_dir / "datasets" / f"{d['key']}.jsonl")
        seeds = d.get("seeds", cfg["sampling"]["seeds"])
        datasets[d["key"]] = (cases, d.get("prompts", cfg["prompts"]), h, seeds)

    n_done = 0
    for m in cfg["models"]:
        info = {"tag": m["tag"]} if dry_run else client.model_info(m["tag"])
        if m.get("digest") and info.get("digest") and not info["digest"].startswith(m["digest"]):
            raise SystemExit(f"{m['key']}: local digest {info['digest']} != pinned {m['digest']}")
        for dkey, (cases, prompt_ids, dhash, seeds) in datasets.items():
            domain = get_domain(dkey)
            for pid in prompt_ids:
                path = out_dir / "runs" / m["key"] / dkey / f"{pid}.jsonl"
                path.parent.mkdir(parents=True, exist_ok=True)
                done = _existing_ids(path)
                with path.open("a", encoding="utf-8") as f:
                    for case in cases:
                        for s, seed in enumerate(seeds):
                            # Seeds and dataset hash are part of the key, so a changed
                            # config never silently reuses records from an old one.
                            run_id = (f"{m['key']}|{dkey}|{pid}|{case['case_id']}|s{s}"
                                      f"|seed{seed}|d{dhash[:12]}")
                            if run_id in done:
                                continue
                            prompt = render(pid, domain, case["input"])
                            options = dict(cfg["sampling"]["options"], seed=seed)
                            if dry_run:
                                gen = {"response": "", "thinking": None}
                            else:
                                try:
                                    gen = client.generate(m["tag"], prompt, options,
                                                          json_mode=cfg.get("json_mode", False),
                                                          think=m.get("think"))
                                except Exception as e:  # network/tooling error, kept separate
                                    gen = {"response": None, "error": repr(e)}
                            p = parse(gen.get("response"), set(domain.decisions))
                            rec = {
                                "run_id": run_id,
                                "model_key": m["key"],
                                "model": info,
                                "domain": dkey,
                                "dataset_sha256": dhash,
                                "prompt_id": pid,
                                "prompt_sha": _sha(prompt),
                                "case_id": case["case_id"],
                                "condition": case["condition"],
                                "input": case["input"],
                                "normative_action": case["normative_action"],
                                "warning_signs": case["warning_signs"],
                                "sample_index": s,
                                "options": options,
                                "json_mode": cfg.get("json_mode", False),
                                "generation": gen,
                                "parse_status": p.status,
                                "parse_repaired": p.repaired,
                                "parse_errors": p.errors,
                                "output": p.data,
                                "reasoning_text": p.reasoning or gen.get("thinking"),
                                "timestamp": datetime.now(timezone.utc).isoformat(),
                            }
                            f.write(json.dumps(rec) + "\n")
                            f.flush()
                            n_done += 1
                            if limit and n_done >= limit:
                                return n_done
    return n_done


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", type=Path, required=True)
    p.add_argument("--dry-run", action="store_true", help="build datasets and records without calling models")
    p.add_argument("--limit", type=int, default=None)
    a = p.parse_args(argv)
    n = run(a.config, a.dry_run, a.limit)
    print(f"wrote {n} new records")


if __name__ == "__main__":
    main()
