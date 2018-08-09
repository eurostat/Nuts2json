#!/usr/bin/env bash

for year in "2016" "2013" "2010"
do
for scale in "10" "20" "60"
do
  for proj in "3035" "3857" "4258"
  do

    echo "3- $year $scale $proj - graticule SHP to geojson"
    rm -f "tmp/$year/$scale/$proj/graticule.json"
    ogr2ogr -overwrite -f geoJSON "tmp/$year/$scale/$proj/graticule.json" "tmp/$year/$scale/$proj/graticule.shp"

    for type in "RG" "BN"
    do

      dir="tmp/$year/$scale/$proj/$type"

      echo "3- $year $scale $proj $type - country SHP to geojson"
	  rm -f $dir"/CNTR.json"
      ogr2ogr -overwrite -f geoJSON $dir"/CNTR.json" $dir"/CNTR.shp"

      for level in 0 1 2 3
      do
        echo "3- $year $scale $proj $type - NUTS $level SHP to geojson"
		rm -f $dir"/"$level".json"
	    ogr2ogr -overwrite -f geoJSON $dir"/"$level".json" $dir"/"$level".shp"
      done
    done
  done
done
done
