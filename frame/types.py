from collections import namedtuple
from dataclasses import dataclass
from enum import Enum

Creds = namedtuple('Creds', ('login', 'password'))


@dataclass
class AccountData:
    fname: str
    lname: str
    email: str
    phone: str
    password_1: str
    password_2: str


@dataclass
class ProductData:
    name: str
    description: str
    model: str
    price: int
    quantity: int
    categories: str


class Currency(Enum):
    USD = '$'
    EUR = '€'
    GBP = '£'
