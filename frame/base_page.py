import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from frame.base_locator import Locator, Selector, BaseLocator
from frame.utils import Utils
from frame.logger import _init_logger

TIMEOUT_MESSAGE = "Can't find element(s) by locator {} in {} s"
TIMEOUT = 3

BASE_URL = f'http://{Utils.get_ip()}:8081'

# BASE_URL = 'http://127.0.0.1:8081'


class BasePage:

    locator = BaseLocator

    def __init__(self, driver, url='', open=False):
        self._logger = _init_logger(type(self).__name__)
        self.driver = driver
        self.actions = ActionChains(driver)
        self.url = url
        self.__wait = lambda timeout=TIMEOUT: WebDriverWait(
            driver, timeout=timeout)
        if open:
            self.open()

    @property
    def locators(self):
        return [p for p in self.locator.__dict__.items() if p[0].startswith('LOCATOR_')]

    @property
    def title(self):
        return self.driver.title

    @property
    def page_src(self):
        return self.driver.page_source

    @property
    def current_url(self):
        return self.driver.current_url

    def go(self, url):
        self._logger.info("go to %s", url)
        with allure.step(f"go to {url}"):
            return self.driver.get(url)

    def open(self):
        self._logger.info("open %s", self.url)
        with allure.step(f"open {self.url}"):
            return self.driver.get(self.url)

    def at_page(self, title):
        self._logger.info("check if driver at page %s", title)
        return self.driver.title == title

    def back(self):
        self._logger.info("go back from %s", self.url)
        with allure.step(f"go back from {self.url}"):
            return self.driver.back()

    def forward(self):
        self._logger.info("go forward from %s", self.url)
        with allure.step(f"go forward from {self.url}"):
            return self.driver.forward()

    def refresh(self):
        self._logger.info("refresh at %s", self.url)
        with allure.step(f"refresh at {self.url}"):
            return self.driver.refresh()

    def enter_text(self, locator, text):
        self._logger.info("input text %s in %s", text, locator)
        with allure.step(f"input text {text} in {locator}"):
            element = self.find_element(locator)
            element.click()
            element.clear()
            element.send_keys(text)
            return element

    @allure.step("input text {text} with dropdown in {locator}")
    def enter_text_with_dropdown(self, locator, text):
        self._logger.info(
            "input text with dropdown %s in %s", text, locator)
        with allure.step(f"input text {text} in {locator}"):
            element = self.find_element(locator)
            element.clear()
            element.click()
            element.send_keys(text)
        with allure.step("click on dropdown"):
            try:
                # handle input with a dropdown
                self.click(Selector(By.PARTIAL_LINK_TEXT, text))
            except:
                element.clear()
            return element

    def click(self, locator, time=TIMEOUT):
        self._logger.info("click on %s", locator)
        with allure.step(f"click on {locator}"):
            if getattr(locator, 'self', None):
                locator = locator.self
            self.__wait(time).until(
                EC.element_to_be_clickable(locator)).click()

    def hover(self, locator, time=TIMEOUT):
        self._logger.info("hover at %s", locator)
        with allure.step(f"hover at {locator}"):
            if getattr(locator, 'self', None):
                locator = locator.self
            element = self.find_element(locator, time)
            self.actions.move_to_element(element).perform()
            return element

    def click_element(self, element):
        self._logger.info("click on element %s", element.text)
        with allure.step(f"click on element {element.text}"):
            element.click()

    def find_element(self, locator, time=TIMEOUT):
        self._logger.info("find element by %s", locator)
        with allure.step(f"find element by {locator}"):
            return self.__wait(time).until(EC.presence_of_element_located(locator),
                                           message=TIMEOUT_MESSAGE.format(locator, time))

    def find_elements(self, locator, time=TIMEOUT):
        self._logger.info("find elements by %s", locator)
        with allure.step(f"find elements by {locator}"):
            return self.__wait(time).until(EC.presence_of_all_elements_located(locator),
                                           message=TIMEOUT_MESSAGE.format(locator, time))

    def is_visible(self, locator, time=TIMEOUT):
        self._logger.info("wait for element is visible %s", locator)
        with allure.step(f"wait for element is visible {locator}"):
            return self.__wait(time).until(EC.visibility_of_element_located(locator),
                                           message=TIMEOUT_MESSAGE.format(locator, time))

    def are_visible(self, locator, time=TIMEOUT):
        self._logger.info("wait for elements are visible %s", locator)
        with allure.step(f"wait for elements are visible {locator}"):
            return self.__wait(time).until(EC.visibility_of_all_elements_located(locator),
                                           message=TIMEOUT_MESSAGE.format(locator, time))

    def is_not_visible(self, locator, time=TIMEOUT):
        self._logger.info("wait for element is not visible %s", locator)
        with allure.step(f"wait for element is not visible {locator}"):
            return self.__wait(time).until(EC.invisibility_of_element_located(locator),
                                           message=TIMEOUT_MESSAGE.format(locator, time))

    def does_present(self, locator, time=TIMEOUT):
        self._logger.info("wait for element is present %s", locator)
        with allure.step(f"wait for element is present {locator}"):
            return self.__wait(time).until(EC.presence_of_element_located(locator),
                                           message=TIMEOUT_MESSAGE.format(locator, time))

    def does_not_present(self, locator, time=0.2):
        self._logger.info("wait for element is not present %s", locator)
        with allure.step(f"wait for element is not present {locator}"):
            try:
                self.does_present(locator, time=time)
            except TimeoutException:
                self._logger.info("element %s is not present", locator)
                return True
            else:
                self._logger.warning("element %s is present", locator)
                return False

    def is_clickable(self, locator, time=TIMEOUT):
        self._logger.info("wait for element is clickable %s", locator)
        with allure.step(f"wait for element is clickable {locator}"):
            return self.__wait(time).until(EC.element_to_be_clickable(locator),
                                           message=TIMEOUT_MESSAGE.format(locator, time))

    @allure.step("check if alert is present")
    def does_alert_present(self, time=0.5):
        self._logger.info("check if alert is present")
        return self.__wait(time).until(EC.alert_is_present())

    @allure.step("accept alert")
    def alert_accept(self):
        self._logger.info("accept the alert")
        self.driver.switch_to.alert.accept()

    @allure.step("dismiss alert")
    def alert_dismiss(self):
        self._logger.info("dismiss the alert")
        self.driver.switch_to.alert.dismiss()
