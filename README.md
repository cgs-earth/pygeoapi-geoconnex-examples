## Demonstrating how to use pygeoapi to publish landing content for the geoconnex system

This repository includes a demonstration deployment and explanations for how to use the [internetofwater/pygeoapi](https://github.com/internetofwater/pygeoapi) fork of [pygeoapi](https://pygeoapi.io) to publish [landing content for individual features](https://docs.ogc.org/per/20-067.html#landingContent) within geospatial datasets suitable for harvesting by the [geoconnex.us](https://docs.geoconnex.us/principles/genprin.html) system.

pygeoapi is a general open-source geospatial web server that implements several OGC-API standards. We leverage the [OGC-API Features](https://ogcapi.ogc.org/features/) standard, which gives every individual feature within a geospatial vector dataset a unique URL with an associated HTML landing page and GeoJSON response. We also leverage some add-ons that enable the injection of templated JSON-LD into the script headers of the HTML pages. Both the HTML pages and JSON-LD responses are generated using jinja templates. This demonstration deployment shows how to use pygeoapi to generate landing pages for the following data sources:

1. A (local or periodically downloaded) csv file with latitude and longitude
2. A (local or periodically downloaded) geojson file 
3. A (local or periodically downloaded) geopackage file 
4. An ESRI FeatureServer or MapServer endpoint
5. A CKAN Data API endpoint

Deploying involves creating a pygeoapi configuration yml file, with blocks for each feature collection, as well as a JSON-LD feature template.

### Example data

For our example data, we are using the California Department of Water Resources (DWR) Groundwater Sustainability Plan (GSP) Monitoring [dataset](https://data.ca.gov/dataset/gsp-monitoring-data), and in particular, its "Existing Sites" feature collection.

### Deploy for local development

docker-compose, explain volume mapping for jsonld templates
