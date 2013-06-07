#!/usr/bin/env sh

. $( dirname "$0" )/config.cfg
param='-t 0 -c 2.0 -h 0'

mkdir -p $data/iterreg
python $src/main.py iterreg \
    --anew  $data/seeds/anew.tsv \
    --sn    $data/seeds/sn.tsv \
    --edges $data/graph/edges.tsv \
    --pred  $data/iterreg/r1.txt \
    --param "$param"

for i in {2..10};
do
    python $src/main.py iterreg \
        --anew  $data/seeds/anew.tsv \
        --sn    $data/seeds/sn.tsv \
        --edges $data/graph/edges.tsv \
        --pis   $data/iterreg/r$((i - 1)).txt \
        --pred  $data/iterreg/r$i.txt \
        --param "$param"
done
