"""Advisory-only, Groq-backed triage pass over an existing
`external_verification_worklist` (see scan.py's module docstring). The
worklist itself is produced entirely offline, deterministically, by
`scan_paper()` -- this module never adds, removes, or regenerates
items. Its only job is to attach two things to each *existing* item: a
`priority` and a `suggested_check` (what a real search/lookup should
specifically look for) -- speed/cost triage before the worklist reaches
an agent with real web search/fetch access (see tools/research_mcp/),
not a replacement for that verification.

This is deliberately the narrowest of this repo's three Groq-backed
advisory features. `bifp`'s rebuttal_judge and `attractor_scan`'s
visual_proof_judge each return one substantive candidate read on a
genuine judgment call. This module never asserts anything about
whether an item's underlying claim holds up -- Groq has no live web
access here, and letting it imply otherwise would collapse the exact
boundary README.md "What this tool does NOT do" names: "It cannot
verify a citation supports its claim." Prioritizing and suggesting
what to check is not verifying; conflating the two would be worse than
not building this at all.

Requires GROQ_API_KEY in the environment. Never hardcoded, never read
from a repo file, never logged. Uses only the standard library
(urllib) so this package's only real dependency stays verification_lint.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass, field

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
# Text-only triage -- same model bifp's rebuttal_judge uses (confirmed
# live 2026-08-17), not attractor_scan's vision model; no image here.
DEFAULT_MODEL = "openai/gpt-oss-120b"

# Same identifying UA as the other two Groq-backed modules, applied
# from the start this time -- see bifp/rebuttal_judge.py for the
# Cloudflare "error code: 1010" this avoids.
_USER_AGENT = "paper-rigor-worklist-triage/0.1 (+https://github.com/danofairanks/PIQOS---AI---Research-public-)"

_VALID_PRIORITIES = ("high", "medium", "low")

_SYSTEM_PROMPT = (
    "You are helping triage a research-verification worklist. Each item was "
    "already found by a deterministic text scanner -- a claim, credential "
    "appeal, consensus assertion, or citation that needs an external check "
    "(a web search, reading a cited source, etc.) to resolve. You do not "
    "have web access and must not claim to have checked anything. Your job "
    "is only to: (1) rate how urgent each item is to actually check, given "
    "how load-bearing the claim appears to be in context, and (2) suggest "
    "specifically what a real check should look for -- not answer it.\n\n"
    "You will receive a JSON array of items, each with an 'index', 'kind', "
    "'item' text, and 'reason' the scanner flagged it. Respond with a JSON "
    "object with exactly one key, \"triaged\", containing a JSON array of "
    "the SAME LENGTH, one entry per input item in the SAME ORDER, each with "
    "exactly these keys:\n"
    '  "index": the same index from the input item\n'
    '  "priority": one of "high", "medium", "low"\n'
    '  "suggested_check": one specific sentence describing what a real '
    "search/lookup should look for to resolve this item -- never an answer, "
    "never a claim that the underlying assertion is true or false\n\n"
    "Do not add, remove, merge, or reorder items."
)

DISCLAIMER = (
    "AI-generated triage read (Groq, see 'model' field). Does not verify "
    "any item and has no web access -- only orders/prioritizes what "
    "scan_paper() already found deterministically and suggests what a real "
    "check should look for. Never invents new worklist items; see "
    "paper_rigor README 'What this tool does NOT do.'"
)


class WorklistTriageError(RuntimeError):
    """Raised for missing credentials, API failures, unparseable
    responses, or a returned item count that doesn't match the input
    (fail loudly rather than silently trust a model that dropped or
    added items). Never includes the API key in its message."""


@dataclass
class TriagedWorklistItem:
    kind: str
    item: str
    context: str
    reason: str
    priority: str  # one of _VALID_PRIORITIES
    suggested_check: str

    def to_dict(self) -> dict:
        return {
            "kind": self.kind, "item": self.item, "context": self.context, "reason": self.reason,
            "priority": self.priority, "suggested_check": self.suggested_check,
        }


@dataclass
class WorklistTriageResult:
    items: list[TriagedWorklistItem]
    model: str
    disclaimer: str = field(default=DISCLAIMER)

    @property
    def high_priority_items(self) -> list[TriagedWorklistItem]:
        return [i for i in self.items if i.priority == "high"]

    def to_dict(self) -> dict:
        return {
            "source": "ai_advisory",
            "name": "worklist_triage",
            "items": [i.to_dict() for i in self.items],
            "high_priority_count": len(self.high_priority_items),
            "model": self.model,
            "disclaimer": self.disclaimer,
        }


def _call_groq_api(payload: dict, api_key: str) -> dict:
    """Isolated so tests can monkeypatch this one function instead of
    mocking urllib directly."""
    request = urllib.request.Request(
        GROQ_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": _USER_AGENT,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise WorklistTriageError(f"Groq API returned HTTP {exc.code}: {body[:500]}") from exc
    except urllib.error.URLError as exc:
        raise WorklistTriageError(f"Could not reach Groq API: {exc.reason}") from exc


def triage_worklist(
    worklist: list[dict],
    *,
    api_key: str | None = None,
    model: str = DEFAULT_MODEL,
) -> WorklistTriageResult:
    """Attach a priority + suggested_check to each item in an existing
    `external_verification_worklist` (from `PaperRigorResult`). Never
    calls the scanner itself and never adds/removes items -- pass the
    same list `scan_paper(...).external_verification_worklist` returns.

    Raises WorklistTriageError if GROQ_API_KEY is not set, the API call
    fails, the response can't be parsed, or the returned item count
    doesn't match the input. Returns immediately with an empty result
    (no API call) if `worklist` is empty -- nothing to triage.
    """
    if not worklist:
        return WorklistTriageResult(items=[], model=model)

    key = api_key or os.environ.get("GROQ_API_KEY")
    if not key:
        raise WorklistTriageError(
            "GROQ_API_KEY not set. This module reads it from the environment "
            "only -- it is never hardcoded or read from a repo file."
        )

    indexed = [
        {"index": i, "kind": w.get("kind", ""), "item": w.get("item", ""), "reason": w.get("reason", "")}
        for i, w in enumerate(worklist)
    ]

    payload = {
        "model": model,
        "temperature": 0.1,
        "response_format": {"type": "json_object"},
        "max_completion_tokens": 2048,
        "messages": [
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(indexed)},
        ],
    }

    response = _call_groq_api(payload, key)

    try:
        content = response["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        triaged = parsed["triaged"]
    except (KeyError, IndexError, json.JSONDecodeError, TypeError) as exc:
        raise WorklistTriageError(f"Could not parse Groq response into expected shape: {exc}") from exc

    if not isinstance(triaged, list) or len(triaged) != len(worklist):
        raise WorklistTriageError(
            f"Groq returned {len(triaged) if isinstance(triaged, list) else 'a non-list'} "
            f"triaged items for {len(worklist)} input items -- refusing to guess at the mapping"
        )

    by_index: dict[int, dict] = {}
    for entry in triaged:
        try:
            idx = entry["index"]
            priority = entry["priority"]
        except (KeyError, TypeError) as exc:
            raise WorklistTriageError(f"Malformed triaged entry: {exc}") from exc
        if priority not in _VALID_PRIORITIES:
            raise WorklistTriageError(
                f"Groq returned an unrecognized priority: {priority!r} (expected one of {_VALID_PRIORITIES})"
            )
        by_index[idx] = entry

    if set(by_index) != set(range(len(worklist))):
        raise WorklistTriageError(
            f"Groq's returned indices {sorted(by_index)} don't match the input indices "
            f"0..{len(worklist) - 1} -- refusing to guess at the mapping"
        )

    items = [
        TriagedWorklistItem(
            kind=w.get("kind", ""), item=w.get("item", ""), context=w.get("context", ""), reason=w.get("reason", ""),
            priority=by_index[i]["priority"], suggested_check=by_index[i].get("suggested_check", ""),
        )
        for i, w in enumerate(worklist)
    ]
    return WorklistTriageResult(items=items, model=model)
