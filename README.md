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

pygeoapi can be deployed from the Dockerfile, building an image with data included as a layer, or with docker compose and volume binding. The only pre-requisite to deploy pygeoapi is a valid pygeoapi configurtion file, with blocks for each feature collection. The only pre-requsite to publish data to geoconnex is a valid JSON-LD object and a PID redirect in geoconnex namespace.

As such, the only requirements to publish data to crawlable by geoconnex is a valid pygeoapi configuration file with a correct JSON-LD feature template. This repository has been setup to satisfy both of these prerequisites out of the box. 

The easiest way to deploy this demonstration is with docker-compose. The [docker-compose file](https://github.com/cgs-earth/pygeoapi-geoconnex-examples/blob/main/docker-compose.yml) binds the data directory of local files, the pygeoapi configuration file, and the preconfigured JSON-LD templates into the pygeoapi docker image.

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
