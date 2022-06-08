# Using pygeoapi to publish data to Geoconnex 

This repository is a demonstration and explanation for how to use [pygeoapi](https://pygeoapi.io) to publish [landing content for individual features](https://docs.ogc.org/per/20-067.html#landingContent) within geospatial datasets suitable for harvesting by the [geoconnex.us](https://docs.geoconnex.us/principles/genprin.html) system.

## Getting started with pygeoapi & docker

pygeoapi is a general open-source geospatial web server that implements several OGC-API standards. We leverage the [OGC-API Features](https://ogcapi.ogc.org/features/) standard, which gives each individual feature within a geospatial vector dataset a unique URL with an associated HTML landing page, GeoJSON response, and JSON-LD response. In addition to the [providers](https://docs.pygeoapi.io/en/latest/data-publishing/ogcapi-features.html) offered by pygeoapi core, [internetofwater/pygeoapi](https://github.com/internetofwater/pygeoapi) fork includes OGC-API Feature providers for ESRI FeatureServer, CKAN Data API, and SODA API. Additionlly, the fork includes add-ons that enable the injection of custom templated JSON-LD into the script headers of the HTML pages. Both the HTML pages and JSON-LD responses are generated using jinja templates.

This demonstration uses [Docker](https://www.docker.com/) to deploy pygeoapi with landing pages generated for data from the following sources:

1. **CSV Provider:** A (local or periodically downloaded) csv file with latitude and longitude
2. **GeoJSON Provider:** A (local or periodically downloaded) geojson file 
3. **SQLiteGPKG Provider:** A (local or periodically downloaded) geopackage file 
4. **ESRI Provider:** An ESRI FeatureServer or MapServer endpoint
5. **CKAN Provider:** A CKAN Data API endpoint

pygeoapi can be deployed from the Dockerfile, producing an image with data included as a layer, or with docker compose and volume binding. The only pre-requsite to publish data to geoconnex is a valid JSON-LD object. The only pre-requisite to deploy pygeoapi is a valid pygeoapi configurtion file, with blocks for each feature collection. 

As such, the only requirements to publish data to crawlable by geoconnex is a valid pygeoapi configuration file with a correct JSON-LD feature template. This repository has been setup to satisfy both requirements out of the box. 

### Example data

For our example data, we are using the California Department of Water Resources (DWR) Groundwater Sustainability Plan (GSP) Monitoring [dataset](https://data.ca.gov/dataset/gsp-monitoring-data), and in particular, its "Existing Sites" feature collection.

- link to CSV download (stored in data directory of this repo)
- link to geojson file (stored in data directory of this repo)
- link to geopackage version (stored in data directory of this repo)
- ESRI feature service: https://services.arcgis.com/aa38u6OgfNoCkTJ6/ArcGIS/rest/services/GSP_Monitoring_Data/FeatureServer/0
- CKAN endpoint: https://data.ca.gov/api/3/action/datastore_search?resource_id=72612518-e45b-4900-9cab-72b8de09c57d

### Deploy for local development

docker-compose, explain volume mapping for jsonld templates
