from pathlib import Path
import subprocess, json, reduceGeoJSON #, urllib.request
import requests
import geopandas as gpd
import pandas as pd
from shapely.geometry import box, MultiPolygon, Polygon, MultiLineString, LineString
import time

################
# Target structure
#
# topojson:  YEAR/GEO/PROJECTION/SCALE/<NUTS_LEVEL>.json
# geojson:   YEAR/GEO/PROJECTION/SCALE/<TYPE>[_<NUTS_LEVEL>].json
# pts:       YEAR/GEO/PROJECTION/nutspt_<NUTS_LEVEL>.json
#
# Requirements:
# - python dependencies: see imports above
# - topojson 2.0 (geo2topo, toposimplify, topo2geo). Install globally with nodeJS (npm install -g topojson)
################


# Set to True/False to show/hide debug messages
debug = True

# The Nuts2json version number
version = "v2"


# save data from url to file
def download_from_url(url, outfile, timeout=50):
   if Path(outfile).exists(): return
   if debug: print(url)

   url = url + "?_=" + str(int(time.time()))
   response = requests.get(url, headers={'Cache-Control': 'no-cache', 'Pragma': 'no-cache'})
   with open(outfile, "wb") as file:
       file.write(response.content)
   '''
   try:
      # Open the URL with a specified timeout
      with urllib.request.urlopen(url, timeout=timeout) as response:
         with open(outfile, 'wb') as out_file:
            out_file.write(response.read())
            print("Done !")
   except urllib.error.HTTPError as e:
      print(f"HTTP Error: {e.code} - {e.reason}")
   except urllib.error.URLError as e:
      print(f"URL Error: {e.reason}")
   except Exception as e:
      print(f"An error occurred: {e}")
    '''



# Download input data from GISCO download API
def download(timeout=30000):
   print("Download")
   Path("download/").mkdir(parents=True, exist_ok=True)
   baseURL = "https://gisco-services.ec.europa.eu/distribution/v2/"

   for year in nutsData["years"]:

      #AT
      if debug: print(year, "AT Download")
      file = "NUTS_AT_"+year+".csv"
      download_from_url(baseURL + "nuts/csv/" + file, "download/"+file, timeout)

      # NUTS LB
      if debug: print(year, "LB Download")
      file = "NUTS_LB_"+year+"_4326.gpkg"
      download_from_url(baseURL + "nuts/gpkg/" + file, "download/"+file, timeout)


      for scale in nutsData["scales"]:
         for type in ["RG", "BN"]:

            # NUTS
            if debug: print(year, scale, type, "NUTS Download")
            file = "NUTS_"+type+"_"+scale+"_"+year+"_4326.gpkg"
            download_from_url(baseURL + "nuts/gpkg/" + file, "download/"+file, timeout)

            # CNTR
            if debug: print(year, scale, type, "CNTR Download")
            file = "CNTR_"+type+"_"+scale+"_"+year+"_4326.gpkg"
            year_ = ("2020" if year=="2021" else year)
            download_from_url(baseURL + "countries/gpkg/CNTR_"+type+"_"+scale+"_"+year_+"_4326.gpkg", "download/"+file, timeout)



