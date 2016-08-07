#!/usr/bin/env bash

mkdir -p json/topojson
for proj in "etrs89" "laea" "wm"
do
    for level in 0 1 2 3
    do
        echo "Produce topojson for level $level and projection $proj"
        topojson -o "json/topojson/RG_lvl"$level"_"$proj".json" "nutsrg=tmp/"$proj"/RGbylevel/RG_lvl"$level".shp"
        topojson -o "json/topojson/BN_lvl"$level"_"$proj".json" "nutsbn=tmp/"$proj"/BNbylevel/BN_lvl"$level".shp"
        topojson -o "json/topojson/RG_BN_lvl"$level"_"$proj".json" "nutsrg=tmp/"$proj"/RGbylevel/RG_lvl"$level".shp" "nutsbn=tmp/"$proj"/BNbylevel/BN_lvl"$level".shp"
    done
done
