"""Pyodide-in-browser aggregator for docs/scan.html. Pure wiring over
the same five agent_tools.py surfaces tools/research_mcp/ wraps for
MCP -- no new research logic, just calling the five text->dict
functions and combining/rendering their output. Runs entirely inside
the visitor's browser (Pyodide/WASM); the input text is never sent
anywhere.

Deliberately does NOT compute a single blended "rigor score." The five
tools measure independent, differently-scoped things -- a self-citation
ratio is not commensurable with a semantic-laundering match count.
Inventing a composite number would be exactly the kind of unearned
precision this project's own papers (laundered_vocabulary_v1.md's
"Metrics vs. Soundness" entry) argue against. The report is a
structured multi-axis summary instead.
"""

import json
from datetime import datetime, timezone

from attractor_scan.agent_tools import attractor_scan_text
from bifp.agent_tools import bifp_scan_text
from debasinizer.agent_tools import debasinizer_scan_text
from paper_rigor.agent_tools import paper_rigor_scan
from verification_lint.agent_tools import verification_lint_scan_text


def run_all_scans(text: str, *, title: str = "") -> dict:
    """Run all five scanners against `text` and return one combined,
    JSON-safe dict. Nothing here writes to disk or makes a network
    call -- the scanned text lives only in this call's return value."""
    return {
        "meta": {
            "title": title or None,
            "word_count": len(text.split()),
            "char_count": len(text),
            "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        },
        "paper_rigor": paper_rigor_scan(text),
        "verification_lint": verification_lint_scan_text(text),
        "attractor_scan": attractor_scan_text(text),
        "bifp": bifp_scan_text(text),
        "debasinizer": debasinizer_scan_text(text),
    }


def _yn(value: bool) -> str:
    return "yes" if value else "no"


def _md_paper_rigor(section: dict) -> list[str]:
    lines = ["### paper_rigor", ""]
    lines.append(f"- Structural gaps: **{section['structural_gap_count']}** "
                 f"(overall ok: {_yn(section['ok'])})")
    fals = section["falsifiability"]
    extra = f", {len(fals['certainty_claims'])} uncited certainty claim(s)" if fals.get("certainty_claims") else ""
    lines.append(f"- Falsifiability: testable markers present = **{_yn(fals['has_testable_markers'])}**{extra}")
    sc = section["self_citation"]
    if sc["ratio"] is not None:
        lines.append(f"- Self-citation ratio: **{sc['ratio']:.2f}** "
                     f"({sc['n_self_cited']}/{sc['n_references']} references)")
    else:
        lines.append("- Self-citation ratio: n/a (no byline authors supplied, or no references found)")
    vm = section["venue_mix"]
    if vm["n_total"]:
        lines.append(f"- Citation venue mix: {vm['n_formal']} formal / {vm['n_informal']} informal / "
                     f"{vm['n_unknown']} unknown ({vm['n_total']} total)")
    lim = section["limitations"]
    applic = "" if lim["applicable"] else " (not applicable -- below minimum word count)"
    lines.append(f"- Limitations section present: **{_yn(lim['present'])}**{applic}")
    cc = section["citability_claim"]
    if cc["claims_citability"] and cc["gap"]:
        lines.append("- **Flag:** claims citability/citable-research grounding while parsing to zero references.")
    worklist = section["external_verification_worklist"]
    if worklist:
        lines.append("")
        lines.append(f"External verification worklist ({len(worklist)} item(s) -- needs a real web "
                     f"search/fetch to resolve, not established by this scan):")
        for item in worklist:
            lines.append(f"  - *{item['kind']}*: {item['item']} — {item['reason']}")
    lines.append("")
    return lines


def _md_verification_lint(section: dict) -> list[str]:
    lines = ["### verification_lint", ""]
    lines.append(f"- Gaps: **{section['gap_count']}** raw / **{section['severe_gap_count']}** severe "
                 f"(overall ok: {_yn(section['ok'])})")
    quotes = section["unattributed_quotes"]
    if quotes:
        lines.append(f"- {len(quotes)} unattributed direct quote(s):")
        for q in quotes[:10]:
            snippet = q["quote"][:80] + ("..." if len(q["quote"]) > 80 else "")
            lines.append(f"  - \"{snippet}\"")
    stats = section["uncited_statistics"]
    if stats:
        values = ", ".join(s["value"] for s in stats[:15])
        lines.append(f"- {len(stats)} uncited high-precision statistic(s): {values}")
    disc = section["disclaimer"]
    if disc["applicable"]:
        lines.append(f"- Scoping/disclaimer section present: **{_yn(disc['present'])}**")
    src = section["sourcing"]
    lines.append(f"- End-of-document sourcing statement found: **{_yn(src['has_end_sourcing'])}**")
    lines.append("")
    return lines


def _md_attractor_scan(section: dict) -> list[str]:
    lines = ["### attractor_scan", ""]
    if section["flagged_maneuvers"]:
        lines.append(f"- Flagged defensive maneuvers: {', '.join(section['flagged_maneuvers'])}")
    else:
        lines.append("- No defensive maneuvers flagged.")
    cases = section["flagged_laundering_cases"]
    if cases:
        lines.append(f"- Flagged semantic-laundering cases: {', '.join(cases)}")
        for case_id in cases:
            case = section["laundering"][case_id]
            lines.append(f"  - **{case['name']}** ({case['confidence']} confidence): {case['explanation']}")
    else:
        lines.append("- No semantic-laundering cases flagged.")
    lines.append(f"- Match density: **{section['density']:.3f}**")
    ufo = section.get("unglossed_formal_object")
    if ufo:
        if ufo["flagged"]:
            lines.append(f"- Unglossed Formal Object ({ufo['confidence']} confidence, not a §2.8 case): {ufo['explanation']}")
            for span in ufo["unglossed_spans"]:
                lines.append(f"  - `{span['text']}`")
        else:
            lines.append("- No unglossed formal object flagged.")
    lines.append("")
    return lines


def _md_bifp(section: dict) -> list[str]:
    lines = ["### bifp", ""]
    keys = ("provisionalization", "status_dismissal", "prohibited_anthropomorphic_terms")
    labels = {"provisionalization": "Provisionalization", "status_dismissal": "Status dismissal",
              "prohibited_anthropomorphic_terms": "Prohibited anthropomorphic terms"}
    if not any(section[k]["flagged"] for k in keys):
        lines.append("- Clean: no provisionalization, status-dismissal, or prohibited anthropomorphic terms.")
    else:
        for key in keys:
            entry = section[key]
            if entry["flagged"]:
                lines.append(f"- **{labels[key]}** flagged ({entry['confidence']} confidence): {entry['explanation']}")
    lines.append("")
    return lines


def _md_debasinizer(section: dict) -> list[str]:
    lines = ["### debasinizer", ""]
    res = section["resonance"]
    n_hit = res["distinct_categories_hit"]
    plural = "category" if n_hit == 1 else "categories"
    detail = f": {', '.join(res['categories_hit'])}" if res["categories_hit"] else ""
    lines.append(f"- Resonance register flagged: **{_yn(section['register_flagged'])}** "
                 f"({n_hit} distinct {plural} hit{detail})")
    lines.append(f"- Self-coherence-assertion flagged: **{_yn(section['self_coherence_flagged'])}**")
    lines.append("")
    return lines


def generate_markdown_report(combined: dict) -> str:
    """Render `run_all_scans()`'s output as a Markdown report matching
    this repository's own documentation house style -- including an
    explicit "what this does not establish" closing section, the same
    convention every paper and case study in this repo uses."""
    meta = combined["meta"]
    title = meta["title"] or "Untitled specimen"
    lines = [f"# Paper-Rigor Scan Report: {title}", ""]
    lines.append(f"Generated {meta['generated_at']} · {meta['word_count']} words · "
                 f"{meta['char_count']} characters")
    lines.append("")
    lines.append("Ran entirely in your browser via Pyodide -- the scanned text was never sent "
                 "to any server. Generated by the PIQOS AI Research (Public) toolkit "
                 "(`paper_rigor`, `verification_lint`, `attractor_scan`, `bifp`, `debasinizer`), "
                 "each running its own independent, differently-scoped heuristic check.")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.extend(_md_paper_rigor(combined["paper_rigor"]))
    lines.extend(_md_verification_lint(combined["verification_lint"]))
    lines.extend(_md_attractor_scan(combined["attractor_scan"]))
    lines.extend(_md_bifp(combined["bifp"]))
    lines.extend(_md_debasinizer(combined["debasinizer"]))
    lines.append("## What this report does NOT establish")
    lines.append("")
    lines.append("- **No blended score.** These five checks measure independent, "
                 "differently-scoped things; this report never combines them into a single "
                 "number, deliberately.")
    lines.append("- **No citation verification.** Nothing here checks whether a citation "
                 "actually supports the claim it's attached to, or whether a cited source is credible.")
    lines.append("- **No soundness check.** Nothing here evaluates whether the underlying "
                 "method, math, or experiment design is correct -- these are text-pattern "
                 "heuristics, not a peer review.")
    lines.append("- **Each flag is a lead, not a verdict.** Every positive flag above is a "
                 "candidate for human review, with a documented false-positive/negative rate "
                 "in its own source package's README -- see `tools/<package>/README.md` in the "
                 "[repository](https://github.com/danofairanks/PIQOS---AI---Research-public-) "
                 "for exactly what each check does and does not detect.")
    lines.append("")
    return "\n".join(lines)


def report_as_json(combined: dict) -> str:
    return json.dumps(combined, indent=2)
