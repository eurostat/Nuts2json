#!/usr/bin/env bash

mkdir -p json/topojson
for level in 0 1 2 3
do
    echo "Produce topojson for level $level"
    topojson -o json/topojson/rg_lvl$level.json nutsrg=tmp/shpbylevel/rg_lvl$level.shp
done
