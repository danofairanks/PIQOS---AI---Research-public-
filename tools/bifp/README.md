# bifp

A structured audit tool for the **Basin-Immune Falsification Protocol
(BIFP)**, the six-phase falsification standard defined in
[`basin_attractors_v1.md`](../../papers/published/basin_attractors_v1.md)
§3. BIFP is a checklist with binary pass/fail criteria across Phase
0 (Pre-Commitment Registry) through Phase 6 (Timeline Escrow), plus a
Meta-Protocol (§3.9) and Semantic Hygiene Amendment (§3.10) governing
the audit process itself. This tool turns that checklist into
something you can actually run: a persistent audit record, a handful
of honest text heuristics for the criteria that are partially
detectable from text, and a stable function surface meant to be called
by an agent mid-conversation, not just by a human at a terminal.

## Install

```bash
cd tools/bifp
pip install -e .
pip install -e ".[dev]"   # adds pytest, for running the test suite
```

Zero *pip* dependencies — no numpy, nothing to download; the HTTP
call the optional Groq-backed advisory feature makes (see below) uses
only the standard library. Requires Python >= 3.10.

## The core idea in one example

The tool doesn't decide whether a claim is true. It tracks, criterion
by criterion, whether the *evidence needed to sustain the claim* has
actually been produced — and it flags one specific, checkable failure
mode automatically: **status dismissal**, §3.7's rule that credentials
and motives are inadmissible as a response to a substantive challenge.

```bash
python3 examples/audit_demo.py
```

replays a real specimen this project already analyzed by hand — Gary
Marcus's reply to a definitional challenge from Grigori Karapetyan
(see [`case_studies/2026-08-06_marcus_karapetyan_status_dismissal.md`](../../case_studies/2026-08-06_marcus_karapetyan_status_dismissal.md))
— and shows the tool catching the same pattern automatically:

```python
from bifp.heuristics import scan_for_status_dismissal

reply = "OMG i wrote some of the original work...dude who probably hasn't read that work..."
result = scan_for_status_dismissal(reply)
# result.flagged == True, result.confidence == "combo"
# matched: a credential assertion ("i wrote") AND dismissal of the
# interlocutor ("probably hasn't"), in the same text
```

## CLI

```bash
bifp phases                          # print the full schema
bifp new --audit claim.json --claim "Model X reasons independently"
bifp record --audit claim.json --phase 5 --criterion no_status_dismissal \
    --no-met --evidence "transcript excerpt..."
bifp scan-text --text "we're working on it" --audit claim.json  # attach heuristic flags
bifp status --audit claim.json
bifp report --audit claim.json       # full markdown report

# Optional: AI-generated candidate read on §3.7's "no weaker-substitute
# rebuttal" criterion (requires GROQ_API_KEY; see "AI-generated advisory
# reads" below -- this never sets a criterion outcome itself)
bifp judge-rebuttal --audit claim.json \
    --claim "the original claim text" --rebuttal "the rebuttal text"
```

Every `bifp` subcommand reads/writes the same JSON file (`--audit`),
so an audit can be built up incrementally across many calls — which is
the realistic shape of a real audit: evidence accumulates over time,
not in one sitting.

## As a library

```python
from bifp import AuditSession, render_report

session = AuditSession.new("Model X achieves human-level reasoning", escrowed=True)
session.record(1, "claim_specified", met=True, evidence="paper §2 defines the construct")
session.record(1, "tested_specified", met=True, evidence="MMLU-Pro, n=12000")
session.record(1, "validity_match", met=False, notes="benchmark score, not a construct-level claim")

print(session.overall_resolution)   # "Falsified" -- one unmet Phase 1 criterion is enough
print(render_report(session))       # full markdown audit trail
```

## Wiring this into an agent

`bifp/agent_tools.py` is the package's tool-calling surface: every
function takes and returns only plain JSON-serializable types (no
dataclasses, no enums crossing the boundary), specifically so it can
be wrapped as MCP tools or referenced from a Claude Skill without an
adapter layer.

