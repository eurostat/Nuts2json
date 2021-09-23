############
# 
# Reduce geometric precision of GeoJSON data.
# Round the coordinates to a specified number of decimals.
# Warning: This can result in invalid geometries.
# 
############

import json


# Reduce geometric precision of a file
def reduceGeoJSONFile(filePath, nbDec, outFilePath=""):

    # Open file
    with open(filePath, mode="r") as fp:
        data = json.load(fp)

    # Apply reduction
    reduceGeoJSON(data, nbDec)

    # Save output
    if not(outFilePath): outFilePath = filePath
    with open(outFilePath, "w") as fp:
        json.dump(data, fp)



# Reduce geometric precision of geojson structure
def reduceGeoJSON(data, nbDec):
    for key in data:
        data_ = data[key]

        # if the key is "coordinates", reduce them
        if key == "coordinates": reduceCoordinatesRec(data_, nbDec)

        # if the key is a list, reduce its elements (recursively)
        elif isinstance(data_, list):
            for i in range(len(data_)): reduceGeoJSON(data_[i], nbDec)

        # if the key is a dict, reduce it (recursively)
        elif isinstance(data_, dict): reduceGeoJSON(data_, nbDec)



# reduce coordinates
def reduceCoordinatesRec(cs, nbDec):

    # empty list
    if len(cs)==0: return

    # get first element
    c = cs[0][0]

    # if it is a list, reduce the components (recursively)
    if isinstance(c, list):
        for i in range(len(cs)):
            reduceCoordinatesRec(cs[i], nbDec)
    else:
        # reduce it
        reduceCoordinates(cs, nbDec)



# reduce a list of coordinates
# TODO: remove duplicate vertices, if any
def reduceCoordinates(cs, nbDec):
    for i in range(len(cs)):
        reduceCoordinate(cs[i], nbDec)

# reduce a coordinate
def reduceCoordinate(c, nbDec):
    for i in range(len(c)):
        c[i] = round(c[i], nbDec)



# Test
#filePath = "pub/v2/2021/3035/03M/nutsbn_0.json"
#data = reduceGeoJSONFile(filePath, 2)

#with open(filePath, mode="r") as fp:
#    data = json.load(fp)

#with open("/home/juju/Bureau/AAA_in.json", "w") as fp:
#    json.dump(data, fp)

#reduceGeoJSON(data, 0)
#print(data)

#with open("/home/juju/Bureau/AAA_out.json", "w") as fp:
#    json.dump(data, fp)


#Test with override
#reduceGeoJSONFile("/home/juju/Bureau/a.json", 0, True)
