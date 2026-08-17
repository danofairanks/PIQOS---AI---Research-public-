---
name: paper-rigor-scan
description: Use this skill whenever the user wants to check a research paper, article, claim, or piece of written argument for evidentiary rigor gaps or epistemic-capture rhetoric -- unattributed quotes, uncited statistics, missing falsifiability/limitations sections, credential-substituted-for-evidence claims, defensive-maneuver rhetoric (goal-post movement, provisionalization, status dismissal), semantic-laundering patterns ("emergence"/"alignment" misuse, AGI-vs-agentic drift), and resonance-vocabulary register. Trigger on "scan this paper", "check this for rigor", "run this through paper-rigor / attractor-scan / BIFP / debasinizer", or when text is pasted/uploaded and the user asks whether it holds up evidentially.
license: MIT -- see this repository's root LICENSE.
---

# Paper-Rigor Scan

Runs the five text-scanning tools this repository ships
(`paper_rigor`, `verification_lint`, `attractor_scan`, `bifp`,
`debasinizer`) against a piece of text and returns a structured,
multi-axis report -- matched spans and named categories, not a single
blended "rigor score." This is the same five-tool pipeline
`docs/scan.html` already runs client-side in-browser via Pyodide; this
skill runs the identical logic locally through the real Python
packages, for use inside an agent session rather than a browser tab.

**Deliberately covers 5 of this repository's 8 tools**, matching the
scope `docs/scan.html` and `docs/assets/py/paper_scan.py` already
established: `basin_depth` needs a real multi-document corpus and a
significance-tested run, not a one-shot text scan; `case_scaffold`
generates and lints new `case_studies/` files rather than scanning
arbitrary text; `research_mcp` is the MCP server that wires these same
five tools' `agent_tools.py` surfaces up as callable tools over the
MCP wire protocol -- infrastructure, not a task a user asks for by
name. If this session already has an MCP client connected to
`tools/research_mcp/`, prefer calling its tools directly over anything
below; this skill exists for sessions that only have local code
execution (Bash/Python), not an MCP connection to this repo's server.

## Setup

Each tool is a standalone, `pip install`-able package under `tools/`
in this repository, with zero or near-zero runtime dependencies
(exception: the three Groq-backed advisory tools noted below, which
degrade to a `{"error": ...}` payload rather than failing if
`GROQ_API_KEY` is unset). From a clone of this repository:

```bash
for t in paper_rigor verification_lint attractor_scan bifp debasinizer; do
  pip install -e "tools/$t"
done
```

No network access is required for the core scanners -- only the three
advisory tools listed in "What this does not do" below call out to
Groq.

## Quick start (CLI)

Each tool ships its own CLI entry point. To scan one file with every
tool that takes a single-document `scan`/`text` mode:

```bash
paper-rigor scan path/to/paper.md
verification-lint scan path/to/paper.md
attractor-scan text --file path/to/paper.md
bifp scan-text --text "$(cat path/to/paper.md)"
debasinizer text --file path/to/paper.md
```

Each prints a JSON report to stdout. `verification-lint` also has a
`scan-dir` mode for an entire directory tree:

```bash
verification-lint scan-dir case_studies/ --pattern '*.md' --only-gaps
```

## Programmatic use (agent_tools.py)

Every tool ships a `agent_tools.py` module -- plain JSON-in/JSON-out
functions, the same stable surface `tools/research_mcp/` wraps as MCP
tools. Prefer this over shelling out to the CLI and parsing stdout
when running inside a Python session:

```python
from paper_rigor.agent_tools import paper_rigor_scan
from verification_lint.agent_tools import verification_lint_scan_text
from attractor_scan.agent_tools import attractor_scan_text
from bifp.agent_tools import bifp_scan_text
from debasinizer.agent_tools import debasinizer_scan_text

text = open("path/to/paper.md").read()

report = {
    "paper_rigor": paper_rigor_scan(text),
    "verification_lint": verification_lint_scan_text(text),
    "attractor_scan": attractor_scan_text(text),
    "bifp": bifp_scan_text(text),
    "debasinizer": debasinizer_scan_text(text),
}
```

