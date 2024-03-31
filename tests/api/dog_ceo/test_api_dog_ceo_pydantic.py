import pytest
from pydantic import BaseModel, HttpUrl, ValidationError, parse, validator
from src.api.simple_api_client import SimpleApiClient

base_url = 'https://dog.ceo/api'

proxies = {
    "http": "http://localhost:8080",
    "https": "http://localhost:8080"
}


class BaseMessage(BaseModel):
    status: str


class BreedsList(BaseMessage):
    message: list[str]


class BreedsSubbreedsList(BaseMessage):
    message: dict[str, list[str]]


class ImageUrl(BaseMessage):
    message: HttpUrl


class ImageUrlList(BaseMessage):
    message: list[HttpUrl]


def validate_object(cls, obj):
    try:
        cls.parse_obj(obj)
    except ValidationError as e:
        print(e.json())
        pytest.fail()


raw_breeds_list = SimpleApiClient(url=base_url, verify=False, proxies=None).GET(
    '/breeds/list/all').json()['message']


def breeds(res):
    for breed, val in res.items():
        for subbreed in val:
            yield breed, subbreed


def idfn(val):
    if isinstance(val, str):
        return val.title()
    if isinstance(val, tuple):
        return f'{val[1].title()} {val[0].title()}'
    return val


@pytest.fixture(params=set(b for b, dummy in breeds(raw_breeds_list)), ids=idfn, scope='session')
def breed(request):
    yield request.param


@pytest.fixture(params=breeds(raw_breeds_list), ids=idfn, scope='session')
def sub_breed(request):
    yield request.param


@pytest.fixture(scope='session')
def api():
    yield SimpleApiClient(url=base_url, verify=False, proxies=None)

# --- tests without sub-breads


def test_breeds_list_all(api):
    r = api.GET('/breeds/list/all')
    assert r.ok
    validate_object(BreedsSubbreedsList, r.json())


def test_breeds_list(api):
    r = api.GET('/breeds/list')
    assert r.ok
    validate_object(BreedsList, r.json())


def test_breeds_image_random(api):
    r = api.GET('/breeds/image/random')
    assert r.ok
    validate_object(ImageUrl, r.json())


@pytest.mark.parametrize('n', range(1, 3))
def test_breeds_image_random_multiple(api, n):
    r = api.GET(f'/breeds/image/random/{n}')
    assert r.ok
    validate_object(ImageUrlList, r.json())

# --- tests with sub-breads


def test_breed_list(api, breed):
    r = api.GET(f'/breed/{breed}/list')
    assert r.ok
    validate_object(BreedsList, r.json())


def test_breed_images_all(api, breed):
    r = api.GET(f'/breed/{breed}/images')
    assert r.ok
    validate_object(ImageUrlList, r.json())


def test_breed_image_random(api, breed):
    r = api.GET(f'/breed/{breed}/images/random')
    assert r.ok
    validate_object(ImageUrl, r.json())


@pytest.mark.parametrize('n', range(1, 3))
def test_breed_image_random_multiple(api, breed, n):
    r = api.GET(f'/breed/{breed}/images/random/{n}')
    assert r.ok
    validate_object(ImageUrlList, r.json())


# --- tests on images with sub-breads
def test_breed_sub_breed_images(api, sub_breed):
    r = api.GET(f'/breed/{sub_breed[0]}/{sub_breed[1]}/images')
    assert r.ok
    validate_object(ImageUrlList, r.json())


def test_breed_sub_breed_images_random(api, sub_breed):
    r = api.GET(f'/breed/{sub_breed[0]}/{sub_breed[1]}/images/random')
    assert r.ok
    validate_object(ImageUrl, r.json())


@pytest.mark.parametrize('n', range(1, 3))
def test_breed_sub_breed_images_random_multiple(api, n, sub_breed):
    r = api.GET(f'/breed/{sub_breed[0]}/{sub_breed[1]}/images/random/{n}')
    assert r.ok
    validate_object(ImageUrlList, r.json())
