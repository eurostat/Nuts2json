import os, json

## Reduce geometric precision of GeoJSON data

def reduceFile(filePath, nbDec):
    with open(filePath, mode="r") as fp:
        data = json.load(fp)
    reduceGeoJSON(data, nbDec)
    return data


def reduceGeoJSON(data, nbDec):
    type = data["type"]
    if(type == "FeatureCollection"): reduceFeatureCollection(data, nbDec)
    if(type == "Feature"): reduceFeature(data, nbDec)
    if(type == "Geometry"): reduceGeometry(data, nbDec)



def reduceFeatureCollection(fc, nbDec):
    for i in range(len(fc["features"])):
        reduceFeature(fc["features"][i], nbDec)

def reduceFeature(f, nbDec):
    reduceGeometry(f["geometry"], nbDec)

def reduceGeometry(g, nbDec):
    type = g["type"]
    if(type == "LineString"): reduceLineString(g, nbDec)
    else: print("Not supported geometry type: " + type)

def reduceLineString(ls, nbDec):
    reduceCoordinates(ls["coordinates"], nbDec)

def reduceCoordinates(cs, nbDec):
    for i in range(len(cs)):
        for j in range(len(cs[i])):
            c = cs[i][j]
            c = round(c, nbDec)
            cs[i][j] = c

#2.1.1. Positions
#2.1.2. Point
#2.1.3. MultiPoint
#2.1.4. 
#2.1.5. MultiLineString
#2.1.6. Polygon
#2.1.7. MultiPolygon
#2.1.8 Geometry Collection



data = reduceFile("pub/v2/2021/3035/03M/nutsbn_0.json", 1)
#print(data)
