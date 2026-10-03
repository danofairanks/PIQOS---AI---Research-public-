#!/usr/bin/env python3
"""Checks on the start-here repository (exact clone). Usage: attacks_start_here.py <repo_root>   (needs full git history)
Predictions written before this script (from earlier static and live reads): SH1 the composition of Evaluator and commit_gate is wired only in
the measured-mutation fixture, not in run_demo.py; SH2 golden corpus: Evaluator agrees on 15/15 verdicts and 12/15 strictly (reason-code only
differences); SH3 the demonstrated engine denies deploy and commit as unknown_action while the core registry knows both as mutating, and ignores
an unknown key; SH4 every commit touching expected/*.json also touches src/engine.py or src/paradox.py; SH5 the shipped scenarios use deploy/commit
only inside paradox cases.
"""
import ast, json, os, re, subprocess, sys
ROOT = os.path.abspath(sys.argv[1]); sys.path.insert(0, ROOT); os.chdir(ROOT)
out = {}
def git(*a): return subprocess.run(["git", *a], capture_output=True, text=True, check=True).stdout
# SH1 call sites of commit_gate( and Evaluator( outside tests; does run_demo import core?
def callers(name):
    hits = []
    for dp, dn, fn in os.walk("."):
        if ".git" in dp or dp.startswith("./tests"): continue
        for f in fn:
            if f.endswith(".py"):
                p = os.path.join(dp, f)
                for i, line in enumerate(open(p, encoding="utf8"), 1):
                    if re.search(r"\b%s\(" % name, line) and not re.match(r"\s*(def|class)\s", line) and not line.lstrip().startswith("#"): hits.append(f"{p[2:]}:{i}")
    return hits
rd = open("run_demo.py", encoding="utf8").read()
out["SH1_composition"] = {"commit_gate_callers_outside_tests": callers("commit_gate"), "Evaluator_callers_outside_tests": callers("Evaluator"),
                          "run_demo_imports_core": bool(re.search(r"from core|import core", rd)), "run_demo_imports_src_engine": "engine" in rd}
# SH2 golden corpus: reference implementation vs Evaluator
from core.golden_corpus import GOLDEN_CORPUS
from core.conformance import evaluate_packet
from core.evaluator import Evaluator
ev = Evaluator(); seen = set(); vagree = sagree = 0; diffs = []
for c in GOLDEN_CORPUS:
    a = evaluate_packet(c.packet_raw, seen); r = ev.evaluate(c.packet_raw)
    v = a["verdict"] == r.verdict; s = v and a["reason_code"] == r.reason_code and a["executed"] == r.executed
    vagree += v; sagree += s
    if not s: diffs.append([c.case_id, a["reason_code"], r.reason_code])
out["SH2_golden_corpus_vs_Evaluator"] = {"cases": len(GOLDEN_CORPUS), "verdict_agree": vagree, "strict_agree": sagree, "strict_differences": diffs}
# SH3 engine vs core registry
from src.engine import GovernanceEngine, KNOWN_ACTIONS
from core.algebra import Action
base = {"name": "t", "actor": "a", "target": "/x", "authority": "valid", "policy": "allowed", "flags": {}}
def dec(**kw):
    e = GovernanceEngine(); s = {**base, "request_id": "R-" + str(len(kw)) + "-" + "-".join(map(str, kw.values())), **kw}; return e.decide(s)
out["SH3_engine_vs_registry"] = {"engine_KNOWN_ACTIONS": sorted(KNOWN_ACTIONS),
    "engine_write": dec(action="write")["decision"], "engine_deploy": [dec(action="deploy")["decision"], dec(action="deploy")["reason_code"]],
    "engine_commit": [dec(action="commit")["decision"], dec(action="commit")["reason_code"]],
    "core_registry_deploy_known_mutating": [Action("deploy", "/x").is_known(), Action("deploy", "/x").is_mutating()] if True else None,
    "core_registry_commit_known_mutating": [Action("commit", "/x").is_known(), Action("commit", "/x").is_mutating()],
    "engine_ignores_unknown_key_expired": dec(action="write", expired=True)["decision"]}
# SH4 fixture and implementation co-commit
commits = git("log", "--format=%H", "--", "expected").split()
co = []
for h in commits:
    files = git("show", "--name-only", "--format=", h).split()
    co.append(any(f in ("src/engine.py", "src/paradox.py") for f in files))
out["SH4_fixture_commits"] = {"commits_touching_expected": len(commits), "also_touching_engine_or_paradox": sum(co), "total_commits": len(git("log", "--format=%H").split())}
# SH5 deploy/commit in shipped scenarios
uses = {}
for f in sorted(os.listdir("scenarios")):
    d = json.load(open(os.path.join("scenarios", f)))
    if d.get("action") in ("deploy", "commit"):
        uses[f] = {"action": d["action"], "flags": sorted(k for k, v in d.get("flags", {}).items() if v), "expected": json.load(open(os.path.join("expected", f))).get("decision")}
out["SH5_deploy_commit_scenarios"] = uses
print(json.dumps(out, indent=1))
