# Extract decomposed information from input SHP files

from pathlib import Path
import ogr2ogr

years = ["2010", "2013", "2016", "2021"]
scales = ["10M", "20M", "60M"]

#for each year, the countrie shown as stat units
filters = {
    "2010" : "'PT','ES','IE','UK','FR','IS','BE','LU','NL','CH','LI','DE','DK','IT','VA','MT','NO','SE','FI','EE','LV','LT','PL','CZ','SK','AT','SI','HU','HR','RO','BG','TR','EL','CY','MK','ME','RS','AL'",
    "2013" : "'PT','ES','IE','UK','FR','IS','BE','LU','NL','CH','LI','DE','DK','IT','VA','MT','NO','SE','FI','EE','LV','LT','PL','CZ','SK','AT','SI','HU','HR','RO','BG','TR','EL','CY','MK','ME','RS','AL'",
    "2016" : "'PT','ES','IE','UK','FR','IS','BE','LU','NL','CH','LI','DE','DK','IT','VA','MT','NO','SE','FI','EE','LV','LT','PL','CZ','SK','AT','SI','HU','HR','RO','BG','TR','EL','CY','MK','ME'",
    "2021" : "'PT','ES','IE','UK','FR','IS','BE','LU','NL','CH','LI','DE','DK','IT','VA','MT','NO','SE','FI','EE','LV','LT','PL','CZ','SK','AT','SI','HU','HR','RO','BG','TR','EL','CY','MK','ME'"
    }

for year in years:
    for scale in scales:
        Path("tmp/"+year+"/"+scale).mkdir(parents=True, exist_ok=True)

        #country: filter, rename attributes
        print(year + " " + scale + " CNTR RG")
        inputFile = "src/resources/shp/" + year + "/CNTR_RG_" + scale + "_" + year + "_4326.shp"
        outputFile = "tmp/" + year + "/" + scale + "/CNTR_RG.shp" #TODO use gpkg?
        ogr2ogr.main(["-overwrite","-f", "ESRI Shapefile", "-lco", "ENCODING=UTF-8", outputFile, inputFile, "-sql", "SELECT CNTR_ID as id,NAME_ENGL as na FROM CNTR_RG_"+scale+"_"+year+"_4326 WHERE CNTR_ID NOT IN ("+filters[year]+")"])

        print(year + " " + scale + " CNTR BN")
        inputFile = "src/resources/shp/" + year + "/CNTR_BN_" + scale + "_" + year + "_4326.shp"
        print(Path(inputFile).exists())

        #nuts: filter, rename attributes
        for lvl in ["0", "1", "2", "3"]:

            print(year + " " + scale + " NUTS RG " + lvl)
            inputFile = "src/resources/shp/" + year + "/NUTS_RG_" + scale + "_" + year + "_4326.shp"
            print(Path(inputFile).exists())

            print(year + " " + scale + " NUTS BN " + lvl)
            inputFile = "src/resources/shp/" + year + "/NUTS_BN_" + scale + "_" + year + "_4326.shp"
            print(Path(inputFile).exists())

#TODO: do something with graticule?
