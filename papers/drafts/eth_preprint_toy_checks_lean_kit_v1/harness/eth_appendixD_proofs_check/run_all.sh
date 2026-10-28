#!/bin/bash
cd "$(dirname "$0")"
python3 appendixD_proofs_check.py D4 > log_D4.txt 2>&1 &
python3 appendixD_proofs_check.py val > log_val.txt 2>&1 &
python3 appendixD_proofs_check.py D5 > log_D5.txt 2>&1 &
python3 appendixD_proofs_check.py D3 > log_D3.txt 2>&1 &
wait
echo done > run_all_done.txt
