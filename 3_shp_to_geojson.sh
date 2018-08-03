#!/usr/bin/env bash

#make topojson base files, one per nuts level
for year in "2013" "2016"
do
  for proj in "etrs89" "laea" "wm"
  do

    dir="tmp/"$year"/"$proj"/"$type

    for level in 0 1 2 3
    do
      echo "$year $proj $level - geojson to topojson"

    done
  done
done