# Prepare data: select attributes, rename them, decompose files by level
def filterRenameDecomposeClean(doCleaning=True):
    print("filterRenameDecompose")
    Path("tmp/").mkdir(parents=True, exist_ok=True)

    for year in nutsData["years"]:
        for scale in nutsData["scales"]:

            if debug: print(year + " " + scale + " CNTR RG - filter, rename attributes")
            # Load the geopackage and filter/rename columns
            gdf_cntr_rg = gpd.read_file(f"download/CNTR_RG_{scale}_{year}_4326.gpkg")
            gdf_cntr_rg = gdf_cntr_rg[['geometry', 'CNTR_ID', 'NAME_ENGL']].rename(columns={'CNTR_ID': 'id', 'NAME_ENGL': 'na'})

            if doCleaning:
                if debug: print(year + " " + scale + " CNTR RG - clean with buffer(0)")
                # Clean geometries using buffer(0)
                gdf_cntr_rg['geometry'] = gdf_cntr_rg['geometry'].buffer(0)

            # Save the filtered geopackage
            gdf_cntr_rg.to_file(f"tmp/{year}_{scale}_CNTR_RG.gpkg", driver="GPKG")

            if debug: print(year + " " + scale + " CNTR BN - filter, rename attributes")
            # Load CNTR BN geopackage, filter, and rename
            gdf_cntr_bn = gpd.read_file(f"download/CNTR_BN_{scale}_{year}_4326.gpkg")
            gdf_cntr_bn = gdf_cntr_bn[['geometry', 'CNTR_BN_ID', 'EU_FLAG', 'EFTA_FLAG', 'CC_FLAG', 'OTHR_FLAG', 'COAS_FLAG']].rename(
                columns={'CNTR_BN_ID': 'id', 'EU_FLAG': 'eu', 'EFTA_FLAG': 'efta', 'CC_FLAG': 'cc', 'OTHR_FLAG': 'oth', 'COAS_FLAG': 'co'})

            # Save the filtered geopackage
            gdf_cntr_bn.to_file(f"tmp/{year}_{scale}_CNTR_BN.gpkg", driver="GPKG")

            for level in ["0", "1", "2", "3"]:

                if debug: print(year + " " + scale + " NUTS RG " + level + " - filter, rename attributes")
                # Load NUTS RG geopackage, filter, and join CSV for additional attributes
                gdf_nuts_rg = gpd.read_file(f"download/NUTS_RG_{scale}_{year}_4326.gpkg")
                gdf_nuts_rg = gdf_nuts_rg[gdf_nuts_rg['LEVL_CODE'] == int(level)]
                #csv_data = pd.read_csv(f"download/NUTS_AT_{year}.csv")
                #gdf_nuts_rg = gdf_nuts_rg.merge(csv_data[['NUTS_ID', 'NAME_LATN']], on='NUTS_ID', how='left')
                #print(csv_data)
                #gdf_nuts_rg = gdf_nuts_rg[['NUTS_ID', 'NAME_LATN', 'geometry']].rename(columns={'NUTS_ID': 'id', 'NAME_LATN': 'na'})
                gdf_nuts_rg = gdf_nuts_rg[['geometry', 'NUTS_ID', 'NAME_LATN']].rename(columns={'NUTS_ID': 'id', 'NAME_LATN': 'na'})

                if doCleaning:
                    if debug: print(year + " " + scale + " NUTS RG " + level + " - clean with buffer(0)")
                    gdf_nuts_rg['geometry'] = gdf_nuts_rg['geometry'].buffer(0)

                # Save the filtered geopackage
                gdf_nuts_rg.to_file(f"tmp/{year}_{scale}_{level}_NUTS_RG.gpkg", driver="GPKG")

                if debug: print(year + " " + scale + " NUTS BN " + level + " - filter, rename attributes")
                # Load NUTS BN geopackage, filter, and rename
                gdf_nuts_bn = gpd.read_file(f"download/NUTS_BN_{scale}_{year}_4326.gpkg")
                gdf_nuts_bn = gdf_nuts_bn[gdf_nuts_bn['LEVL_CODE'] <= int(level)]
                gdf_nuts_bn = gdf_nuts_bn[['geometry', 'NUTS_BN_ID', 'LEVL_CODE', 'EU_FLAG', 'EFTA_FLAG', 'CC_FLAG', 'OTHR_FLAG', 'COAS_FLAG']].rename(
                    columns={'NUTS_BN_ID': 'id', 'LEVL_CODE': 'lvl', 'EU_FLAG': 'eu', 'EFTA_FLAG': 'efta', 'CC_FLAG': 'cc', 'OTHR_FLAG': 'oth', 'COAS_FLAG': 'co'})

                # Save the filtered geopackage
                gdf_nuts_bn.to_file(f"tmp/{year}_{scale}_{level}_NUTS_BN.gpkg", driver="GPKG")

                continue


