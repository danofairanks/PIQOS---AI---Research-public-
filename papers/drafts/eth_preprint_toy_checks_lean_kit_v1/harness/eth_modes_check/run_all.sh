#!/bin/bash
cd "$(dirname "$0")"
python3 modes_check.py AB > log_AB.txt 2>&1 &
python3 modes_check.py C > log_C.txt 2>&1 &
python3 modes_check.py D > log_D.txt 2>&1 &
wait
echo done > done.txt
