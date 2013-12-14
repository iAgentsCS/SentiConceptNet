#!/usr/bin/env sh

. $( dirname "$0" )/config.cfg

mkdir -p $data/iterreg_randwalk_out
for i in {1..9};
do
    python $src/main.py randwalk \
        --edges $data/graph/edges.tsv \
        --seed  $data/iterreg/r3.txt \
        --pred  $data/iterreg_randwalk_out/r$i.txt \
        --cin   $data/certainty/iterreg.txt \
        --cout  $data/certainty/iterreg_randwalk_in_$i.txt \
        --alpha 0.$i \
        --axis 0
done
