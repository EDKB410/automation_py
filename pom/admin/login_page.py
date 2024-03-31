import allure
from frame.base_locator import BaseLocator, Selector
from frame.base_page import BasePage
from selenium.webdriver.common.by import By


class AdminLoginPageLocators(BaseLocator):

    URL = '/admin'

    URL_ADMIN_LOGIN_PAGE = URL

    TITLE_ADMIN_LOGIN_PAGE = "Administration"
    TITLE_ADMIN_PAGE = "Dashboard"
    TITLE_FORGOTTEN_PASSWORD_PAGE = "Forgot Your Password?"

    LOCATOR_INPUT_USERNAME = Selector(By.CSS_SELECTOR, "#input-username")
    LOCATOR_INPUT_PASSWORD = Selector(By.CSS_SELECTOR, "#input-password")
    LOCATOR_INPUT_EMAIL = Selector(By.CSS_SELECTOR, "#input-email")

    LOCATOR_BUTTON_LOGIN_SUBMIT = Selector(
        By.CSS_SELECTOR, "button.btn.btn-primary")
    LOCATOR_BUTTON_FORGOTTEN_PASSWORD_CANCEL = Selector(
        By.CSS_SELECTOR, "a.btn.btn-default")
    LOCATOR_BUTTON_FORGOTTEN_PASSWORD_SUBMIT = Selector(
        By.CSS_SELECTOR, "button.btn.btn-primary")
    LOCATOR_BUTTON_ALERT_CLOSE = Selector(By.CSS_SELECTOR, "button.close")

    LOCATOR_LINK_FORGOTTEN_PASSWORD = Selector(
        By.LINK_TEXT, "Forgotten Password")

    LOCATOR_ALERT_DANGER_MESSAGE = Selector(
        By.CSS_SELECTOR, "div.alert.alert-danger.alert-dismissible")
    LOCATOR_ALERT_SUCCESS_MESSAGE = Selector(
        By.CSS_SELECTOR, "div.alert.alert-success.alert-dismissible")


class AdminLoginPage(BasePage):

    locator = AdminLoginPageLocators

    @allure.step("enter login {login}")
    def enter_login(self, login):
        self._logger.info("enter login %s", login)
        inp = self.find_element(self.locator.LOCATOR_INPUT_USERNAME)
        inp.clear()
        inp.click()
        inp.send_keys(login)

    @allure.step("enter password {password}")
    def enter_password(self, password):
        self._logger.info("enter password %s", password)
        inp = self.find_element(self.locator.LOCATOR_INPUT_PASSWORD)
        inp.clear()
        inp.click()
        inp.send_keys(password)

    @allure.step("enter email {email}")
    def enter_email(self, email):
        self._logger.info("enter email %s", email)
        inp = self.find_element(self.locator.LOCATOR_INPUT_EMAIL)
        inp.clear()
        inp.click()
        inp.send_keys(email)

    @allure.step("click Login button")
    def click_login_button(self):
        self._logger.info("click Login button")
        self.click(self.locator.LOCATOR_BUTTON_LOGIN_SUBMIT)

    @allure.step("admin login with login {login}, password {password}")
    def admin_login_with(self, login, password):
        self._logger.info("admin login with %s, %s", login, password)
        self.enter_login(login)
        self.enter_password(password)
        self.click_login_button()

    @allure.step("click Forgotten password link")
    def click_forgotten_password_link(self):
        self._logger.info("click Forgotten password link")
        self.click(self.locator.LOCATOR_LINK_FORGOTTEN_PASSWORD)

    @allure.step("click Cancel button on Forgotten password page")
    def click_forgotten_password_cancel_button(self):
        self._logger.info("click Cancel button")
        self.click(
            self.locator.LOCATOR_BUTTON_FORGOTTEN_PASSWORD_CANCEL)

    @allure.step("click Reset button on Forgotten password page")
    def click_forgotten_password_reset_button(self):
        self._logger.info("click Reset button")
        self.click(
            self.locator.LOCATOR_BUTTON_FORGOTTEN_PASSWORD_SUBMIT)

    @allure.step("check if alert danger is present")
    def does_present_alert_danger(self):
        self._logger.info("check if alert danger is present")
        return self.does_present(self.locator.LOCATOR_ALERT_DANGER_MESSAGE)

    @allure.step("check if alert danger does not present")
    def does_not_present_alert_danger(self):
        self._logger.info("check if alert danger is not present")
        return self.does_not_present(self.locator.LOCATOR_ALERT_DANGER_MESSAGE)

    @allure.step("check if alert success is present")
    def does_present_alert_success(self):
        self._logger.info("check if alert success is present")
        return self.does_present(self.locator.LOCATOR_ALERT_SUCCESS_MESSAGE)

    @allure.step("check if alert success is not present")
    def does_not_present_alert_success(self):
        self._logger.info("check if alert success is not present")
        return self.does_not_present(self.locator.LOCATOR_ALERT_SUCCESS_MESSAGE)

    @allure.step("close alert")
    def close_alert(self):
        self._logger.info("close alert")
        self.click(self.locator.LOCATOR_BUTTON_ALERT_CLOSE)


if __name__ == '__main__':

    print(AdminLoginPage.locator.locators)
