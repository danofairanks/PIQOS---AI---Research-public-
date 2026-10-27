#!/bin/bash
# deletes per-module setup json files (about 5.6 MB each, regenerated on demand) of modules finished more than 2 minutes ago
while pgrep -f "bin/comparator Comparator" >/dev/null; do
  n=$(find /srv/lean/proj/.lake/build/ir -name '*.setup.json' -mmin +2 -print -delete 2>/dev/null | wc -l)
  echo "$(date -u +%FT%TZ) pruned $n setup.json; free $(df -BM / | awk 'NR==2{print $4}')" >> /srv/lean/prune_ir.log
  sleep 90
done
echo "$(date -u +%FT%TZ) comparator gone; pruner exit" >> /srv/lean/prune_ir.log
