from pathlib import Path
import ogr2ogr, subprocess, json, urllib.request

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
debug = True

# The Nuts2json version number
version = "v1"

# NUTS year versions and, for each one, the countries for which NUTS/statistical units are shown
nutsData = {
   "years" : {
      "2021" : "'PT','ES','IE','UK','FR','IS','BE','LU','NL','CH','LI','DE','DK','IT','VA','MT','NO','SE','FI','EE','LV','LT','PL','CZ','SK','AT','SI','HU','HR','RO','BG','TR','EL','CY','MK','ME','AL'",
      "2016" : "'PT','ES','IE','UK','FR','IS','BE','LU','NL','CH','LI','DE','DK','IT','VA','MT','NO','SE','FI','EE','LV','LT','PL','CZ','SK','AT','SI','HU','HR','RO','BG','TR','EL','CY','MK','ME','AL'",
      "2013" : "'PT','ES','IE','UK','FR','IS','BE','LU','NL','CH','LI','DE','DK','IT','VA','MT','NO','SE','FI','EE','LV','LT','PL','CZ','SK','AT','SI','HU','HR','RO','BG','TR','EL','CY','MK','ME'",
      "2010" : "'PT','ES','IE','UK','FR','IS','BE','LU','NL','CH','LI','DE','DK','IT','VA','MT','NO','SE','FI','EE','LV','LT','PL','CZ','SK','AT','SI','HU','HR','RO','BG','TR','EL','CY','MK','ME'",
   },
   "scales" : ["01M", "03M", "10M", "20M", "60M"]
}

