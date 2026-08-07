"""Real in-memory MCP client-server harness, not a mock.

Uses `mcp.shared.memory.create_client_server_memory_streams` -- the
same in-memory transport the `mcp` SDK's own test suite uses -- paired
with a real `mcp.client.session.ClientSession` talking to this
project's actual `app` (`research_mcp.server.app`, an `MCPServer`
instance) over its actual low-level protocol handler. No part of the
MCP request/response cycle is stubbed: JSON schema generation from type
hints, request dispatch, tool invocation, and JSON-RPC content framing
are all the real library code. This is the round trip
`tools/bifp/README.md` flagged as never having been exercised when
`agent_tools.py` first shipped without a live server behind it.
"""

from __future__ import annotations

import asyncio
import json
from contextlib import asynccontextmanager

import pytest
from mcp.client.session import ClientSession
from mcp.shared.memory import create_client_server_memory_streams

from research_mcp.server import app

CALL_TIMEOUT = 15  # generous: basin_depth_demo's bootstrap resampling is the slowest tool


@asynccontextmanager
async def _live_session():
    async with create_client_server_memory_streams() as (client_streams, server_streams):
        client_read, client_write = client_streams
        server_read, server_write = server_streams

        async def run_server():
            await app._lowlevel_server.run(
                server_read, server_write,
                app._lowlevel_server.create_initialization_options(),
            )

        server_task = asyncio.create_task(run_server())
        try:
            async with ClientSession(client_read, client_write) as session:
                await asyncio.wait_for(session.initialize(), timeout=CALL_TIMEOUT)
                yield session
        finally:
            server_task.cancel()
            try:
                await server_task
            except (asyncio.CancelledError, Exception):
                pass


async def _call(tool_name: str, arguments: dict) -> dict:
    """Call a tool over a real in-memory MCP session and return its
    JSON-decoded result. Raises if the tool call itself errored at the
    protocol level (as opposed to returning an `{"error": ...}` payload,
    which every agent_tools.py function does deliberately on its own
    recoverable failures -- see each source package's agent_tools.py)."""
    async with _live_session() as session:
        result = await asyncio.wait_for(session.call_tool(tool_name, arguments), timeout=CALL_TIMEOUT)
        # NB: the constructor kwarg is the camelCase alias `isError` (see
        # the class's __init__ signature), but the actual pydantic field
        # -- and the only spelling that works for attribute access -- is
        # snake_case `is_error`. Accessing `.isError` doesn't raise at
        # call time; it's silently treated as a missing attribute by
        # pydantic's __getattr__, so this was caught by an assertion
        # actually running, not by a type checker.
        if result.is_error:
            raise RuntimeError(f"tool call {tool_name!r} errored: {result.content}")
        return json.loads(result.content[0].text)


async def _list_tool_names() -> list[str]:
    async with _live_session() as session:
        tools = await asyncio.wait_for(session.list_tools(), timeout=CALL_TIMEOUT)
        return [t.name for t in tools.tools]


@pytest.fixture
def call_tool():
    """Synchronous wrapper so test functions don't need to be async
    themselves or pull in pytest-asyncio -- each call opens its own
    fresh in-memory session (cheap; no real I/O)."""
    def _run(tool_name: str, arguments: dict) -> dict:
        return asyncio.run(_call(tool_name, arguments))
    return _run


@pytest.fixture
def list_tool_names():
    def _run() -> list[str]:
        return asyncio.run(_list_tool_names())
    return _run
