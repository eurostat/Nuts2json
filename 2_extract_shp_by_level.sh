#!/usr/bin/env bash

for year in "2016" "2013" "2010"
do
for scale in "10" "20" "60"
do
  for proj in "3035" "3857" "4258"
  do

    dirRG="tmp/$year/$scale/$proj/RG"
    dirBN="tmp/$year/$scale/$proj/BN"

    for level in 0 1 2 3
    do
        echo "2- $year $scale $proj $level NUTS RG: extract by level "
        ogr2ogr -overwrite -lco ENCODING=UTF-8 \
            -sql "SELECT id,na FROM NUTS WHERE lvl="$level \
            $dirRG"/"$level".shp" \
            $dirRG"/NUTS.shp"
            #" AND NUTS_ID NOT IN ('FRA','FRA1','FRA2','FRA3','FRA4','FRA5','FRA10','FRA20','FRA30','FRA40','FRA50','PT2','PT20','PT200','PT3','PT30','PT300','ES7','ES70','ES701','ES702','ES703','ES704','ES705','ES706','ES707','ES708','ES709')"

        echo "2- $year $scale $proj $level NUTS BN: extract by level "
        ogr2ogr -overwrite -lco ENCODING=UTF-8 \
            -sql "SELECT * FROM NUTS WHERE lvl<="$level"" \
            $dirBN"/"$level".shp" \
            $dirBN"/NUTS.shp"
    done
  done
done
done
