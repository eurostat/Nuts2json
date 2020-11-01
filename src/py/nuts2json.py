# Extract decomposed information from input SHP files

from pathlib import Path

import ogr2ogr


####
# Target structure:
# topojson:  YEAR/GEO/PROJECTION/SCALE/<NUTS_LEVEL>.json
# geojson: YEAR/GEO/PROJECTION/SCALE/<TYPE>[_<NUTS_LEVEL>].json
# pts:      YEAR/GEO/PROJECTION/nutspt_<NUTS_LEVEL>.json
####

#years and scales covered
years = ["2010", "2013", "2016", "2021"]
scales = ["10M", "20M", "60M"]

#for each year, the countrie shown as stat units
filters = {
    "2010" : "'PT','ES','IE','UK','FR','IS','BE','LU','NL','CH','LI','DE','DK','IT','VA','MT','NO','SE','FI','EE','LV','LT','PL','CZ','SK','AT','SI','HU','HR','RO','BG','TR','EL','CY','MK','ME','RS','AL'",
    "2013" : "'PT','ES','IE','UK','FR','IS','BE','LU','NL','CH','LI','DE','DK','IT','VA','MT','NO','SE','FI','EE','LV','LT','PL','CZ','SK','AT','SI','HU','HR','RO','BG','TR','EL','CY','MK','ME','RS','AL'",
    "2016" : "'PT','ES','IE','UK','FR','IS','BE','LU','NL','CH','LI','DE','DK','IT','VA','MT','NO','SE','FI','EE','LV','LT','PL','CZ','SK','AT','SI','HU','HR','RO','BG','TR','EL','CY','MK','ME'",
    "2021" : "'PT','ES','IE','UK','FR','IS','BE','LU','NL','CH','LI','DE','DK','IT','VA','MT','NO','SE','FI','EE','LV','LT','PL','CZ','SK','AT','SI','HU','HR','RO','BG','TR','EL','CY','MK','ME'"
    }

#regions, CRSs and extends
geos = {
   "EUR" : {
      "4326" : { "xmin" : -25, "ymin" : 32.5, "xmax" : 46.5, "ymax" : 73.9},
      "4258" : { "xmin" : -25, "ymin" : 32.5, "xmax" : 46.5, "ymax" : 73.9},
      "3857" : { "xmin" : -2800000, "ymin" : 3884000, "xmax" : 5200000, "ymax" : 11690000},
      "3035" : { "xmin" : 2434560, "ymin" : 1340340, "xmax" : 7512390, "ymax" : 5664590}
   }
}


#prepare input data into tmp folder: filter, rename attributes, decompose by nuts level
def filterRenameDecompose():
   print("Graticule")
   ogr2ogr.main(["-overwrite","-f", "GPKG", "tmp/graticule.gpkg", "src/resources/shp/graticule.shp"])

   for year in years:
       for scale in scales:
           Path("tmp/").mkdir(parents=True, exist_ok=True)

           print(year + " " + scale + " CNTR RG - filter, rename attributes")
           ogr2ogr.main(["-overwrite","-f", "GPKG",
              "tmp/" + year + "_" + scale + "_CNTR_RG.gpkg",
              "src/resources/shp/" + year + "/CNTR_RG_" + scale + "_" + year + "_4326.shp",
              "-sql", "SELECT CNTR_ID as id,NAME_ENGL as na FROM CNTR_RG_" + scale + "_" + year + "_4326 WHERE CNTR_ID NOT IN (" + filters[year] + ")"])

           print(year + " " + scale + " CNTR BN - filter, rename attributes")
           ogr2ogr.main(["-overwrite","-f", "GPKG",
              "tmp/" + year + "_" + scale + "_CNTR_BN.gpkg",
              "src/resources/shp/" + year + "/CNTR_BN_" + scale + "_" + year + "_4326.shp",
              "-sql", "SELECT CNTR_BN_ID as id,CC_FLAG as cc,OTHR_FLAG as oth,COAS_FLAG as co FROM CNTR_BN_" + scale + "_" + year + "_4326 WHERE EU_FLAG='F' AND EFTA_FLAG='F'"])

           #nuts: filter, rename attributes
           for level in ["0", "1", "2", "3"]:

               print(year + " " + scale + " NUTS RG " + level + " - filter, rename attributes")
               ogr2ogr.main(["-overwrite","-f", "GPKG",
                 "tmp/" + year + "_" + scale + "_" + level + "_NUTS_RG.gpkg",
                 "src/resources/shp/" + year + "/NUTS_RG_" + scale + "_" + year + "_4326.shp",
                 "-sql", "SELECT N.NUTS_ID as id,A.NAME_LATN as na FROM NUTS_RG_" + scale + "_" + year + "_4326 as N left join 'src/resources/shp/" + year + "/NUTS_AT_" + year + ".csv'.NUTS_AT_" + year + " as A on N.NUTS_ID = A.NUTS_ID WHERE N.LEVL_CODE = " + level])

               print(year + " " + scale + " NUTS BN " + level + " - filter, rename attributes")
               ogr2ogr.main(["-overwrite","-f", "GPKG",
                 "tmp/" + year + "_" + scale + "_" + level + "_NUTS_BN.gpkg",
                 "src/resources/shp/" + year + "/NUTS_BN_" + scale + "_" + year + "_4326.shp",
                 "-sql", "SELECT NUTS_BN_ID as id,LEVL_CODE as lvl,EU_FLAG as eu,EFTA_FLAG as efta,CC_FLAG as cc,OTHR_FLAG as oth,COAS_FLAG as co FROM NUTS_BN_" + scale + "_" + year + "_4326 WHERE LEVL_CODE = " + level])



