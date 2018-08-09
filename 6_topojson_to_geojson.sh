#!/usr/bin/env bash

#produce geojson from topojson
#https://github.com/topojson/topojson-client/blob/master/README.md#topo2geo
for year in "2016" "2013" "2010"
do
  for scale in "10" "20" "60"
  do
    for proj in "3035" "3857" "4258"
    do
      dir="tmp/$year/$scale/$proj"
      for level in 0 1 2 3
      do
        echo "6- $year $scale $proj $level - topojson to geojson"
        outdir=$year"/"$proj"/"$scale"M"
        mkdir -p $outdir
        topo2geo nutsrg=$outdir"/nutsrg_"$level".json" nutsbn=$outdir"/nutsbn_"$level".json" cntrg=$outdir"/cntrg.json" cntbn=$outdir"/cntbn.json" gra=$outdir"/gra.json" < $outdir"/"$level".json"
      done
    done
  done
done
