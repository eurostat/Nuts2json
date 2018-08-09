#!/usr/bin/env bash

#simplify topojson files
#https://github.com/topojson/topojson-simplify/blob/master/README.md#toposimplify
for year in "2016" "2013" "2010"
do
  for scale in "10" "20" "60"
  do
    for proj in "3035" "3857" "4258"
    do
      dir="tmp/$year/$scale/$proj"
      for level in 0 1 2 3
      do
        echo "5- $year $scale $proj $level - topojson simplify"
        outdir=$year"/"$proj"/"$scale"M"
        mkdir -p $outdir
        toposimplify -f -P 0.99 -o "$outdir/$level.json" "$dir/$level.json"
      done
    done
  done
done