# TODO extract that.
# Geographical territories for map insets.
# For each, the CRSs to handle and the geographical extent.
geos = {
   "EUR" : {
      "name" : "Europe",
      "crs" : {
      "4326" : { "xmin" : -25, "ymin" : 32.5, "xmax" : 46.5, "ymax" : 73.9},
      "3857" : { "xmin" : -2800000, "ymin" : 3884000, "xmax" : 5200000, "ymax" : 11690000},
      "3035" : { "xmin" : 2434560, "ymin" : 1340340, "xmax" : 7512390, "ymax" : 5664590}
      },
      "scales" : ["03M", "10M", "20M", "60M"]
   },
   "PT20" : {
      "name" : "Azores",
      "crs" : {
      "4326" : { "xmin" : -32.67, "ymin" : 35.92, "xmax" : -23.89, "ymax" : 40.53},
      "3857" : { "xmin" : -3692767, "ymin" : 4238065, "xmax" : -2526564, "ymax" : 4972707},
      "32626" : { "xmin" : 74783, "ymin" : 4020123, "xmax" : 727948, "ymax" : 4431039}
      },
      "scales" : ["01M", "03M", "10M", "20M"]
   },
    "PT30" : {
      "name" : "Madeira",
      "crs" : {
      "4326" : { "xmin" : -18.18, "ymin" : 29.73, "xmax" : -15.46, "ymax" : 33.52},
      "3857" : { "xmin" : -1987937, "ymin" : 3483657, "xmax" : -1698033, "ymax" : 3938279},
      "32628" : { "xmin" : 189150, "ymin" : 3262646, "xmax" : 525471, "ymax" : 3697671}
      },
      "scales" : ["01M", "03M", "10M", "20M"]
   },
   "IC" : {
      "name" : "Canary islands",
      "crs" : {
      "4326" : { "xmin" : -18.599, "ymin" : 27.131, "xmax" : -12.82, "ymax" : 29.77},
      "3857" : { "xmin" : -2093768, "ymin" : 3148045, "xmax" : -1438191, "ymax" : 3480775},
      "32628" : { "xmin" : 79480, "ymin" : 2951914, "xmax" : 755779, "ymax" : 3306514}
      },
      "scales" : ["01M", "03M", "10M", "20M"]
    },
   "GF" : {
      "name" : "French Guiana",
      "crs" : {
      "4326" : { "xmin" : -56, "ymin" : 1, "xmax" : -50, "ymax" : 7},
      "3857" : { "xmin" : -6123000, "ymin" : 194000, "xmax" : -5702000, "ymax" : 680000},
      "32622" : { "xmin" : 70000, "ymin" : 204000, "xmax" : 456000, "ymax" : 667000}
      },
      "scales" : ["01M", "03M", "10M", "20M"]
   },
   "GP" : {
      "name" : "Guadeloupe",
      "crs" : {
      "4326" : { "xmin" : -64.197, "ymin" : 13.732, "xmax" : -59.967, "ymax" : 18.813},
      "3857" : { "xmin" : -7057292, "ymin" : 1766063, "xmax" : -6759747, "ymax" : 2071532},
      "32620" : { "xmin" : 457264, "ymin" : 1733655, "xmax" : 742535, "ymax" : 2023133}
     },
     "scales" : ["01M", "03M", "10M", "20M"]
   },
   "MQ" : {
      "name" : "Martinique",
      "crs" : {
      "4326" : { "xmin" : -61.398, "ymin" : 14.293, "xmax" : -60.618, "ymax" : 15.059},
      "3857" : { "xmin" : -6843610, "ymin" : 1596556, "xmax" : -6743775, "ymax" : 1692156},
      "32620" : { "xmin" : 658362, "ymin" : 1580492, "xmax" : 760525, "ymax" : 1660906}
     },
     "scales" : ["01M", "03M", "10M", "20M"]
   },
   "CARIB" : {
      "name" : "Caribbean islands",
      "crs" : {
      "4326" : { "xmin" : -64.074, "ymin" : 12.816, "xmax" : -60.257, "ymax" : 18.350},
      "3857" : { "xmin" : -7114435, "ymin" : 1438782, "xmax" : -6701775, "ymax" : 2080865},
      "32620" : { "xmin" : 390901, "ymin" : 1412066, "xmax" : 803644, "ymax" : 2038195}
     },
     "scales" : ["01M", "03M", "10M", "20M"]
   },
   "RE" : {
      "name" : "Reunion",
      "crs" : {
      "4326" : { "xmin" : 55.087, "ymin" : -21.521, "xmax" : 55.981, "ymax" : -20.752},
      "3857" : { "xmin" : 6118552, "ymin" : -2456745, "xmax" : 6240595, "ymax" : -2355898},
      "32740" : { "xmin" : 301152, "ymin" : 7625194, "xmax" : 397346, "ymax" : 7708036}
     },
     "scales" : ["01M", "03M", "10M", "20M"]
   },
   "YT" : {
      "name" : "Mayotte",
      "crs" : {
      "4326" : { "xmin" : 44.869, "ymin" : -13.088, "xmax" : 45.362, "ymax" : -12.590},
      "3857" : { "xmin" : 5008923, "ymin" : -1461785, "xmax" : 5045741, "ymax" : -1415417},
      "32738" : { "xmin" : 495615, "ymin" : 8559198, "xmax" : 535145, "ymax" : 8605147}
     },
     "scales" : ["01M", "03M", "10M", "20M"]
   },
   "MT" : {
      "name" : "Malta",
      "crs" : {
      "4326" : { "xmin" : 14, "ymin" : 35.4, "xmax" : 15, "ymax" : 37},
      "3857" : { "xmin" : 1573000, "ymin" : 4270000, "xmax" : 1632000, "ymax" : 4320000},
      "3035" : { "xmin" : 4692000, "ymin" : 1420000, "xmax" : 4750000, "ymax" : 1466000}
      },
      "scales" : ["01M", "03M", "10M", "20M"]
   },
   "LI" : {
      "name" : "Liechtenstein",
      "crs" : {
      "4326" : { "xmin" : 9.3204, "ymin" : 46.9912, "xmax" : 9.7605, "ymax" : 47.3929},
      "3857" : { "xmin" : 1026000, "ymin" : 5925000, "xmax" : 1099000, "ymax" : 6002000},
      "3035" : { "xmin" : 4256797, "ymin" : 2645615, "xmax" : 4320880, "ymax" : 2696748}
      },
      "scales" : ["01M", "03M", "10M", "20M"]
   },
   "IS" : {
      "name" : "Iceland",
      "crs" : {
      "4326" : { "xmin" : -25.1, "ymin" : 62.6, "xmax" : -12.1, "ymax" : 67.7},
      "3857" : { "xmin" : -2847407, "ymin" : 9094947, "xmax" : -1355181, "ymax" : 10129307},
      "3035" : { "xmin" : 2705235, "ymin" : 4731507, "xmax" : 3328521, "ymax" : 5193241}
      },
      "scales" : ["01M", "03M", "10M", "20M"]
   },
   "SJ_SV" : {
      "name" : "Svalbard",
      "crs" : {
      "4326" : { "xmin" : 7.31, "ymin" : 73.38, "xmax" : 34.84, "ymax" : 81.62},
      "3857" : { "xmin" : 370942, "ymin" : 12238601, "xmax" : 4275361, "ymax" : 16477683},
      "3035" : { "xmin" : 4169002, "ymin" : 5588027, "xmax" : 4881559, "ymax" : 6487832}
      },
      "scales" : ["01M", "03M", "10M", "20M"]
   },
   "SJ_JM" : {
      "name" : "Jan Mayen",
      "crs" : {
      "4326" : { "xmin" : -10.26, "ymin" : 69.88, "xmax" : -6.61, "ymax" : 71.92},
      "3857" : { "xmin" : -1169541, "ymin" : 11210247, "xmax" : -692469, "ymax" : 11604247},
      "3035" : { "xmin" : 3575911, "ymin" : 5344013, "xmax" : 3723336, "ymax" : 5455429}
      },
      "scales" : ["01M", "03M", "10M", "20M"]
   }
}




