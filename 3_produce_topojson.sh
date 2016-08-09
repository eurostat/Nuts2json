#!/usr/bin/env bash

for proj in "etrs89" #"laea" "wm"
do
    for level in 0 #1 2 3
    do
        for scaleM in 3 10 30 60
        do
            #make directory
            dir="json/topojson/"$proj"/"$scaleM"M"
            mkdir -p $dir

            #compute resolution
            res=0
            if [ $proj = "etrs89" ]
                #then res=$((200*$scaleM))
                then res=$(echo "$scaleM / 60" | bc -l)
                else res=$((200*$scaleM))
            fi

            #qua=$res

            echo "   Produce topojson - lvl"$level" - "$proj" - 1:"$scaleM"M - res="$res   #" - qua="$qua
            topojson -o \
                $dir"/RG_lvl"$level"_"$scaleM"M.json" \
                "nutsrg=tmp/"$proj"/RGbylevel/RG_lvl"$level".shp" \
                -s 1e-7
                #-q qua #--id-property NUTS_ID  \
            #topojson -o $dir"/BN_lvl"$level"_"$scaleM"M.json" "nutsbn=tmp/"$proj"/BNbylevel/BN_lvl"$level".shp" -s $res
            #topojson -o $dir"/RG_BN_lvl"$level"_"$scaleM"M.json" "nutsrg=tmp/"$proj"/RGbylevel/RG_lvl"$level".shp" "nutsbn=tmp/"$proj"/BNbylevel/BN_lvl"$level".shp" -s $res
        done
    done
done
