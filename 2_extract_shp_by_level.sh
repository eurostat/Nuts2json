#!/usr/bin/env bash

for proj in "etrs89" "laea" "wm"
do
    echo "Extract nuts level - "$proj

    #make folders
    dirRG="tmp/"$proj"/RGbylevel"
    dirBN="tmp/"$proj"/BNbylevel"
    mkdir -p $dirRG
    mkdir -p $dirBN

    for level in 0 1 2 3
    do
        echo "   RG level "$level
        ogr2ogr -overwrite -where STAT_LEVL_=$level $dirRG"/RG_lvl"$level".shp" "tmp/"$proj"/RG.shp"
        echo "   BN level "$level
        ogr2ogr -overwrite -sql "SELECT * FROM BN WHERE STAT_LEVL_<="$level $dirBN"/BN_lvl"$level".shp" "tmp/"$proj"/BN.shp"
    done
done
