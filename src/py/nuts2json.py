from pathlib import Path
import os, ogr2ogr, subprocess, json, urllib.request

################
# Target structure
#
# topojson:  YEAR/GEO/PROJECTION/SCALE/<NUTS_LEVEL>.json
# geojson:   YEAR/GEO/PROJECTION/SCALE/<TYPE>[_<NUTS_LEVEL>].json
# pts:       YEAR/GEO/PROJECTION/nutspt_<NUTS_LEVEL>.json
#
# Requirements:
# - GDAL (ogr2ogr and ogrinfo)
# - topojson (geo2topo, toposimplify, topo2geo). Install with nodeJS (npm install -g topojson)
################


# Set to True/False to show/hide debug messages
debug = False

# The Nuts2json version number
version = "v1"

# Download base data from GISCO download API
def download():
   print("Download")
   Path("download/").mkdir(parents=True, exist_ok=True)
   baseURL = "http://gisco-services.ec.europa.eu/distribution/v2/"

   for year in nutsData["years"]:

      if debug: print( year + " AT Download")
      outfile = "download/NUTS_AT_"+year+".csv"
      if not Path(outfile).exists(): urllib.request.urlretrieve(baseURL + "nuts/csv/NUTS_AT_"+year+".csv", outfile)

      # NUTS LB
      outfile = "download/NUTS_LB_"+year+"_4326.geojson"
      if not Path(outfile).exists(): urllib.request.urlretrieve(baseURL + "nuts/geojson/NUTS_LB_"+year+"_4326.geojson", outfile)

      for scale in nutsData["scales"]:
         if debug: print( year + " " + scale + " Download")

         for type in ["RG", "BN"]:

            # NUTS
            outfile = "download/NUTS_"+type+"_"+scale+"_"+year+"_4326.geojson"
            if not Path(outfile).exists(): urllib.request.urlretrieve(baseURL + "nuts/geojson/NUTS_"+type+"_"+scale+"_"+year+"_4326.geojson", outfile)

            # CNTR
            outfile = "download/CNTR_"+type+"_"+scale+"_"+year+"_4326.geojson"
            year_ = ("2020" if year=="2021" else year)
            if not Path(outfile).exists(): urllib.request.urlretrieve(baseURL + "countries/geojson/CNTR_"+type+"_"+scale+"_"+year_+"_4326.geojson", outfile)




