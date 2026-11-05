"""Do the double-quoted strings in a reading occur in the text layer of the PDF it reads?
Run: python3 -I quote_checks.py reading.md paper.pdf     (needs pdftotext; the PDF is not stored here)
The text layer is read three ways (default, -layout, -raw) because two-column pages interleave in some of them. Strings of at least 3 words inside straight or curly double quotes are checked after normalising whitespace, quote marks,
dashes, ligatures and line-break hyphenation. FOUND/NOT FOUND is a lexical test, not a judgement: a quote that is the
reading's own wording, a quotation of another document, or a paraphrase in quotation marks will show as NOT FOUND."""
import re, subprocess, sys, hashlib, unicodedata
md, pdf = sys.argv[1], sys.argv[2]
def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"-\s*\n\s*", "", s)                       # line-break hyphenation
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"[‐-―−]", "-", s)
    s = s.replace("ﬁ", "fi").replace("ﬂ", "fl")
    return re.sub(r"\s+", " ", s).strip().lower()
text = " ".join(norm(subprocess.run(["pdftotext"] + mode + [pdf, "-"], capture_output=True, text=True).stdout) for mode in ([], ["-layout"], ["-raw"]))  # three extraction orders: columns interleave in some
body = open(md, encoding="utf-8").read()
quotes = [q for q in re.findall(r'(?<![\w.,;:!?)\]])["\u201c]([^"\u201c\u201d\n]{12,300}?)["\u201d](?![\w])', body) if len(q.split()) >= 3]  # an opening quote must not follow a word character or punctuation
seen, found, miss = set(), 0, []
for q in quotes:
    n = norm(q.rstrip(".,;:"))
    if n in seen: continue
    seen.add(n)
    if n in text: found += 1
    else: miss.append(q)
print(f"pdf sha256 {hashlib.sha256(open(pdf,'rb').read()).hexdigest()}")
print(f"{found}/{len(seen)} quoted strings found in the PDF text layer")
for q in miss: print("  NOT FOUND:", q)
