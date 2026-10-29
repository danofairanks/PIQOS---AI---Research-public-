# DECOY. Not the paper's method. Replaces the decoupled-evaluation loop of eth_sections345_run.run_system with the
# brute-force Taylor data. Everything downstream (Hermite recovery, per-V-coefficient and count checks) is the real code.
import sys, os, inspect, re
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "eth_sections345_run")
os.chdir(ROOT)
sys.path.insert(0, ROOT)
import sections345_run as S

def make_decoy_run_system():
    src = inspect.getsource(S.run_system)
    a = src.index("    for t in range(1, Q+1):\n        design = ctr.design_at(t)")
    b = src.index("    taylor_ok = None")
    repl = ("    for s in range(l):\n        for t in range(1, Q+1):\n"
            "            taylor[s][t-1] = ec.trim(brute_taylor[s][t-1], J)\n")
    src2 = src[:a] + repl + src[b:]
    src2 = src2.replace("def run_system(", "def decoy_run_system(", 1)
    exec(compile(src2, "<decoy_run_system>", "exec"), S.__dict__)
    return S.decoy_run_system
