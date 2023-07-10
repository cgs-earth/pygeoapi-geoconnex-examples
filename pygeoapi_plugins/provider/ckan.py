# =================================================================
#
# Author: Benjamin Webb <bwebb@lincolninst.edu>
#
# Copyright (c) 2023 Center for Geospatial Solutions
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

import json
from json.decoder import JSONDecodeError
from requests import Session
import logging

from pygeoapi.provider.base import (BaseProvider, ProviderQueryError,
                                    ProviderConnectionError)

LOGGER = logging.getLogger(__name__)


class CKANProvider(BaseProvider):
    """CKAN API Provider"""

    def __init__(self, provider_def):
        """
        CKAN Class constructor

        :param provider_def: provider definitions from yml pygeoapi-config.
                             data, id_field, name set in parent class

        :returns: pygeoapi_plugins.provider.ckan.CKANProvider
        """
        LOGGER.debug('Logger CKAN init')

        super().__init__(provider_def)
        self.resource_id = provider_def['resource_id']

        self.http = Session()
        self.get_fields()

    def get_fields(self):
        """
        Get fields of CKAN Provider

        :returns: dict of fields
        """

        if not self.fields:
            params = {}

            if self.properties:
                self.properties = \
                    set(self.properties) \
                    | set([self.id_field, self.x_field, self.y_field])
                params['fields'] = ','.join(self.properties)

            r = self._get_response(self.data)
            self.fields = {
                field.pop('id'): field for field in r['fields']
            }

        return self.fields

    def query(self, offset=0, limit=10, resulttype='results',
              bbox=[], datetime_=None, properties=[], sortby=[],
              select_properties=[], skip_geometry=False, q=None, **kwargs):
        """
        CKAN query

        :param offset: starting record to return (default 0)
        :param limit: number of records to return (default 10)
        :param resulttype: return results or hit limit (default results)
        :param bbox: bounding box [minx,miny,maxx,maxy]
        :param datetime_: temporal (datestamp or extent)
        :param properties: list of tuples (name, value)
        :param sortby: list of dicts (property, order)
        :param select_properties: list of property names
        :param skip_geometry: bool of whether to skip geometry (default False)
        :param q: full-text search term(s)

        :returns: dict of GeoJSON FeatureCollection
        """

        return self._load(offset, limit, resulttype, bbox=bbox,
                          datetime_=datetime_, properties=properties,
                          sortby=sortby, select_properties=select_properties,
                          skip_geometry=skip_geometry, q=q)

    def get(self, identifier, **kwargs):
        """
        Query CKAN by id

        :param identifier: feature id

        :returns: dict of single GeoJSON feature
        """

        fc = self._load(identifier=identifier)
        return fc.get('features').pop()

    def _load(self, offset=0, limit=10, resulttype='results',
              identifier=None, bbox=[], datetime_=None, properties=[],
              sortby=[], select_properties=[], skip_geometry=False, q=None):
        """
        Private function: Load CKAN data

        :param offset: starting record to return (default 0)
        :param limit: number of records to return (default 10)
        :param resulttype: return results or hit limit (default results)
        :param identifier: feature id (get collections item)
        :param bbox: bounding box [minx,miny,maxx,maxy]
        :param datetime_: temporal (datestamp or extent)
        :param properties: list of tuples (name, value)
        :param sortby: list of dicts (property, order)
        :param select_properties: list of property names
        :param skip_geometry: bool of whether to skip geometry (default False)
        :param q: full-text search term(s)

        :returns: dict of GeoJSON FeatureCollection
        """

        # Default feature collection and request parameters
        fc = {
            'type': 'FeatureCollection',
            'features': []
        }

        params = {
            'offset': offset,
            'limit': limit
        }

        if self.properties or select_properties:
            required = [self.id_field, self.x_field, self.y_field]
            select_properties.extend(required)

            params['fields'] = ','.join(
                set(self.properties) | set(select_properties))

        if identifier:
            # Add feature id to request params
            properties = [(self.id_field, identifier), ]
            params['filters'] = self._make_where(properties)

        else:
            # Add queryables to request params
            if properties:
                params['filters'] = self._make_where(properties)

            if resulttype == 'hits':
                params['include_total'] = 'true'

            if sortby:
                params['sort'] = self._make_orderby(sortby)

            if q:
                params['q'] = q

        # Form URL for GET request
        LOGGER.debug('Sending query')
        response = self._get_response(self.data, params)

        if response.get('total'):
            fc['numberMatched'] = response['total']

        if resulttype == 'hits':
            # Return hits
            LOGGER.debug('Returning hits')
            return fc

        # Return feature collection
        v = [self._make_feature(f, skip_geometry)
             for f in response['records']]

        step = len(v)

        # Query if values are less than expected
        while len(v) < limit:
            LOGGER.debug('Fetching next set of values')
            params['offset'] += step
            response = self._get_response(self.data, params)

            if len(response['records']) == 0:
                break
            else:
                _ = [self._make_feature(f, skip_geometry)
                     for f in response['records']]
                v.extend(_)

        fc['features'] = v
        fc['numberReturned'] = len(v)

        return fc

    def _get_response(self, url, params={}):
        """
        Private function: Get CKAN response

        :param url: request url
        :param params: query parameters

        :returns: STA response
        """
        params.update({'resource_id': self.resource_id})

        r = self.http.get(url, params=params)

        if not r.ok:
            LOGGER.error('Bad http response code')
            raise ProviderConnectionError('Bad http response code')

        print(r.url)
        try:
            response = r.json()
        except JSONDecodeError as err:
            LOGGER.error('JSON decode error')
            raise ProviderQueryError(err)

        if not response['success']:
            LOGGER.error('Bad CKAN response')
            raise ProviderConnectionError('Bad CKAN response')

        return response['result']

    def _make_feature(self, feature, skip_geometry):
        """
        Private function: Make feature from CKAN response

        :param feature: CKAN feature
        :param skip_geometry: bool of whether to skip geometry

        :returns: STA response
        """
        f = {
            'type': 'Feature',
            'id': feature.pop(self.id_field),
            'geometry': None
        }

        if not skip_geometry:
            f['geometry'] = {
                'type': 'Point',
                'coordinates': [
                    float(feature.pop(self.x_field)),
                    float(feature.pop(self.y_field))
                ]
            }

        f['properties'] = feature

        return f

    @staticmethod
    def _make_orderby(sortby):
        """
        Private function: Make CKAN filter from query properties

        :param sortby: `list` of dicts (property, order)

        :returns: CKAN query `order` clause
        """
        __ = {'+': 'asc', '-': 'desc'}
        ret = [f"{_['property']} {__[_['order']]}" for _ in sortby]

        return ','.join(ret)

    def _make_where(self, properties, bbox=[]):
        """
        Private function: Make CKAN filter from query properties

        :param properties: `list` of tuples (name, value)
        :param bbox: bounding box [minx,miny,maxx,maxy]

        :returns: CKAN query `where` clause
        """

        p = {}

        if properties:
            p.update(
                {k: v for (k, v) in properties}
            )

        return json.dumps(p)

    def __repr__(self):
        return f'<CKANProvider> {self.data}'
