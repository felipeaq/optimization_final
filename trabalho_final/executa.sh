#!/bin/bash
for i in instancias/k*.dat instancias/F25.dat
do
    for j in $(seq 1 10); do  python arc_heuristic.py $i ; done

done
