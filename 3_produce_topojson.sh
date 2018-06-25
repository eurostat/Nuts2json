#!/usr/bin/env bash

q0=6000
q1=3000
s=3

for year in "2013"
do

for proj in "laea" "wm" #"etrs89"
do
    for size in 1200 1000 800 600 400
    do
        for level in 0 1 2 3
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
                $dir"/NUTS_lvl"$level".json" \
                "nutsrg=tmp/"$year"/"$proj"/RGbylevel/RG_lvl"$level".shp" \
                "nutsbn=tmp/"$year"/"$proj"/BNbylevel/BN_lvl"$level".shp" \
                "cntrg=tmp/"$year"/"$proj"/CNTR_RG.shp" \
                "cntbn=tmp/"$year"/"$proj"/CNTR_BN.shp" \
                -p id=NUTS_ID,na=name,eu=EU_FLAG,efta=EFTA_FLAG,cc=CC_FLAG,lvl=STAT_LEVL_,oth=OTHR_CNTR_,cid=CNTR_RG_03,cna=CNTR_AT__6 \
                --id-property NUTS_ID \
                -e "shp/"$year"NUTS_AT_"$year"_prep.csv" \
                --bbox --width $size --height $size \
	            -s $s \
	            --q0 $q0 --q1 $q1
            fi
        done
    done
done

done
