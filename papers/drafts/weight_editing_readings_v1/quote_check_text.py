"""Do the double-quoted strings in a reading occur in the saved text of its sources?
Run: python3 -I quote_check_text.py reading.md source1.txt [source2 ...]   (PDF sources: pass the pdftotext output)
Strings of at least 3 words inside straight or curly double quotes are tested after normalising case, quotes, dashes, ligatures and whitespace.
FOUND/NOT FOUND is lexical: a quote that is the reading's own wording, a title quoted from elsewhere, or a paraphrase in quotation marks will show as NOT FOUND."""
import re, sys, hashlib, unicodedata
md, srcs = sys.argv[1], sys.argv[2:]
def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"-\s*\n\s*", "", s)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"[‐-―−]", "-", s)
    return re.sub(r"\s+", " ", s).strip().lower()
text = " ".join(norm(open(f, encoding="utf8", errors="ignore").read()) for f in srcs)
body = open(md, encoding="utf-8").read()
quotes = [q for q in re.findall(r'(?<![\w.,;:!?)\]])["“]([^"“”\n]{12,300}?)["”](?![\w])', body) if len(q.split()) >= 3]
seen, found, miss = set(), 0, []
for q in quotes:
    n = norm(q.rstrip(".,;:"))
    if n in seen: continue
    seen.add(n)
    if n in text: found += 1
    else: miss.append(q)
print(f"{found}/{len(seen)} quoted strings found in the source text ({len(srcs)} source file(s))")
for q in miss: print("  NOT FOUND:", q)
