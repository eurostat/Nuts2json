import json

# Reduce geometric precision of GeoJSON data

# simplify: find "coordinates"

def reduceGeoJSONFile(filePath, nbDec):
    with open(filePath, mode="r") as fp:
        data = json.load(fp)
    reduceGeoJSON(data, nbDec)
    return data


def reduceGeoJSON(data, nbDec):
    for key in data:
        data_ = data[key]
        if key == "coordinates": reduceCoordinates(data_, nbDec)
        elif isinstance(data_, list):
            for i in range(len(data_)): reduceGeoJSON(data_[i], nbDec)
        elif isinstance(data_, dict): reduceGeoJSON(data_, nbDec)



# reduce an array of coordinates
def reduceCoordinates(cs, nbDec):
    print(cs)
    if len(cs)==0: return
    c = cs[0]
    if isinstance(c, list):
        print("A")
    else:
        print("XXX")

    #for i in range(len(cs)):
    #    reduceCoordinate(cs[i], nbDec)

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
#print(data)
