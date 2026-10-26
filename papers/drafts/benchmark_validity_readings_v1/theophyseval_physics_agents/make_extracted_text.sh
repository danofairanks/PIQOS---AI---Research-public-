#!/bin/bash
# Builds extracted_text.txt (per-page `pdftotext -layout`, with =====PAGE n===== markers) from the paper's PDF, as checks_from_reported_tables.py expects.
# Usage: bash make_extracted_text.sh /path/to/2610.16733v1.pdf   (run in this folder; the extracted text is not stored in the repository)
PDF="$1"; N=$(pdfinfo "$PDF" | awk '/Pages/{print $2}'); : > extracted_text.txt
for p in $(seq 1 $N); do echo "=====PAGE $p=====" >> extracted_text.txt; pdftotext -layout -f $p -l $p "$PDF" - | tr -d '\f' >> extracted_text.txt; echo >> extracted_text.txt; done