# Prepare input data into tmp folder: filter, rename attributes, decompose by nuts level and clean
def filterRenameDecomposeClean(doCleaning = True):
   print("filterRenameDecompose")
   Path("tmp/").mkdir(parents=True, exist_ok=True)

   for year in nutsData["years"]:
       for scale in nutsData["scales"]:

           if debug: print(year + " " + scale + " CNTR RG - filter, rename attributes")
           ogr2ogr.main(["-overwrite","-f", "GPKG",
              "tmp/" + year + "_" + scale + "_CNTR_RG.gpkg",
              "-nln", "lay", "-nlt", "MULTIPOLYGON",
              "download/CNTR_RG_"+scale+"_"+year+"_4326.geojson",
              "-a_srs", "EPSG:4326",
              "-sql", "SELECT CNTR_ID as id,NAME_ENGL as na FROM CNTR_RG_" + scale + "_" + year + "_4326 WHERE CNTR_ID NOT IN (" + nutsData["years"][year] + ")"])

           if(doCleaning):
              if debug: print(year + " " + scale + " CNTR RG - clean with buffer(0)")
              subprocess.run(["ogrinfo", "-dialect", "indirect_sqlite", "-sql", "update lay set geom=ST_Multi(ST_Buffer(geom,0))", "tmp/" + year + "_" + scale + "_CNTR_RG.gpkg"])

           if debug: print(year + " " + scale + " CNTR BN - filter, rename attributes")
           ogr2ogr.main(["-overwrite","-f", "GPKG",
              "tmp/" + year + "_" + scale + "_CNTR_BN.gpkg",
              "-nln", "lay", "-nlt", "MULTILINESTRING",
              "download/CNTR_BN_"+scale+"_"+year+"_4326.geojson",
              "-a_srs", "EPSG:4326",
              "-sql", "SELECT CNTR_BN_ID as id,CC_FLAG as cc,OTHR_FLAG as oth,COAS_FLAG as co FROM CNTR_BN_" + scale + "_" + year + "_4326 WHERE EU_FLAG='F' AND EFTA_FLAG='F'"])

           for level in ["0", "1", "2", "3"]:

               if debug: print(year + " " + scale + " NUTS RG " + level + " - filter, rename attributes")
               ogr2ogr.main(["-overwrite","-f", "GPKG",
                 "tmp/" + year + "_" + scale + "_" + level + "_NUTS_RG.gpkg",
                 "-nln", "lay", "-nlt", "MULTIPOLYGON",
                 "download/NUTS_RG_"+scale+"_"+year+"_4326.geojson",
                 "-a_srs", "EPSG:4326",
                 "-sql", "SELECT N.NUTS_ID as id,A.NAME_LATN as na FROM NUTS_RG_" + scale + "_" + year + "_4326 as N left join 'download/NUTS_AT_" + year + ".csv'.NUTS_AT_" + year + " as A on N.NUTS_ID = A.NUTS_ID WHERE N.LEVL_CODE = " + level])

               if(doCleaning):
                  if debug: print(year + " " + scale + " NUTS RG " + level + " - clean with buffer(0)")
                  subprocess.run(["ogrinfo", "-dialect", "indirect_sqlite", "-sql", "update lay set geom=ST_Multi(ST_Buffer(geom,0))", "tmp/" + year + "_" + scale + "_" + level + "_NUTS_RG.gpkg"])

               if debug: print(year + " " + scale + " NUTS BN " + level + " - filter, rename attributes")
               ogr2ogr.main(["-overwrite","-f", "GPKG",
                 "tmp/" + year + "_" + scale + "_" + level + "_NUTS_BN.gpkg",
                 "-nln", "lay", "-nlt", "MULTILINESTRING",
                 "download/NUTS_BN_"+scale+"_"+year+"_4326.geojson",
                 "-a_srs", "EPSG:4326",
                 "-sql", "SELECT NUTS_BN_ID as id,LEVL_CODE as lvl,EU_FLAG as eu,EFTA_FLAG as efta,CC_FLAG as cc,OTHR_FLAG as oth,COAS_FLAG as co FROM NUTS_BN_" + scale + "_" + year + "_4326 WHERE LEVL_CODE <= " + level])



# Perform coarse clipping by region, to improve reprojection process
def coarseClipping():
   print("coarseClipping")
   for year in nutsData["years"]:
      for geo in geos:

         extends = geos[geo]["crs"]["4326"]
         marginDeg = 33 if(geo == "EUR") else 10

         if debug: print(year + " " + geo + " graticule - coarse clipping")
         ogr2ogr.main(["-overwrite","-f", "GPKG",
           "tmp/" + year + "_" + geo + "_graticule.gpkg",
           "src/resources/graticule.gpkg",
           "-nlt", "MULTILINESTRING",
           "-a_srs", "EPSG:4326",
           "-clipsrc", str(extends["xmin"]-marginDeg), str(extends["ymin"]-marginDeg), str(extends["xmax"]+marginDeg), str(extends["ymax"]+marginDeg)])

         for type in ["RG", "BN"]:
            for scale in geos[geo]["scales"]:

