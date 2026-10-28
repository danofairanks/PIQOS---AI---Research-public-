#!/bin/bash
cd "$(dirname "$0")"
for cfg in "2 3 2" "2 3 3" "3 2 2"; do python3 run_tests.py sweep $cfg 4 5 12 > log_sweep_n4_${cfg// /_}.txt 2>&1; done
for cfg in "2 3 2" "2 3 3" "3 2 2"; do python3 run_tests.py sweep $cfg 5 7 8 > log_sweep_n5_${cfg// /_}.txt 2>&1; done
echo done > sweep_done.txt
