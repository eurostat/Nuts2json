#!/usr/bin/env bash

#4258-etrs89 3857-wm 3035-laea

years=(2013 2016)
projs=("4258" "3857" "3035")
xmin=(-12.5 -1490000 2434550)
ymin=(32.5 3884000 1340330)
xmax=(46.5 5200000 7512400)
ymax=(73.9 11690000 5664600)

mkdir -p tmp

for yi in ${!years[@]}
do

year=${years[yi]}

mkdir -p "tmp/"$year


echo "$year Country RG: Clip and filter"
ogr2ogr -overwrite -f "ESRI Shapefile" -lco ENCODING=UTF-8 \
   "tmp/"$year"/CNTR_RG.shp" \
   "shp/"$year"/CNTR_RG_01M_"$year".shp" \
   -sql "SELECT CNTR_ID as id,NAME_ENGL as na FROM CNTR_RG_01M_"$year" WHERE CNTR_ID NOT IN ('PT','ES','IE','UK','FR','IS','BE','LU','NL','CH','LI','DE','DK','IT','VA','MT','NO','SE','FI','EE','LV','LT','PL','CZ','SK','AT','SI','HU','HR','RO','BG','TR','EL','CY','MK','ME')" \
   -clipsrc -179 -89 179 89

#necessary?
#echo "$year Country RG: Join attributes"
#ogr2ogr -overwrite -f "ESRI Shapefile" -lco ENCODING=UTF-8 \
#   "tmp/"$year"/CNTR_RG.shp" \
#   "tmp/"$year"/CNTR_RG_.shp" \
#   -sql "select CNTR_RG_.CNTR_ID as cid, CNTR_AT_"$year".CNTR_NAME as cna from CNTR_RG_ left join 'shp/"$year"/CNTR_AT_"$year".csv'.CNTR_AT_"$year" on CNTR_RG_.CNTR_ID = CNTR_AT_"$year".CNTR_ID" \
#   -clipsrc -179 -89 179 89

echo "$year Country BN: Clip and filter"
ogr2ogr -overwrite -f "ESRI Shapefile" -lco ENCODING=UTF-8 \
   "tmp/"$year"/CNTR_BN.shp" \
   "shp/"$year"/CNTR_BN_01M_"$year".shp" \
   -sql "SELECT OTHR_FLAG as oth FROM CNTR_BN_01M_"$year" WHERE COAS_FLAG='F' AND OTHR_FLAG='T'" \
   -clipsrc -179 -89 179 89


echo "$year NUTS RG: Clip and filter"
ogr2ogr -overwrite -f "ESRI Shapefile" -lco ENCODING=UTF-8 \
   "tmp/"$year"/NUTS_RG.shp" \
   "shp/"$year"/NUTS_RG_01M_"$year".shp" \
   -sql "SELECT NUTS_ID as id,NUTS_NAME as na,LEVL_CODE as lvl FROM NUTS_RG_01M_"$year \
   -clipsrc -179 -89 179 89

echo "$year NUTS BN: Clip and filter"
ogr2ogr -overwrite -f "ESRI Shapefile" -lco ENCODING=UTF-8 \
   "tmp/"$year"/NUTS_BN.shp" \
   "shp/"$year"/NUTS_BN_01M_"$year".shp" \
   -sql "SELECT LEVL_CODE as lvl,EU_FLAG as eu,EFTA_FLAG as efta,CC_FLAG as cc,OTHR_CNTR_ as oth,COAS_FLAG as coas FROM NUTS_BN_01M_"$year \
   -clipsrc -179 -89 179 89


  for pi in ${!projs[@]}
  do
    proj=${projs[pi]}
    for type in "RG" "BN"
    do
    	dir="tmp/$year/$proj/$type"
        mkdir -p $dir

        echo "$year $proj $type NUTS: Project"
        ogr2ogr -overwrite -f "ESRI Shapefile" -lco ENCODING=UTF-8 \
            $dir"/NUTS_proj.shp" \
            "tmp/"$year"/NUTS_"$type".shp" \
            -t_srs EPSG:$proj -s_srs EPSG:4258

        echo "$year $proj $type NUTS: Clip"
        ogr2ogr -overwrite -f "ESRI Shapefile" -lco ENCODING=UTF-8 \
            $dir"/NUTS.shp" \
            $dir"/NUTS_proj.shp" \
            -clipsrc ${xmin[pi]} ${ymin[pi]} ${xmax[pi]} ${ymax[pi]}

        echo "$year $proj $type Country: Project"
        ogr2ogr -overwrite -f "ESRI Shapefile" -lco ENCODING=UTF-8 \
            $dir"/CNTR_proj.shp" \
            "tmp/"$year"/CNTR_"$type".shp" \
            -t_srs EPSG:$proj -s_srs EPSG:4258

        echo "$year $proj $type Country: Clip"
        ogr2ogr -overwrite -f "ESRI Shapefile" -lco ENCODING=UTF-8 \
            $dir"/CNTR.shp" \
            $dir"/CNTR_proj.shp" \
            -clipsrc ${xmin[pi]} ${ymin[pi]} ${xmax[pi]} ${ymax[pi]}

    done
  done
done
