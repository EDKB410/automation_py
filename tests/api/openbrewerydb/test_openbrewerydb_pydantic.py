from enum import Enum

import pytest
from pydantic import (BaseModel, ValidationError, conlist)

'''
according to the API's hint:
"Brewery type must include one of these types: [\"micro\", 
\"nano\", \"regional\", \"brewpub\", \"large\", \"planning\",
\"bar\", \"contract\", \"proprieter\", \"closed\"]"
'''


class BreweryType(Enum):
    micro = 'micro'
    nano = 'nano'
    regional = 'regional'
    brewpub = 'brewpub'
    large = 'large'
    planning = 'planning'
    bar = 'bar'
    contract = 'contract'
    proprietor = 'proprietor'
    closed = 'closed'


class Brewery(BaseModel):
    id: str
    name: str
    brewery_type: BreweryType
    street: str = None
    address_2: str = None
    address_3: str = None
    city: str
    state: str = None
    county_province: str = None
    postal_code: str
    country: str
    longitude: str = None
    latitude: str = None
    phone: str = None
    website_url: str = None
    updated_at: str
    created_at: str


class BreweryAutoComplete(BaseModel):
    id: str
    name: str


class NonEmptyBreweryList(BaseModel):
    __root__: conlist(item_type=Brewery, min_items=1)


class BreweryList(BaseModel):
    __root__: list[Brewery]


class BreweryAutoCompleteList(BaseModel):
    __root__: list[BreweryAutoComplete]


def validate_object(cls, obj):
    try:
        cls.parse_obj(obj)
    except ValidationError as e:
        print(e.json())
        pytest.fail()


def test_brewery_list_all(api):
    r = api.GET('/')
    assert r.ok
    validate_object(NonEmptyBreweryList, r.json())


def test_get_single_brewery(api, brewery_id):
    r = api.GET(f'/{brewery_id}')
    assert r.ok
    validate_object(Brewery, r.json())


@pytest.mark.xfail(strict=True, reason='Should not be more than 15 items per request')
def test_autocomplete_limit(api):
    r = api.GET('/autocomplete', params={'query': 'good'})
    assert r.ok
    assert len(r.json()) <= 15


def test_autocomplete_item_structure(api):
    r = api.GET('/autocomplete', params={'query': 'good'})
    assert r.ok
    validate_object(BreweryAutoCompleteList, r.json())


def test_brewery_search(api):
    r = api.GET('/search', params={'query': 'good'})
    assert r.ok
    validate_object(BreweryList, r.json())


# есть элемент с типом 'proprietor', но API понимает 'proprieter'
xfailed = ['proprietor']


@pytest.mark.parametrize('brewery_type',
                         [bt.value for bt in BreweryType
                          if bt.value not in xfailed] +
                         [pytest.param(p, marks=pytest.mark.xfail(strict=True))
                          for p in xfailed]
                         )
def test_brewery_search_by_type(api, brewery_type):
    r = api.get_all_pages('/', params={'by_type': brewery_type})
    validate_object(NonEmptyBreweryList, r)


def test_brewery_search_by_name(api, brewery_name):
    r = api.get_all_pages('/', params={'by_name': brewery_name})
    validate_object(NonEmptyBreweryList, r)


def test_brewery_search_by_city(api, city):
    r = api.get_all_pages('/', params={'by_city': city, 'per_page': 50})
    validate_object(NonEmptyBreweryList, r)


def test_brewery_search_by_state(api, state):
    r = api.get_all_pages('/', params={'by_state': state})
    validate_object(NonEmptyBreweryList, r)


def test_brewery_search_by_country(api, country):
    r = api.get_all_pages('/', params={'by_country': country})
    validate_object(NonEmptyBreweryList, r)


def test_brewery_search_by_postal(api, postal_code):
    r = api.get_all_pages('/', params={'by_postal': postal_code})
    validate_object(NonEmptyBreweryList, r)


@pytest.mark.parametrize('per_page, expected', [(None, 20), (0, 0), (42, 42)], ids=['default', 'zero', 'number'])
def test_per_page(api, per_page, expected):
    r = api.GET('/', params={'per_page': per_page})
    assert r.ok
    assert len(r.json()) == expected
