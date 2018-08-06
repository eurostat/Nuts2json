#!/usr/bin/env bash

#simplify topojson files
#https://github.com/topojson/topojson-simplify/blob/master/README.md#toposimplify
for year in "2016" "2013" "2010"
do
  for proj in "3035" "3857" "4258"
  do
    dir="tmp/"$year"/"$proj
    for level in 0 1 2 3
    do
      for size in 1200 1000 800 600 400
      do
        echo "5- $year $proj $level $size - topojson simplify"

        outdir=$year"/"$proj"/"$size"px"
        mkdir -p $outdir

        if [ $proj = "4258" ]
        then
          #toposimplify -f -s $(( 160000 / ($size * $size) )) -o $outdir"/"$level".json" $dir"/"$level".json"
          toposimplify -f -p $(( 42000000000000 / ($size * $size) )) -o $outdir"/"$level".json" $dir"/"$level".json"
        else
          toposimplify -f -p $(( 42000000000000 / ($size * $size) )) -o $outdir"/"$level".json" $dir"/"$level".json"
        fi
      done
    done
  done
done
