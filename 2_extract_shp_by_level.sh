#!/usr/bin/env bash

for year in "2013"
do

for proj in "etrs89" "laea" "wm"
do
    echo "Extract nuts level - "$proj

    #make folders
    dirRG="tmp/"$year"/"$proj"/RGbylevel"
    dirBN="tmp/"$year"/"$proj"/BNbylevel"
    mkdir -p $dirRG
    mkdir -p $dirBN

    for level in 0 1 2 3
    do
        echo "   NUTS RG level "$level
        ogr2ogr -overwrite \
            -sql "SELECT * FROM NUTS_RG WHERE STAT_LEVL_="$level \
            $dirRG"/RG_lvl"$level".shp" \
            "tmp/"$year"/"$proj"/NUTS_RG.shp"
            #" AND NUTS_ID NOT IN ('FRA','FRA1','FRA2','FRA3','FRA4','FRA5','FRA10','FRA20','FRA30','FRA40','FRA50','PT2','PT20','PT200','PT3','PT30','PT300','ES7','ES70','ES701','ES702','ES703','ES704','ES705','ES706','ES707','ES708','ES709')"

        echo "   NUTS BN level "$level
        ogr2ogr -overwrite \
            -sql "SELECT * FROM NUTS_BN WHERE STAT_LEVL_<="$level" AND COAS_FLAG <> 'T'" \
            $dirBN"/BN_lvl"$level".shp" \
            "tmp/"$year"/"$proj"/NUTS_BN.shp"
    done
done

done
