#!/usr/bin/env python3
"""Fills the results table and counts into the paper template. Usage: build_paper.py <template.md> <out.md> <table.md> <accepted> <rejected> <unfinished>"""
import sys
tpl, out, table, a, r, u = sys.argv[1:7]
s = open(tpl).read().replace('{{TABLE}}', open(table).read().strip()).replace('{{ACC}}', a).replace('{{REJ}}', r).replace('{{UNF}}', u)
open(out, 'w').write(s)
