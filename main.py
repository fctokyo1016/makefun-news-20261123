#!/usr/bin/env python3
"""make.fun bounty entry: 'Sum up 23 November's world news in one image'.

Writes the bundled poster (entry.png, next to this file) to
/output/entry.png. No network, no randomness: every run writes
exactly the same bytes.
"""
import os
from pathlib import Path

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_ENTRY_BYTES = 1024 * 1024  # the competition caps the image at 1 MiB

def main() -> None:
    src = Path(__file__).resolve().parent / "entry.png"
    data = src.read_bytes()
    # Fail loudly rather than submit a broken entry: the bundled file
    # must be a real PNG within the size cap.
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("entry.png is not a PNG file")
    if len(data) > MAX_ENTRY_BYTES:
        raise ValueError(f"entry.png is {len(data)} bytes, over the 1 MiB cap")
    dst = Path("/output/entry.png")
    dst.parent.mkdir(parents=True, exist_ok=True)
    # Write via a temp file + rename so a crash mid-write can never
    # leave a truncated entry.png behind.
    tmp = dst.with_suffix(".tmp")
    tmp.write_bytes(data)
    os.replace(tmp, dst)
    print(f"wrote {dst} ({len(data)} bytes)")

if __name__ == "__main__":
    main()
