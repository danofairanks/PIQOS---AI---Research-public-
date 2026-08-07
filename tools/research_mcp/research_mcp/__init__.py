"""MCP server wiring for basin_depth, bifp, and attractor_scan.

See server.py for the tool registration and README.md for install and
usage. This package deliberately contains no research logic of its own
-- it is a thin transport layer over three sibling packages' own
agent_tools.py surfaces.
"""

from .server import app

__all__ = ["app"]

__version__ = "0.1.0"
