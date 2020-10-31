# Extract decomposed information from input SHP files

from pathlib import Path
import ogr2ogr

#years and scales covered
years = ["2010", "2013", "2016", "2021"]
scales = ["10M", "20M", "60M"]

#for each year, the countrie shown as stat units
filters = {
    "2010" : "'PT','ES','IE','UK','FR','IS','BE','LU','NL','CH','LI','DE','DK','IT','VA','MT','NO','SE','FI','EE','LV','LT','PL','CZ','SK','AT','SI','HU','HR','RO','BG','TR','EL','CY','MK','ME','RS','AL'",
    "2013" : "'PT','ES','IE','UK','FR','IS','BE','LU','NL','CH','LI','DE','DK','IT','VA','MT','NO','SE','FI','EE','LV','LT','PL','CZ','SK','AT','SI','HU','HR','RO','BG','TR','EL','CY','MK','ME','RS','AL'",
    "2016" : "'PT','ES','IE','UK','FR','IS','BE','LU','NL','CH','LI','DE','DK','IT','VA','MT','NO','SE','FI','EE','LV','LT','PL','CZ','SK','AT','SI','HU','HR','RO','BG','TR','EL','CY','MK','ME'",
    "2021" : "'PT','ES','IE','UK','FR','IS','BE','LU','NL','CH','LI','DE','DK','IT','VA','MT','NO','SE','FI','EE','LV','LT','PL','CZ','SK','AT','SI','HU','HR','RO','BG','TR','EL','CY','MK','ME'"
    }



print("Graticule")
ogr2ogr.main(["-overwrite","-f", "GPKG", "tmp/graticule.gpkg", "src/resources/shp/graticule.shp"])

for year in years:
    for scale in scales:
        Path("tmp/").mkdir(parents=True, exist_ok=True)

        print(year + " " + scale + " CNTR RG - filter, rename attributes")
        ogr2ogr.main(["-overwrite","-f", "GPKG",
           "tmp/" + year + "_" + scale + "_CNTR_RG.gpkg",
           "src/resources/shp/" + year + "/CNTR_RG_" + scale + "_" + year + "_4326.shp",
           "-sql", "SELECT CNTR_ID as id,NAME_ENGL as na FROM CNTR_RG_" + scale + "_" + year + "_4326 WHERE CNTR_ID NOT IN (" + filters[year] + ")"])

        print(year + " " + scale + " CNTR BN - filter, rename attributes")
        ogr2ogr.main(["-overwrite","-f", "GPKG",
           "tmp/" + year + "_" + scale + "_CNTR_BN.gpkg",
           "src/resources/shp/" + year + "/CNTR_BN_" + scale + "_" + year + "_4326.shp",
           "-sql", "SELECT CNTR_BN_ID as id,CC_FLAG as cc,OTHR_FLAG as oth,COAS_FLAG as co FROM CNTR_BN_" + scale + "_" + year + "_4326 WHERE EU_FLAG='F' AND EFTA_FLAG='F'"])

        #nuts: filter, rename attributes
        for lvl in ["0", "1", "2", "3"]:

            print(year + " " + scale + " NUTS RG " + lvl + " - filter, rename attributes")
            ogr2ogr.main(["-overwrite","-f", "GPKG",
              "tmp/" + year + "_" + scale + "_" + lvl + "_NUTS_RG.gpkg",
              "src/resources/shp/" + year + "/NUTS_RG_" + scale + "_" + year + "_4326.shp",
              "-sql", "SELECT N.NUTS_ID as id,A.NAME_LATN as na FROM NUTS_RG_" + scale + "_" + year + "_4326 as N left join 'src/resources/shp/" + year + "/NUTS_AT_" + year + ".csv'.NUTS_AT_" + year + " as A on N.NUTS_ID = A.NUTS_ID WHERE N.LEVL_CODE = " + lvl])

            print(year + " " + scale + " NUTS BN " + lvl + " - filter, rename attributes")
            ogr2ogr.main(["-overwrite","-f", "GPKG",
              "tmp/" + year + "_" + scale + "_" + lvl + "_NUTS_BN.gpkg",
              "src/resources/shp/" + year + "/NUTS_BN_" + scale + "_" + year + "_4326.shp",
              "-sql", "SELECT NUTS_BN_ID as id,LEVL_CODE as lvl,EU_FLAG as eu,EFTA_FLAG as efta,CC_FLAG as cc,OTHR_FLAG as oth,COAS_FLAG as co FROM NUTS_BN_" + scale + "_" + year + "_4326 WHERE LEVL_CODE = " + lvl])
