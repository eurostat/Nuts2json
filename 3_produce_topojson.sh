#!/usr/bin/env bash

for proj in "etrs89" #"laea" #"wm"
do
    mkdir -p "json/topojson/"$proj
    for level in 0 #1 2 3
    do
        for scaleM in 3 10 30 60
        do
            res=$((2/10*$scaleM*1000))
            echo "Produce topojson for level "$level" - projection "$proj" - scale 1:"$scaleM"M - resolution="$res
            topojson -o "json/topojson/"$proj"/RG_lvl"$level"_"$scaleM"M.json" "nutsrg=tmp/"$proj"/RGbylevel/RG_lvl"$level".shp" -s res #--id-property NUTS_ID
            topojson -o "json/topojson/"$proj"/BN_lvl"$level"_"$scaleM"M.json" "nutsbn=tmp/"$proj"/BNbylevel/BN_lvl"$level".shp" -s $res
            topojson -o "json/topojson/"$proj"/RG_BN_lvl"$level"_"$scaleM"M.json" "nutsrg=tmp/"$proj"/RGbylevel/RG_lvl"$level".shp" "nutsbn=tmp/"$proj"/BNbylevel/BN_lvl"$level".shp" -s $res
        done
    done
done
