#!/usr/bin/env bash

projs=("etrs89" "wm" "laea")
epsgs=("4258" "3857" "3035")
xmin=(-12.5 -1490000 2434550)
ymin=(32.5 3884000 1340330)
xmax=(46.5 5200000 7512400)
ymax=(73.9 11690000 5664600)

mkdir -p tmp

echo "Clip and filter country RG"
ogr2ogr -overwrite -f "ESRI Shapefile" \
   "tmp/CNTR_RG_03M_2014___.shp" \
   "shp/CNTR_RG_03M_2014.shp" \
   -sql "SELECT * FROM CNTR_RG_03M_2014 WHERE CNTR_ID NOT IN ('PT','ES','IE','UK','FR','IS','BE','LU','NL','CH','LI','DE','DK','IT','VA','MT','NO','SE','FI','EE','LV','LT','PL','CZ','SK','AT','SI','HU','HR','RO','BG','TR','EL','CY','MK','ME')" \
   -clipsrc -179 -89 179 89

echo "Clip and filter country BN and select"
ogr2ogr -overwrite -f "ESRI Shapefile" \
   "tmp/CNTR_BN_03M_2014___.shp" \
   "shp/CNTR_BN_03M_2014.shp" \
   -sql "SELECT * FROM CNTR_BN_03M_2014 WHERE COAS_FLAG='F' AND OTHR_CNTR_='T'" \
   -clipsrc -179 -89 179 89

for pi in ${!projs[@]}
do
    proj=${projs[pi]}
    epsg=${epsgs[pi]}
    mkdir -p tmp/$proj
    for type in "RG" "BN"
    do
        echo "Project NUTS $type to $proj"
        ogr2ogr -overwrite -f "ESRI Shapefile" \
            "tmp/"$proj"/NUTS_"$type"_proj.shp" \
            "shp/NUTS_"$type"_01M_2013.shp" \
            -t_srs EPSG:$epsg -s_srs EPSG:4258

        echo "Clip NUTS $type $proj"
        ogr2ogr -overwrite -f "ESRI Shapefile" \
            "tmp/"$proj"/NUTS_"$type".shp" \
            "tmp/"$proj"/NUTS_"$type"_proj.shp" \
            -clipsrc ${xmin[pi]} ${ymin[pi]} ${xmax[pi]} ${ymax[pi]}

        echo "Project country $type to $proj"
        ogr2ogr -overwrite -f "ESRI Shapefile" \
            "tmp/"$proj"/CNTR_"$type"_proj.shp" \
            "tmp/CNTR_"$type"_03M_2014___.shp" \
            -t_srs EPSG:$epsg -s_srs EPSG:4258

        echo "Clip country $type $proj"
        ogr2ogr -overwrite -f "ESRI Shapefile" \
            "tmp/"$proj"/CNTR_"$type".shp" \
            "tmp/"$proj"/CNTR_"$type"_proj.shp" \
            -clipsrc ${xmin[pi]} ${ymin[pi]} ${xmax[pi]} ${ymax[pi]}
    done
done
