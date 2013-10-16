#!/usr/bin/env sh

. $( dirname "$0" )/config.cfg

python $src/main.py lookup \
    --nodes $data/graph/nodes.tsv \
    --anew  $data/seeds/anew.tsv \
    --sn    $data/seeds/sn.tsv \
    --pred  $data/iterreg_randwalk_in/r1.txt \
    --rels  $data/graph/rels.tsv \
    --edges $data/graph/edges.tsv
