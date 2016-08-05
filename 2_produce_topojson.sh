#!/usr/bin/env bash

mkdir json
for level in 0 1 2 3
do
    echo "Produce topojson for level $level"
    topojson -o json/rg_lvl$level.json nutsrg=shp/bylevel/rg_lvl$level.shp
done
