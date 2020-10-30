print("Tests")

#run command
#https://stackoverflow.com/questions/89228/how-to-call-an-external-command

import subprocess
subprocess.run(["ls", "-l"])

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

####
# topojson: YEAR/GEO/PROJECTION/SCALE/<TYPE>[_<NUTS_LEVEL>].json
# geojson:  YEAR/GEO/PROJECTION/SCALE/<NUTS_LEVEL>.json
# pts:      YEAR/GEO/PROJECTION/nutspt_<NUTS_LEVEL>.json
####

