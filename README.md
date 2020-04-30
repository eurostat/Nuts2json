# Nuts2json

[Nuts2json](https://github.com/eurostat/Nuts2json) provides various reusable versions of [Eurostat NUTS dataset](http://ec.europa.eu/eurostat/web/nuts/overview) as web formats such as [TopoJSON](https://github.com/mbostock/topojson/wiki) and [GeoJSON](http://geojson.org/). It is provided to support the development of statistical web maps of [Eurostat data](http://ec.europa.eu/eurostat/) based on NUTS regions. In a way, it provides a blank map of geometries ready for use with your own data and colors.

For a faster creation of maps based on Nuts2json, check out [**eurostat-map.js**](https://github.com/eurostat/eurostat.js/blob/master/doc/README-map.md).

See [some examples below](https://github.com/eurostat/Nuts2json#some-examples).

[![Example](doc/img/sc_simple.png)](https://bl.ocks.org/jgaffuri/raw/e7e0a76a6e0f851b253d3b1c8fb17ffb?proj=3035&lvl=3&w=1000&s=20M&time=2016)
[![Example](doc/img/sc_advanced.png)](https://bl.ocks.org/jgaffuri/raw/71d130bf5963c5ffe0a436399f401af3?proj=3035&lvl=3&w=1000&s=20M&time=2016)

## API

Base URL: `https://raw.githubusercontent.com/eurostat/Nuts2json/master/`

URL patterns:

- For TopoJSON format: `/<YEAR>/<PROJECTION>/<SCALE>/<NUTS_LEVEL>.json`
- For GeoJSON format: `/<YEAR>/<PROJECTION>/<SCALE>/<TYPE>[_<NUTS_LEVEL>].json`

For example, [`https://raw.githubusercontent.com/eurostat/Nuts2json/master/2016/3035/20M/2.json`](https://raw.githubusercontent.com/eurostat/Nuts2json/master/2016/3035/20M/2.json) returns a TopoJSON file of 2016 NUTS regions level 2 in European LAEA projection ([EPSG 3035](http://spatialreference.org/ref/epsg/etrs89-etrs-laea/)) at 1:20M scale.

The parameters are:

| Parameter | Supported values | Description |
| ------------- | ------------- |-------------|
| `YEAR` | `2016` `2013` `2010` | The NUTS version. |
| `PROJECTION` | `3035` `3857` `4258` `4326` | The coordinate reference system EPSG code. Two projections are provided: European LAEA projection ([EPSG 3035](http://spatialreference.org/ref/epsg/etrs89-etrs-laea/)) and web mercator ([EPSG 3857](http://spatialreference.org/ref/sr-org/7483/)). For statistical maps, it is strongly adviced to use an equal-area projection such as `3035`. Geographic coordinates ETRS89 ([EPSG 4258](http://spatialreference.org/ref/epsg/4258/)) and WGS84 ([EPSG 4326](http://spatialreference.org/ref/epsg/4326/)) are also provided. |
| `SCALE` | `60M` `20M` `10M` | The intended map scale factor. The larger the value, the stronger the simplification. For example, for a map width of 1000 pixels the scale 1:20M is the most suitable. |
| `NUTS_LEVEL` | `0` `1` `2` `3` | The NUTS level to be displayed on the map, from national (NUTS_LEVEL=`0`) to local level (NUTS_LEVEL=`3`). |
| `TYPE` | `nutsrg` `nutsbn` `cntrg` `cntbn` `gra` | For GeoJSON format, the feature type has to be specified. The available feature types are described below. For NUTS feature types (`nutsrg` and `nutsbn`), the `NUTS_LEVEL` to be displayed on the map has to be specified.  |

For additional projections, formats, scales, etc., feel free to [ask](https://github.com/eurostat/Nuts2json/issues/new) !

### Feature types

Five feature types are provided:

- NUTS regions (feature type `nutsrg`) with the following properties:
  - `id`: The NUTS identifier to be used to join Eurostat statistical figures and then assign colors to the regions.
  - `na`: The geographical name of the region.

- NUTS boundaries (feature type `nutsbn`) with the following properties:
  - `lvl`: The NUTS level of the boundary, from 0 (national level) to 3 (provincial level).
  - `eu`: T if the boundary separate two EU member states, F otherwise.
  - `efta`: T if the boundary touches at least one EFTA country, F otherwise.
  - `cc`: T if the boundary touches at least one Candidate Country, F otherwise.
  - `oth`: T if the boundary touches a country wich is not EU, EFTA,CC. F otherwise.
  - `co`: T if the boundary is coastal. F otherwise.

- Non-european countries (feature type `cntrg`) with the following properties:
  - `id`: The country identifier (2 letters code).
  - `na`: The country name.

- Non-european boundaries (feature type `cntbn`) with the following properties:
  - `cc`: T if the boundary touches at least one Candidate Country, F otherwise.
  - `oth`: T if the boundary touches a country wich is not EU, EFTA,CC. F otherwise.
  - `co`: T if the boundary is coastal. F otherwise.

- The map graticule (meridian and parrallel lines) is provided as feature type `gra` with a single `id` property, which is the lat/lon of the parallel/meridian.

### NUTS regions as points

NUTS regions are also provided as point geometries. These points can be used for label placement or simplified maps such as [Dorling cartograms](http://www.dannydorling.org/wp-content/files/dannydorling_publication_id1448.pdf). Since this data does not depend on the `<SCALE>` parameter, it can be retrieved directly under the `/<YEAR>/<PROJECTION>/nutspt_<NUTS_LEVEL>.json` URL pattern, as GeoJSON format.

For example, [`https://raw.githubusercontent.com/eurostat/Nuts2json/master/2013/4326/nutspt_2.json`](https://raw.githubusercontent.com/eurostat/Nuts2json/master/2013/4326/nutspt_2.json) returns a GeoJSON file of 2013 NUTS points level 2 in WGS84 ([EPSG 4326](http://spatialreference.org/ref/epsg/etrs89-etrs-laea/)) geographic coordinates.

The point features are provided with the following properties:
  - `id`: The NUTS identifier.
  - `na`: The geographical name of the region.
  - `ar`: The area of the region, in m².

## Some examples

These examples are based on [d3js](https://d3js.org/) library.

- [Basic example](https://bl.ocks.org/jgaffuri/raw/e7e0a76a6e0f851b253d3b1c8fb17ffb/) (see the [code](https://bl.ocks.org/jgaffuri/e7e0a76a6e0f851b253d3b1c8fb17ffb)).
- [Advanced example](https://bl.ocks.org/jgaffuri/raw/71d130bf5963c5ffe0a436399f401af3/) (see the [code](https://bl.ocks.org/jgaffuri/71d130bf5963c5ffe0a436399f401af3)).
- [Statistical map examples](https://github.com/eurostat/eurostat.js/blob/master/doc/README-map.md#some-examples) based on [eurostat-map.js](https://github.com/eurostat/eurostat.js/blob/master/doc/README-map.md).
- [NUTS regions as points](https://observablehq.com/@jgaffuri/nuts-regions-as-points).
- [NUTS regions Dorling cartogram](https://observablehq.com/@jgaffuri/dorling-cartogram).
- [NUTS population Dorling cartogram](https://observablehq.com/@jgaffuri/dorling-cartogram-population).
- [NUTS population change Dorling cartogram](https://observablehq.com/@jgaffuri/dorling-cartogram-population-change).

## Technical details

These files are produced from the NUTS SHP files provided on [Eurostat-GISCO website](http://ec.europa.eu/eurostat/web/gisco/geodata/reference-data/administrative-units-statistical-units/nuts). The input files are in the [shp folder](/shp).

These input files are transformed using [GDAL](http://www.gdal.org/) and [TopoJSON](https://github.com/mbostock/topojson/wiki). The transformation process is automated in bash files, which are also shared in the [sh folder](/sh). This process has 6 successive steps:
1. *filter_project_clip*: Filter and reproject the input data for each year, each scale and each projection.
2. *extract_shp_by_level*: For each year, scale and projection, decompose the data by NUTS level.
3. *shp_to_geojson*: Convert from SHP to GeoJSON format.
4. *geojson_to_topojson*: Convert from GeoJSON to TopoJSON format.
5. *simplify_topojson*: Simplify the TopoJSON files using [TopoJSON Simplify](https://github.com/topojson/topojson-simplify/) program.
6. *topojson_to_geojson*: Convert from TopoJSON to GeoJSON format.

And finally:

9. *points*: Produces the NUTS regions as points.

## Support and contribution

Feel free to [ask support](https://github.com/eurostat/Nuts2json/issues/new), fork the project or simply star it (it's always a pleasure).

## Copyright

The [Eurostat NUTS dataset](http://ec.europa.eu/eurostat/web/nuts/overview) is copyrighted. There are [specific provisions](https://ec.europa.eu/eurostat/web/gisco/geodata/reference-data/administrative-units-statistical-units) for the usage of this dataset which must be respected. The usage of these data is subject to their acceptance. See the [Eurostat-GISCO website](http://ec.europa.eu/eurostat/web/gisco/geodata/reference-data/administrative-units-statistical-units/nuts) for more information.

## Disclaimer
The designations employed and the presentation of material on these maps do not imply the expression of any opinion whatsoever on the part of the European Union concerning the legal status of any country, territory, city or area or of its authorities, or concerning the delimitation of its frontiers or boundaries. Kosovo*: This designation is without prejudice to positions on status, and is in line with UNSCR 1244/1999 and the ICJ Opinion on the Kosovo declaration of independence. Palestine*: This designation shall not be construed as recognition of a State of Palestine and is without prejudice to the individual positions of the Member States on this issue.
