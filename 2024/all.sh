#!/bin/sh
for i in $(seq -f '%02g' 1 25); do
    echo "Day $i"
    cd "day$i/" || exit
    time python3 "day$i.py" -h
    cd ..
done
