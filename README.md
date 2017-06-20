# Nuts2json

<a href="https://github.com/jgaffuri/Nuts2json">Nuts2json</a> provides various reusable versions of <a href="http://ec.europa.eu/eurostat/web/nuts/overview" target="_blank">Eurostat NUTS dataset</a> as web formats such as <a href="http://geojson.org/" target="_blank">GeoJSON</a> and <a href="https://github.com/mbostock/topojson/wiki" target="_blank">TopoJSON</a>. It supports the design of statistical web maps of <a href="http://ec.europa.eu/eurostat/web/json-and-unicode-web-services/getting-started/rest-request" target="_blank">Eurostat data</a>. In a way, it provides a blank map of geometries ready for use with your own data and colors.

For an example of such blank map, see <a href="http://jgaffuri.github.io/Nuts2json/overview.html?proj=laea&lvl=3&s=1000" target="_blank"><b>HERE</b></a> (the URL parameters can be changed).

For an example of thematic map, see <a href="http://jgaffuri.github.io/EurostatVisu/population_map.html"><b>this map</b></a> showing population in Europe.


## Supported formats

The JSON files are available in the folder <a href="/json" target="_blank">json</a> according to a predefined path pattern. For example, <a href="https://jgaffuri.github.io/Nuts2json/json/topojson/wm/600px/NUTS_lvl2.json" target="_blank">json/topojson/wm/600px/NUTS_lvl2.json</a> is the path to a TopoJSON file of NUTS regions level 2 in projection web mercator, for a map size 600*600px.

The file path pattern is: <i>/json/\<FORMAT\>/\<PROJECTION\>/\<SIZE\>/\NUTS_lvl\<NUTS_LEVEL\>.json</i>

where:

- <i>FORMAT</i> is the file format. Currently, only <a href="https://github.com/mbostock/topojson/wiki" target="_blank">TopoJSON</a> is provided. <a href="http://geojson.org/" target="_blank">GeoJSON</a> format is to come.
- <i>PROJECTION</i> is the map projection. Currently, European projection LAEA (<a href="http://spatialreference.org/ref/epsg/etrs89-etrs-laea/" target="_blank">EPSG 3035</a>) and Web Mercator (<a href="http://spatialreference.org/ref/sr-org/7483/" target="_blank">EPSG 3857</a>) are provided.
- <i>SIZE</i> is the size of the map, in pixel. Currently, all maps are squared. The available sizes are 400, 600, 800, 1000 and 1200 pixels.
- <i>NUTS_LEVEL</i> is the NUTS level to be shown on the map, from national level (NUTS_LEVEL=0) to provincial level (NUTS_LEVEL=3).

### Features

Each file provides 4 feature types with the following properties:

NUTS regions (feature type <i>nutsrg</i>) have two properties:
  - <i>id</i>: The NUTS identifier to be used to join Eurostat statistical figures and then assign colors to the regions.
  - <i>na</i>: The geographical name of the region.

NUTS boundaries (feature type <i>nutsbn</i>) have the following properties:
  - <i>lvl</i>: The NUTS level of the boundary, from 0 (national level) to 3 (provincial level).
  - <i>eu</i>: T if the boundary separate two EU member states, F otherwise.
  - <i>efta</i>: T if the boundary touches at least one EFTA country, F otherwise.
  - <i>cc</i>: T if the boundary touches at least one Candidate Country, F otherwise.
  - <i>oth</i>: T if the boundary touches a country wich is not EU, EFTA,CC. F otherwise.
<u>NB:</u> The coastal boundaries are not included.

Non-european countries (feature type <i>cntrg</i>)
  - <i>cid</i>: The country identifier (2 letters code).
  - <i>cna</i>: The country name.

Non-european boundaries (feature type <i>cntbn</i>). Coastal boundaries are not included.

## Usage example

See <a href="http://jgaffuri.github.io/EurostatVisu/population_map.html">this map</a> on <a href="https://github.com/jgaffuri/EurostatVisu/blob/gh-pages/README.md">EurostatVisu</a> project.

[TODO: describe simple examples, based on d3.]

## Technical details

These files are produced from the NUTS SHP files provided on Eurostat website, <a href="http://ec.europa.eu/eurostat/web/gisco/geodata/reference-data/administrative-units-statistical-units/nuts" target="_blank">here</a>. The input SHP files are in the <a href="/shp" target="_blank">shp folder</a>. They are transformed using <a href="http://www.gdal.org/" target="_blank">GDAL</a> and, of course, <a href="https://github.com/mbostock/topojson/wiki" target="_blank">TopoJSON</a> libraries. The processes are automated in Bash files, which are also shared in this repository.

## Support and contribution

Feel free to [ask support](https://github.com/jgaffuri/Nuts2json/issues/new), fork the project or simply star it (it's always a pleasure).

## Copyright

The <a href="http://ec.europa.eu/eurostat/web/nuts/overview" target="_blank">Eurostat NUTS dataset</a> is copyrighted. See the <a href="http://ec.europa.eu/eurostat/web/gisco/geodata/reference-data/administrative-units-statistical-units/nuts" target="_blank">Eurostat-GISCO</a> website for more information.
