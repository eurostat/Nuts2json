import os, json

# Reduce geometric precision of GeoJSON data

# simplify: find "coordinates"

def reduceGeoJSONFile(filePath, nbDec):
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
    if(type == "Point"): reducePoint(g, nbDec)
    if(type == "LineString"): reduceLineString(g, nbDec)
    if(type == "Polygon"): reducePolygon(g, nbDec)
    else: print("Not supported geometry type: " + type)

# https://datatracker.ietf.org/doc/html/rfc7946#appendix-A.1

def reducePoint(pt, nbDec):
    reduceCoordinate(pt["coordinates"], nbDec)

def reduceLineString(ls, nbDec):
    reduceCoordinates(ls["coordinates"], nbDec)

def reducePolygon(poly, nbDec):
    reduceCoordinatesX(poly["coordinates"], nbDec)


# reduce an array of coordinates
def reduceCoordinates(cs, nbDec):
    for i in range(len(cs)):
        reduceCoordinate(cs[i], nbDec)

# reduce an array of arrays of coordinates
def reduceCoordinatesX(css, nbDec):
    for i in range(len(css)):
        reduceCoordinates(css[i], nbDec)

# reduce a coordinate
def reduceCoordinate(c, nbDec):
    for i in range(len(c)):
        c[i] = round(c[i], nbDec)



# Test
data = reduceGeoJSONFile("pub/v2/2021/3035/03M/nutsbn_0.json", 1)
print(data)
