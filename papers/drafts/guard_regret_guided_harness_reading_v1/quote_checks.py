"""Quote and number check for the reading: every quoted string in the reading, and each printed number it cites, must occur in the
paper's text. Usage: python3 quote_checks.py <pdf_text_file> ; text extracted with `pdftotext paper.pdf out.txt` (default reading
order, not -layout, because the paper is two-column). The PDF is not stored here (sha256 in the output).
Normalisation: unicode NFKC, join line breaks, collapse whitespace, remove hyphenation at line ends."""
import sys, re, unicodedata
txt = open(sys.argv[1], encoding='utf-8', errors='ignore').read()
def norm(s):
    s = unicodedata.normalize('NFKC', s)
    s = re.sub(r'-\n\s*', '', s)
    s = re.sub(r'\s+', ' ', s)
    return s.strip()
T = norm(txt)
QUOTES = [
 "guaranteeing non-regression on its gated buffer",
 "At test time, one frozen harness runs in a single pass",
 "consistently improves performance without catastrophic forgetting or memory pollution",
 "substantially cutting deployment token usage",
 "rather than a non-vacuous finite-sample certificate at our benchmark task counts",
 "hold within each round’s gated task buffer rather than telescoping unconditionally across distribution shifts",
 "The GUARD row is the final of five hosted configurations evaluated on this test split",
 "mean 77.09%, range 75.57–80.80%; all five above every baseline",
 "every unresolved invariant fails a derived criterion",
 "formal non-regression guarantees on the self-review objective",
 "reads only the task prompt, visible tool declarations, and schema once at Turn 0",
 "checks execution predicates deterministically on an ephemeral sandbox copy",
 "grades semantic predicates individually",
 "The incumbent score used by the gate is the score recorded when the incumbent was itself evaluated",
 "cutting hosted tokens per task by 54.5%",
 "seed 42",
 "we plan to release reference harness code",
 "subject to approval",
 "drops five-domain macro accuracy by −10.35pp",
 "reduces five-domain macro accuracy by −7.33pp",
 "an unvetted Stage-v4 candidate instructs a hallucinated MCP tool call",
 "69.86% ± 0.18pp",
 "its original-distiller control at 75.57%",
 "the initial one-layer run at 75.98% in Table 4",
 "the 95% CI [+0.00, +31.25] touches 0",
 "with a minor trade-off on strict all-or-nothing solve rate",
 "in which solver, distiller, critic, and grader all use the exact same model",
 "serves as distiller, self-reviewer, critic, and rubric judge",
 "Held-out evaluation draws one rollout per task",
 "whereas full GUARD maintains 0/5 regressed domains",
 "360 adaptation / 360 held-out test rollouts per arm",
 "Paired over the 43 test tasks (exact sign-flip test)",
 "p = 0.11; 95% bootstrap CI [−0.4, +14.5]pp",
]
NUMBERS = ["59,651", "131,032", "78,705", "167.6", "158.8", "233.8", "45.97%", "73.90%", "82.6%", "4,059", "82.2%", "75.6%", "169", "0.369", "19/19", "p = 0.008", "p = 0.023", "p = 0.010", "p = 0.094", "80.80", "74.52", "77.09", "76.69%", "76.42%", "59.13%", "56.11%", "66.46%", "7.61%", "0.18pp"]
print('quote check against', sys.argv[1])
missing = 0
for q in QUOTES:
    ok = norm(q) in T
    missing += (not ok)
    print(('FOUND   ' if ok else 'MISSING ') + q[:110])
print(f'{len(QUOTES)-missing}/{len(QUOTES)} quoted strings found in the text layer')
nm = 0
for n in NUMBERS:
    ok = norm(n) in T
    nm += (not ok)
    print(('FOUND   ' if ok else 'MISSING ') + 'number ' + n)
print(f'{len(NUMBERS)-nm}/{len(NUMBERS)} cited printed numbers found in the text layer')
