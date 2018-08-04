#!/usr/bin/env bash

#make topojson base files, one per nuts level
#https://github.com/topojson/topojson-server/blob/master/README.md#geo2topo
for year in "2013" "2016"
do
  for proj in "etrs89" "laea" "wm"
  do
    dir="tmp/"$year"/"$proj
    for level in 0 1 2 3
    do
      echo "$year $proj $level - geojson to topojson"
      geo2topo -q 20000 nutsrg=$dir"/RG/"$level".json" nutsbn=$dir"/BN/"$level".json" cntrg=$dir"/RG/CNTR.json" cntbn=$dir"/BN/CNTR.json" > $dir"/"$level".topojson"
      #quantization: q small means strong simplification
    done
  done
done
