#!/usr/bin/env bash

margin=20
for size in 300 500 700 1000 1200
do
    for level in 0 1 2 3
    do
        for proj in "laea" "wm" "etrs89"
        do
            #make directory
            dir="json/topojson/"$proj"/"$size"px"
            mkdir -p $dir

            if [ $proj = "etrs89" ]
            then

            #compute resolution
            #res=0
            #if [ $proj = "etrs89" ]
            #    #then res=$((200*$scaleM))
            #    then res=$(echo "$scaleM / 60" | bc -l)
            #    else res=$((200*$scaleM))
            #fi

            else

            echo "   Produce topojson - lvl"$level" - "$proj" - "$size"px"
            topojson -o \
                $dir"/RG_lvl"$level".json" \
                "nutsrg=tmp/"$proj"/RGbylevel/RG_lvl"$level".shp" \
                --width $size --height $size --margin $margin \
                -s 1
                #-s 1e-7
                #--id-property NUTS_ID  \
            topojson -o \
                $dir"/BN_lvl"$level".json" \
                "nutsbn=tmp/"$proj"/BNbylevel/BN_lvl"$level".shp" \
                --width $size --height $size --margin $margin \
                -s 1
            topojson -o \
                $dir"/RG_BN_lvl"$level".json" \
                "nutsrg=tmp/"$proj"/RGbylevel/RG_lvl"$level".shp" \
                "nutsbn=tmp/"$proj"/BNbylevel/BN_lvl"$level".shp" \
                --width $size --height $size --margin $margin \
                -s 1
            fi
        done
    done
done
