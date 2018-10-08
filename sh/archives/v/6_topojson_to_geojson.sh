#!/usr/bin/env bash

#produce geojson from topojson
#https://github.com/topojson/topojson-client/blob/master/README.md#topo2geo
for year in "2016" "2013" "2010"
do
  for proj in "3035" "3857" "4258"
  do
    dir="tmp/"$year"/"$proj
    for level in 0 1 2 3
    do
      for size in 1200 1000 800 600 400
      do
        outdir=$year"/"$proj"/"$size"px"
        mkdir -p $outdir

        echo "6- $year $proj $level $size - topojson to geojson"
        topo2geo nutsrg=$outdir"/nutsrg_"$level".json" nutsbn=$outdir"/nutsbn_"$level".json" cntrg=$outdir"/cntrg.json" cntbn=$outdir"/cntbn.json" gra=$outdir"/gra.json" < $outdir"/"$level".json"
      done
    done
  done
done