# TODO: fix that warning:
# Warning 1: A geometry of type GEOMETRYCOLLECTION is inserted into layer lay of geometry type MULTIPOLYGON, which is not normally allowed by the GeoPackage specification, but the driver will however do it. To create a conformant GeoPackage, if using ogr2ogr, the -nlt option can be used to override the layer geometry type. This warning will no longer be emitted for this combination of layer and feature geometry type.
# Use geojson format instead ? Or use GEOMETRYCOLLECTION as -nlt ?

               if debug: print(year + " " + geo + " " + scale + " CNTR " + type + " - coarse clipping")
               ogr2ogr.main(["-overwrite","-f", "GPKG",
                 "tmp/" + year + "_" + geo + "_" + scale + "_CNTR_" + type + ".gpkg",
                 "tmp/" + year + "_" + scale + "_CNTR_" + type + ".gpkg",
                 "-nlt", "MULTIPOLYGON" if type=="RG" else "MULTILINESTRING",
                 #"-makevalid",
                 "-a_srs", "EPSG:4326",
                 "-clipsrc", str(extends["xmin"]-marginDeg), str(extends["ymin"]-marginDeg), str(extends["xmax"]+marginDeg), str(extends["ymax"]+marginDeg)])

               for level in ["0", "1", "2", "3"]:

                  if debug: print(year + " " + geo + " " + scale + " NUTS " + type + " - coarse clipping")
                  ogr2ogr.main(["-overwrite","-f", "GPKG",
                    "tmp/" + year + "_" + geo + "_" + scale + "_" + level + "_NUTS_" + type + ".gpkg",
                    "tmp/" + year + "_" + scale + "_" + level + "_NUTS_" + type + ".gpkg",
                    "-nlt", "MULTIPOLYGON" if type=="RG" else "MULTILINESTRING",
                    #"-makevalid",
                    "-a_srs", "EPSG:4326",
                    "-clipsrc", str(extends["xmin"]-marginDeg), str(extends["ymin"]-marginDeg), str(extends["xmax"]+marginDeg), str(extends["ymax"]+marginDeg)])



# Clip, reproject and convert as geojson
def reprojectClipGeojson(doCleaning = True):
   print("reprojectClipGeojson")

   for year in nutsData["years"]:
      for geo in geos:
         for crs in geos[geo]["crs"]:
            outpath = "tmp/"+year+"/"+geo+"/"+crs+"/"
            Path(outpath).mkdir(parents=True, exist_ok=True)
            extent = geos[geo]["crs"][crs]

            if debug: print(year + " " + geo + " " + crs + " - reproject + clip + geojson graticule")
            ogr2ogr.main(["-overwrite","-f","GeoJSON",
              outpath + "graticule.geojson",
              "tmp/" + year + "_" + geo + "_graticule.gpkg",
              "-a_srs" if(crs=="4326") else "-t_srs", "EPSG:"+crs,
              #"-makevalid",
              "-clipdst", str(extent["xmin"]), str(extent["ymin"]), str(extent["xmax"]), str(extent["ymax"])
              ])

            for type in [ "RG", "BN" ]:
               for scale in geos[geo]["scales"]:

                  if debug: print(year + " " + geo + " " + crs + " " + scale + " " + type + " - reproject CNTR")
                  ogr2ogr.main(["-overwrite","-f","GPKG",
                    outpath + scale + "_CNTR_" + type + "_reproject.gpkg",
                    "tmp/" + year + "_" + geo + "_" + scale + "_CNTR_" + type + ".gpkg",
                    #"-makevalid",
                    "-nln", "lay",
                    "-a_srs" if(crs=="4326") else "-t_srs", "EPSG:"+crs
                    ])

                  if(doCleaning and type=="RG"):
                     if debug: print(year + " " + geo + " " + crs + " " + scale + " " + type + " - clean CNTR")
                     subprocess.run(["ogrinfo", "-dialect", "indirect_sqlite", "-sql", "update lay set geom=ST_Multi(ST_Buffer(geom,0))", outpath + scale + "_CNTR_" + type + "_reproject.gpkg"])

                  if debug: print(year + " " + geo + " " + crs + " " + scale + " " + type + " - clip + geojson CNTR")
                  ogr2ogr.main(["-overwrite","-f","GeoJSON",
                    outpath + scale + "_CNTR_" + type + ".geojson",
                    outpath + scale + "_CNTR_" + type + "_reproject.gpkg",
                    #"-makevalid",
                    "-clipdst", str(extent["xmin"]), str(extent["ymin"]), str(extent["xmax"]), str(extent["ymax"])
                    ])

                  for level in ["0", "1", "2", "3"]:

                     if debug: print(year + " " + geo + " " + crs + " " + scale + " " + type + " " + level + " - reproject + clip + geojson NUTS")
                     ogr2ogr.main(["-overwrite","-f","GeoJSON",
                       outpath + scale + "_" + level + "_NUTS_" + type + ".geojson",
                       "tmp/" + year + "_" + geo + "_" + scale + "_" + level + "_NUTS_" + type + ".gpkg",
                       "-a_srs" if(crs=="4326") else "-t_srs", "EPSG:"+crs,
                       #"-makevalid",
                       "-clipdst", str(extent["xmin"]), str(extent["ymin"]), str(extent["xmax"]), str(extent["ymax"])
                       ])




