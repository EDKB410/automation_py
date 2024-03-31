import copy
import random

import pytest
from src.api.simple_api_client import SimpleApiClient
from tests.api.openbrewerydb.test_openbrewerydb_pydantic import Brewery

proxies = {
    "http": "http://localhost:8080",
    "https": "http://localhost:8080"
}

base_url = 'https://api.openbrewerydb.org/breweries'


@pytest.fixture(scope='session')
def api():
    yield SimpleApiClient(url=base_url, verify=False, proxies=None)


def breweries():
    with SimpleApiClient(url=base_url, verify=False, proxies=None).GET('/search?query=*') as r:
        for j in r.json():
            yield j


raw = {k: set() for k in Brewery.__fields__.keys()}
xfailed = copy.deepcopy(raw)

# API do not recognize brewery_type = 'taproom' but some of items consist it (England)

for b in breweries():
    for k, v in b.items():
        raw[k].add(v)
        if (b['brewery_type'] in ('taproom',)):
            xfailed[k].add(v)


def choises(k, n):
    return random.sample(list(raw[k]), n)


def params_filter(p_name):
    def wrapper(p):
        if p in xfailed[p_name]:
            return pytest.param(p, marks=pytest.mark.xfail(strict=True))
        return p
    return wrapper


@ pytest.fixture(params=map(params_filter('id'), choises('id', 5)), scope='session')
def brewery_id(request):
    yield request.param


@ pytest.fixture(params=map(params_filter('name'), choises('name', 5)), scope='session')
def brewery_name(request):
    yield request.param


@ pytest.fixture(params=(b for b in raw['brewery_type']), scope='session')
def brewery_type(request):
    yield request.param


@ pytest.fixture(params=map(params_filter('city'), choises('city', 5)), scope='session')
def city(request):
    yield request.param


@ pytest.fixture(params=map(params_filter('state'), choises('state', 1)), scope='session')
def state(request):
    yield request.param


@ pytest.fixture(params=map(params_filter('country'), choises('country', 1)), scope='session')
def country(request):
    yield request.param


@ pytest.fixture(params=map(params_filter('postal_code'), choises('postal_code', 5)), scope='session')
def postal_code(request):
    yield request.param