For the exact pattern used to turn that combined dict into a
human-readable Markdown report (per-tool sections, a top-level
summary, no blended score), read `docs/assets/py/paper_scan.py` in
this repository directly and mirror its `_md_*` formatter functions
rather than inventing a new report shape -- that module is the
canonical, already-tested reference for exactly this composition.

## What each tool flags

| Tool | Flags |
|---|---|
| `paper_rigor` | Placeholder/hand-wave phrases, missing falsifiability condition, self-citation ratio, formal-vs-informal citation mix, uncited empirical-certainty claims, credential-substituted-for-evidence claims, unsupported consensus claims, claimed-citability-with-zero-references, missing limitations section. Domain-agnostic -- applies to any paper, not just this project's own vocabulary. |
| `verification_lint` | Unattributed direct quotes (40+ chars, no attribution signal nearby), uncited high-precision statistics (decimal percentages, dollar amounts, large comma-grouped counts, fractions), missing "what this does not claim" scoping section. Recognizes this project's own blanket end-of-document `Sources: ...` citation convention so a well-sourced document isn't misread as riddled with gaps. |
| `attractor_scan` | Seven defensive-maneuver rhetorical patterns (goal-post movement, provisionalization, status dismissal, burden-shifting, equivocation, volume/velocity defense, appeal-to-future-proof) and five semantic-laundering cases (pattern-recognition-vs-matching, understanding/reasoning, emergence, alignment/safety, AGI/agentic bidirectional drift), plus an Unglossed Formal Object detector (a bare equation with a private variable, ungrounded, co-occurring with "law of X" + "founder of" self-titling language). |
| `bifp` | Two of the Basin-Immune Falsification Protocol's Phase 5 criteria detectable from text alone (status dismissal, provisionalization) and the §3.10 prohibited-anthropomorphic-terms check. Also structures a full six-phase audit record if the user wants to formally work through BIFP against a specific claim (`bifp new`/`bifp record`), not just run the text heuristics. |
| `debasinizer` | Resonance-vocabulary register (resonance/wave/signal/mirror language, consciousness/persistence themes, "great convergence" inevitability framing) requiring 2+ categories co-occurring, not any single common word, plus a separate self-coherence-assertion detector ("this proves," "the pieces align"). |

## What this does not do

- **A flag is a lead, not a verdict.** Every scanner returns matched
  spans for a human (or the requesting user) to review -- report
  findings as findings to check, not as a rigor score or a pass/fail
  verdict on the paper.
- **No AI-as-judge for claims about AI.** `basin_attractors_v1.md`
  §3.9's Meta-Protocol states this explicitly: an AI system judging a
  claim about AI is a structural conflict of interest. When the text
  being scanned makes claims about AI systems, present this skill's
  findings as evidence for the user's own judgment, not as this
  skill's (or Claude's) independent verdict on whether the claim
  holds.
- **Three tools call an external API (Groq), advisory-only, and are
  not part of the default scan above:** `bifp_judge_rebuttal` /
  `bifp_attach_rebuttal_judgment`, `attractor_scan_judge_visual_proof`,
  and `paper_rigor_triage_worklist`. Each requires `GROQ_API_KEY` and
  returns a recoverable `{"error": ...}` payload if it's missing --
  invoke these only if the user specifically asks for a rebuttal
  judgment, a visual-proof read, or worklist triage, and say so
  explicitly when using one, since these are the one part of the
  pipeline that isn't pure local computation.
- **`attractor_scan` deliberately does not scan for Case 6** (a term's
  own technical precision borrowed as visual proof via imagery/pun) --
  it's a cross-modal, single-instance rhetorical move, not a
  generalizable text pattern. Don't report its absence from a scan as
  a clean result on that specific case; it was never checked.

## Next steps

For full detail on any one tool -- design rationale, known false
positives already caught and fixed, exact test counts, honesty notes
-- read that tool's own `README.md` under `tools/<name>/README.md`
directly rather than relying on the summary table above.
