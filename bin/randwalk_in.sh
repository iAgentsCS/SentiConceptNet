#!/usr/bin/env sh

. $( dirname "$0" )/config.cfg

mkdir -p $data/randwalk_in
for i in {1..9};
do
    python $src/main.py randwalk \
        --edges $data/graph/edges.tsv \
        --seed  $data/seeds/anew.tsv \
        --pred  $data/randwalk_in/r$i.txt \
        --cin   $data/certainty/anew.txt \
        --cout  $data/certainty/randwalk_in_$i.txt \
        --alpha 0.$i \
        --axis 1
done
