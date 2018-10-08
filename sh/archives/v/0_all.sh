#!/usr/bin/env bash

bash 1_filter_project_clip.sh
bash 2_extract_shp_by_level.sh
bash 3_shp_to_geojson.sh
bash 4_geojson_to_topojson.sh
bash 5_simplify_topojson.sh
bash 6_topojson_to_geojson.sh

#https://github.com/dwtkns/gdal-cheat-sheet
#npm install -g topojson
