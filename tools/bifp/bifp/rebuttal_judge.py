"""Advisory-only, Groq-backed candidate read for §3.7's "no weaker-
substitute rebuttal" criterion -- the one row `heuristics.py` leaves
deliberately unimplemented, because judging whether a rebuttal
addresses a weaker version of a claim than the one actually made
requires comparing what two pieces of text *mean*, not matching
keywords.

§3.9's Meta-Protocol has its own tracked criterion for exactly this
territory: `no_ai_as_judge` -- "No AI-as-judge for claims about AI
(structural conflict of interest avoided)." This module does not
violate that, by construction: nothing in here ever calls
`AuditSession.record()` or sets a `CriterionStatus`. It produces one
candidate read, explicitly labeled as AI-generated and subject to
§3.9, for a human or agent to weigh -- the same non-authoritative
contract every scanner in `heuristics.py` already has (see that
module's docstring: "these are lint flags, not verdicts"). The
`no_ai_as_judge` criterion itself is still recorded, by a human, in
the Meta-Protocol section, exactly as before this module existed.

Requires GROQ_API_KEY in the environment. Never hardcoded, never read
from a repo file, never included in any returned dict or exception
message. Uses only the standard library (urllib) so this package keeps
its zero-dependency install -- see pyproject.toml.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass, field

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_MODEL = "llama-3.3-70b-versatile"

_VALID_READS = ("addresses_actual_claim", "weaker_substitute", "unclear")

_SYSTEM_PROMPT = (
    "You are assisting a structured audit protocol (BIFP, §3.7) that checks "
    "whether a rebuttal to a claim actually engages the claim as stated, or "
    "instead rebuts an easier, narrower, or otherwise weaker version of it "
    "(a 'weaker-substitute rebuttal'). You are not adjudicating whether the "
    "original claim is true. You are only comparing the CLAIM text against "
    "the REBUTTAL text to check whether the rebuttal's target matches the "
    "claim's actual scope and strength.\n\n"
    "Respond with a single JSON object, no other text, with exactly these "
    "keys:\n"
    '  "candidate_read": one of "addresses_actual_claim", "weaker_substitute", '
    'or "unclear"\n'
    '  "reasoning": a short, specific explanation grounded in the two texts\n'
    '  "weakened_restatement_quote": the exact phrase from the rebuttal that '
    "restates the claim in a weaker form, if candidate_read is "
    '"weaker_substitute" -- otherwise null\n'
    '  "self_reported_confidence": one of "low", "medium", "high"\n\n'
    "Use \"unclear\" rather than guessing when the rebuttal's target is "
    "ambiguous. Do not evaluate whether the claim or the rebuttal is "
    "factually correct -- only whether the rebuttal's target matches the "
    "claim's actual scope."
)

DISCLAIMER = (
    "AI-generated candidate read (Groq, see 'model' field). Not a verdict. "
    "§3.9's no_ai_as_judge criterion governs this audit's process integrity "
    "independently of this flag -- record it yourself based on the full "
    "audit, not on whether this module ran. A human or agent must still "
    "call AuditSession.record() for §3.7's no_weaker_substitute_rebuttal "
    "criterion; this module never does."
)


class RebuttalJudgeError(RuntimeError):
    """Raised for missing credentials, API failures, or unparseable
    responses. Never includes the API key in its message."""


@dataclass
class RebuttalJudgeResult:
    claim_text: str
    rebuttal_text: str
    candidate_read: str  # one of _VALID_READS
    reasoning: str
    weakened_restatement_quote: str | None
    self_reported_confidence: str
    model: str
    disclaimer: str = field(default=DISCLAIMER)

    @property
    def flagged(self) -> bool:
        return self.candidate_read == "weaker_substitute"

    def to_dict(self) -> dict:
        return {
            "source": "ai_advisory",
            "name": "rebuttal_weaker_substitute_candidate_read",
            "phase": 5,
            "criterion_key": "no_weaker_substitute_rebuttal",
            "flagged": self.flagged,
            "candidate_read": self.candidate_read,
            "reasoning": self.reasoning,
            "weakened_restatement_quote": self.weakened_restatement_quote,
            "self_reported_confidence": self.self_reported_confidence,
            "model": self.model,
            "disclaimer": self.disclaimer,
        }


def _call_groq_api(payload: dict, api_key: str) -> dict:
    """Isolated so tests can monkeypatch this one function instead of
    mocking urllib directly. Returns the parsed JSON response body."""
    request = urllib.request.Request(
        GROQ_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RebuttalJudgeError(f"Groq API returned HTTP {exc.code}: {body[:500]}") from exc
    except urllib.error.URLError as exc:
        raise RebuttalJudgeError(f"Could not reach Groq API: {exc.reason}") from exc


def judge_rebuttal(
    claim_text: str,
    rebuttal_text: str,
    *,
    api_key: str | None = None,
    model: str = DEFAULT_MODEL,
) -> RebuttalJudgeResult:
    """Get one AI-generated candidate read on whether `rebuttal_text`
    addresses `claim_text` as actually made, or a weaker substitute.

    Raises RebuttalJudgeError if GROQ_API_KEY is not set (and no
    api_key passed explicitly), if the API call fails, or if the
    response cannot be parsed into the expected shape. Fails loudly
    rather than returning a silently-wrong result, same discipline as
    AuditSession.record() on an unknown criterion.
    """
    key = api_key or os.environ.get("GROQ_API_KEY")
    if not key:
        raise RebuttalJudgeError(
            "GROQ_API_KEY not set. This module reads it from the environment "
            "only -- it is never hardcoded or read from a repo file."
        )

    payload = {
        "model": model,
        "temperature": 0.1,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": _SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"CLAIM:\n{claim_text}\n\nREBUTTAL:\n{rebuttal_text}"
                ),
            },
        ],
    }

    response = _call_groq_api(payload, key)

    try:
        content = response["choices"][0]["message"]["content"]
        parsed = json.loads(content)
    except (KeyError, IndexError, json.JSONDecodeError) as exc:
        raise RebuttalJudgeError(f"Could not parse Groq response into expected shape: {exc}") from exc

    candidate_read = parsed.get("candidate_read")
    if candidate_read not in _VALID_READS:
        raise RebuttalJudgeError(
            f"Groq returned an unrecognized candidate_read: {candidate_read!r} "
            f"(expected one of {_VALID_READS})"
        )

    return RebuttalJudgeResult(
        claim_text=claim_text,
        rebuttal_text=rebuttal_text,
        candidate_read=candidate_read,
        reasoning=parsed.get("reasoning", ""),
        weakened_restatement_quote=parsed.get("weakened_restatement_quote"),
        self_reported_confidence=parsed.get("self_reported_confidence", "unknown"),
        model=model,
    )