| Function | Purpose |
|---|---|
| `bifp_list_phases()` | Full schema — call first so the caller knows what phases/criteria exist |
| `bifp_start_audit(audit_path, claim_text, ...)` | Create a new audit, persisted to a file |
| `bifp_record_criterion(audit_path, phase, key, met, evidence, notes)` | Record one assessment |
| `bifp_scan_text(text)` | Run the heuristic scanners against a piece of text, standalone |
| `bifp_attach_scan_to_audit(audit_path, text)` | Same, but attaches results to an audit's record |
| `bifp_get_status(audit_path)` | Current phase-by-phase status + overall resolution |
| `bifp_generate_report(audit_path)` | Full markdown report |
| `bifp_judge_rebuttal(claim_text, rebuttal_text)` | AI-generated (Groq) candidate read on §3.7 no-weaker-substitute-rebuttal, standalone -- see "AI-generated advisory reads" below |
| `bifp_attach_rebuttal_judgment(audit_path, claim_text, rebuttal_text)` | Same, attached to an audit's `ai_advisory_flags` -- never sets a criterion outcome |
| `bifp_start_closed_path_ledger(ledger_path, artifact_label)` | Create a new closed-path evidence ledger, persisted to a file -- see "The closed-path / open-path evidence ledger" above |
| `bifp_record_fixture(ledger_path, fixture_id, outcome_derivation, notes)` | Classify one fixture as asserted/derived/unknown |
| `bifp_get_closed_path_status(ledger_path)` | Current fixture counts + closed-path ratio for an existing ledger |
| `bifp_scan_closed_path_language(text)` | Standalone lexical lead over prose, no ledger required |
| `bifp_scan_hardcoded_assertion_style(text)` | Standalone weak syntactic lead over code-shaped text, no ledger required |

**On MCP specifically:** a live MCP server now exists —
[`tools/research_mcp/`](../research_mcp/). It registers all fourteen
`agent_tools.py` functions above (plus `basin_depth`'s and
`attractor_scan`'s own agent_tools surfaces) against a real
`MCPServer` instance, and is tested over the actual MCP wire protocol
via an in-memory client-server round trip, including a stateful
multi-turn bifp audit flow — see that package's README for what
closed the earlier blocker (`pip install mcp` conflicting with this
build environment's system `PyJWT` package: install into an isolated
virtualenv instead of the system interpreter) and for a real bug the
round-trip test suite's own first draft caught.

## The closed-path / open-path evidence ledger

A separate, generic tool inside this package, distinct from the BIFP
audit above: operationalizes the defeat condition in
[`closed_path_confirmation_v1.md`](../../papers/drafts/closed_path_confirmation_v1.md)
§2 for the specific case of a governance artifact whose only offered
evidence is its own author-authored test suite. A green suite
establishes only an *existential* claim over paths the author controls
(closed-path); a binding claim needs the *universal* claim over all
paths (open-path). This tool doesn't decide whether any artifact
binds — it gives you a place to record, fixture by fixture, whether
each one's expected outcome was asserted (a literal constant matching
the artifact's own output) or derived (computed from an independent
specification), and reports the ratio.

```python
from bifp import ClosedPathLedger

ledger = ClosedPathLedger(artifact_label="generic artifact under test")
ledger.add_fixture("f1", "asserted", notes="literal constant, matches code's own output")
ledger.add_fixture("f2", "derived", notes="computed from an independent spec")
print(ledger.closed_path_ratio)      # 0.5
print(ledger.flagged_fixture_ids)    # ["f1"]
```

```bash
bifp cp-new --ledger artifact.json --artifact-label "generic artifact under test"
bifp cp-record --ledger artifact.json --fixture-id f1 --derivation asserted --notes "..."
bifp cp-status --ledger artifact.json
bifp cp-scan-language --text "..."       # lexical lead: closed-path vs open-path phrasing in prose
bifp cp-scan-assertions --text "..."     # weak syntactic lead: `assert x == <literal>` in code
```

**`artifact_label` is entirely caller-controlled.** This tool never
inspects, validates, or infers anything about it — redact it, name it
generically, or leave it descriptive; that decision belongs to
whoever is running the tool, not to this package.

**What `closed_path_ratio` does and does not mean.** It is `None`
until at least one fixture has been classified — distinct from `0.0`,
which is a real result (everything classified so far is derived). It
is computed only over fixtures actually read and classified; unread
fixtures (`"unknown"`) don't count either way. A high ratio is a lead
to go read the flagged fixtures, never a verdict that an artifact
fails to bind — no defeat condition is evaluated by this tool, only
recorded evidence about how that evidence was constructed. See
`closed_path_confirmation_v1.md` §5 for why this project explicitly
does not propose a numeric threshold (e.g. "10:1 means captured") —
a single ledger, or even many, cannot support one without an
independently-established base rate.

