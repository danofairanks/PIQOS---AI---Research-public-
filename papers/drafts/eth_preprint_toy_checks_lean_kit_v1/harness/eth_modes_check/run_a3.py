import sys, json
sys.path.insert(0, '.')
from modes_check import test_D
r = test_D(3, 3, seed=7, trials=1)
print("D_a3", r, flush=True)
json.dump(r, open("modes_D_a3.json", "w"))
