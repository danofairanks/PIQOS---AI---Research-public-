#!/bin/bash
cd "$(dirname "$0")"
for spec in "2 3 3 6 9 6" "2 3 2 6 9 6" "2 3 3 7 10 4" "2 3 3 8 12 3" "2 3 3 9 13 2"; do
  set -- $spec
  python3 run_tests.py big $1 $2 $3 $4 $5 $6 > log_big_n$4_$1_$2_$3.txt 2>&1
done
echo done > sweep2_done.txt
