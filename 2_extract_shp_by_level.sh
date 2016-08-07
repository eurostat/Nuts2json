#!/usr/bin/env bash

mkdir -p tmp/shpbylevel
for level in 0 1 2 3
do
    echo "Extract nuts level $level"
    ogr2ogr -overwrite -where STAT_LEVL_=$level tmp/shpbylevel/rg_lvl$level.shp shp/NUTS_RG_01M_2013.shp
done
