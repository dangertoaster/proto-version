"""Prototype package for the hand-maintained versioning scheme."""

import importlib.metadata

from ._rs import hello

# Read the version from the installed package metadata so it always matches
# what pip reports verbatim.
__version__ = importlib.metadata.version("proto-parts")

__all__ = ["__version__", "hello"]
