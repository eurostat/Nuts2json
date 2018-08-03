#!/usr/bin/env bash

#simplify topojson files
#https://github.com/topojson/topojson-server/blob/master/README.md#geo2topo
for year in "2013" "2016"
do
  for proj in "etrs89" "laea" "wm"
  do
    dir="tmp/"$year"/"$proj
    for level in 0 1 2 3
    do
      for size in 1200 #1000 800 600 400
      do
        echo "$year $proj $level $size - topojson simplify"
        #toposimplify $dir"/"$level".topojson"
      done
    done
  done
done
