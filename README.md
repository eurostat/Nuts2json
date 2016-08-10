# Nuts2json

<a href="https://github.com/jgaffuri/Nuts2json">Nuts2json</a> supports the design of web maps of <a href="http://ec.europa.eu/eurostat/web/json-and-unicode-web-services/getting-started/rest-request" target="_blank">Eurostat data</a>. It provides various reusable versions of <a href="http://ec.europa.eu/eurostat/web/nuts/overview" target="_blank">Eurostat NUTS dataset</a> as web formats such as <a href="http://geojson.org/" target="_blank">GeoJSON</a> and <a href="https://github.com/mbostock/topojson/wiki" target="_blank">TopoJSON</a>. In a way, it provides a blank map of geometries ready for use with your own data and colors.

For an example of such blank map, see <a href="http://jgaffuri.github.io/Nuts2json/overview.html" target="_blank"><b>HERE</b></a>.

## Supported formats

The JSON files are available in the folder <a href="/json" target="_blank">json</a>. Each file path pattern is:
/json/\<FORMAT\>/\<PROJECTION\>/\<SIZE\>/\<TYPE\>_lvl\<NUTS_LEVEL\>.json
- FORMAT is the file format. Currently, only <a href="https://github.com/mbostock/topojson/wiki" target="_blank">TopoJSON</a> is provided. <a href="http://geojson.org/" target="_blank">GeoJSON</a> format is to come.
- PROJECTION is the map projection. Currently, European projection LAEA (<a href="http://spatialreference.org/ref/epsg/etrs89-etrs-laea/" target="_blank">EPSG 3035</a>) and Web Mercator (<a href="http://spatialreference.org/ref/sr-org/7483/" target="_blank">EPSG 3857</a>) are provided.
- SIZE is the size of the map, in pixel.
- TYPE is the type of objects: either the regions (TYPE=RG), the boundaries (TYPE=BN) or both (TYPE=RG_BN)
- NUTS_LEVEL is the NUTS level to be shown on the map, from national level (NUTS_LEVEL=0) to province level (NUTS_LEVEL=3).

### Feature properties

- Regions (TYPE=RG)
  - id: The NUTS identifier
- Boundaries (TYPE=BN)
  - lvl: The NUTS level of the boundary, from 0 (national level) to 3 (provincial level).
  - cst: T if the boundary is coastal, F otherwise.
  - eu: T if the boundary separate two EU member states, F otherwise.
  - efta: T if the boundary touches at least one EFTA country, F otherwise.
  - cc: T if the boundary touches at least one Candidate Country, F otherwise.
  - oth: T if the boundary touches a country wich is not EU, EFTA,CC. F otherwise.

## Technical details

These files are produced from the NUTS SHP files provided on Eurostat website, <a href="http://ec.europa.eu/eurostat/web/gisco/geodata/reference-data/administrative-units-statistical-units/nuts" target="_blank">here</a>. These files are transformed using http://www.gdal.org/ <a href="" target="_blank">GDAL</a> and, of course, <a href="https://github.com/mbostock/topojson/wiki" target="_blank">TopoJSON</a> libraries. The processes are automated in Bash.
