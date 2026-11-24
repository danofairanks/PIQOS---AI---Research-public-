#!/usr/bin/env python3
"""IUP-1 run-sheet generator. Deterministic (seeded) so the order is reproducible and fixed before any run.
Usage: python3 make_run_sheet.py full|min  > run_sheet_<mode>.tsv
Columns: transcript_id (random, condition-free), run_order, model, task, condition.
The condition column is the operator's KEY; keep it out of the files handed to the scorer."""
import random, sys, hashlib
SEED = 20261123
TASKS = {"P": ["P1","P2","P3","P4"], "U": ["U1","U2","U3","U4"], "F": ["F1","F2","F3","F4"]}
mode = sys.argv[1] if len(sys.argv) > 1 else "full"
rng = random.Random(SEED)
if mode == "full":
    tasks, models, conds = [t for k in TASKS for t in TASKS[k]], ["ChatGPT","Gemini"], ["N","D","DC","S"]
elif mode == "min":
    tasks = [t for k in TASKS for t in rng.sample(TASKS[k], 2)]   # 2 per category
    models, conds = ["ChatGPT"], ["N","D","DC"]
else:
    sys.exit("mode must be full or min")
rows = [(m, t, c) for m in models for t in tasks for c in conds]
rng.shuffle(rows)
print("transcript_id\trun_order\tmodel\ttask\tcondition")
for i, (m, t, c) in enumerate(rows, 1):
    tid = hashlib.sha256(f"{SEED}:{m}:{t}:{c}".encode()).hexdigest()[:8]
    print(f"{tid}\t{i}\t{m}\t{t}\t{c}")
