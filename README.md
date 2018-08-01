# Nuts2json

<a href="https://github.com/eurostat/Nuts2json">Nuts2json</a> provides various reusable versions of <a href="http://ec.europa.eu/eurostat/web/nuts/overview" target="_blank">Eurostat NUTS dataset</a> as web formats such as <a href="http://geojson.org/" target="_blank">GeoJSON</a> and <a href="https://github.com/mbostock/topojson/wiki" target="_blank">TopoJSON</a>. It is provided to support the development of statistical web maps of <a href="http://ec.europa.eu/eurostat/web/json-and-unicode-web-services/getting-started/rest-request" target="_blank">Eurostat data</a> based on NUTS regions. In a way, it provides a blank map of geometries ready for use with your own data and colors.

Examples: For an example of such blank map, see <a href="http://eurostat.github.io/Nuts2json/overview.html?proj=laea&lvl=3&s=1000&y=2013" target="_blank">this map</a>. The URL parameters can be changed. For an example of thematic map, see <a href="http://eurostat.github.io/EurostatVisu/population_map.html">this map</a> showing population in Europe.

[![Example](img/ex_population.png)](http://eurostat.github.io/EurostatVisu/population_map.html)

## Supported formats

The files can be retrieved on-the-fly from the base URL `https://raw.githubusercontent.com/eurostat/Nuts2json/gh-pages/` according to the file pattern:

`/<YEAR>/<PROJECTION>/<SIZE>/<NUTS_LEVEL>.<FORMAT>`

For example, <a href="https://raw.githubusercontent.com/eurostat/Nuts2json/gh-pages/2013/wm/600px/2.topojson" target="_blank">`https://raw.githubusercontent.com/eurostat/Nuts2json/gh-pages/2013/wm/600px/2.topojson`</a> returns a TopoJSON file of 2013 NUTS regions level 2 in web mercator projection, for a map size 600*600px.

The parameters are:

| Parameter | Description | Possible values |
| ------------- | ------------- |-------------|
| `YEAR` | The NUTS version year. | `2013` |
| `PROJECTION` | The map projection. Currently, European projection LAEA (<a href="http://spatialreference.org/ref/epsg/etrs89-etrs-laea/" target="_blank">EPSG 3035</a>) and Web Mercator (<a href="http://spatialreference.org/ref/sr-org/7483/" target="_blank">EPSG 3857</a>) are provided. ETRS89 (<a href="http://spatialreference.org/ref/epsg/4258/" target="_blank">EPSG 4258</a>) should be provided soon. | `laea`, `wm` |
| `SIZE` | The map size, in pixel. Currently, all maps are squared. | `400`, `600`, `800`, `1000`, `1200` |
| `NUTS_LEVEL` | The NUTS level to be shown on the map, from national level (NUTS_LEVEL=0) to provincial level (NUTS_LEVEL=3). | `0`, `1`, `2`, `3` |
| `FORMAT` | The file format. Currently, only <a href="https://github.com/mbostock/topojson/wiki" target="_blank">TopoJSON</a> is provided. <a href="http://geojson.org/" target="_blank">GeoJSON</a> format is to come. | `topojson` |

For additional projections, formats, sizes, etc., feel free to [ask](https://github.com/eurostat/Nuts2json/issues/new) !

### TopoJSON features

Four feature types are provided:

NUTS regions (feature type `nutsrg`) with the following properties:
  - `id`: The NUTS identifier to be used to join Eurostat statistical figures and then assign colors to the regions.
  - `na`: The geographical name of the region.

NUTS boundaries (feature type `nutsbn`) with the following properties:
  - `lvl`: The NUTS level of the boundary, from 0 (national level) to 3 (provincial level).
  - `eu`: T if the boundary separate two EU member states, F otherwise.
  - `efta`: T if the boundary touches at least one EFTA country, F otherwise.
  - `cc`: T if the boundary touches at least one Candidate Country, F otherwise.
  - `oth`: T if the boundary touches a country wich is not EU, EFTA,CC. F otherwise.
NB: Coastal boundaries are not included.

Non-european countries (feature type `cntrg`) with the following properties:
  - `cid`: The country identifier (2 letters code).
  - `cna`: The country name.

Non-european boundaries (feature type `cntbn`). Coastal boundaries are not included.

### GeoJSON features

[TODO]

## Usage example

See <a href="http://eurostat.github.io/EurostatVisu/population_map.html">this map</a> on <a href="https://github.com/eurostat/EurostatVisu/blob/gh-pages/README.md">EurostatVisu</a> project.

[TODO: describe simple examples, based on d3.]

## Technical details

These files are produced from the NUTS SHP files provided on <a href="http://ec.europa.eu/eurostat/web/gisco/geodata/reference-data/administrative-units-statistical-units/nuts" target="_blank">Eurostat-GISCO website</a>. The input SHP files are in the <a href="/shp" target="_blank">shp folder</a>. They are transformed using <a href="http://www.gdal.org/" target="_blank">GDAL</a> and <a href="https://github.com/mbostock/topojson/wiki" target="_blank">TopoJSON</a>. The processes are automated in bash files, which are also shared in this repository.

## Support and contribution

Feel free to [ask support](https://github.com/eurostat/Nuts2json/issues/new), fork the project or simply star it (it's always a pleasure).

## Copyright

The <a href="http://ec.europa.eu/eurostat/web/nuts/overview" target="_blank">Eurostat NUTS dataset</a> is copyrighted. See the <a href="http://ec.europa.eu/eurostat/web/gisco/geodata/reference-data/administrative-units-statistical-units/nuts" target="_blank">Eurostat-GISCO</a> website for more information.