**`cp-scan-language` and `cp-scan-assertions` are standalone lexical
leads, not the ledger.** They scan prose or code-shaped text for
signal phrases and hardcoded-literal-comparison patterns respectively
— useful for a first pass before deciding whether an artifact is worth
building a full fixture-by-fixture ledger for, but neither one reads
or classifies an actual fixture. Both carry the same "read every match
directly" caveat as every other heuristic in this package.

## What's implemented, mapped to the protocol text

| Protocol section | Module | Status |
|---|---|---|
| §3.1 Core Axiom | `protocol.CORE_AXIOM` | Transcribed verbatim |
| §3.2-3.8 Phase 0-6 criteria | `protocol.py` | All 30 criteria transcribed, structured, and enforced by `audit.py`'s pass/fail logic |
| §3.7 binary resolution (Sustained/Falsified/Indeterminate, escrow default) | `audit.AuditSession.overall_resolution` | Implemented exactly per the protocol text |
| §3.9 Meta-Protocol, §3.10 Semantic Hygiene | `protocol.py`, tracked as `protocol_integrity_resolution` | Modeled as audit-process integrity, separate from the claim's own resolution — see "A design choice worth flagging" below |
| §3.7 "no provisionalization" | `heuristics.scan_for_provisionalization` | Phrase-match against the paper's own seed vocabulary |
| §3.7 "no status dismissal" | `heuristics.scan_for_status_dismissal` | Phrase-match + a credential-assertion/dismiss-interlocutor combined-signal detector, validated against a real specimen (see demo) |
| §3.10 prohibited anthropomorphic terms | `heuristics.scan_for_prohibited_anthropomorphic_terms` | Coarse verb-list matcher, explicitly recall-oriented |
| §3.7 "no weaker-substitute rebuttal" | `rebuttal_judge.judge_rebuttal` (advisory only) | A keyword scanner still can't do this honestly (see heuristics.py's docstring), so this is an optional Groq-backed candidate read instead of a regex heuristic — never a verdict, never calls `record()`. Requires `GROQ_API_KEY`. See "AI-generated advisory reads" below for why this doesn't conflict with §3.9's `no_ai_as_judge`. **Confirmed against the live Groq API 2026-08-17 — see that section for the actual result.** |
| §3.2-3.6 everything requiring an actual independent team, red team, or contamination audit | `audit.py`'s `record()` call | Not automatable by construction — these are real-world processes this tool tracks the outcome of, not substitutes for |

## A design choice worth flagging

The Meta-Protocol (§3.9) and Semantic Hygiene Amendment (§3.10) read,
in the paper, as governing the *audit process itself* — no-AI-as-judge,
a cooling-off period, independent linguistic review — rather than as
additional pass/fail gates on the claim under audit. This tool models
them that way: `overall_resolution` is computed from Phase 0-6 only,
and `protocol_integrity_resolution` is a separate field. A claim can
be `Sustained` while its own audit process is `compromised` (e.g. no
cooling-off period observed) — that's a real, reportable condition in
its own right, not something that should silently flip the claim's
verdict or get silently dropped. If you read §3.9-3.10 as intended to
gate the claim itself, that's a one-line change in
`AuditSession.overall_resolution` — flagged here so the choice is
visible rather than buried.

## AI-generated advisory reads (§3.7 rebuttal judge)

`rebuttal_judge.py` adds one optional, Groq-backed feature:
`judge_rebuttal(claim_text, rebuttal_text)` asks an LLM whether a
rebuttal engages a claim as actually made, or a weaker substitute of
it — the one §3.7 criterion `heuristics.py` deliberately declines to
touch, because that comparison requires reading what two texts mean,
not matching keywords.

**Why this doesn't conflict with §3.9's `no_ai_as_judge`.** That
criterion — "No AI-as-judge for claims about AI (structural conflict
of interest avoided)" — is real, tracked, and unchanged by this
feature. `judge_rebuttal` never calls `AuditSession.record()` and
never touches `overall_resolution` or `protocol_integrity_resolution`.
It returns one candidate read, stored separately from every other
signal in `ai_advisory_flags` (not `heuristic_flags` — those are
deterministic regex matches, a different kind of thing), explicitly
labeled with a disclaimer naming §3.9 in every result. The actual
`no_ai_as_judge` criterion is still recorded by a human, against the
whole audit process, exactly as before this module existed — this
feature does not touch that recording, is not evaluated by it, and
cannot make it pass or fail. The contract is stricter than what §3.9
already tolerates elsewhere in the same section (AI-generated audit
reports spot-checked at ≥10% with override power): here, *every*
candidate read requires a human/agent decision before it can support
a `record()` call, with 0% treated as "reviewed by default."