# Perform coarse clipping by region, to improve reprojection process
def coarseClipping():
    print("coarseClipping")

    for year in nutsData["years"]:
        for geo in geos:

            # Define the bounding box (clipsrc equivalent)
            extends = geos[geo]["crs"]["4326"]
            marginDeg = 33 if geo == "EUR" else 10
            bbox = box(extends["xmin"] - marginDeg, extends["ymin"] - marginDeg,
                       extends["xmax"] + marginDeg, extends["ymax"] + marginDeg)

            # Convert bbox to a GeoDataFrame for clipping
            bbox_gdf = gpd.GeoDataFrame({"geometry": [bbox]}, crs="EPSG:4326")

            if debug: print(f"{year} {geo} graticule - coarse clipping")
            # Load the graticule and perform clipping
            gdf_graticule = gpd.read_file("src/resources/graticule.gpkg")
            gdf_graticule_clipped = gpd.clip(gdf_graticule, bbox_gdf)
            gdf_graticule_clipped['geometry'] = gdf_graticule_clipped['geometry'].apply(lambda geom: MultiLineString([geom]) if isinstance(geom, LineString) else geom)
            gdf_graticule_clipped.to_file(f"tmp/{year}_{geo}_graticule.gpkg", driver="GPKG") #, geometry_type="MULTILINESTRING"

            for type in ["RG", "BN"]:
                for scale in geos[geo]["scales"]:

                    # Handle the clipping and geometry type for CNTR layers
                    if debug: print(f"{year} {geo} {scale} CNTR {type} - coarse clipping")
                    gdf_cntr = gpd.read_file(f"tmp/{year}_{scale}_CNTR_{type}.gpkg")
                    #TODO should not be necessary once corrected at gisco
                    gdf_cntr.set_crs("EPSG:4326", allow_override=True, inplace=True)

                    # Clip the data with the bounding box
                    gdf_cntr_clipped = gpd.clip(gdf_cntr, bbox_gdf)

                    # force multi geometry
                    if type == "BN": gdf_cntr_clipped['geometry'] = gdf_cntr_clipped['geometry'].apply(lambda geom: MultiLineString([geom]) if isinstance(geom, LineString) else geom)
                    else: gdf_cntr_clipped['geometry'] = gdf_cntr_clipped['geometry'].apply(lambda geom: MultiPolygon([geom]) if isinstance(geom, Polygon) else geom)

                    # Save the clipped geopackage
                    gdf_cntr_clipped.to_file(f"tmp/{year}_{geo}_{scale}_CNTR_{type}.gpkg", driver="GPKG")

                    # Perform the clipping for each NUTS level
                    for level in ["0", "1", "2", "3"]:

                        if debug: print(f"{year} {geo} {scale} NUTS {type} - coarse clipping")
                        gdf_nuts = gpd.read_file(f"tmp/{year}_{scale}_{level}_NUTS_{type}.gpkg")
                        #TODO should not be necessary once corrected at gisco
                        gdf_nuts.set_crs("EPSG:4326", allow_override=True, inplace=True)

                        # Clip the data with the bounding box
                        gdf_nuts_clipped = gpd.clip(gdf_nuts, bbox_gdf)
                        
                        # force multi geometry
                        if type == "BN": gdf_nuts_clipped['geometry'] = gdf_nuts_clipped['geometry'].apply(lambda geom: MultiLineString([geom]) if isinstance(geom, LineString) else geom)
                        else: gdf_nuts_clipped['geometry'] = gdf_nuts_clipped['geometry'].apply(lambda geom: MultiPolygon([geom]) if isinstance(geom, Polygon) else geom)

                        # Save the clipped geopackage
                        gdf_nuts_clipped.to_file(f"tmp/{year}_{geo}_{scale}_{level}_NUTS_{type}.gpkg", driver="GPKG")