# Save information on API structure
print("save data")
Path("pub/" + version + "/").mkdir(parents=True, exist_ok=True)
with open("pub/" + version + "/data.json", "w") as fp:
    json.dump(geos, fp, indent=3)




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
def filterRenameDecomposeClean():
   print("filterRenameDecompose")
   Path("tmp/").mkdir(parents=True, exist_ok=True)

   for year in nutsData["years"]:
       for scale in nutsData["scales"]:

           if debug: print(year + " " + scale + " CNTR RG - filter, rename attributes")
           ogr2ogr.main(["-overwrite","-f", "GPKG",
              "tmp/" + year + "_" + scale + "_CNTR_RG.gpkg",
              "-nln", "lay", "-nlt", "MULTIPOLYGON",
              "download/CNTR_RG_"+scale+"_"+year+"_4326.geojson",
              "-sql", "SELECT CNTR_ID as id,NAME_ENGL as na FROM CNTR_RG_" + scale + "_" + year + "_4326 WHERE CNTR_ID NOT IN (" + nutsData["years"][year] + ")"])

           if debug: print(year + " " + scale + " CNTR RG - clean with buffer(0)")
           subprocess.run(["ogrinfo", "-dialect", "indirect_sqlite", "-sql", "update lay set geom=ST_Multi(ST_Buffer(geom,0))", "tmp/" + year + "_" + scale + "_CNTR_RG.gpkg"])

           if debug: print(year + " " + scale + " CNTR BN - filter, rename attributes")
           ogr2ogr.main(["-overwrite","-f", "GPKG",
              "tmp/" + year + "_" + scale + "_CNTR_BN.gpkg",
              "-nln", "lay", "-nlt", "MULTILINESTRING",
              "download/CNTR_BN_"+scale+"_"+year+"_4326.geojson",
              "-sql", "SELECT CNTR_BN_ID as id,CC_FLAG as cc,OTHR_FLAG as oth,COAS_FLAG as co FROM CNTR_BN_" + scale + "_" + year + "_4326 WHERE EU_FLAG='F' AND EFTA_FLAG='F'"])

           for level in ["0", "1", "2", "3"]:

               if debug: print(year + " " + scale + " NUTS RG " + level + " - filter, rename attributes")
               ogr2ogr.main(["-overwrite","-f", "GPKG",
                 "tmp/" + year + "_" + scale + "_" + level + "_NUTS_RG.gpkg",
                 "-nln", "lay", "-nlt", "MULTIPOLYGON",
                 "download/NUTS_RG_"+scale+"_"+year+"_4326.geojson",
                 "-sql", "SELECT N.NUTS_ID as id,A.NAME_LATN as na FROM NUTS_RG_" + scale + "_" + year + "_4326 as N left join 'download/NUTS_AT_" + year + ".csv'.NUTS_AT_" + year + " as A on N.NUTS_ID = A.NUTS_ID WHERE N.LEVL_CODE = " + level])

               if debug: print(year + " " + scale + " NUTS RG " + level + " - clean with buffer(0)")
               subprocess.run(["ogrinfo", "-dialect", "indirect_sqlite", "-sql", "update lay set geom=ST_Multi(ST_Buffer(geom,0))", "tmp/" + year + "_" + scale + "_" + level + "_NUTS_RG.gpkg"])

               if debug: print(year + " " + scale + " NUTS BN " + level + " - filter, rename attributes")
               ogr2ogr.main(["-overwrite","-f", "GPKG",
                 "tmp/" + year + "_" + scale + "_" + level + "_NUTS_BN.gpkg",
                 "-nln", "lay", "-nlt", "MULTILINESTRING",
                 "download/NUTS_BN_"+scale+"_"+year+"_4326.geojson",
                 "-sql", "SELECT NUTS_BN_ID as id,LEVL_CODE as lvl,EU_FLAG as eu,EFTA_FLAG as efta,CC_FLAG as cc,OTHR_FLAG as oth,COAS_FLAG as co FROM NUTS_BN_" + scale + "_" + year + "_4326 WHERE LEVL_CODE <= " + level])



# Perform coarse clipping by region, to improve reprojection process
def coarseClipping():
   print("coarseClipping")
   for year in nutsData["years"]:
      for geo in geos:

         extends = geos[geo]["crs"]["4326"]
         marginDeg = 31 if(geo == "EUR") else 10

         for type in ["RG", "BN"]:
            for scale in geos[geo]["scales"]:

