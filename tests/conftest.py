import json
import logging
import random
import time
from datetime import datetime
from pathlib import Path

import allure
import pytest
from allure_commons.types import AttachmentType
from faker import Faker
from frame.base_page import BASE_URL
from frame.browser import Browser
from frame.db import DB
from frame.logger import _init_logger
from frame.types import AccountData, Creds, ProductData
from frame.utils import Utils
from pom.element.store.product import product
from selenium import webdriver

MAX_TIMEOUT = 5

USER_OPTIONS = ('--headless',
                '--start-maximized',
                '--start-fullscreen')


def pytest_addoption(parser):
    parser.addoption("--myip", default=Utils.get_ip())
    parser.addoption("--db-host", default=Utils.get_ip())
    parser.addoption("--base-url", default=BASE_URL)
    parser.addoption("--browser", default="chrome",
                     choices=('chrome', 'firefox', 'edge', 'opera', 'yandex'))
    parser.addoption("--bversion", default=None)
    parser.addoption("--executor", default="local")
    parser.addoption("--headless", action="store_true")
    parser.addoption("--start-maximized", default=True, action="store_true")
    parser.addoption("--start-fullscreen", action="store_true")
    parser.addoption("--test-log-level", default="INFO",
                     choices=("DEBUG", "INFO", "WARNING", "ERROR"))
    parser.addoption("--test-log-file", default="artifacts/testrun.log")
    parser.addoption("--screenshots-dir", default="artifacts/screenshots")


def pytest_configure(config: pytest.Config):
    global option
    option = config.option


@pytest.fixture(scope='session')
def options():
    return option


@pytest.fixture(scope='session')
def _app_logger(options):
    return _init_logger('', level=options.test_log_level, logfile=options.test_log_file)


# logger for conftest's fixtures
@pytest.fixture(scope='session')
def _logger(options, _app_logger):
    return _init_logger(__name__)


@pytest.fixture(scope='session')
def screenshots_dir(driver, rootdir, _logger):
    workdir = Path(rootdir, "artifacts/screenshots", driver.session_id)
    try:
        workdir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        _logger.exception(e)
        pytest.fail()
    else:
        _logger.info("created screenshots directory %s", workdir)
        return workdir


def skip_if(opt):
    return pytest.mark.skipif(
        getattr(option, opt, None),
        reason=f"Incompatible with {opt}"
    )


def skip_if_not(opt):
    return pytest.mark.skipif(
        not getattr(option, opt, None),
        reason=f"Only with {opt}"
    )


@pytest.fixture(autouse=True)
def log(request, _logger):
    _logger.info(">>> RUN <%s> <<<", request.node.name)

    yield

    _logger.info(">>> END <%s> <<<", request.node.name)


@pytest.fixture(scope='session')
def my_IP(request):
    return request.config.getoption("--myip")


@pytest.fixture(scope='session')
def db_host(request):
    return request.config.getoption("--db-host")


@pytest.fixture(scope='session')
def base_url(request):
    return request.config.getoption("--base-url")


@pytest.fixture(scope='session')
def valid_creds():
    return Creds('user', 'bitnami')


@pytest.fixture(scope='session')
def invalid_creds():
    return Creds('user', 'bitnomi')


@pytest.fixture(scope='session')
def driver(request, options, _app_logger):

    logger = _init_logger('driver')

    browser = request.config.getoption('browser')
    bversion = request.config.getoption('bversion')
    executor = request.config.getoption('executor')
    start_maximized = request.config.getoption('start_maximized')

    options = {}
    for option in USER_OPTIONS:
        if request.config.getoption(option):
            options.update({option: True})

    capabilities = {
        "browserName": browser,
        "browserVersion": bversion,
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": False
        }
    }

    if executor != "local":
        logger.info("using remote executor at %s with %s", executor, browser)
        executor_url = f'http://{executor}:4444/wd/hub'
        options = Browser(browser, options=options).options
        for k, v in capabilities.items():
            options.set_capability(k, v) if v else next

        driver = webdriver.Remote(
            command_executor=executor_url,
            options=options
        )
    else:
        executor_url = 'Local'
        logger.info("using local instance of %s", browser)
        driver = Browser(browser, options=options)()

    allure.attach(
        name=driver.session_id,
        body=json.dumps(driver.capabilities),
        attachment_type=allure.attachment_type.JSON)

    with open("artifacts/allure-results/environment.xml", "w+") as file:
        file.write(f"""
            <environment>
                <parameter>
                    <key>Browser</key>
                    <value>{browser}</value>
                </parameter>
                <parameter>
                    <key>Browser.version</key>
                    <value>{bversion}</value>
                </parameter>
                <parameter>
                    <key>Executor</key>
                    <value>{executor_url}</value>
                </parameter>
            </environment>
        """)

    driver.logger = logger
    driver.test_name = request.node.name

    if start_maximized:
        driver.maximize_window()

    logger.info("starting webdriver %s session %s", browser, driver.session_id)

    yield driver

    logger.info("closing webdriver %s session %s", browser, driver.session_id)

    driver.quit()


