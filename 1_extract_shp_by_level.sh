#!/usr/bin/env bash

mkdir shp/bylevel
for level in 0 1 2 3
do
    echo "Extract nuts level $level"
    ogr2ogr -overwrite -where STAT_LEVL_=$level shp/bylevel/rg_lvl$level.shp shp/input/NUTS_RG_01M_2013.shp
done
