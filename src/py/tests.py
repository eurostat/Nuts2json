print("Tests")

#run command
#https://stackoverflow.com/questions/89228/how-to-call-an-external-command

import subprocess
subprocess.run(["ls", "-l"])

#
#https://gis.stackexchange.com/questions/39080/using-ogr2ogr-to-convert-gml-to-shapefile-in-python
#import ogr2ogr
#ogr2ogr.main(["","-f", "KML", "out.kml", "data/san_andres_y_providencia_administrative.shp"])
