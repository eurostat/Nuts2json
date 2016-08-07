#!/usr/bin/env bash

for proj in "etrs89" "laea" "wm"
do
    echo "Projection "$proj
    dir="tmp/"$proj"/RGbylevel"
    mkdir -p $dir

    for level in 0 1 2 3
    do
        echo "   Extract nuts level "$level
        ogr2ogr -overwrite -where STAT_LEVL_=$level $dir"/RG_lvl"$level".shp" "tmp/"$proj"/RG.shp"
    done
done
