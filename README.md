# Nuts2json

<a href="https://github.com/jgaffuri/Nuts2json">Nuts2json</a> supports the design of web maps of <a href="http://ec.europa.eu/eurostat/web/json-and-unicode-web-services/getting-started/rest-request" target="_blank">Eurostat data</a>. It provides various reusable versions of <a href="http://ec.europa.eu/eurostat/web/nuts/overview" target="_blank">Eurostat NUTS dataset</a> as web formats such as <a href="http://geojson.org/" target="_blank">GeoJSON</a> and <a href="https://github.com/mbostock/topojson/wiki" target="_blank">TopoJSON</a>. In a way, it provides a blank map of geometries ready for use with your own data and colors.

For an example of such blank map, see <a href="http://jgaffuri.github.io/Nuts2json/overview.html?proj=laea&lvl=3" target="_blank"><b>HERE</b></a>.

file:///H:/workspace/Nuts2json/overview.html

## Supported formats

The JSON files are available in the folder <a href="/json" target="_blank">json</a> according to a predefined path pattern. For example, <a href="https://jgaffuri.github.io/Nuts2json/json/topojson/wm/500px/RG_lvl2.json" target="_blank">json/topojson/wm/500px/RG_lvl2.json</a> is the path to a topojson file of NUTS regions level 2 in projection web mercator, for a map size 500*500px.

The file path pattern is: <i>/json/\<FORMAT\>/\<PROJECTION\>/\<SIZE\>/\<TYPE\>_lvl\<NUTS_LEVEL\>.json</i>

where:

- <i>FORMAT</i> is the file format. Currently, only <a href="https://github.com/mbostock/topojson/wiki" target="_blank">TopoJSON</a> is provided. <a href="http://geojson.org/" target="_blank">GeoJSON</a> format is to come.
- <i>PROJECTION</i> is the map projection. Currently, European projection LAEA (<a href="http://spatialreference.org/ref/epsg/etrs89-etrs-laea/" target="_blank">EPSG 3035</a>) and Web Mercator (<a href="http://spatialreference.org/ref/sr-org/7483/" target="_blank">EPSG 3857</a>) are provided.
- <i>SIZE</i> is the size of the map, in pixel.
- <i>TYPE</i> is the type of objects: either the regions (TYPE=RG), the boundaries (TYPE=BN) or both (TYPE=RG_BN)
- <i>NUTS_LEVEL</i> is the NUTS level to be shown on the map, from national level (NUTS_LEVEL=0) to provincial level (NUTS_LEVEL=3).

### Feature properties

NUTS regions (TYPE=RG) have a single property, <i>id</i>, which is the NUTS identifier used to join statistical figures and then colors to the regions.

NUTS boundaries (TYPE=BN) have the following properties:
  - <i>lvl</i>: The NUTS level of the boundary, from 0 (national level) to 3 (provincial level).
  - <i>cst</i>: T if the boundary is coastal, F otherwise.
  - <i>eu</i>: T if the boundary separate two EU member states, F otherwise.
  - <i>efta</i>: T if the boundary touches at least one EFTA country, F otherwise.
  - <i>cc</i>: T if the boundary touches at least one Candidate Country, F otherwise.
  - <i>oth</i>: T if the boundary touches a country wich is not EU, EFTA,CC. F otherwise.

## Usage example

[TODO: describe example, based on d3]

## Technical details

These files are produced from the NUTS SHP files provided on Eurostat website, <a href="http://ec.europa.eu/eurostat/web/gisco/geodata/reference-data/administrative-units-statistical-units/nuts" target="_blank">here</a>. The input SHP files are in the <a href="/shp" target="_blank">shp folder</a>. They are transformed using <a href="http://www.gdal.org/" target="_blank">GDAL</a> and, of course, <a href="https://github.com/mbostock/topojson/wiki" target="_blank">TopoJSON</a> libraries. The processes are automated in Bash files, which are also shared in this repository.
