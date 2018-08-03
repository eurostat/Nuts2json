#!/usr/bin/env bash

for year in "2013" "2016"
do

  for proj in "laea" "wm" "etrs89"
  do
    for level in 0 1 2 3
    do
      for type in "RG" "BN"
      do
        echo "$year $proj $level $type - SHP to geojson"

		    dir="tmp/$year/$proj/"$type"bylevel"

			rm -f $dir"/"$level".json"

	        ogr2ogr -overwrite -f geoJSON \
    	        $dirRG"/RG_lvl"$level".json" \
				$dirRG"/RG_lvl"$level".shp"

      done
    done
  done
done
