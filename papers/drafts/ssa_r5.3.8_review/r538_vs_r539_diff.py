"""Word-level comparison of SSA R5.3.8 and R5.3.9 (usage: python3 r538_vs_r539_diff.py R5.3.8.pdf R5.3.9.pdf > output.txt).
Page headers/footers and version labels are masked before comparing so that only body text differs.
Needs pymupdf (pip install pymupdf). Prints the unchanged share, the removed/added word counts and every non-equal segment (first 140 characters)."""
import difflib, re, sys
import pymupdf

def words(path):
    t = " ".join(p.get_text() for p in pymupdf.open(path))
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r"ŠKRINJAR STRUCTURAL ARCHITECTURE / [A-Z0-9\. ]+ SSA(?: R5\.3\.\d)? · Canonical Architectural Specification ·(?: \d\d \w+ 2026)?", "", t)
    t = re.sub(r"(R5\.3\.\d )+\d\d (September|October) 2026", "", t)
    t = re.sub(r"\bR5\.3\.\d\b", "R5.3.x", t)
    return t.split()

a, b = words(sys.argv[1]), words(sys.argv[2])
removed = added = 0
for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
    if tag == "equal":
        continue
    removed += i2 - i1; added += j2 - j1
    print(tag, f"[-{i2-i1} +{j2-j1}]", "OLD:", " ".join(a[i1:i2])[:140], "| NEW:", " ".join(b[j1:j2])[:140])
print(f"words in R5.3.8 (masked) {len(a)}, R5.3.9 (masked) {len(b)}; removed {removed}, added {added}; share of R5.3.8 words unchanged {1 - removed/len(a):.3f}")
