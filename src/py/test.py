import os, ogr2ogr, subprocess, json, urllib.request

#import os
#from osgeo import ogr
#import geopandas
#from geopandas import datasets, GeoDataFrame, read_file

year="2021"
scale="60M"
geo=""
crs="3035"
type="RG"

outpath = "tmp/"+year+"/"+geo+"/"+crs+"/"

input = outpath + scale + "_CNTR_" + type + ".geojson",
output = outpath + scale + "_LAND_" + type + ".geojson",


ogr2ogr.main(["-overwrite","-f","GeoJSON",
                    output,
                    input,
                    "-nlt", "MULTIPOLYGON" if type=="RG" else "MULTILINESTRING",
                    "-dialect", "sqlite"
                    "-sql", "SELECT ST_Union(geometry) FROM input",
])

#ogr2ogr output.shp input.shp -dialect sqlite -sql "SELECT ST_Union(geometry), dissolve_field FROM input GROUP BY dissolve_field"





# https://geopandas.org/getting_started/introduction.html
#path_to_data = geopandas.datasets.get_path("nybb")
#gdf = geopandas.read_file(path_to_data)
#gdf


#def dedup(geometries):
#    """Return a geometry that is the union of all geometries."""
#    if not geometries:  return None
#    multi  = ogr.Geometry(ogr.wkbMultiPolygon)
#    for g in geometries:
#        multi.AddGeometry(g.geometry())
#    return multi.UnionCascaded()

#from shapely.geometry import Polygon
#from shapely.ops import cascaded_union
#polygon1 = Polygon([(0, 0), (5, 3), (5, 0)])
#polygon2 = Polygon([(0, 0), (3, 10), (3, 0)])
#polygons = [polygon1, polygon2]
#u = cascaded_union(polygons)


# write file
#gdf.to_file("my_file.geojson", driver="GeoJSON")
