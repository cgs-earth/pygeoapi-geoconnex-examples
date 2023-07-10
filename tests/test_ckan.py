# =================================================================
#
# Authors: Benjamin Webb <bwebb@lincolninst.edu>
#
# Copyright (c) 2023 Benjamin Webb
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

import pytest

from pygeoapi_plugins.provider.ckan import CKANProvider


@pytest.fixture()
def config():
    # New Mexico Reservoirs
    # source: https://catalog.newmexicowaterdata.org
    return {
        'name': 'pygeoapi_plugins.provider.ckan.CKAN',
        'type': 'feature',
        'data': 'https://catalog.newmexicowaterdata.org/api/3/action/datastore_search',  # noqa
        'resource_id': '08369d21-520b-439e-97e3-5ecb50737887',
        'id_field': '_id',
        'x_field': 'LONDD',
        'y_field': 'LATDD'
    }


def test_query(config):
    p = CKANProvider(config)

    fields = p.get_fields()
    assert len(fields) == 46
    assert fields['DAMNAME']['type'] == 'text'
    assert fields['RES_ID']['type'] == 'numeric'

    results = p.query()
    assert len(results['features']) == 10
    assert results['numberMatched'] == 25
    assert results['numberReturned'] == 10

    assert results['features'][0]['id'] == 1
    assert results['features'][0]['properties']['DAMNAME'] == 'NAVAJO'
    assert results['features'][0]['geometry']['coordinates'][0] == -107.609
    assert results['features'][0]['geometry']['coordinates'][1] == 36.8078

    assert results['features'][2]['id'] == 3
    assert results['features'][2]['properties']['DAMNAME'] == 'LA JARA LAKE'
    assert results['features'][2]['geometry']['coordinates'][0] == -107
    assert results['features'][2]['geometry']['coordinates'][1] == 36.74

    results = p.query(limit=1)
    assert len(results['features']) == 1
    assert results['features'][0]['id'] == 1

    results = p.query(offset=2, limit=1)
    assert len(results['features']) == 1
    assert results['features'][0]['id'] == 3

    results = p.query(limit=25)
    assert len(results['features']) == 25
    assert results['numberMatched'] == 25
    assert results['numberReturned'] == 25

    results = p.query(skip_geometry=True)
    assert results['features'][0]['geometry'] is None


def test_query_by_properties(config):
    p = CKANProvider(config)
    results = p.query(properties=[('SOURCE', 'E')])
    assert results['numberMatched'] == 11
    assert results['numberReturned'] == 10

    results = p.query(properties=[('RIVER', 'RIO CHAMA')])
    assert results['numberMatched'] == 2
    assert results['numberReturned'] == 2

    results = p.query(properties=[('SOURCE', 'E'), ('RIVER', 'RIO CHAMA')])
    assert results['numberMatched'] == 1
    assert results['numberReturned'] == 1


def test_query_sortby(config):
    p = CKANProvider(config)
    results = p.query()
    assert results['features'][0]['properties']['YEAR'] == 1963

    results = p.query(sortby=[{'property': 'YEAR', 'order': '+'}])
    assert results['features'][0]['properties']['YEAR'] == 1893

    results = p.query(sortby=[{'property': 'YEAR', 'order': '-'}])
    assert results['features'][0]['properties']['YEAR'] == 1980


def test_query_q(config):
    p = CKANProvider(config)
    results = p.query(q='RESERVOIR')
    assert results['numberMatched'] == 14
    assert results['numberReturned'] == 10

    results = p.query(q='CREEK')
    assert results['numberMatched'] == 7
    assert results['numberReturned'] == 7


def test_query_select_properties(config):
    p = CKANProvider(config)
    results = p.query()
    assert len(results['features'][0]['properties']) == 43

    results = p.query(select_properties=['DAMNAME'])
    assert len(results['features'][0]['properties']) == 1

    results = p.query(select_properties=['DAMNAME', 'STATE'])
    assert len(results['features'][0]['properties']) == 2

    config['properties'] = ['DAMNAME', 'RIVER']
    p = CKANProvider(config)
    results = p.query()
    assert len(results['features'][0]['properties']) == 2
    assert results['features'][0]['properties']['DAMNAME'] == 'NAVAJO'


def test_get(config):
    p = CKANProvider(config)

    result = p.get(1)
    assert result['id'] == 1
    assert result['properties']['DAMNAME'] == 'NAVAJO'