# produce input geojson files, reprojected and clipped
def reprojectClipGeojson(doCleaning=True):
    print("reprojectClipGeojson")

    for year in nutsData["years"]:
        for geo in geos:
            for crs in geos[geo]["crs"]:
                # Create output directories
                outpath = f"tmp/{year}/{geo}/{crs}/"
                Path(outpath).mkdir(parents=True, exist_ok=True)
                extent = geos[geo]["crs"][crs]

                # Define the bounding box for clipping
                bbox = box(extent["xmin"], extent["ymin"], extent["xmax"], extent["ymax"])
                bbox_gdf = gpd.GeoDataFrame({"geometry": [bbox]}, crs="EPSG:"+crs)

                # Graticule processing
                if debug: print(f"{year} {geo} {crs} - reproject + clip + geojson graticule")
                gdf_graticule = gpd.read_file(f"tmp/{year}_{geo}_graticule.gpkg")
                if crs != "4326": gdf_graticule = gdf_graticule.to_crs(epsg=int(crs))

                gdf_graticule_clipped = gpd.clip(gdf_graticule, bbox_gdf)
                gdf_graticule_clipped.to_file(f"{outpath}graticule.geojson", driver="GeoJSON")

                for type in ["RG", "BN"]:
                    for scale in geos[geo]["scales"]:
                        # Reproject and save CNTR layers
                        if debug: print(f"{year} {geo} {crs} {scale} {type} - reproject CNTR")
                        gdf_cntr = gpd.read_file(f"tmp/{year}_{geo}_{scale}_CNTR_{type}.gpkg")
                        gdf_cntr_reprojected = gdf_cntr.to_crs(epsg=int(crs))
                        gdf_cntr_reprojected.to_file(f"{outpath}{scale}_CNTR_{type}_reproject.gpkg", driver="GPKG")

                        # Optionally clean with buffer(0) for RG type
                        if doCleaning and type == "RG":
                            if debug: print(f"{year} {geo} {crs} {scale} {type} - clean CNTR")
                            gdf_cntr_reprojected['geometry'] = gdf_cntr_reprojected.buffer(0)
                            gdf_cntr_reprojected.to_file(f"{outpath}{scale}_CNTR_{type}_reproject.gpkg", driver="GPKG")

                        # Clip and save as GeoJSON
                        if debug: print(f"{year} {geo} {crs} {scale} {type} - clip + geojson CNTR")
                        gdf_cntr_clipped = gpd.clip(gdf_cntr_reprojected, bbox_gdf)
                        gdf_cntr_clipped.to_file(f"{outpath}{scale}_CNTR_{type}.geojson", driver="GeoJSON")

                        for level in ["0", "1", "2", "3"]:
                            # Reproject, clip, and save NUTS layers as GeoJSON
                            if debug: print(f"{year} {geo} {crs} {scale} {type} {level} - reproject + clip + geojson NUTS")
                            gdf_nuts = gpd.read_file(f"tmp/{year}_{geo}_{scale}_{level}_NUTS_{type}.gpkg")
                            gdf_nuts_reprojected = gdf_nuts.to_crs(epsg=int(crs))
                            gdf_nuts_clipped = gpd.clip(gdf_nuts_reprojected, bbox_gdf)
                            gdf_nuts_clipped.to_file(f"{outpath}{scale}_{level}_NUTS_{type}.geojson", driver="GeoJSON")





