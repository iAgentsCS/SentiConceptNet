#!/usr/bin/env sh

. $( dirname "$0" )/config.cfg

mkdir -p $data/graph
python $src/main.py split \
    --graph $data/raw/conceptnet5/conceptnet4_[0-4].csv \
    --nodes $data/graph/nodes.tsv \
    --edges $data/graph/edges.tsv \
    --rels  $data/graph/rels.tsv
