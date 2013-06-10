#!/usr/bin/env sh

. $( dirname "$0" )/config.cfg

mkdir -p $data/seeds
python $src/main.py seed anew \
    --raw   $data/raw/anew.csv \
    --seed  $data/seeds/anew.tsv \
    --nodes $data/graph/nodes.tsv
python $src/main.py seed sn \
    --raw   $data/raw/senticnet.rdf.xml \
    --seed  $data/seeds/sn.tsv \
    --nodes $data/graph/nodes.tsv
