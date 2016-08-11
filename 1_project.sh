#!/usr/bin/env bash

projs=("etrs89" "wm" "laea")
epsgs=("4258" "3857" "3035")

for pi in ${!projs[@]}
do
    proj=${projs[pi]}
    epsg=${epsgs[pi]}
    mkdir -p tmp/$proj
    for type in "RG" "BN"
    do
        echo "Project $type to $proj"
        ogr2ogr -overwrite -f "ESRI Shapefile" \
            "tmp/"$proj"/"$type".shp" \
            "shp/NUTS_"$type"_01M_2013.shp" \
            -t_srs EPSG:$epsg -s_srs EPSG:4258
    done
done
