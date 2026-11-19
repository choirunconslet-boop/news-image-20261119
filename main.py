#!/usr/bin/env python3
"""Write the front-page image to the grader's output path.

The repository holds the finished image (entry.png, drawn by
render_frontpage.py in this session). This program only copies it, so it
is deterministic, needs no network, and uses only the standard library.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    shutil.copyfile(SOURCE, dest)
    # sanity check: the copy must be a whole PNG
    with open(dest, "rb") as fh:
        magic = fh.read(8)
    assert magic == b"\x89PNG\r\n\x1a\n", "entry.png is not a PNG"
    print(f"wrote {dest} ({dest.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
