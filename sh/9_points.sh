#!/usr/bin/env bash


#filter and project

#4326-wgs84 4258-etrs89 3857-wm 3035-laea
projs=("4326" "4258" "3857" "3035")
xmin=(-25 -25 -2800000 2434560)
ymin=(32.5 32.5 3884000 1340340)
xmax=(46.5 46.5 5200000 7512390)
ymax=(73.9 73.9 11690000 5664590)

years=("2016" "2013" "2010")

for yi in ${!years[@]}
do
  year=${years[yi]}

  echo "9- $year NUTS LB: Join"
  dir="../tmp/$year/LB"
  mkdir -p $dir

  ogr2ogr -overwrite -f "ESRI Shapefile" -lco ENCODING=UTF-8 \
     $dir"/NUTS_LB.shp" \
     "../shp/"$year"/NUTS_LB_"$year"_4326.shp" \
     -sql "select NUTS_LB_"$year"_4326.NUTS_ID as id, NUTS_LB_"$year"_4326.LEVL_CODE as lvl, NUTS_LB_"$year"_4326.NUTS_NAME as na, AREA.area as ar FROM NUTS_LB_"$year"_4326 left join '../shp/"$year"/AREA.csv'.AREA on NUTS_LB_"$year"_4326.NUTS_ID = AREA.nuts_id"

  for pi in ${!projs[@]}
  do
    proj=${projs[pi]}
    echo "9- $year $proj NUTS LB: Project"
    ogr2ogr -overwrite -f "ESRI Shapefile" -lco ENCODING=UTF-8 \
       $dir"/NUTS_LB_"$proj".shp" \
       $dir"/NUTS_LB.shp" \
       -t_srs EPSG:$proj -s_srs EPSG:4258
  done
done


#extract shp by level
for year in "2016" "2013" "2010"
do
  for proj in "3035" "3857" "4258" "4326"
  do
    for level in 0 1 2 3
    do
      echo "9- $year $proj $level NUTS LB: extract by level"
      dir="../tmp/$year/LB"
      ogr2ogr -overwrite -lco ENCODING=UTF-8 \
         -sql "SELECT id,na,ar FROM NUTS_LB_"$proj" WHERE lvl="$level \
         $dir"/NUTS_LB_"$proj"_"$level".shp" \
         $dir"/NUTS_LB_"$proj".shp"
    done
  done
done


#shp to geojson
for year in "2016" "2013" "2010"
do
  for proj in "3035" "3857" "4258" "4326"
  do
    for level in 0 1 2 3
    do
      echo "9- $year $proj $level - NUTS LB SHP to geojson"
      mkdir -p "../"$year"/"$proj
      outjson="../"$year"/"$proj"/nutspt_"$level".json"
      rm -f $outjson
      ogr2ogr -overwrite -f geoJSON $outjson "../tmp/$year/LB/NUTS_LB_"$proj"_"$level".shp"
    done
  done
done
