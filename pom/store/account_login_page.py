import allure
from frame.base_locator import BaseLocator, Selector
from frame.base_page import BasePage
from selenium.webdriver.common.by import By


class AccountLoginPageLocators(BaseLocator):

    LOCATOR_BUTTON_CONTINUE = Selector(
        By.CSS_SELECTOR, '#content > div > div > a')
    LOCATOR_INPUT_EMAIL = Selector(By.ID, 'input-email')
    LOCATOR_INPUT_PASSWORD = Selector(By.ID, 'input-password')
    LOCATOR_BUTTON_LOGIN = Selector(By.CSS_SELECTOR, 'input[type=submit]')


class AccountLoginPage(BasePage):

    locator = AccountLoginPageLocators

    @allure.step("enter email {email}")
    def enter_email(self, email):
        self._logger.info("enter email %s", email)
        self.enter_text(self.locator.LOCATOR_INPUT_EMAIL, email)

    @allure.step("enter password {password}")
    def enter_password(self, password):
        self._logger.info("enter password, %s", password)
        self.enter_text(self.locator.LOCATOR_INPUT_PASSWORD, password)

    @allure.step("click Login button")
    def click_login(self):
        self._logger.info("click Login button")
        self.click(self.locator.LOCATOR_BUTTON_LOGIN)

    @allure.step("login with email {email} and password {password}")
    def login_with(self, email, password):
        self._logger.info(
            "login with email %s and password %s", email, password)
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()