# Make topojson file from geojson files
# Simplify with topojson simplify
# Produce new geojson from topojson
# Reduce geojson
# See: https://github.com/topojson/topojson-server/blob/master/README.md#geo2topo
# See: https://github.com/topojson/topojson-simplify/blob/master/README.md#toposimplify
# See: https://github.com/topojson/topojson-client/blob/master/README.md#topo2geo
def topoGeojson():
   print("topoGeojson")
   for year in nutsData["years"]:
      for geo in geos:
         for crs in geos[geo]["crs"]:
            for scale in geos[geo]["scales"]:
               inpath = "tmp/"+year+"/"+geo+"/"+crs+"/"
               outpath = "pub/" + version + "/" + year + "/" + ("" if geo=="EUR" else geo + "/") + crs + "/" + scale + "/"
               Path(outpath).mkdir(parents=True, exist_ok=True)

               for level in ["0", "1", "2", "3"]:

                  # make topojson base files, one per nuts level
                  # quantization: q small means strong 'simplification'
                  if debug: print(year + " " + geo + " " + crs + " " + scale + " " + level + " - make topojson")
                  subprocess.run(["geo2topo", "-q", "20000",
                    "nutsrg=" + inpath + scale + "_" + level + "_NUTS_RG.geojson",
                    "nutsbn=" + inpath + scale + "_" + level + "_NUTS_BN.geojson",
                    "cntrg=" + inpath + scale + "_CNTR_RG.geojson",
                    "cntbn=" + inpath + scale + "_CNTR_BN.geojson",
                    "gra=" + inpath + "graticule.geojson",
                    "-o", inpath + level + ".json"])

                  if debug: print(year + " " + geo + " " + crs + " " + scale + " " + level + " - simplify topojson")
                  subprocess.run(["toposimplify", "-f", "-P", "0.99", "-o",
                    outpath + level + ".json",
                    inpath + level + ".json"])

                  if debug: print(year + " " + geo + " " + crs + " " + scale + " " + level + " - topojson to geojson")
                  subprocess.run(["topo2geo",
                    "nutsrg=" + outpath + "nutsrg_" + level + ".json",
                    "nutsbn=" + outpath + "nutsbn_" + level + ".json",
                    "cntrg=" + outpath + "cntrg.json",
                    "cntbn=" + outpath + "cntbn.json",
                    "gra=" + outpath + "gra.json",
                    "-i", outpath + level + ".json"])

                  if debug: print(year + " " + geo + " " + crs + " " + scale + " " + level + " - reduce geojson")
                  nbDec = 3 if crs == "4326" else 0
                  reduceGeoJSON.reduceGeoJSONFile(outpath + "nutsrg_" + level + ".json", nbDec)
                  reduceGeoJSON.reduceGeoJSONFile(outpath + "nutsbn_" + level + ".json", nbDec)
                  reduceGeoJSON.reduceGeoJSONFile(outpath + "cntrg.json", nbDec)
                  reduceGeoJSON.reduceGeoJSONFile(outpath + "cntbn.json", nbDec)
                  reduceGeoJSON.reduceGeoJSONFile(outpath + "gra.json", nbDec)

               #make files with all levels
               if debug: print(year + " " + geo + " " + crs + " " + scale + " - make topojson")
               subprocess.run(["geo2topo", "-q", "20000",
                 "nutsrg0=" + inpath + scale + "_" + "0_NUTS_RG.geojson",
                 "nutsbn0=" + inpath + scale + "_" + "0_NUTS_BN.geojson",
                 "nutsrg1=" + inpath + scale + "_" + "1_NUTS_RG.geojson",
                 "nutsbn1=" + inpath + scale + "_" + "1_NUTS_BN.geojson",
                 "nutsrg2=" + inpath + scale + "_" + "2_NUTS_RG.geojson",
                 "nutsbn2=" + inpath + scale + "_" + "2_NUTS_BN.geojson",
                 "nutsrg3=" + inpath + scale + "_" + "3_NUTS_RG.geojson",
                 "nutsbn3=" + inpath + scale + "_" + "3_NUTS_BN.geojson",
                 "cntrg=" + inpath + scale + "_CNTR_RG.geojson",
                 "cntbn=" + inpath + scale + "_CNTR_BN.geojson",
                 "gra=" + inpath + "graticule.geojson",
                 "-o", inpath + "all.json"])

               if debug: print(year + " " + geo + " " + crs + " " + scale + " - simplify topojson")
               subprocess.run(["toposimplify", "-f", "-P", "0.99", "-o",
                 outpath + "all.json",
                 inpath + "all.json"])




