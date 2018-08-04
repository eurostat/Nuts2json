#!/usr/bin/env bash

#simplify topojson files
#https://github.com/topojson/topojson-simplify/blob/master/README.md#toposimplify
for year in "2016" #"2013"
do
  for proj in "laea" "etrs89" "laea" "wm"
  do
    dir="tmp/"$year"/"$proj
    for level in 0 1 2 3
    do
      for size in 1200 1000 800 600 400
      do
        outdir=$year"/"$proj"/"$size"px"
        mkdir -p $outdir

        echo "$year $proj $level $size - topojson simplify"
        toposimplify -f -p $(( 35000000000000 / ($size * $size) )) -o $outdir"/"$level".topojson" $dir"/"$level".topojson"
      done
    done
  done
done
