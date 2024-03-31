from collections import namedtuple
from selenium.webdriver.common.by import By

Locator = namedtuple('Locator', ('name', 'locator'))
Selector = namedtuple('Selector', ('by', 'selector'))


class BaseLocator:

    @classmethod
    @property
    def locators(cls):
        d = {}
        for b in cls, *cls.__bases__:
            d.update(b.__dict__)
        return [Locator(*p) for p in d.items() if p[0].startswith('LOCATOR_')]

    @classmethod
    @property
    def root(cls):
        cls.locators.sort(key=lambda x: len(x.name))
        return Locator(*cls.locators[0])

    @classmethod
    def find_by_selector(cls, selector):
        try:
            return [Locator(*l) for l in cls.locators if selector in l.locator].pop()
        except IndexError:
            pass

    @classmethod
    def find_by_name(cls, name):
        try:
            return [Locator(*l) for l in cls.locators if name == l.name].pop()
        except IndexError:
            pass

    @classmethod
    def find_children(cls, val):
        if isinstance(val, Selector):
            name = cls.find_by_selector(val.selector).name
        else:
            name = val
        return [Locator(*l) for l in cls.locators if l.name.startswith(f'{name}_')]

    @classmethod
    def idfn(cls, val):
        if isinstance(val, Selector):
            return cls.find_by_selector(val.selector).name
        elif isinstance(val, Locator):
            return val.name
        else:
            return repr(val)

    @classmethod
    def mapper(cls, text):
        l = cls.find_by_name(text)
        return l if l else cls.find_by_name(f'{cls.root.name}_{text.upper()}')