@pytest.fixture
def account_valid():
    return AccountData(
        fname='Denzel',
        lname='Washington',
        email='denzel.washington@holliwood.com',
        phone='1 234 5678 90',
        password_1='helloUser',
        password_2='helloUser',
    )


@pytest.fixture
def account_random():
    faker = Faker()
    return AccountData(
        fname=faker.first_name(),
        lname=faker.last_name(),
        email=faker.email(),
        phone=faker.phone_number(),
        password_1=faker.password(),
        password_2=faker.password(),
    )


@pytest.fixture
def product_random():
    faker = Faker()
    return ProductData(
        name=f'test_{faker.word()}',
        description=faker.paragraph(),
        model=f'test_{faker.word()}',
        price=faker.pyint(),
        quantity=faker.pyint(),
        categories=random.choice(product.item_names)
    )


@pytest.fixture(autouse=True)
def back_to_base(request, _logger: logging.Logger):
    yield
    try:
        request.instance.driver.get(request.instance.url)
    except:
        pass
    else:
        _logger.info("go back to %s", request.instance.url)
        pass


@pytest.fixture(scope='session')
def account_admin_valid():
    return ('user', 'bitnami')


@pytest.fixture(scope='session')
def db_connector(db_host):
    connection = DB(host=db_host, database='bitnami_opencart',
                    user='bn_opencart', password='')

    yield connection

    connection.close()


@pytest.fixture
def db_product_random(db_connector: DB, product_random, _logger):
    _logger.info("adding random product")

    yield db_connector.add_product(product_random)

    _logger.info("deleting product")
    db_connector.delete_product('test')


@pytest.fixture
def db_delete_product(db_connector: DB, _logger):

    yield

    _logger.info("deleting product")
    db_connector.delete_product('test')


@pytest.fixture
def db_customer_valid(db_connector: DB, account_valid, _logger):
    _logger.info("adding valid customer account")

    yield db_connector.create_customer(account_valid)

    _logger.info("deleting customer {}".format(account_valid.email))
    db_connector.delete_customer(account_valid.email)


@pytest.fixture
def db_delete_customer_valid(db_connector: DB, account_valid, _logger):
    _logger.info("deleting valid customer account")

    yield

    _logger.info("deleting customer {}".format(account_valid.email))
    db_connector.delete_customer(account_valid.email)


@pytest.fixture
def db_customer_random(db_connector: DB, account_random, _logger):
    _logger.info("adding random customer account")

    yield db_connector.create_customer(account_random)

    _logger.info("deleting customer {}".format(account_random.email))
    db_connector.delete_customer(account_random.email)


@pytest.fixture
def db_delete_customer_random(db_connector: DB, account_random, _logger):
    _logger.info("deleting random customer account")

    yield

    _logger.info("deleting customer {}".format(account_random.email))
    db_connector.delete_customer(account_random.email)


# https://docs.pytest.org/en/latest/example/simple.html#post-process-test-reports-failures
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield

    rep = outcome.get_result()

    # set a report attribute for each phase of a call
    # which can be "setup", "call", "teardown"

    setattr(item, "rep_" + rep.when, rep)


def take_screenshot_selenium(driver, dir, nodeid):
    time.sleep(1)
    file_name = f'{nodeid}_{datetime.today().strftime("%Y-%m-%d_%H:%M")}.png'.replace("/",
                                                                                      "_").replace("::", "__")
    driver.save_screenshot(f"{dir}/{file_name}")
    return file_name


def take_screenshot_allure(driver, nodeid):
    time.sleep(1)
    allure.attach(driver.get_screenshot_as_png(), name=nodeid,
                  attachment_type=AttachmentType.PNG)


@pytest.fixture(scope="function", autouse=True)
def fail_check(request, driver, _logger, screenshots_dir):

    yield

    if request.node.rep_setup.failed:
        _logger.error("setting up a test %s failed", request.node.nodeid)
    elif request.node.rep_setup.passed:
        if request.node.rep_call.failed:
            # driver = request.node.funcargs['driver']
            screenshot = take_screenshot_selenium(
                driver, screenshots_dir, request.node.nodeid)
            take_screenshot_allure(driver, request.node.nodeid)
            _logger.error("executing test %s failed", request.node.nodeid)
            _logger.info("screenshot stored in %s",
                         Path(screenshots_dir, screenshot))
