import os, json

## Reduce geometric precision of GeoJSON data

def reduceFile(filePath):
    with open(filePath, mode="r") as fp:
        data = json.load(fp)
    return reduceGeoJSON(data)


def reduceGeoJSON(data):
    type = data["type"]
    if(type == "FeatureCollection"): reduceFeatureCollection(data)
    if(type == "Feature"): reduceFeature(data)
    if(type == "Geometry"): reduceGeometry(data)




def reduceFeatureCollection(fc):
    for i in range(len(fc["features"])):
        f = fc["features"][i]
        reduceFeature(f)
        fc["features"][i] = f

def reduceFeature(f):
    g = f["geometry"]
    reduceGeometry(g)
    f["geometry"] = g

def reduceGeometry(g):
    type = g["type"]
    if(type == "LineString"): reduceLineString(g)
    else: print("Not supported geometry type: " + type)

def reduceLineString(ls):
    cs = ls["coordinates"]
    reduceCoordinates(cs)
    ls["coordinates"] = cs

def reduceCoordinates(cs):
    for i in range(len(cs)):
        for j in range(len(cs[i])):
            c = cs[i][j]
            print(c)

#2.1.1. Positions
#2.1.2. Point
#2.1.3. MultiPoint
#2.1.4. 
#2.1.5. MultiLineString
#2.1.6. Polygon
#2.1.7. MultiPolygon
#2.1.8 Geometry Collection



reduceFile("pub/v2/2021/3035/03M/nutsbn_0.json")
