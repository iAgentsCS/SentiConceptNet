#!/usr/bin/env sh

. $( dirname "$0" )/config.cfg

for i in {1..9};
do
    python $src/main.py shift mva \
        --seed      $data/seeds/anew.tsv \
        --pred_in   $data/iterreg_randwalk_in/r$i.txt \
        --pred_out  $data/iterreg_randwalk_in/r$i.txt
done
