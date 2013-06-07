#!/usr/bin/env sh

. $( dirname "$0" )/config.cfg

echo --- iterreg ---
for i in {1..10};
do
    echo [iter $i] \
        Polarity Accuracy = \
        `python $src/main.py eval polarity \
            --pred  $data/iterreg/r$i.txt \
            --truth $data/truth/1.txt`, \
        `python $src/main.py eval polarity \
            --pred  $data/iterreg/r$i.txt \
            --truth $data/truth/2.txt`, \
        Kendall-Tau = \
        `python $src/main.py eval kendall \
            --pred  $data/iterreg/r$i.txt \
            --truth $data/truth/pairs1.txt`, \
        `python $src/main.py eval kendall \
            --pred  $data/iterreg/r$i.txt \
            --truth $data/truth/pairs2.txt`
done
