# Nuts2json

[Nuts2json](https://github.com/eurostat/Nuts2json) provides various reusable versions of [Eurostat NUTS dataset](http://ec.europa.eu/eurostat/web/nuts/overview) as web formats such as [GeoJSON](http://geojson.org/) and [TopoJSON](https://github.com/mbostock/topojson/wiki). It is provided to support the development of statistical web maps of [Eurostat data](http://ec.europa.eu/eurostat/) based on NUTS regions. In a way, it provides a blank map of geometries ready for use with your own data and colors.

Examples: For an example of such blank map, see [this map](http://eurostat.github.io/Nuts2json/overview.html?proj=laea&lvl=3&s=1000&y=2013). For an example of statistical map, see [this map](http://eurostat.github.io/EurostatVisu/population_map.html) showing population in Europe.

[![Example](img/ex_population.png)](http://eurostat.github.io/EurostatVisu/population_map.html)

## Supported formats

The files can be retrieved on-the-fly from the base URL `https://raw.githubusercontent.com/eurostat/Nuts2json/gh-pages/` according to the file pattern:

`/<YEAR>/<PROJECTION>/<SIZE>/<NUTS_LEVEL>.<FORMAT>`

For example, [`https://raw.githubusercontent.com/eurostat/Nuts2json/gh-pages/2013/wm/600px/2.topojson`](https://raw.githubusercontent.com/eurostat/Nuts2json/gh-pages/2013/wm/600px/2.topojson)</a> returns a TopoJSON file of 2013 NUTS regions level 2 in web mercator projection, for a map size 600*600px.

The parameters are:

| Parameter | Description | Possible values |
| ------------- | ------------- |-------------|
| `YEAR` | The NUTS version year. | `2013` |
| `PROJECTION` | The map projection. Currently, European projection LAEA ([EPSG 3035](http://spatialreference.org/ref/epsg/etrs89-etrs-laea/)) and Web Mercator ([EPSG 3857](http://spatialreference.org/ref/sr-org/7483/)) are provided. ETRS89 ([EPSG 4258](http://spatialreference.org/ref/epsg/4258/)) should be provided soon. | `laea`, `wm` |
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

A map showing the TopoJSON geometries with [d3js](https://d3js.org/):

(See it online [here](https://eurostat.github.io/Nuts2json/usage.html)).

```html
<!DOCTYPE html>
<svg width="800px" height="800px"></svg>

<script src="https://d3js.org/d3.v4.min.js"></script>
<script src="https://d3js.org/topojson.v1.min.js"></script>

<style>
	.rg { fill: #fdbf6f; }
	.rg:hover { fill: #ff7f00; }
	.bn { fill: none; stroke-linecap:round; stroke-linejoin:round }
	.bn_0 { stroke: #333; stroke-width: 1.3px; }
	.bn_1 { stroke: #333; stroke-width: 1px; }
	.bn_2 { stroke: #333; stroke-width: 1px; }
	.bn_3 { stroke: #333; stroke-width: 0.7px; }
	.bn_oth { stroke: #aaa; stroke-width: 1px; }
	.cntrg { fill: lightgray; }
	.cntrg:hover { fill: darkgray; }
	.cntbn { fill: none; stroke: #aaa; stroke-width: 1px; stroke-linecap:round; stroke-linejoin:round }
</style>

<script>

	var svg = d3.select("svg");
	var path = d3.geoPath();

	d3.json("https://raw.githubusercontent.com/eurostat/Nuts2json/gh-pages/2013/laea/800px/3.topojson", function(error, nuts) {
		if (error) throw error;

		//country regions
		svg.append("g").selectAll("path").data(topojson.feature(nuts, nuts.objects.cntrg).features).enter()
				.append("path").attr("d", path)
				.attr("class", "cntrg")

		//country boundaries
		svg.append("g").selectAll("path").data(topojson.feature(nuts, nuts.objects.cntbn).features).enter()
				.append("path").attr("d", path)
				.attr("class", "cntbn");

		//nuts regions
		svg.append("g").selectAll("path").data(topojson.feature(nuts, nuts.objects.nutsrg).features).enter()
				.append("path").attr("d", path)
				.attr("class", "rg")

		//nuts boundaries
		var bn = topojson.feature(nuts, nuts.objects.nutsbn).features;
		bn.sort(function(bn1,bn2){ return bn2.properties.lvl - bn1.properties.lvl; });
		svg.append("g").selectAll("path").data(bn).enter()
				.append("path").attr("d", path)
				.attr("class", function(bn){
					bn = bn.properties;
					var cl = ["bn","bn_"+bn.lvl];
					if(bn.oth==="T") cl.push("bn_oth");
					return cl.join(" ");
				});
	});

</script>
```

For a map showing a choropleth map based on [Eurostat statistical data API](http://ec.europa.eu/eurostat/web/json-and-unicode-web-services/getting-started/rest-request), see [this map](http://eurostat.github.io/EurostatVisu/population_map.html) on [EurostatVisu repo](https://github.com/eurostat/EurostatVisu/blob/gh-pages/population_map.html).

## Technical details

These files are produced from the NUTS SHP files provided on [Eurostat-GISCO website](http://ec.europa.eu/eurostat/web/gisco/geodata/reference-data/administrative-units-statistical-units/nuts). The input SHP files are in the [shp folder](/shp). These input files are transformed using [GDAL](http://www.gdal.org/) and [TopoJSON](https://github.com/mbostock/topojson/wiki). The processes are automated in bash files, which are also shared in this repository.

## Support and contribution

Feel free to [ask support](https://github.com/eurostat/Nuts2json/issues/new), fork the project or simply star it (it's always a pleasure).

## Copyright

The [Eurostat NUTS dataset](http://ec.europa.eu/eurostat/web/nuts/overview) is copyrighted. See the [Eurostat-GISCO website](http://ec.europa.eu/eurostat/web/gisco/geodata/reference-data/administrative-units-statistical-units/nuts) for more information.
