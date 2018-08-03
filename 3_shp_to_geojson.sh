#!/usr/bin/env bash

for year in "2013" "2016"
do
  for proj in "etrs89" "laea" "wm"
  do
    for type in "RG" "BN"
    do

      dir="tmp/"$year"/"$proj"/"$type

      for level in 0 1 2 3
      do
        echo "$year $proj $level $type - SHP to geojson"
		rm -f $dir"/"$level".json"
	    ogr2ogr -overwrite -f geoJSON $dir"/"$level".json" $dir"/"$level".shp"

      done
    done
  done
done
