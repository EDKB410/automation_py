from frame.base_locator import BaseLocator, Selector
from frame.base_page import BasePage
from selenium.webdriver.common.by import By
import allure

class SearchStringLocators(BaseLocator):
    
    LOCATOR_INPUT_SEARCH = Selector(By.NAME, "search")
    LOCATOR_BUTTON_SEARCH = Selector(
        By.CSS_SELECTOR, "button.btn.btn-default.btn-lg")
        

class SearchString(BasePage):

    locator = SearchStringLocators

    @allure.step("click Search button")
    def click_search_button(self):
        self._logger.info("click Search button")
        return self.click(self.locator.LOCATOR_BUTTON_SEARCH)

    @allure.step("do search by text {text}")
    def do_search(self, text):
        self._logger.info("do search by text, %s", text)
        element = self.find_element(self.locator.LOCATOR_INPUT_SEARCH)
        element.click()
        element.clear()
        element.send_keys(text)
        self.click_search_button()
