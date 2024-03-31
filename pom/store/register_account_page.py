import allure
from frame.base_locator import BaseLocator, Selector
from frame.base_page import BasePage
from selenium.webdriver.common.by import By


class RegisterAccountPageLocators(BaseLocator):

    URL = "/index.php?route=account/register"
    URL_REGISTER_ACCOUNT = URL
    TITLE_REGISTER_ACCOUNT = "Register Account"

    LOCATOR_LINK_LOGIN = Selector(By.CSS_SELECTOR, "#content > p > a")
    LOCATOR_LINK_PRIVACY_POLICY = Selector(
        By.CSS_SELECTOR, "#content > form > div > div > a")
    LOCATOR_INPUT_FIRST_NAME = Selector(By.CSS_SELECTOR, "#input-firstname")
    LOCATOR_INPUT_LAST_NAME = Selector(By.CSS_SELECTOR, "#input-lastname")
    LOCATOR_INPUT_EMAIL = Selector(By.CSS_SELECTOR, "#input-email")
    LOCATOR_INPUT_TELEPHONE = Selector(By.CSS_SELECTOR, "#input-telephone")
    LOCATOR_INPUT_PASSWORD = Selector(By.CSS_SELECTOR, "#input-password")
    LOCATOR_INPUT_PASSWORD_CONFIRM = Selector(
        By.CSS_SELECTOR, "#input-confirm")

    TEXT_ACCOUNT_CREATED = "Your Account Has Been Created!"
    TEXT_PASSWORDS_MISMATCH = "Password confirmation does not match password!"
    TEXT_FIRST_NAME_ERROR = "First Name must be between 1 and 32 characters!"
    TEXT_LAST_NAME_ERROR = "Last Name must be between 1 and 32 characters!"
    TEXT_EMAIL_ERROR = "E-Mail Address does not appear to be valid!"
    TEXT_TELEPHONE_ERROR = "Telephone must be between 3 and 32 characters!"
    TEXT_PASSWORD_ERROR = "Password must be between 4 and 20 characters!"

    LOCATOR_CHECKBOX_AGREE = Selector(By.CSS_SELECTOR, "input[type=checkbox]")
    LOCATOR_BUTTON_CONTINUE = Selector(
        By.CSS_SELECTOR, ".btn.btn-primary")
    LOCATOR_ALERT_DANGER = Selector(
        By.CSS_SELECTOR, ".alert.alert-danger.alert-dismissible")
    LOCATOR_BUTTON_CLOSE_PRIVACY_POLICY = Selector(
        By.CSS_SELECTOR, "button.close")


class RegisterAccountPage(BasePage):

    locator = RegisterAccountPageLocators

    @allure.step("enter first name {fname}")
    def enter_first_name(self, fname):
        self._logger.info("enter first name %s", fname)
        self.enter_text(self.locator.LOCATOR_INPUT_FIRST_NAME, fname)

    @allure.step("enter last name {lname}")
    def enter_last_name(self, lname):
        self._logger.info("enter last name %s", lname)
        self.enter_text(self.locator.LOCATOR_INPUT_LAST_NAME, lname)

    @allure.step("enter email {email}")
    def enter_email(self, email):
        self._logger.info("enter email %s", email)
        self.enter_text(self.locator.LOCATOR_INPUT_EMAIL, email)

    @allure.step("enter phone number {telephone}")
    def enter_telephone(self, telephone):
        self._logger.info("enter phone number %s", telephone)
        self.enter_text(self.locator.LOCATOR_INPUT_TELEPHONE, telephone)

    @allure.step("enter password {password}")
    def enter_password(self, password):
        self._logger.info("enter pssword %s", password)
        self.enter_text(self.locator.LOCATOR_INPUT_PASSWORD, password)

    @allure.step("confirm password {password}")
    def enter_password_confirm(self, password):
        self._logger.info("confirm pssword %s", password)
        self.enter_text(
            self.locator.LOCATOR_INPUT_PASSWORD_CONFIRM, password)

    @allure.step("check if box 'Agree' is checked")
    def is_checked_agree(self):
        self._logger.info("check if box 'Agree' is checked")
        return self.find_element(self.locator.LOCATOR_CHECKBOX_AGREE).get_attribute('checked')

    @allure.step("check 'Agree' box")
    def check_box_agree(self):
        self._logger.info("check 'Agree' box")
        if not self.is_checked_agree():
            self.click(self.locator.LOCATOR_CHECKBOX_AGREE)

    @allure.step("uncheck 'Agree' box")
    def uncheck_box_agree(self):
        self._logger.info("uncheck 'Agree' box")
        if self.is_checked_agree():
            self.click(self.locator.LOCATOR_CHECKBOX_AGREE)

    @allure.step("click Continue button")
    def click_button_continue(self):
        self._logger.info("click Continue button")
        self.click(self.locator.LOCATOR_BUTTON_CONTINUE)

    @allure.step("click Privacy policy link")
    def click_privacy_policy(self):
        self._logger.info("click Privacy policy link")
        self.click(self.locator.LOCATOR_LINK_PRIVACY_POLICY)

    @allure.step("close Privacy policy")
    def close_privacy_policy(self):
        self._logger.info("close Privacy policy")
        self.click(self.locator.LOCATOR_BUTTON_CLOSE_PRIVACY_POLICY)

    @allure.step("fill in and submit registration form")
    def submit_form(self, data, agree=True):
        self._logger.info("fill in and submit registration form")
        self.enter_first_name(data.fname)
        self.enter_last_name(data.lname)
        self.enter_email(data.email)
        self.enter_telephone(data.phone)
        self.enter_password(data.password_1)
        self.enter_password_confirm(data.password_2)
        if agree:
            self.check_box_agree()
        self.click_button_continue()


if __name__ == '__main__':

    print(RegisterAccountPage.locator.locators)
