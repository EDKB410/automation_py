import pytest
from pydantic import BaseModel, HttpUrl, ValidationError
from src.api.simple_api_client import SimpleApiClient


class Geo(BaseModel):
    lat: str
    lng: str


class Address(BaseModel):
    street: str
    suite: str
    city: str
    zipcode: str
    geo: Geo


class Company(BaseModel):
    name: str
    catchPhrase: str
    bs: str


class User(BaseModel):
    id: int
    name: str
    username: str
    email: str
    address: Address
    phone: str
    website: str
    company: Company


class UserList(BaseModel):
    __root__: list[User]


class Post(BaseModel):
    userId: int
    id: int
    title: str
    body: str


class PostList(BaseModel):
    __root__: list[Post]


class Comment(BaseModel):
    postId: int
    id: int
    name: str
    email: str
    body: str


class CommentList(BaseModel):
    __root__: list[Comment]


class Album(BaseModel):
    userId: int
    id: int
    title: str


class AlbumList(BaseModel):
    __root__: list[Album]


class Photo(BaseModel):
    albumId: int
    id: int
    title: str
    url: HttpUrl
    thumbnailUrl: HttpUrl


class PhotosList(BaseModel):
    __root__: list[Photo]


class Todo(BaseModel):
    userId: int
    id: int
    title: str
    completed: bool


class TodosList(BaseModel):
    __root__: list[Todo]


def validate_object(cls, obj):
    try:
        cls.parse_obj(obj)
    except ValidationError as e:
        print(e.json())
        pytest.fail()


proxies = {
    "http": "http://localhost:8080",
    "https": "http://localhost:8080"
}

base_url = 'https://jsonplaceholder.typicode.com'

CHOICES = 5


@pytest.fixture(scope='session')
def api():
    yield SimpleApiClient(url=base_url, verify=False, proxies=None)


def test_get_all_users(api):
    r = api.GET('/users')
    assert r.ok
    validate_object(UserList, r.json())


def test_get_all_posts(api):
    r = api.GET('/posts')
    assert r.ok
    validate_object(PostList, r.json())


def test_get_all_albums(api):
    r = api.GET('/albums')
    assert r.ok
    validate_object(AlbumList, r.json())


def test_get_all_photos(api):
    r = api.GET('/photos')
    assert r.ok
    validate_object(PhotosList, r.json())


def test_get_all_todos(api):
    r = api.GET('/todos')
    assert r.ok
    validate_object(TodosList, r.json())


@pytest.mark.parametrize('userid', range(1, CHOICES))
def test_get_single_user(api, userid):
    r = api.GET(f'/users/{userid}')
    assert r.ok
    validate_object(User, r.json())


@pytest.mark.parametrize('postid', range(1, CHOICES))
def test_get_single_post(api, postid):
    r = api.GET(f'/posts/{postid}')
    assert r.ok
    validate_object(Post, r.json())

