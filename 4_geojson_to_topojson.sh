#!/usr/bin/env bash

#make topojson base files, one per nuts level
#https://github.com/topojson/topojson-server/blob/master/README.md#geo2topo
for year in "2016" "2013" "2010"
do
  for scale in "10" "20" "60"
  do
    for proj in "3035" "3857" "4258"
    do
      dir="tmp/$year/$scale/$proj"
      for level in 0 1 2 3
      do
        echo "4- $year $scale $proj $level - geojson to topojson"
        geo2topo -q 20000 nutsrg=$dir"/RG/"$level".json" nutsbn=$dir"/BN/"$level".json" cntrg=$dir"/RG/CNTR.json" cntbn=$dir"/BN/CNTR.json" gra=$dir"/graticule.json" > $dir"/"$level".json"
        #quantization: q small means strong 'simplification'
      done
    done
  done
done
