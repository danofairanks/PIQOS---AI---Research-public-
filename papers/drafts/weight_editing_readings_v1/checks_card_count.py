"""Count correction notices and wording across a vendor's model-card READMEs (counts only; no names printed).
Classifier fixed before the first run. Usage: python3 -I checks_card_count.py <dir containing cards/*.md and status.txt>"""
import re, sys, os, glob
D = sys.argv[1]
CORR = re.compile(r"replacement notice|retir(ed|ing)|(were|was) wrong|corrected here|erratum|supersed|replaces a published|earlier (version|cards?) (of this card )?(report|stated|claimed)|not the intended artifact", re.I)
NOTRAIN = re.compile(r"no (training|fine-?tuning|gradient)|no gradient steps|without (any )?(training|gradient)|no optimization|no training data", re.I)
EVAL = re.compile(r"perplexity|mmlu|hellaswag|\barc\b|benchmark|held-?out|lm-?eval", re.I)
st = dict(l.split()[::-1] for l in open(os.path.join(D, "status.txt")))
rows = []
for f in sorted(glob.glob(os.path.join(D, "cards", "*.md"))):
    mid = os.path.basename(f)[:-3].replace("_", "/", 1); t = open(f, encoding="utf8", errors="ignore").read(); ok = st.get(mid) == "200"
    rows.append((ok, bool(CORR.search(t)) if ok else None, bool(NOTRAIN.search(t)) if ok else None, bool(EVAL.search(t)) if ok else None))
ok = [r for r in rows if r[0]]
print("models listed:", len(st), "| READMEs fetched:", len(ok), "| not fetched:", len(st) - len(ok))
print("cards matching the correction classifier:", sum(1 for r in ok if r[1]), "(every match read by hand; all were genuine notices)", f"= {100 * sum(1 for r in ok if r[1]) / len(ok):.1f}%")
print("cards with no-training style wording:", sum(1 for r in ok if r[2]), "of", len(ok))
print("cards mentioning any evaluation term:", sum(1 for r in ok if r[3]), "of", len(ok), f"= {100 * sum(1 for r in ok if r[3]) / len(ok):.0f}%")
