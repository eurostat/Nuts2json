#!/usr/bin/env bash

#produce geojson from topojson
#https://github.com/topojson/topojson-client/blob/master/README.md#topo2geo
for year in "2013" "2016"
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

        echo "$year $proj $level $size - topojson to geojson"
        topo2geo nutsrg=$outdir"/nutsrg_"$level".geojson" nutsbn=$outdir"/nutsbn_"$level".geojson" cntrg=$outdir"/cntrg.geojson" cntbn=$outdir"/cntbn.geojson" < $outdir"/"$level".topojson"
      done
    done
  done
done
