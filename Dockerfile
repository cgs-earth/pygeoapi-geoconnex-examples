FROM geopython/pygeoapi:latest

ADD . /pygeoapi_plugins

RUN pip3 install -e /pygeoapi_plugins

ENTRYPOINT [ "/entrypoint.sh" ]
