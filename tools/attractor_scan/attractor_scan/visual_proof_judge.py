"""Advisory-only, Groq-backed candidate read for Case 6 ("A Term's Own
Technical Precision Borrowed as Visual Proof for Its Unrelated Hype
Meaning" -- basin_attractors_v1.md §2.8), the one laundering case
`laundering.py` deliberately declines to give a keyword scanner: the
paper's own example is a single, cross-modal, pun-based rhetorical
move (a math-formula collage captioned "math Singularity"), not a
generalizable text pattern.

This module does not reopen that decision. It is not a corpus scanner
and is not wired into `scan()`/`scan_corpus()` -- see README "Why Case
6 isn't here" and this module's own docstring below for why. It is a
single-specimen research aid: given one image and one claimed-hype
text, it returns one AI-generated candidate read on whether the
image's actual technical content genuinely supports the claim, or is
connected to it only by wordplay/coincidental terminology -- meant to
help a human draft a case study faster, the same way `bifp`'s
rebuttal_judge.py assists a §3.7 audit without adjudicating it. It
never scans a corpus, never stores or vendors the image anywhere, and
never asserts a verdict -- the case study, with full independent
verification, is still the actual research output.

Requires GROQ_API_KEY in the environment. Never hardcoded, never read
from a repo file, never logged. Uses only the standard library
(urllib) so this package keeps its zero-dependency install.
"""

from __future__ import annotations

import base64
import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
# Confirmed live against GET /openai/v1/models 2026-08-17 (see
# tools/bifp's README for the same confirmation on the text-only side):
# qwen/qwen3.6-27b is the one model on Groq's current catalog with
# "image" in input_modalities plus json_mode + reasoning support.
DEFAULT_MODEL = "qwen/qwen3.6-27b"

# Honest, descriptive identification -- not a spoofed browser UA. See
# tools/bifp/bifp/rebuttal_judge.py's identical constant and comment:
# Groq's edge (Cloudflare) bot-fights Python's bare default urllib UA
# string with an HTTP 403 "error code: 1010"; this avoids that from
# the start rather than discovering it in CI a second time.
_USER_AGENT = "attractor-scan-visual-proof-judge/0.1 (+https://github.com/danofairanks/PIQOS---AI---Research-public-)"

_VALID_READS = ("genuine_technical_support", "unrelated_borrowed_precision", "unclear")

_MEDIA_TYPE_BY_SUFFIX = {
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".webp": "image/webp", ".gif": "image/gif",
}

_SYSTEM_PROMPT = (
    "You are assisting research into a specific rhetorical pattern: a term's "
    "own genuine technical precision (from a real formula, diagram, or "
    "notation) being borrowed as apparent visual 'proof' for an unrelated "
    "hype claim, via wordplay or coincidental terminology -- not because the "
    "image's actual technical content supports the claim. You are given one "
    "image and one claim text it was reportedly used to support. Describe "
    "what the image actually, literally shows first. Then assess whether its "
    "genuine technical content substantively supports the claim, or whether "
    "the connection is only a pun/wordplay/coincidental term shared between "
    "the image and the claim. You are not evaluating whether the claim "
    "itself is true or false -- only whether the image is genuine evidence "
    "for it or borrowed precision unrelated to it.\n\n"
    "Respond with a single JSON object, no other text, with exactly these "
    "keys:\n"
    '  "image_description": a literal, factual description of what the image shows\n'
    '  "candidate_read": one of "genuine_technical_support", '
    '"unrelated_borrowed_precision", or "unclear"\n'
    '  "reasoning": a short, specific explanation grounded in the image and the claim\n'
    '  "borrowed_term": the specific word/phrase doing double duty between the '
    'image\'s real content and the claim, if candidate_read is '
    '"unrelated_borrowed_precision" -- otherwise null\n'
    '  "self_reported_confidence": one of "low", "medium", "high"\n\n'
    "Use \"unclear\" rather than guessing when the relationship is ambiguous."
)

DISCLAIMER = (
    "AI-generated candidate read (Groq, see 'model' field). Not a verdict. "
    "This is a single-specimen research aid for drafting a case study, not "
    "a corpus classifier -- see attractor_scan README 'Why Case 6 isn't "
    "here.' Independent verification of the image and claim is still "
    "required before anything here is cited as a finding."
)


class VisualProofJudgeError(RuntimeError):
    """Raised for missing credentials, API failures, unparseable
    responses, or an unreadable image file. Never includes the API key
    in its message."""


