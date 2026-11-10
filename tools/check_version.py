#!/usr/bin/env python3
"""Assert that the pushed tag matches the version in Cargo.toml.

Run in CI on tag pushes (GITHUB_REF=refs/tags/X.Y.Z). The release tag is the
single source of truth for the published version; this check ensures the
hand-maintained Cargo.toml version agrees with it before artifacts are built
and published.
"""

import os
import re
import sys
from pathlib import Path

CARGO_TOML = Path(__file__).resolve().parent.parent / "Cargo.toml"
def main() -> int:
    """Check that the pushed tag matches the Cargo.toml package version."""
    ref = os.getenv("GITHUB_REF", "")
    tag = re.sub(r"^refs/tags/", "", ref)
    if not tag or tag == ref:
        print(f'✖ GITHUB_REF "{ref}" is not a tag ref')
        return 1

    match = re.search(
        r'^version = "(.+)"', CARGO_TOML.read_text(), flags=re.MULTILINE
    )
    if not match:
        print(f"✖ no version field found in {CARGO_TOML}")
        return 1

    cargo_version = match.group(1)
    if cargo_version == tag:
        print(f"✓ tag matches {CARGO_TOML} version {cargo_version!r}")
        return 0

    print(f"✖ tag {tag!r} does not match {CARGO_TOML} version {cargo_version!r}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
