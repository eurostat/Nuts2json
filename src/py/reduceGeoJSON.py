import os, json

## Reduce geometric precision of GeoJSON data

def reduceFile(filePath):
    with open(filePath, mode="r") as fp:
        data = json.load(fp)
    return reduceGeoJSON(data)


def reduceGeoJSON(data):
    type = data["type"]
    if(type == "FeatureCollection"): return reduceFeatureCollection(data)
    if(type == "Feature"): return reduceFeature(data)
    if(type == "Geometry"): return reduceGeometry(data)



def reduceFeatureCollection(fc):
    print(fc)
    #aa

def reduceFeature(f):
    print(f)
    ##

def reduceGeometry(g):
    print(g)
    ##


reduceFile("pub/v2/2021/3035/03M/nutsbn_0.json")
