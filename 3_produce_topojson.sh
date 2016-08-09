#!/usr/bin/env bash

margin=10
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

            echo "Not supported yet"
            #-s 1e-7

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
                -p id=NUTS_ID --id-property id \
                --width $size --height $size --margin $margin \
                -s 1
            topojson -o \
                $dir"/BN_lvl"$level".json" \
                "nutsbn=tmp/"$proj"/BNbylevel/BN_lvl"$level".shp" \
                -p eu=EU_FLAG,efta=EFTA_FLAG,cc=CC_FLAG,lvl=STAT_LEVL_,cst=COAS_FLAG,oth=OTHR_CNTR_ \
                --width $size --height $size --margin $margin \
                -s 1
            topojson -o \
                $dir"/RG_BN_lvl"$level".json" \
                "nutsrg=tmp/"$proj"/RGbylevel/RG_lvl"$level".shp" \
                "nutsbn=tmp/"$proj"/BNbylevel/BN_lvl"$level".shp" \
                -p id=NUTS_ID,eu=EU_FLAG,efta=EFTA_FLAG,cc=CC_FLAG,lvl=STAT_LEVL_,cst=COAS_FLAG,oth=OTHR_CNTR_ \
                --id-property id \
                --width $size --height $size --margin $margin \
                -s 1
            fi
        done
    done
done
