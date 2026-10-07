#!/bin/bash
# usage: run_cmp.sh Name  (runs the Comparator on ComparatorChallenges/Name.json as an unprivileged user, no network)
n=$1
unshare -n setpriv --reuid=65534 --regid=65534 --clear-groups env -i bash -c "source /srv/lean/env.sh; export PATH=\$PATH:/srv/lean; export COMPARATOR_LANDRUN=/srv/lean/landrun COMPARATOR_LEAN4EXPORT=/srv/lean/tools/lean4export/.lake/build/bin/lean4export; cd /srv/lean/proj; lake env /srv/lean/tools/comparator/.lake/build/bin/comparator ComparatorChallenges/$n.json" > /srv/lean/cmp_$n.log 2>&1
echo "$n exit=$? $(tail -1 /srv/lean/cmp_$n.log | cut -c1-120)"
