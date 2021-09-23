"""
Reduce geometric precision of GeoJSON data: Round the coordinates to a specified number of decimals.
Warning: This can result in invalid geometries (self overlaping linestrings for example).
"""

import json

def reduceGeoJSONFile(filePath, nbDec, outFilePath=""):
    """
    Reduce geometric precision of a GeoJSON file by rounding its coordinates.

    Args:
        filePath (str): The file location.
        nbDec (int): The number of decimals.
        outFilePath (str): The output file location. If not specified, the input file is overriden.
    """

    # Open file
    with open(filePath, mode="r") as fp:
        data = json.load(fp)

    # Apply reduction
    reduceGeoJSON(data, nbDec)

    # Get output file path
    if not outFilePath: outFilePath = filePath

    # Save output
    with open(outFilePath, "w") as fp:
        json.dump(data, fp)





# Reduce geometric precision of geojson structure
def reduceGeoJSON(data, nbDec):
    """
    Reduce geometric precision of a GeoJSON data by rounding its coordinates.

    Args:
        data (dict): The GeoJSON data.
        nbDec (int): The number of decimals.
    """

    for key in data:
        data_ = data[key]

        # if the key is "coordinates", reduce them
        if key == "coordinates": reduceCoordinatesRec(data_, nbDec)

        # if the key is a list, reduce its elements (recursively)
        elif isinstance(data_, list):
            for i in range(len(data_)): reduceGeoJSON(data_[i], nbDec)

        # if the key is a dict, reduce it (recursively)
        elif isinstance(data_, dict): reduceGeoJSON(data_, nbDec)





def reduceCoordinatesRec(cs, nbDec):
    """
    Reduce geometric precision of a GeoJSON coordinates by rounding its values.
    If a list of lists is used, then the function is called recursivelly.

    Args:
        cs (list): The GeoJSON coordinates.
        nbDec (int): The number of decimals.
    """

    # empty list
    if len(cs)==0: return

    # get first element
    c = cs[0]

    # if the first element is not a list, the cs is a coordinate
    if not isinstance(c, list):
        reduceCoordinate(cs, nbDec)
        return;

    # get first element - one level below
    c = cs[0][0]

    # if it is a list, reduce the components (recursively)
    if isinstance(c, list):
        for i in range(len(cs)):
            reduceCoordinatesRec(cs[i], nbDec)
    else:
        # reduce it
        reduceCoordinates(cs, nbDec)



def reduceCoordinates(cs, nbDec):
    """
    Reduce geometric precision of a GeoJSON coordinates by rounding its values.
    The input is supposed to be a list of coordinates.

    Args:
        cs (list): The GeoJSON coordinates.
        nbDec (int): The number of decimals.
    """

    # TODO: remove duplicate vertices, if any
    for i in range(len(cs)):
        reduceCoordinate(cs[i], nbDec)




def reduceCoordinate(c, nbDec):
    """
    Reduce geometric precision of a GeoJSON coordinate by rounding its values.
    The input is supposed to be a list of values.

    Args:
        cs (list): The GeoJSON coordinate.
        nbDec (int): The number of decimals.
    """

    for i in range(len(c)):
        c[i] = round(c[i], nbDec)
        if nbDec == 0: c[i] = int(c[i])
        #TODO make it possible to round also 32455 to 32000









# Tests
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
