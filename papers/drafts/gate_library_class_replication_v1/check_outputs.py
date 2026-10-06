"""Compare a freshly produced probe output with the committed one, ignoring random token ids and timestamps. Exit 1 on any difference."""
import json, re, sys
def norm(o):
    s = json.dumps(o, sort_keys=True)
    s = re.sub(r"Token [0-9a-f]{16} already consumed", "Token <id> already consumed", s)
    s = re.sub(r"[0-9a-f]{16,32}", "<hex>", s)
    return json.loads(s)
a, b = norm(json.load(open(sys.argv[1]))), norm(json.load(open(sys.argv[2])))
bad = [k for k in sorted(set(a) | set(b)) if a.get(k) != b.get(k)]
print("DIFF:" if bad else "SAME:", bad if bad else f"{len(a)} keys")
sys.exit(1 if bad else 0)
