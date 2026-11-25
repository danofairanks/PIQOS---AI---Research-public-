#!/usr/bin/env python3
"""Recount the ownership table of a public reconstruction repository (Addendum A.14).

Usage: python3 -I recount_ownership.py PATH/TO/Global_Ownership.tsv.gz

Reads the gzipped table (columns: declaration, kind, class, file:line, liveness, status, owner_or_evidence)
and prints, for the exact-edge live rows, the count by status and, within the status
"CLOSED VIA PRIOR PACKAGE", the count by kind of evidence taken from the owner string.
Standard library only. Reads data; runs none of the repository's code.
"""
import collections
import gzip
import sys

path = sys.argv[1]
by_live_status = collections.Counter()
evidence = collections.Counter()
rows = 0
with gzip.open(path, "rt", errors="replace") as f:
    header = f.readline().rstrip("\n").split("\t")
    for line in f:
        parts = line.rstrip("\n").split("\t")
        rows += 1
        declaration, kind, cls, loc, liveness, status, owner = parts[:7]
        by_live_status[(liveness, status)] += 1
        if liveness.startswith("LIVE") and status == "CLOSED VIA PRIOR PACKAGE":
            if owner.startswith("region of "):
                evidence["inherited from a mentioned ancestor theorem (region)"] += 1
            elif owner.startswith("shared Lean-internal"):
                evidence["shared remainder (leftover live theorems)"] += 1
            elif owner.startswith("definition, no proof obligation"):
                evidence["definitions (closed by kind)"] += 1
            else:
                evidence["declaration-level evidence (a named report or exclusive set)"] += 1

print("header:", header)
print("rows:", rows)
for key in sorted(by_live_status):
    print(key, by_live_status[key])
live = sum(v for (liveness, status), v in by_live_status.items() if liveness.startswith("LIVE"))
print("exact-edge live total:", live)
print("closed via prior package, by kind of evidence:")
for key, v in sorted(evidence.items(), key=lambda kv: -kv[1]):
    print("  ", key, v)
print("closed via prior package total:", sum(evidence.values()))
