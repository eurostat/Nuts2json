#!/usr/bin/env bash

projs=("etrs89" "wm" "laea")
epsgs=("4258" "3857" "3035")
xmin=(-12.5 -1490000 2434550)
ymin=(32.5 3884000 1340330)
xmax=(46.5 5200000 7512400)
ymax=(73.9 11690000 5664600)

for pi in ${!projs[@]}
do
    proj=${projs[pi]}
    epsg=${epsgs[pi]}
    mkdir -p tmp/$proj
    for type in "RG" "BN"
    do
        echo "Project $type to $proj"
        ogr2ogr -overwrite -f "ESRI Shapefile" \
            "tmp/"$proj"/"$type"_proj.shp" \
            "shp/NUTS_"$type"_01M_2013.shp" \
            -t_srs EPSG:$epsg -s_srs EPSG:4258

        echo "Clip $type"
        ogr2ogr -overwrite -f "ESRI Shapefile" \
            "tmp/"$proj"/"$type".shp" \
            "tmp/"$proj"/"$type"_proj.shp" \
            -clipsrc ${xmin[pi]} ${ymin[pi]} ${xmax[pi]} ${ymax[pi]}
    done
done