# Produce point representations
def points():
    print("points")

    # Prepare points data
    for year in nutsData["years"]:
        Path(f"tmp/pts/{year}/").mkdir(parents=True, exist_ok=True)

        # Load NUTS_LB data as GeoDataFrame
        if debug: print(f"{year} PTS join areas")
        gdf_lb = gpd.read_file(f"download/NUTS_LB_{year}_4326.gpkg")

        # Load area data from CSV and join with GeoDataFrame
        area_df = pd.read_csv(f"src/resources/nuts_areas/AREA_{year}.csv")
        gdf_lb = gdf_lb.merge(area_df, left_on="NUTS_ID", right_on="nuts_id", how="left")

        #if debug: print(f"{year} PTS join latn names")
        # Load name data and join
        #nuts_at_df = pd.read_csv(f"download/NUTS_AT_{year}.csv")
        #gdf_lb = gdf_lb.merge(nuts_at_df, left_on="NUTS_ID", right_on="NUTS_ID", how="left")

        gdf_lb = gdf_lb[['geometry', 'NUTS_ID', 'LEVL_CODE', 'NAME_LATN', 'area']].rename(columns={'NUTS_ID': 'id', 'NAME_LATN': 'na', 'area': 'ar'})

        # Save the resulting GeoDataFrame to a temporary file
        gdf_lb.to_file(f"tmp/pts/{year}/NUTS_LB.gpkg", driver="GPKG")

        # Decompose by NUTS level and save
        for level in ["0", "1", "2", "3"]:
            if debug: print(f"{year} {level} - PTS decompose by NUTS level")
            gdf_level = gdf_lb[gdf_lb["LEVL_CODE"] == int(level)]
            gdf_level[["geometry", "id", "na", "ar"]].to_file(f"tmp/pts/{year}/NUTS_LB_{level}.gpkg", driver="GPKG")

    # Reproject and clip
    for year in nutsData["years"]:
        for geo in geos:
            for crs in geos[geo]["crs"]:
                extends = geos[geo]["crs"][crs]

                # Create output path
                outpath = f"pub/{version}/{year}/{'' if geo == 'EUR' else geo + '/'}{crs}/"
                Path(outpath).mkdir(parents=True, exist_ok=True)

                # Define clipping box
                bbox = box(extends["xmin"], extends["ymin"], extends["xmax"], extends["ymax"])
                bbox_gdf = gpd.GeoDataFrame({"geometry": [bbox]}, crs="EPSG:" + crs)

                for level in ["0", "1", "2", "3"]:
                    if debug: print(f"{year} {geo} {crs} {level} - reproject PTS")
                    gdf_pts = gpd.read_file(f"tmp/pts/{year}/NUTS_LB_{level}.gpkg")

                    # Reproject the GeoDataFrame
                    gdf_pts_reprojected = gdf_pts.to_crs(epsg=int(crs))

                    # Clip the GeoDataFrame to the bounding box
                    gdf_pts_clipped = gpd.clip(gdf_pts_reprojected, bbox_gdf)

                    # Save the clipped data as GeoJSON
                    gdf_pts_clipped.to_file(f"{outpath}nutspt_{level}.json", driver="GeoJSON")

                    # Reduce precision if necessary
                    if debug: print(f"{year} {geo} {crs} {level} - reduce PTS")
                    nbDec = 3 if crs == "4326" else 0
                    reduceGeoJSON.reduceGeoJSONFile(f"{outpath}nutspt_{level}.json", nbDec)



######## Full process #########

# Load parameters
with open("src/py/param.json", mode="r") as fp:
   param = json.load(fp)

# NUTS year versions and, for each one, the countries for which NUTS/statistical units are shown
nutsData = param["nutsData"]

# Geographical territories for map insets.
# For each, the CRSs to handle and the geographical extent.
geos = param["geos"]

# Publish information on API structure
print("save data")
Path("pub/" + version + "/").mkdir(parents=True, exist_ok=True)
with open("pub/" + version + "/data.json", "w") as fp:
    json.dump(geos, fp, indent=3)

# 1
download()
# 2
filterRenameDecomposeClean()
# 3
coarseClipping()
# 4
reprojectClipGeojson()
# 5
topoGeojson()
# 6
points()
##############################