@dataclass
class VisualProofJudgeResult:
    claim_text: str
    image_description: str
    candidate_read: str  # one of _VALID_READS
    reasoning: str
    borrowed_term: str | None
    self_reported_confidence: str
    model: str
    disclaimer: str = field(default=DISCLAIMER)

    @property
    def flagged(self) -> bool:
        return self.candidate_read == "unrelated_borrowed_precision"

    def to_dict(self) -> dict:
        return {
            "source": "ai_advisory",
            "name": "visual_proof_case6_candidate_read",
            "case": "6",
            "flagged": self.flagged,
            "candidate_read": self.candidate_read,
            "image_description": self.image_description,
            "reasoning": self.reasoning,
            "borrowed_term": self.borrowed_term,
            "self_reported_confidence": self.self_reported_confidence,
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
        raise VisualProofJudgeError(f"Groq API returned HTTP {exc.code}: {body[:500]}") from exc
    except urllib.error.URLError as exc:
        raise VisualProofJudgeError(f"Could not reach Groq API: {exc.reason}") from exc


def _image_data_uri(image_path: str | None, image_bytes: bytes | None, media_type: str | None) -> str:
    if (image_path is None) == (image_bytes is None):
        raise VisualProofJudgeError("pass exactly one of image_path or image_bytes")
    if image_path is not None:
        path = Path(image_path)
        try:
            raw = path.read_bytes()
        except OSError as exc:
            raise VisualProofJudgeError(f"could not read image_path {image_path!r}: {exc}") from exc
        resolved_media_type = media_type or _MEDIA_TYPE_BY_SUFFIX.get(path.suffix.lower())
        if not resolved_media_type:
            raise VisualProofJudgeError(
                f"could not infer media type from {image_path!r}; pass media_type= explicitly"
            )
    else:
        raw = image_bytes
        if not media_type:
            raise VisualProofJudgeError("media_type= is required when passing image_bytes")
        resolved_media_type = media_type
    encoded = base64.b64encode(raw).decode("ascii")
    return f"data:{resolved_media_type};base64,{encoded}"


def judge_visual_proof(
    claim_text: str,
    *,
    image_path: str | None = None,
    image_bytes: bytes | None = None,
    media_type: str | None = None,
    api_key: str | None = None,
    model: str = DEFAULT_MODEL,
) -> VisualProofJudgeResult:
    """Get one AI-generated candidate read on whether an image is
    genuine technical support for `claim_text`, or borrowed precision
    connected only by wordplay (Case 6). Pass exactly one of
    `image_path` (a local file) or `image_bytes` (+ `media_type`, e.g.
    "image/png") -- neither is stored or vendored anywhere by this
    function.

    Raises VisualProofJudgeError if GROQ_API_KEY is not set, the image
    can't be read, the API call fails, or the response can't be parsed
    -- fails loudly rather than returning a silently-wrong result.
    """
    key = api_key or os.environ.get("GROQ_API_KEY")
    if not key:
        raise VisualProofJudgeError(
            "GROQ_API_KEY not set. This module reads it from the environment "
            "only -- it is never hardcoded or read from a repo file."
        )

    data_uri = _image_data_uri(image_path, image_bytes, media_type)

    payload = {
        "model": model,
        "temperature": 0.1,
        "response_format": {"type": "json_object"},
        # qwen/qwen3.6-27b is reasoning-capable; a harder cross-modal
        # judgment call (an abstract math graph vs. a labeled bar
        # chart) can consume the whole default token budget on
        # reasoning before ever emitting the JSON answer, surfacing as
        # HTTP 400 json_validate_failed with an EMPTY failed_generation
        # -- confirmed live 2026-08-17 (the bar-chart pair succeeded
        # under the exact same code path; the graph pair failed this
        # way). Explicit headroom at the model's own advertised cap
        # (confirmed via GET /openai/v1/models) rather than leaving it
        # to a provider default not sized for reasoning + vision.
        "max_completion_tokens": 16384,
        "messages": [
            {"role": "system", "content": _SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"CLAIM this image was reportedly used to support:\n{claim_text}"},
                    {"type": "image_url", "image_url": {"url": data_uri}},
                ],
            },
        ],
    }

    response = _call_groq_api(payload, key)

    try:
        content = response["choices"][0]["message"]["content"]
        parsed = json.loads(content)
    except (KeyError, IndexError, json.JSONDecodeError) as exc:
        raise VisualProofJudgeError(f"Could not parse Groq response into expected shape: {exc}") from exc

    candidate_read = parsed.get("candidate_read")
    if candidate_read not in _VALID_READS:
        raise VisualProofJudgeError(
            f"Groq returned an unrecognized candidate_read: {candidate_read!r} "
            f"(expected one of {_VALID_READS})"
        )

    return VisualProofJudgeResult(
        claim_text=claim_text,
        image_description=parsed.get("image_description", ""),
        candidate_read=candidate_read,
        reasoning=parsed.get("reasoning", ""),
        borrowed_term=parsed.get("borrowed_term"),
        self_reported_confidence=parsed.get("self_reported_confidence", "unknown"),
        model=model,
    )
