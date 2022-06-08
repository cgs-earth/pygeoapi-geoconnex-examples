## Demonstrating how to use pygeoapi to publish landing content for the geoconnex system

This repository includes a demonstration deployment and explanations for how to use the [internetofwater/pygeoapi](https://github.com/internetofwater/pygeoapi) fork of [pygeoapi](https://pygeoapi.io) to publish [landing content for individual features](https://docs.ogc.org/per/20-067.html#landingContent) within geospatial datasets suitable for harvesting by the [geoconnex.us](https://docs.geoconnex.us/principles/genprin.html) system.

## Install
Installation is quite simple
```
docker run -d -p 5000:80 --restart always internetofwater/pygeoapi-geoconnex:latest
docker run -d --name watchtower -v /var/run/docker.sock:/var/run/docker.sock --restart always containrrr/watchtower -i 30 --cleanup
```
