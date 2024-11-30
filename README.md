# Using pygeoapi to publish data to Geoconnex 

This repository is a demonstration and explanation for how to use [pygeoapi](https://pygeoapi.io) to publish [landing content for individual features](https://docs.ogc.org/per/20-067.html#landingContent) within geospatial datasets suitable for harvesting by the [geoconnex.us](https://docs.geoconnex.us/principles/genprin.html) system. Geoconnex relies on [JSON-LD](https://json-ld.org/) to output standardized data structures across disparate data sources and providers.

## Getting started with pygeoapi and docker

pygeoapi is a general open-source geospatial web server that implements several OGC-API standards. We leverage the [OGC-API Features](https://ogcapi.ogc.org/features/) standard, which gives each individual feature within a geospatial vector dataset a unique URL with an associated HTML landing page, a GeoJSON response, and a JSON-LD response. In addition to the [feature providers](https://docs.pygeoapi.io/en/latest/data-publishing/ogcapi-features.html) in pygeoapi core, the [internetofwater/pygeoapi](https://github.com/internetofwater/pygeoapi) fork includes feature providers for the ESRI FeatureServer, the CKAN Data API, and the SODA API. It also includes modifications that enable the injection of custom templated JSON-LD into the script headers of the HTML pages. Both the HTML pages and JSON-LD responses are generated using jinja templates.

This demonstration uses [Docker](https://www.docker.com/) to deploy pygeoapi with landing pages generated for data from the following sources:

1. **CSV Provider:** A (local or periodically downloaded) csv file with latitude and longitude
2. **GeoJSON Provider:** A (local or periodically downloaded) geojson file 
3. **SQLiteGPKG Provider:** A (local or periodically downloaded) geopackage file 
4. **ESRI Provider:** An ESRI FeatureServer or MapServer endpoint
5. **CKAN Provider:** A CKAN Data API endpoint

### Example data

For our example data, we are using the California Department of Water Resources (DWR) Groundwater Sustainability Plan (GSP) Monitoring [dataset](https://data.ca.gov/dataset/gsp-monitoring-data), and in particular, its "Existing Sites" feature collection.

- CSV file: https://github.com/cgs-earth/pygeoapi-geoconnex-examples/blob/main/data/data.csv
- GeoJSON file: https://github.com/cgs-earth/pygeoapi-geoconnex-examples/blob/main/data/data.geojson
- Geopackage file: https://github.com/cgs-earth/pygeoapi-geoconnex-examples/blob/main/data/data.gpkg
- ESRI feature service: https://services.arcgis.com/aa38u6OgfNoCkTJ6/ArcGIS/rest/services/GSP_Monitoring_Data/FeatureServer/0
- CKAN API endpoint: https://data.ca.gov/api/3/action/datastore_search?resource_id=72612518-e45b-4900-9cab-72b8de09c57d

### Deploying locally

pygeoapi can be deployed from the Dockerfile, building an image with data included as a layer, or with docker compose and volume binding. The only pre-requisite to deploy pygeoapi is a valid pygeoapi configuration file, with blocks for each feature collection. The only pre-requsite to publish data to geoconnex is a valid JSON-LD object and a PID redirect in geoconnex namespace.

As such, the only requirements to publish data to crawlable by geoconnex is a valid pygeoapi configuration file with a correct JSON-LD feature template. This repository has been setup to satisfy both of these prerequisites out of the box. 

The easiest way to deploy this demonstration is with docker-compose. The [docker-compose file](https://github.com/cgs-earth/pygeoapi-geoconnex-examples/blob/main/docker-compose.yml) binds the data directory of local files, the [pygeoapi configuration file](https://github.com/cgs-earth/pygeoapi-geoconnex-examples/blob/main/pygeoapi.config.yml), and the preconfigured [JSON-LD template](https://github.com/cgs-earth/pygeoapi-geoconnex-examples/blob/main/jsonld/hydrologic-location.jsonld) into the pygeoapi docker image.

### Quickstart

1. Clone this repository on your machine.
```
git clone https://github.com/cgs-earth/pygeoapi-geoconnex-examples.git
cd pygeoapi-geoconnex-examples
```
2. Deploy the demonstration (make sure port 5000 is available)
```
docker compose up
```
3. Explore the OGC-API feature collections at `http://localhost:5000/collections`

### Extending the demonstration

From here, using pygeoapi to create HTML landing pages for your data should feel within reach. 

The process is similar to the steps described in the quickstart, except with an additional requirement to setup your own configurations. After you decide the format for your data source, create a pygeoapi configuration file with metadata specific to your organization and a resource provider configured for your data. Then create a JSON-LD jinja template that outputs your data in a structured and standarized way. Once you have your data, your configuration file, and JSON-LD templates, deployment is not that dissimilar from the steps described in the quickstart. 

### Persistent Identifiers,

As you explore the feature collections, notice the individual feature HTML resources (e.g. http://localhost:5000/collections/demo-ckan/items/31) and their json-ld versions (e.g. http://localhost:5000/collections/demo-ckan/items/31?f=jsonld).

```
{
    "@context": [
        {
            "schema": "https://schema.org/",
            "skos": "http://www.w3.org/2004/02/skos/core#",
            "hyf": "https://www.opengis.net/def/schema/hy_features/hyf/",
            "name": "schema:name",
            "gsp": "http://www.opengis.net/ont/geosparql#",
            "sameAs": "schema:sameAs",
            "related": "skos:related",
            "description": "schema:description",
            "image": {
                "@id": "schema:image",
                "@type": "@id"
            }
        }
    ],
    "@id": "http://localhost:5000/collections/demo-ckan/items/31",
    "@type": [
        "https://www.opengis.net/def/schema/hy_features/hyf/HY_HydrometricFeature",
        "https://www.opengis.net/def/schema/hy_features/hyf/HY_HydroLocation"
    ],
    "name": "DWR at Gravelly Ford Canal",
    "description": "Surveying/Benchmark Sites at DWR at Gravelly Ford Canal",
    "schema:provider": "SJRRP",
    "hyf:HY_HydroLocationType": "hydrometricStation",
    "sosa:isFeatureOfInterestOf": {
        "schema:url": "http://www.restoresjr.net/science/subsidence-monitoring/",
        "@type": "sosa:ObservationCollection",
        "schema:format": [
            "application/json"
        ]
    },
    "schema:geoWithin": "https://geoconnex.us/ref/states/06",
    "geo": {
        "@type": "schema:GeoCoordinates",
        "schema:longitude": -120.169,
        "schema:latitude": 36.8078
    },
    "gsp:hasGeometry": {
        "@type": "http://www.opengis.net/ont/sf#Point",
        "gsp:asWKT": {
            "@type": "http://www.opengis.net/ont/geosparql#wktLiteral",
            "@value": "POINT (-120.169 36.8078)"
        }
    }
}
```

Notice how `"@id"` is the URL for the API call. This can be configured to be an external URI instead, such as those [minted with geoconnex.us](https://docs.geoconnex.us/contributing/pids.html). You can then add these identifiers as a field in your data, whether in a local file or at an ESRI or CKAN api endpoint, and then specify this field as the `uri_field:` in the pygeoapi configuration yml file in the `providers:` block, like so:

```
    demo-ckan:
        type: collection
        title: geoconnex landing page demo (CKAN web service)
        description: Demonstration Geoconnex Landing Pages (from CKAN REST service source)
        keywords:
            - Existing Sites
        template: jsonld/hydrologic-location.jsonld
        links:
            - type: application/html
              rel: canonical
              title: data source
              href: https://data.ca.gov/dataset/gsp-monitoring-data/resource/72612518-e45b-4900-9cab-72b8de09c57d
              hreflang: en-US
        extents:
            spatial:
                bbox: [-170,15,-51,72]
                crs: http://www.opengis.net/def/crs/OGC/1.3/CRS84
            temporal:
                begin: null
                end: null
        providers:
            - type: feature
              name: CKAN
              data: https://data.ca.gov/api/3/action/datastore_search
              resource_id: 72612518-e45b-4900-9cab-72b8de09c57d
              id_field: EXISTING_INFO_ID
              uri_field: EXAMPLE_URI_FIELD_RENAME_AS_NECESSARY
              x_field: LONGITUDE
              y_field: LATITUDE
```
