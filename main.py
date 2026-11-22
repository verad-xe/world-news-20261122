"""Entry for make.fun "news-image-20261122": sum up the world news of
Sunday 22 November 2026 in a single image.

The picture itself (entry.png) sits beside this program: an original
illustration generated with Stable Diffusion XL on a GPU, captioned by
caption.py with the day's reported headlines.  This program's whole job
is to place those exact bytes at /output/entry.png.  It runs offline,
with the Python 3 standard library only, and writes the same bytes on
every run.

Locally:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import sys
from pathlib import Path

CAP_BYTES = 1_048_576  # the bounty's 1 MiB image cap


def main() -> None:
    os.umask(0o022)
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    source = Path(__file__).resolve().parent / "entry.png"
    target = output_dir / "entry.png"

    size = source.stat().st_size
    if size > CAP_BYTES:
        # Fail loudly rather than hand in an entry the gate would refuse.
        raise SystemExit(f"entry.png is {size} bytes, over the 1 MiB cap")

    output_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    os.chmod(target, 0o644)
    print(f"news image for 2026-11-22 written to {target} ({size} bytes)")


if __name__ == "__main__":
    sys.exit(main())
