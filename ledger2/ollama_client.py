"""Minimal Ollama HTTP client that records everything needed to reproduce a run.

Uses only the documented REST endpoints (/api/version, /api/tags, /api/show,
/api/generate). The host is taken from OLLAMA_HOST (default
http://localhost:11434; inside docker compose it is http://ollama:11434).
"""
from __future__ import annotations

import os
import time
from typing import Optional

import requests


class OllamaClient:
    def __init__(self, host: Optional[str] = None, timeout: float = 300.0):
        host = host or os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        if not host.startswith("http"):
            host = "http://" + host
        self.host = host.rstrip("/")
        self.timeout = timeout

    def _post(self, path, payload):
        r = requests.post(self.host + path, json=payload, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def version(self) -> str:
        r = requests.get(self.host + "/api/version", timeout=30)
        r.raise_for_status()
        return r.json().get("version", "unknown")

    def model_info(self, model: str) -> dict:
        """Digest, size, quantization and family of a local model tag."""
        tags = requests.get(self.host + "/api/tags", timeout=30).json().get("models", [])
        entry = next((m for m in tags if m.get("name") == model or m.get("model") == model), {})
        show = self._post("/api/show", {"model": model})
        details = show.get("details", {}) or entry.get("details", {})
        return {
            "tag": model,
            "digest": entry.get("digest"),
            "size_bytes": entry.get("size"),
            "modified_at": entry.get("modified_at"),
            "family": details.get("family"),
            "parameter_size": details.get("parameter_size"),
            "quantization_level": details.get("quantization_level"),
            "format": details.get("format"),
        }

    def pull(self, model: str):
        return self._post("/api/pull", {"model": model, "stream": False})

    def generate(self, model: str, prompt: str, options: dict, json_mode: bool = True,
                 think: Optional[bool] = None) -> dict:
        payload = {"model": model, "prompt": prompt, "stream": False, "options": options}
        if json_mode:
            payload["format"] = "json"
        if think is not None:
            payload["think"] = think
        t0 = time.time()
        out = self._post("/api/generate", payload)
        return {
            "response": out.get("response", ""),
            "thinking": out.get("thinking"),
            "done_reason": out.get("done_reason"),
            "prompt_eval_count": out.get("prompt_eval_count"),
            "eval_count": out.get("eval_count"),
            "total_duration_ns": out.get("total_duration"),
            "wall_seconds": round(time.time() - t0, 3),
        }
