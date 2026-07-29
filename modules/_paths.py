"""Centralised project-root resolution for the extractor.

Locates the project root regardless of whether the package is:
  - run from a source checkout (`python main.py` or `pip install -e .`)
  - installed into a pipx venv (where `__file__` resolves inside site-packages
    and the source is NOT in the venv tree)
  - installed into a system site-packages (same as pipx from the path-detection
    perspective)

The trick:
  1. Start from `__file__`'s directory.
  2. Walk upwards looking for a marker file (`assets/fields.txt`).
  3. If not found (typical pipx case), fall back to the pipx `direct_url.json`
     in the matching `dist-info/` directory, which records the install source.
  4. As a last resort, raise with a clear error message.
"""

from __future__ import annotations
import json
import os
import sys
from pathlib import Path

_MARKER = "assets/fields.txt"


def _find_marker(start: Path) -> Path | None:
    """Walk upwards from `start` looking for the marker; return its parent."""
    cur = start.resolve()
    for _ in range(10):  # reasonable ceiling
        if (cur / _MARKER).is_file():
            return cur
        parent = cur.parent
        if parent == cur:
            return None
        cur = parent
    return None


def _pipx_source_dir(start: Path) -> Path | None:
    """Inspect the venv's dist-info/direct_url.json to recover the original install dir."""
    # We're somewhere inside site-packages/. Walk upwards to find site-packages/
    cur = start.resolve()
    while cur != cur.parent:
        if cur.name == "site-packages":
            break
        cur = cur.parent
    else:
        return None

    # Find any dist-info/direct_url.json and parse it for a "file://" URL.
    for entry in cur.iterdir():
        if entry.name.endswith(".dist-info"):
            direct_url = entry / "direct_url.json"
            if direct_url.is_file():
                try:
                    info = json.loads(direct_url.read_text())
                except Exception:
                    continue
                url = info.get("url", "")
                if url.startswith("file://"):
                    p = Path(url[len("file://"):])
                    if p.is_dir():
                        return p.resolve()
    return None


def project_root() -> Path:
    """Return the path to the project root (where Data/, assets/, Output/ live)."""
    here = Path(__file__).parent  # modules/

    # 1. Walk up looking for the marker (works for source checkouts + editable installs)
    found = _find_marker(here)
    if found:
        return found

    # 2. pipx fallback: read install source from dist-info
    pipx_root = _pipx_source_dir(here)
    if pipx_root:
        found = _find_marker(pipx_root)
        if found:
            return found
        # Even if no marker at pipx_root, return it — caller will fail loudly.
        return pipx_root

    raise RuntimeError(
        f"Could not locate project root from {here}. "
        f"Looked for {_MARKER} walking up and via pipx dist-info."
    )


PROJECT_ROOT = project_root()
FIELDS = PROJECT_ROOT / _MARKER
ENV_FILE = PROJECT_ROOT / ".env"
OUTPUT_DIR = PROJECT_ROOT / "Output"
