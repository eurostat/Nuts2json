#!/usr/bin/env bash

# ETRS89:4258 WM:3857 LAEA:3035
mkdir -p tmp/etrs89
mkdir -p tmp/wm
mkdir -p tmp/laea

for type in "RG" "BN"
do
    echo "Project $type"

    echo "   to ETRS 89"
    ogr2ogr -overwrite -f "ESRI Shapefile" \
        "tmp/etrs89/"$type".shp" \
        "shp/NUTS_"$type"_01M_2013.shp" \
        -t_srs EPSG:4258 -s_srs EPSG:4258

    echo "   to Web Mercator"
    ogr2ogr -overwrite -f "ESRI Shapefile" \
        "tmp/wm/"$type".shp" \
        "shp/NUTS_"$type"_01M_2013.shp" \
        -t_srs EPSG:3857 -s_srs EPSG:4258

    echo "   to LAEA"
    ogr2ogr -overwrite -f "ESRI Shapefile" \
        "tmp/laea/"$type".shp" \
        "shp/NUTS_"$type"_01M_2013.shp" \
        -t_srs EPSG:3035 -s_srs EPSG:4258
done
