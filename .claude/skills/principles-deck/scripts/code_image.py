#!/usr/bin/env python3
"""
code_image.py - render a code snippet to a syntax-highlighted PNG via Carbon.

House standard: every code snippet in a deck goes through this, so all of them
share one theme, one font and one set of proportions. Flat monospace text on a
dark rectangle is not acceptable for code - highlighting is what makes a snippet
readable at a glance on a projector.

Requires the Carbon CLI once:

    npm install -g carbon-now-cli

Use from a build script:

    from code_image import code_image
    png, ratio = code_image('''
    import tiktoken
    enc = tiktoken.get_encoding("o200k_base")
    ''', out_dir=ASSETS, name="tiktoken")
    picture(s, png, 0.34, 1.56, 5.60, ratio=ratio)

Or from the terminal:

    python3 code_image.py snippet.py out/ my-snippet

Renders are cached by a hash of the code and settings, so rebuilding a deck
costs nothing unless the snippet actually changed.
"""
from __future__ import annotations

import hashlib
import json
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

# House Carbon settings. Source Code Pro is the deck's own body font, so code and
# copy share a typeface; the card sits on a transparent ground with no window
# chrome, no traffic lights and no shadow, matching the vector mocks.
SETTINGS = {
    "theme": "one-dark",
    "backgroundColor": "rgba(0,0,0,0)",
    "windowTheme": "none",
    "windowControls": False,
    "dropShadow": False,
    "fontFamily": "Source Code Pro",
    "fontSize": "15px",
    "lineNumbers": False,
    # No padding around the card: the PNG edge IS the card edge, so a code image
    # lines up with the mock panels beside it instead of floating inset.
    "paddingVertical": "0px",
    "paddingHorizontal": "0px",
    "exportSize": "3x",          # crisp when projected
    "language": "python",
}


def png_ratio(path: Path) -> float:
    """Width / height of a PNG, so callers can size the picture correctly."""
    head = path.read_bytes()[:33]
    w, h = struct.unpack(">II", head[16:24])
    return w / h


def code_image(code: str, out_dir: Path | str, name: str,
               language: str = "python", **overrides) -> tuple[Path, float]:
    """Render `code` to `<out_dir>/<name>.png` and return (path, aspect ratio)."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    png = out_dir / f"{name}.png"

    settings = {**SETTINGS, "language": language, **overrides}
    code = code.strip("\n")
    stamp = hashlib.sha256(
        (code + json.dumps(settings, sort_keys=True)).encode()).hexdigest()[:16]
    marker = out_dir / f".{name}.hash"

    if png.exists() and marker.exists() and marker.read_text().strip() == stamp:
        return png, png_ratio(png)          # unchanged - reuse

    ext = {"python": ".py", "javascript": ".js", "bash": ".sh"}.get(language, ".txt")
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / f"snippet{ext}"
        src.write_text(code + "\n")
        subprocess.run(
            ["carbon-now", str(src), "--save-to", str(out_dir), "--save-as", name,
             "--skip-display", "--settings", json.dumps(settings)],
            check=True, capture_output=True, text=True,
        )
    if not png.exists():
        raise RuntimeError(f"carbon-now produced no image at {png}")
    marker.write_text(stamp)
    return png, png_ratio(png)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit("usage: code_image.py <snippet-file> <out-dir> <name> [language]")
    src = Path(sys.argv[1])
    lang = sys.argv[4] if len(sys.argv) > 4 else "python"
    p, r = code_image(src.read_text(), sys.argv[2], sys.argv[3], language=lang)
    print(f"{p}  ratio {r:.3f}")