# Make topojson file from geojson files
# Simplify with topojson simplify
# Produce new geojson from topojson
# See: https://github.com/topojson/topojson-server/blob/master/README.md#geo2topo
# See: https://github.com/topojson/topojson-simplify/blob/master/README.md#toposimplify
# See: https://github.com/topojson/topojson-client/blob/master/README.md#topo2geo
def topoGeojson():
   print("topoGeojson")
   for year in nutsData["years"]:
      for geo in geos:
         for crs in geos[geo]["crs"]:
            for scale in geos[geo]["scales"]:
               for level in ["0", "1", "2", "3"]:
                  inpath = "tmp/"+year+"/"+geo+"/"+crs+"/"
                  outpath = "pub/" + version + "/" + year + "/" + ("" if geo=="EUR" else geo + "/") + crs + "/" + scale + "/"
                  Path(outpath).mkdir(parents=True, exist_ok=True)

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




# Produce point representations
def points():
   print("points")

   # prepare
   for year in nutsData["years"]:

      Path("tmp/pts/" + year + "/").mkdir(parents=True, exist_ok=True)

      if debug: print(year + " PTS join areas")
      ogr2ogr.main(["-overwrite","-f", "GeoJSON",
        "tmp/pts/" + year + "/NUTS_LB_.gpkg",
        "-nln", "lay",
        "download/NUTS_LB_" + year + "_4326.geojson",
        "-sql", "select LB.NUTS_ID as id, LB.LEVL_CODE as lvl, A.area as ar FROM NUTS_LB_" + year + "_4326 AS LB left join 'src/resources/nuts_areas/AREA_" + year + ".csv'.AREA_" + year + " AS A ON LB.NUTS_ID = A.nuts_id"
        ])

      if debug: print(year + " PTS join latn names")
      ogr2ogr.main(["-overwrite","-f", "GPKG",
        "tmp/pts/" + year + "/NUTS_LB.gpkg",
        "-nln", "lay",
        "tmp/pts/" + year + "/NUTS_LB_.gpkg",
        "-sql", "select LB.id as id, LB.lvl as lvl, A.NAME_LATN as na, LB.ar as ar FROM lay AS LB left join 'download/NUTS_AT_" + year + ".csv'.NUTS_AT_" + year + " as A on LB.id = A.NUTS_ID"
        ])

      for level in ["0", "1", "2", "3"]:

         if debug: print(year + " " + level + " - PTS decompose by NUTS level")
         ogr2ogr.main(["-overwrite","-f", "GPKG",
           "tmp/pts/" + year + "/NUTS_LB_" + level + ".gpkg",
           "-nln", "lay",
           "tmp/pts/" + year + "/NUTS_LB.gpkg",
           "-sql", "SELECT geom,id,na,ar FROM lay AS LB WHERE lvl=" + level
           ])

   for year in nutsData["years"]:
      for geo in geos:
         for crs in geos[geo]["crs"]:
            extends = geos[geo]["crs"][crs]

            outpath = "pub/" + version + "/" + year + "/" + ("" if geo=="EUR" else geo + "/") + crs + "/"
            Path(outpath).mkdir(parents=True, exist_ok=True)

            for level in ["0", "1", "2", "3"]:

               if debug: print(year + " " + geo + " " + crs + " " + level + " - reproject PTS")
               ogr2ogr.main(["-overwrite","-f","GeoJSON",
                 outpath + "nutspt_" + level + ".json",
                 "tmp/pts/" + year + "/NUTS_LB_" + level + ".gpkg",
                 "-nln", "nutspt_" + level,
                 "-a_srs" if(crs=="4326") else "-t_srs", "EPSG:"+crs,
                 "-clipdst", str(extends["xmin"]), str(extends["ymin"]), str(extends["xmax"]), str(extends["ymax"])
                 ])






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
