# research-mcp

A live MCP (Model Context Protocol) server exposing
[`basin_depth`](../basin_depth/), [`bifp`](../bifp/),
[`attractor_scan`](../attractor_scan/), [`debasinizer`](../debasinizer/),
and [`paper_rigor`](../paper_rigor/) as agent tool calls. This is pure
wiring — every tool here is an unmodified function imported from its
source package's own `agent_tools.py`, registered against a real
`MCPServer` instance and round-trip tested over the actual MCP wire
protocol (in-memory transport, not a mock).

`bifp/README.md` originally noted that its `agent_tools.py` surface
was designed for MCP but never shipped as a live server, because
`pip install mcp` conflicted with this build environment's system
`PyJWT` package. That blocker is resolved here the straightforward
way: install into an isolated virtualenv rather than the system
interpreter — see "Install" below. `mcp` (2.0.0 at the time of
writing) installs cleanly in a fresh venv with no conflict.

## Install

```bash
cd tools/research_mcp
python3 -m venv .venv
source .venv/bin/activate

# the wrapped packages aren't on PyPI -- install them from source first.
# verification_lint isn't wrapped as its own MCP tool (see below) but
# paper_rigor imports its disclaimer check directly, so it's a real
# install-time dependency here too.
pip install -e ../basin_depth -e ../bifp -e ../attractor_scan -e ../verification_lint -e ../debasinizer -e ../paper_rigor

pip install -e .
pip install -e ".[dev]"   # adds pytest
```

Requires Python >= 3.10 and `mcp>=1.2.0`. This package's own runtime
dependency footprint is just `mcp` — no new dependency is introduced
by the wrapped tools beyond what they already require.

## What's registered

All 19 functions across the five packages' `agent_tools.py` modules,
unchanged:

| Tool | From | Purpose |
|---|---|---|
| `basin_depth_demo` | basin_depth | Run the Noether-Temporal Coherence pipeline against the bundled synthetic corpus |
| `basin_depth_run` | basin_depth | Run the full pipeline against a caller-supplied corpus |
| `basin_depth_derive_vocab` | basin_depth | Empirically derive claim/immune/neutral vocabulary pools from a corpus |
| `bifp_list_phases` | bifp | Full BIFP Phase 0-6 schema |
| `bifp_start_audit` | bifp | Create a new persisted audit session |
| `bifp_record_criterion` | bifp | Record one criterion's pass/fail |
| `bifp_scan_text` | bifp | Standalone heuristic scan (no audit required) |
| `bifp_attach_scan_to_audit` | bifp | Same, attached to an existing audit's record |
| `bifp_get_status` | bifp | Phase-by-phase status + overall resolution |
| `bifp_generate_report` | bifp | Render the full markdown report |
| `bifp_judge_rebuttal` | bifp | **Calls Groq.** One candidate read on whether a rebuttal addresses a claim (BIFP §3.7) as actually made, or a weaker substitute — advisory only, never calls `record()`; see bifp/README.md for why this doesn't conflict with §3.9's `no_ai_as_judge`. Requires `GROQ_API_KEY`. |
| `bifp_attach_rebuttal_judgment` | bifp | Same, attached to an existing audit's `ai_advisory_flags` rather than returned standalone |
| `attractor_scan_text` | attractor_scan | Classify a single text for maneuvers + laundering cases |
| `attractor_scan_corpus` | attractor_scan | Aggregate category frequency across a corpus |
| `attractor_scan_judge_visual_proof` | attractor_scan | **Calls Groq (vision).** One candidate read on a single image + claim pair: does the image's genuine technical content support the claim, or is it connected only by wordplay (§2.8 Case 6)? Single-specimen only — never wired into `attractor_scan_corpus`; a corpus-wide version would be exactly the "unearned precision" mistake the package's own README argues against. Requires `GROQ_API_KEY`. |
| `debasinizer_scan_text` | debasinizer | Classify a single text for the resonance-vocabulary register (2+ categories co-occurring) and self-coherence-assertion phrasing |
| `debasinizer_scan_corpus` | debasinizer | Aggregate flag frequency across a corpus |
| `paper_rigor_scan` | paper_rigor | Scan any paper for placeholders, falsifiability, self-citation, credentialing, consensus claims, citation-type mix, a claimed-citability-with-zero-references contradiction, and a missing limitations section — returns an `external_verification_worklist` naming the specific items that need a real web search/fetch to resolve |
| `paper_rigor_triage_worklist` | paper_rigor | **Calls Groq.** Takes an existing `external_verification_worklist` (pass `paper_rigor_scan`'s own output straight through) and attaches a Groq-generated `priority` + `suggested_check` to each item — advisory triage, not verification; never adds, removes, or resolves items. Requires `GROQ_API_KEY`. Empty worklist short-circuits with no API call. |

**Three of these 19 tools call Groq and require `GROQ_API_KEY`** —
every other tool is pure local computation with no network access at
all. All three share the same contract: advisory-only, never a
verdict, and each returns `{"error": ...}` rather than failing the
tool call itself if the key is missing or the API call fails. If
you're running this server yourself, set `GROQ_API_KEY` in the
environment before starting it for those three; the other 16 work
with no setup beyond installation.

Each tool's docstring (visible to an MCP client as its description)
and type hints (used to generate its JSON input schema) come straight
from the source package — see each package's own `agent_tools.py` and
README for exactly what each function does and does not detect.
`case_scaffold` is not wrapped here: it's a repository-maintenance tool
(generate/lint/index this repo's own `case_studies/` files) rather
than a research-measurement tool an external agent would call against
arbitrary input — a narrower fit for MCP exposure. Wiring it in later
is the same mechanical pattern as the five here. `verification_lint`
is installed (paper_rigor depends on its disclaimer check) but its own
`scan_document`/`scan_file` aren't separately exposed as MCP tools —
same repository-maintenance reasoning as `case_scaffold`.

`paper_rigor_scan` is the one tool here that's meant to feed back into
agent behavior rather than just report a result: its
`external_verification_worklist` output is a to-do list (uncited
empirical claims, credential assertions, informal-source citations)
for whatever agent is calling it — an MCP host with real web
search/fetch access is expected to resolve each item and, optionally,
use `bifp_start_audit`/`bifp_record_criterion` to track the resolution
persistently, the same two-step flow the original scoping conversation
for this tool described. `paper_rigor_triage_worklist` is an optional
third step in that same flow: run it on the worklist before handing
items to the search-capable agent, to get a priority order and a
concrete suggested check per item — it does not shorten the flow (the
agent still has to do the actual searching) but can make the order it
works through the list better-informed.

The other two Groq-backed tools work the same way at their own scope:
`bifp_judge_rebuttal` and `attractor_scan_judge_visual_proof` are each
a single-specimen research aid for a genuine judgment call their
source package's own text/corpus heuristics can't make honestly — see
`bifp/README.md` "AI-generated advisory reads" and
`attractor_scan/README.md` "Why Case 6 isn't a scanner" for the design
reasoning each was built under, including the §3.9 `no_ai_as_judge`
boundary `bifp_judge_rebuttal` respects and the "not a corpus
classifier" boundary `attractor_scan_judge_visual_proof` respects.

## 30-second demo

```bash
python3 examples/mcp_demo.py
```

Connects a real `mcp.client.session.ClientSession` to this server over
the SDK's own in-memory transport, lists all 19 tools, and calls one
(sometimes two) from each wrapped package — `basin_depth_demo`,
`bifp_scan_text` + `bifp_judge_rebuttal`, `attractor_scan_text` against
the same real Musk quote `attractor_scan`'s own test suite validates
against + `attractor_scan_judge_visual_proof`, `debasinizer_scan_text`
against a constructed specimen combining both patterns it detects, and
`paper_rigor_scan` against a deliberately bad constructed paragraph +
`paper_rigor_triage_worklist` on that scan's own output. The three
Groq-backed calls are skipped gracefully with a printed note if
`GROQ_API_KEY` isn't set — every other step runs fully offline.

## Wiring this into an MCP host

Run the server directly (stdio transport, what most MCP hosts expect):

```bash
research-mcp
```

For a host that reads a JSON config (e.g. Claude Desktop's
`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "piqos-research-tools": {
      "command": "/absolute/path/to/tools/research_mcp/.venv/bin/research-mcp"
    }
  }
}
```

## The real round trip

The bifp README flagged the untested gap explicitly: `agent_tools.py`
was shaped for MCP but never actually driven by a real client. This
package closes that gap with `tests/conftest.py`'s `_live_session`
fixture, built on `mcp.shared.memory.create_client_server_memory_streams`
— the same in-memory transport the `mcp` SDK's own test suite uses —
paired with a real `mcp.client.session.ClientSession` talking to this
project's actual `MCPServer` instance over its actual low-level
protocol handler. Nothing in the request/response cycle is stubbed:
JSON schema generation from type hints, request dispatch, tool
invocation, and JSON-RPC content framing are all the real library
code, exercised by 21 tests including a stateful bifp audit flow
(start → record → get_status) that persists across three separate
tool calls the way an agent's turns actually would.

## A real bug this test suite's own first draft surfaced

`mcp.types.CallToolResult`'s constructor takes an `isError` keyword
(camelCase, a JSON-alias convention), but the actual pydantic field —
and the only spelling that works for attribute access after
construction — is snake_case `is_error`. The first draft of
`conftest.py`'s error-checking helper wrote `if result.isError:`,
which doesn't raise at call time; pydantic's `__getattr__` just
returns nothing usable, and the check silently never fired. Caught by
`test_protocol_level_error_is_distinct_from_payload_level_error` in
`tests/test_server.py`, which deliberately trips the failure by
calling a tool with missing required arguments and asserting on
`result.is_error` directly — the fix and the regression test that
would have caught the original bug are the same assertion.

That test also pins a distinction worth knowing before writing more
tools against this server: a **protocol-level** error (bad arguments,
unknown tool name — MCP's own schema validation failing) sets
`is_error=True` on the `CallToolResult`. A **payload-level** error (an
`agent_tools.py` function's own deliberate `{"error": "..."}` return,
e.g. a missing audit file) is a completely normal, successfully
returned JSON result — `is_error` stays `False`. Callers need to check
both: `result.is_error` for "the tool call itself failed," and
`"error" in json.loads(result.content[0].text)` for "the tool ran and
reported a recoverable problem."

## Live-verification status: confirmed, 2026-08-17, first attempt

The offline suite above proves the MCP wiring round-trips correctly;
it doesn't prove the three Groq-backed tools actually work end-to-end
through that wiring against the real API, since their own live
verification happened in each source package (`bifp/README.md`,
`attractor_scan/README.md`, `paper_rigor/README.md`) calling
`judge_rebuttal`/`judge_visual_proof`/`triage_worklist` directly, not
through this server. Run via
[`.github/workflows/research_mcp_demo.yml`](../../.github/workflows/research_mcp_demo.yml)
(`workflow_dispatch`-only, same reason as the other three Groq demo
workflows: this build environment has `api.groq.com` blocked at the
network-policy level).

This run needed no live iteration — a real risk existed and was fixed
before triggering, not discovered by a failure. `examples/mcp_demo.py`
makes three separate Groq calls in one process (`bifp_judge_rebuttal`,
then `attractor_scan_judge_visual_proof`, then
`paper_rigor_triage_worklist`), and `attractor_scan`'s own live
verification had already found that a single vision call alone can use
7996 of this account's 8000 on_demand-tier TPM budget — three calls
back-to-back with no pacing would very likely have 429'd the second and
third. `mcp_demo.py` was updated to wait 65s after each Groq call
before the next one *before* this run was triggered, applying that
finding forward the same way `paper_rigor`'s own worklist-triage demo
applied both of the earlier lessons (Cloudflare User-Agent, conservative
token budget) proactively and passed clean on its first live attempt.

All 21 offline tests passed, and all three Groq calls succeeded with
the pacing holding — no rate-limit errors anywhere in the run:

- `bifp_judge_rebuttal` on a constructed claim/rebuttal pair (a strong
  claim about causal modeling, rebutted only by a poor MMLU score) came
  back `candidate_read: "unclear"` — a defensible read, since a
  benchmark-score rebuttal neither squarely addresses nor is obviously
  a weaker substitute for a causal-modeling claim.
- `attractor_scan_judge_visual_proof` on the committed
  `genuine_benchmark_chart.png` plus its matching claim came back
  `candidate_read: "genuine_technical_support"` — correct, the same
  read `attractor_scan`'s own live verification got for this pair.
- `paper_rigor_triage_worklist`, run on the real
  `external_verification_worklist` that `paper_rigor_scan` produced
  moments earlier in the same demo (not a canned worklist), returned
  `[high] uncited_empirical_claim` with a concrete suggested check
  ("Search for peer-reviewed studies or reputable reports on the
  topic...") — the full pipeline, scan-output-to-triage-input, working
  over the real wire in one process.

Total run time was a little over two minutes, almost all of it the two
deliberate 65s pacing waits plus package installation — the actual
Groq round trips and the rest of the demo are fast.

## What this tool does NOT do

- **It adds no new research logic.** Every tool call here delegates
  directly to the source package's own `agent_tools.py` function —
  read that package's own README for what the tool actually measures
  or detects, and its own limitations.
- **It does not ship auth, rate limiting, or a hosted deployment.**
  This is a local stdio-transport server for a single agent/host
  process, matching the MCP SDK's own default `MCPServer.run()`
  behavior. SSE and streamable-HTTP transports are available from the
  underlying `MCPServer` (see `app.run(transport=...)` in
  `research_mcp/server.py`) but are untested here.
- **The `mcp` package version is not pinned tightly.** `pyproject.toml`
  requires `mcp>=1.2.0`; this was built and tested against 2.0.0. The
  `MCPServer` class name (`mcp.server.mcpserver.MCPServer` in 2.0.0)
  moved from an earlier `mcp.server.fastmcp.FastMCP` name in older
  1.x releases — `server.py` has an import-compatibility fallback for
  that, but it has only actually been exercised against 2.0.0.

## Development

```bash
source .venv/bin/activate
python3 -m pytest tests/ -v
```

21 tests, all going over the real in-memory MCP wire protocol rather
than calling Python functions directly (that coverage already exists
in each source package's own test suite).

## License

MIT.
