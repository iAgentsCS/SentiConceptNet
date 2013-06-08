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

for approach in randwalk_out randwalk_in iterreg_randwalk_out iterreg_randwalk_in;
do
    echo --- ${approach} ---
    for i in {1..9};
    do
        echo [alpha 0.$i] \
            Polarity Accuracy = \
            `python $src/main.py eval polarity \
                --pred  $data/${approach}/r$i.txt \
                --truth $data/truth/1.txt`, \
            `python $src/main.py eval polarity \
                --pred  $data/${approach}/r$i.txt \
                --truth $data/truth/2.txt`, \
            Kendall-Tau = \
            `python $src/main.py eval kendall \
                --pred  $data/${approach}/r$i.txt \
                --truth $data/truth/pairs1.txt`, \
            `python $src/main.py eval kendall \
                --pred  $data/${approach}/r$i.txt \
                --truth $data/truth/pairs2.txt`
    done
done

echo --- SenticNet ---
echo \
    Polarity Accuracy = \
    `python src/main.py eval polarity \
        --pred $data/graph/sn.tsv \
        --truth $data/truth/1.txt`, \
    Kendall-Tau = \
    `python $src/main.py eval kendall \
        --pred $data/graph/sn.tsv \
        --truth $data/truth/pairs1.txt`
