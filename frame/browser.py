from enum import Enum

from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
# from selenium.webdriver.opera.options import Options as OperaOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.opera import OperaDriverManager

from frame.logger import _init_logger


DRIVER_PATH = '/home/user/Downloads/webdrivers'

COMMON_OPTIONS = ('--no-sandbox', '--disable-infobars',
                  '--disable-extensions', '--disable-gpu',
                  '--disable-dev-shm-usage')


class BaseBrowser:

    def __init__(self, options=None):
        self._logger = _init_logger(type(self).__name__)
        self._set_options(options)

    # set common options for different browsers
    def _set_options(self, options):
        self._logger.debug(
            "setting options for %s", type(self).__name__)
        for option in *COMMON_OPTIONS, *options:
            self._options.add_argument(option)

    @property
    def options(self):
        return self._options


class BrowserChrome(BaseBrowser):

    def __init__(self, options=None):
        self._options = ChromeOptions()
        super().__init__(options)
        self._options.set_capability("browserName", "chrome")

    def __call__(self):
        return webdriver.Chrome(
            service=ChromeService(
                ChromeDriverManager().install()),
            options=self._options)


class BrowserFirefox(BaseBrowser):

    def __init__(self, options=None):
        self._options = FirefoxOptions()
        super().__init__(options)
        self._options.set_capability("browserName", "firefox")

    def __call__(self):
        return webdriver.Firefox(
            service=FirefoxService(
                GeckoDriverManager().install()),
            options=self._options)


class BrowserEdge(BaseBrowser):

    def __init__(self, options=None):
        self._options = EdgeOptions()
        super().__init__(options)
        self._options.set_capability("browserName", "MicrosoftEdge")

    def __call__(self):
        return webdriver.Edge(
            service=EdgeService(
                EdgeChromiumDriverManager().install()),
            options=self._options)


class BrowserOpera(BaseBrowser):

    def __init__(self, options=None):
        self._options = ChromeOptions()
        # self._options = OperaOptions()
        super().__init__(options)
        # self._options.binary_location = '/usr/bin/opera'
        self._options.set_capability("browserName", "opera")
        # https://github.com/operasoftware/operachromiumdriver/issues/96
        self._options.add_experimental_option('w3c', True)

    def __call__(self):
        # return webdriver.Opera(executable_path=OperaDriverManager().install(), options=self._options)
        return webdriver.Chrome(
            service=ChromeService(
                OperaDriverManager().install()),
            options=self._options)


class BrowserYandex(BaseBrowser):

    def __init__(self, options=None):
        self._options = ChromeOptions()
        super().__init__(options)
        self._options.binary_location = '/opt/yandex/browser-beta/yandex-browser-beta'

    def __call__(self):
        return webdriver.Chrome(
            service=ChromeService(f'{DRIVER_PATH}/yandexdriver'),
            options=self._options)


class BROWSERS(Enum):
    chrome = BrowserChrome
    firefox = BrowserFirefox
    edge = BrowserEdge
    opera = BrowserOpera
    yandex = BrowserYandex


class Browser:

    def __init__(self, name, options=None):
        self._logger = _init_logger(type(self).__name__)
        self._name = name
        try:
            self._browser = BROWSERS[name].value(options=options)
        except KeyError:
            self._logger.error("unsupported browser: %s", self.name)
            raise AssertionError(f'Unsupported browser: {self._name}')
        self.options = self._browser.options

    def __call__(self, *args, **kwargs):
        self._logger.debug("%s webdriver is ready for use", self._name)
        return self._browser(*args, **kwargs)
