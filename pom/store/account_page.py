import allure
from frame.base_locator import BaseLocator, Selector
from frame.base_page import BasePage
from selenium.webdriver.common.by import By


class AccountPageLocators(BaseLocator):

    TITLE = 'My Account'
    LOCATOR_BUTTON_CONTINUE = Selector(
        By.CSS_SELECTOR, '#content > div > div > a')


class AccountPage(BasePage):

    locator = AccountPageLocators

    @allure.step("click Continue button")
    def click_continue(self):
        self._logger.info("click Continue button")
        self.click(self.locator.LOCATOR_BUTTON_CONTINUE)