#clip, reproject and convert as geojson
def clipReprojGeojson():
   for year in years:
      for geo in geos:
         for crs in geos[geo]:
            print(year + " " + geo + " " + crs)
            extends = geos[geo][crs]

            #handle gra?

            for scale in scales:
               # clip - reproject - to geojson
               for type in ["RG", "BN"]:
                  print()
                  #cntr
               for level in ["0", "1", "2", "3"]:
                  for type in ["RG", "BN"]:
                     #nuts
                     print()


#make topojson file from geojson files
#simplify them with topojson simplify
def topojsonSimplify():
   print()

   #run command
   #https://stackoverflow.com/questions/89228/how-to-call-an-external-command
   #import subprocess
   #subprocess.run(["ls", "-l"])

   #make topojson base files, one per nuts level
   #https://github.com/topojson/topojson-server/blob/master/README.md#geo2topo
   #echo "4- $year $scale $proj $level - geojson to topojson"
   #geo2topo -q 20000 nutsrg=$dir"/RG/"$level".json" nutsbn=$dir"/BN/"$level".json" cntrg=$dir"/RG/CNTR.json" cntbn=$dir"/BN/CNTR.json" gra=$dir"/graticule.json" > $dir"/"$level".json"
   #quantization: q small means strong 'simplification'

   #simplify topojson files
   #https://github.com/topojson/topojson-simplify/blob/master/README.md#toposimplify
   #echo "5- $year $scale $proj $level - topojson simplify"
   #outdir="../"$year"/"$proj"/"$scale"M"
   #mkdir -p $outdir
   #toposimplify -f -P 0.99 -o "$outdir/$level.json" "$dir/$level.json"


#produces geojson from topojson
def topoToGeojson():
   print()


#produce point representations
def pts():
   print()



#filterRenameDecompose()
clipReprojGeojson()
#topojsonSimplify()
#topoToGeojson()
#pts()




#run command
#https://stackoverflow.com/questions/89228/how-to-call-an-external-command

#import subprocess
#subprocess.run(["ls", "-l"])

#
#https://gis.stackexchange.com/questions/39080/using-ogr2ogr-to-convert-gml-to-shapefile-in-python
#import ogr2ogr
#https://github.com/OSGeo/gdal/tree/master/gdal/swig/python
#https://pcjericks.github.io/py-gdalogr-cookbook/
#ogr2ogr.main(["","-f", "KML", "out.kml", "data/san_andres_y_providencia_administrative.shp"])


#For TopoJSON format: /<YEAR>/<PROJECTION>/<SCALE>/<NUTS_LEVEL>.json
#For GeoJSON format: /<YEAR>/<PROJECTION>/<SCALE>/<TYPE>[_<NUTS_LEVEL>].json
#nutsrg nutsbn cntrg cntbn gra
#PTs: /<YEAR>/<PROJECTION>/nutspt_<NUTS_LEVEL>.json
