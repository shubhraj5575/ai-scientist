"""Utility helpers: timing, memory, environment capture, digests."""
from __future__ import annotations

import hashlib
import json
import os
import platform
import resource
import subprocess
import time
from pathlib import Path
from typing import Any

import numpy as np


def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()) + "Z"


def perf_timer():
    """Context-free timer: call t0=perf_timer() ... elapsed=t0()."""
    t0 = time.perf_counter()
    return lambda: time.perf_counter() - t0


def peak_rss_mb() -> float:
    """Peak resident set size in MB for this process (macOS: bytes, Linux: KB)."""
    ru = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if platform.system() == "Darwin":
        return ru / (1024 * 1024)
    return ru / 1024


def git_commit(repo: Path) -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True, check=True
        )
        return out.stdout.strip()
    except Exception:
        return "unknown"


def env_snapshot(extra: dict[str, Any] | None = None) -> dict:
    snap = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "hostname": platform.node(),
        "numpy": np.__version__,
        "cpu_count": os.cpu_count(),
        "peak_rss_mb_at_capture": round(peak_rss_mb(), 1),
    }
    if extra:
        snap.update(extra)
    return snap


def stable_digest(obj: Any) -> str:
    """Deterministic SHA256 of any JSON-serialisable object or ndarray."""
    h = hashlib.sha256()
    if isinstance(obj, np.ndarray):
        h.update(obj.tobytes())
        h.update(str(obj.dtype).encode())
        h.update(str(obj.shape).encode())
    else:
        h.update(json.dumps(obj, sort_keys=True, default=str).encode())
    return h.hexdigest()


def json_dumps_compact(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)


def set_global_seed(seed: int) -> np.random.Generator:
    """Return a dedicated Generator; callers pass rng explicitly (no hidden state)."""
    return np.random.default_rng(seed)
