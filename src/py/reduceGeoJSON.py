import json

# Reduce geometric precision of GeoJSON data

def reduceGeoJSONFile(filePath, nbDec):
    with open(filePath, mode="r") as fp:
        data = json.load(fp)
    reduceGeoJSON(data, nbDec)
    return data


def reduceGeoJSON(data, nbDec):
    for key in data:
        data_ = data[key]
        if key == "coordinates": reduceCoordinatesRec(data_, nbDec)
        elif isinstance(data_, list):
            for i in range(len(data_)): reduceGeoJSON(data_[i], nbDec)
        elif isinstance(data_, dict): reduceGeoJSON(data_, nbDec)



# reduce coordinates
def reduceCoordinatesRec(cs, nbDec):
    if len(cs)==0: return
    c = cs[0]
    if isinstance(c, list):
        for i in range(len(cs)):
            reduceCoordinatesRec(cs[i], nbDec)
    else:
        reduceCoordinates(cs, nbDec)

# reduce a list of coordinates
def reduceCoordinates(cs, nbDec):
    for i in range(len(cs)):
        reduceCoordinate(cs[i], nbDec)

# reduce a coordinate
def reduceCoordinate(c, nbDec):
    print(c)
    for i in range(len(c)):
        c[i] = round(c[i], nbDec)



# Test
data = reduceGeoJSONFile("pub/v2/2021/3035/03M/nutsbn_0.json", 1)
#print(data)
