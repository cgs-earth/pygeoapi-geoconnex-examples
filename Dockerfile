FROM internetofwater/pygeoapi:latest
# test2
#add requirements and mods
COPY ./pygeoapi.config.yml /pygeoapi/local.config.yml
COPY ./jsonld /pygeoapi/pygeoapi/templates/jsonld
COPY ./data /data
