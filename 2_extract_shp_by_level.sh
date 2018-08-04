#!/usr/bin/env bash

for year in "2013" "2016"
do
  for proj in "3035" "3857" "4258"
  do

    dirRG="tmp/"$year"/"$proj"/RG"
    dirBN="tmp/"$year"/"$proj"/BN"

    for level in 0 1 2 3
    do
        echo "$year $proj $level NUTS RG: extract by level "
        ogr2ogr -overwrite -lco ENCODING=UTF-8 \
            -sql "SELECT id,na FROM NUTS WHERE lvl="$level \
            $dirRG"/"$level".shp" \
            $dirRG"/NUTS.shp"
            #" AND NUTS_ID NOT IN ('FRA','FRA1','FRA2','FRA3','FRA4','FRA5','FRA10','FRA20','FRA30','FRA40','FRA50','PT2','PT20','PT200','PT3','PT30','PT300','ES7','ES70','ES701','ES702','ES703','ES704','ES705','ES706','ES707','ES708','ES709')"

        echo "$year $proj $level NUTS BN: extract by level "
        ogr2ogr -overwrite -lco ENCODING=UTF-8 \
            -sql "SELECT lvl,eu,efta,cc,oth FROM NUTS WHERE lvl<="$level" AND coas <> 'T'" \
            $dirBN"/"$level".shp" \
            $dirBN"/NUTS.shp"
    done
  done
done