**Setup:** set `GROQ_API_KEY` in the environment — never hardcoded,
never read from a repo file, never included in any output or error
message. Uses only `urllib` from the standard library, so the package
keeps its zero-pip-dependency install; the network call only happens
if you call `judge_rebuttal`/`bifp_judge_rebuttal`/`bifp
judge-rebuttal` directly.

**Live-verification status: confirmed, 2026-08-17.** The offline test
suite (`tests/test_rebuttal_judge.py`, 64 tests) mocks the Groq call
and covers key handling, prompt construction, response parsing, and
error paths. This project's own build environment has `api.groq.com`
blocked at the sandbox/network-policy level, so the live call was run
instead via a manual (`workflow_dispatch`-only) GitHub Actions
workflow, [`.github/workflows/bifp_rebuttal_judge_demo.yml`](../../.github/workflows/bifp_rebuttal_judge_demo.yml)
— see that file for why it exists and its own honesty note. Two
findings from getting that run green, both fixed and covered by
regression tests:

- Groq's edge (Cloudflare) returned HTTP 403 "error code: 1010" — a
  browser-signature bot-fight block triggered by Python's bare default
  `urllib` User-Agent. Fixed by setting an honest, descriptive UA (not
  a spoofed browser), same practice as `requests`/the official SDKs.
- The original `DEFAULT_MODEL` (`llama-3.3-70b-versatile`) no longer
  exists on Groq's catalog at all. Confirmed the current catalog via
  `GET /openai/v1/models` and switched to `openai/gpt-oss-120b`, one of
  three current models supporting both `json_mode` and `reasoning`.

With both fixed, `examples/rebuttal_judge_demo.py`'s discrimination
check passed cleanly against real API output: the `weaker_substitute`
pair (a rebuttal attacking general MMLU performance instead of the
specific claim) came back `flagged: true`, `weakened_restatement_quote:
"it isn't reasoning"`, correctly explaining the rebuttal never engages
the actual single-observation causal-model claim; the
`addresses_actual_claim` pair (a rebuttal testing that exact claim)
came back `flagged: false`, high confidence, correctly recognizing it
as the real test. Re-run the workflow any time to re-confirm — Groq's
catalog changing again is the most likely future failure mode, and the
"List currently available Groq models" step in that workflow exists
specifically to diagnose it quickly if `DEFAULT_MODEL` ever drifts
stale again.

## Honesty notes

- **A heuristic flag is not a verdict.** Every scanner in
  `heuristics.py` returns matches for review, never a `met=True/False`
  call on its own — `record()` always requires an explicit human/agent
  decision, even when a heuristic strongly suggests the answer.
- **Most of BIFP cannot be automated, and this tool doesn't pretend
  otherwise.** Phases 0, 2, 3, 4, and most of Phase 1 require real
  independent teams, red teams, and contamination audits happening in
  the world — `bifp` tracks whether that happened and what it found;
  it does not simulate having done it.
- **The credential/dismissal detector is pattern-matching, not
  semantic understanding.** It will miss dismissals phrased
  differently than its patterns, and could in principle flag a
  passage that mentions credentials for an unrelated reason. Treat
  every flag as "read this passage," never as "this passage is
  guilty."

## Development

```bash
pip install -e ".[dev]"
pytest tests/ -q
```

83 tests total (`pytest tests/ -q` is the current, authoritative count
— treat any specific number in prose as a snapshot, not a promise).
Cover: the protocol schema's structural integrity (no duplicate
criterion keys, only Phase 6 is timeline-only), audit session logic
(phase pass/fail composition, the escrow-defaults-to-falsified rule,
protocol-integrity independence from claim resolution, JSON
round-tripping), the heuristic scanners (including a regression test
pinning the real Marcus/Karapetyan specimen at `combo` confidence),
the agent-tools JSON boundary (every function's output round-trips
through `json.dumps`, errors return as dicts rather than raising across
the tool-call boundary), report rendering, and (`tests/test_closed_
path.py` + additions to `tests/test_agent_tools.py`) the closed-path
ledger's None-vs-0.0 ratio distinction, its fixture-replace-not-
duplicate semantics, a regression pin against this project's own
published 5-of-59 specimen ratio (generic fixture ids, no identifying
detail), and both standalone lexical scanners.

## License

MIT, same as the rest of this repository.