# TODO: fix that warning:
# Warning 1: A geometry of type GEOMETRYCOLLECTION is inserted into layer lay of geometry type MULTIPOLYGON, which is not normally allowed by the GeoPackage specification, but the driver will however do it. To create a conformant GeoPackage, if using ogr2ogr, the -nlt option can be used to override the layer geometry type. This warning will no longer be emitted for this combination of layer and feature geometry type.

               if debug: print(year + " " + geo + " " + scale + " CNTR " + type + " - coarse clipping")
               ogr2ogr.main(["-overwrite","-f", "GPKG",
                 "tmp/" + year + "_" + geo + "_" + scale + "_CNTR_" + type + ".gpkg",
                 "tmp/" + year + "_" + scale + "_CNTR_" + type + ".gpkg",
                 "-nlt", "MULTIPOLYGON" if type=="RG" else "MULTILINESTRING",
                 #"-makevalid",
                 "-clipsrc", str(extends["xmin"]-marginDeg), str(extends["ymin"]-marginDeg), str(extends["xmax"]+marginDeg), str(extends["ymax"]+marginDeg)])

               for level in ["0", "1", "2", "3"]:

                  if debug: print(year + " " + geo + " " + scale + " NUTS " + type + " - coarse clipping")
                  ogr2ogr.main(["-overwrite","-f", "GPKG",
                    "tmp/" + year + "_" + geo + "_" + scale + "_" + level + "_NUTS_" + type + ".gpkg",
                    "tmp/" + year + "_" + scale + "_" + level + "_NUTS_" + type + ".gpkg",
                    "-nlt", "MULTIPOLYGON" if type=="RG" else "MULTILINESTRING",
                    #"-makevalid",
                    "-clipsrc", str(extends["xmin"]-marginDeg), str(extends["ymin"]-marginDeg), str(extends["xmax"]+marginDeg), str(extends["ymax"]+marginDeg)])



# Clip, reproject and convert as geojson
def reprojectClipGeojson():
   print("reprojectClipGeojson")
   for year in nutsData["years"]:
      for geo in geos:
         for crs in geos[geo]["crs"]:
            outpath = "tmp/"+year+"/"+geo+"/"+crs+"/"
            Path(outpath).mkdir(parents=True, exist_ok=True)
            extends = geos[geo]["crs"][crs]

            if debug: print(year + " " + geo + " " + crs + " - reproject + clip + geojson graticule")
            ogr2ogr.main(["-overwrite","-f","GeoJSON",
              outpath + "graticule.geojson",
              "src/resources/graticule.gpkg",
              "-t_srs", "EPSG:"+crs, "-s_srs", "EPSG:4258",
              #"-makevalid",
              "-clipdst", str(extends["xmin"]), str(extends["ymin"]), str(extends["xmax"]), str(extends["ymax"])
              ])

            for type in ["RG", "BN"]:
               for scale in geos[geo]["scales"]:

                  if debug: print(year + " " + geo + " " + crs + " " + scale + " " + type + " - reproject + clip + geojson CNTR")
                  ogr2ogr.main(["-overwrite","-f","GeoJSON",
                    outpath + scale + "_CNTR_" + type + ".geojson",
                    "tmp/" + year + "_" + geo + "_" + scale + "_CNTR_" + type + ".gpkg",
                    "-t_srs", "EPSG:"+crs, "-s_srs", "EPSG:4258",
                    #"-makevalid",
                    "-clipdst", str(extends["xmin"]), str(extends["ymin"]), str(extends["xmax"]), str(extends["ymax"])
                    ])

                  for level in ["0", "1", "2", "3"]:

                     if debug: print(year + " " + geo + " " + crs + " " + scale + " " + type + " " + level + " - reproject + clip + geojson NUTS")
                     ogr2ogr.main(["-overwrite","-f","GeoJSON",
                       outpath + scale + "_" + level + "_NUTS_" + type + ".geojson",
                       "tmp/" + year + "_" + geo + "_" + scale + "_" + level + "_NUTS_" + type + ".gpkg",
                       "-t_srs", "EPSG:"+crs, "-s_srs", "EPSG:4258",
                       #"-makevalid",
                       "-clipdst", str(extends["xmin"]), str(extends["ymin"]), str(extends["xmax"]), str(extends["ymax"])
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
                 "-t_srs", "EPSG:"+crs, "-s_srs", "EPSG:4258",
                 "-clipdst", str(extends["xmin"]), str(extends["ymin"]), str(extends["xmax"]), str(extends["ymax"])
                 ])



######## Full process #########
download()
filterRenameDecomposeClean()
coarseClipping()
reprojectClipGeojson()
topoGeojson()
points()
##############################

