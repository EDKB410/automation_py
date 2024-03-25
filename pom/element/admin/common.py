import allure
from frame.base_locator import BaseLocator, Selector
from frame.base_page import BasePage
from selenium.webdriver.common.by import By


class AdminCommonElementsLocators(BaseLocator):

    LOCATOR_LOGO = Selector(By.CSS_SELECTOR, "#header-logo")
    LOCATOR_LOGOUT = Selector(
        By.CSS_SELECTOR, '#header > div > ul > li:nth-child(2) > a')


class AdminCommonElements(BasePage):

    locator = AdminCommonElementsLocators

    @allure.step("click on Logo")
    def click_logo(self):
        self._logger.info("click on Logo")
        self.click(self.locator.LOCATOR_LOGO)

    @allure.step("click Logout")
    def click_logout(self):
        self._logger.info("click Logout")
        self.click(self.locator.LOCATOR_LOGOUT)
