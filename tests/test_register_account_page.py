import pytest
from pom.element.store.account_dropdown import account_dropdown
from pom.store.register_account_page import (RegisterAccountPage,
                                             RegisterAccountPageLocators)
import allure


@pytest.fixture(scope='class', autouse=True)
def page(request, driver, base_url) -> RegisterAccountPage:
    request.cls.driver = driver
    request.cls.url = base_url + RegisterAccountPageLocators.URL
    page = RegisterAccountPage(driver, request.cls.url)
    page.open()
    return page


@allure.feature("Customer-side scenarios")
@allure.story("Customer account registration")
class TestRegisterAccountPage:

    @allure.title("Go to Register page from Main page")
    def test_go_to_register_from_main_page(self, base_url, page: RegisterAccountPage):
        page.go(base_url)
        page.click(account_dropdown)
        page.click(account_dropdown.register)
        assert page.at_page(
            RegisterAccountPageLocators.TITLE_REGISTER_ACCOUNT)

    @allure.title("Read Privacy policy")
    def test_read_privacy_policy(self, page: RegisterAccountPage):
        page.click_privacy_policy()
        page.close_privacy_policy()

    @allure.title("Check and uncheck the 'agree' checkbox")
    def test_check_agree(self, page: RegisterAccountPage):
        page.check_box_agree()
        assert page.is_checked_agree()
        page.uncheck_box_agree()
        assert not page.is_checked_agree()

    @allure.title("Register account with valid data")
    def test_submit_form_valid_data(self, page: RegisterAccountPage, account_valid, db_delete_customer_valid):

        with allure.step("submit registration form"):
            page.submit_form(account_valid)
            assert 'Your Account Has Been Created!' in page.page_src

        with allure.step("do logout"):
            page.click(account_dropdown)
            page.click(account_dropdown.logout)

    @allure.title("Try to register account for existent customer")
    def test_submit_form_duplicate_data(self, page: RegisterAccountPage, account_valid, db_customer_valid):
        page.submit_form(account_valid)
        assert page.does_present(page.locator.LOCATOR_ALERT_DANGER)

    @allure.title("Register customer with random data")
    def test_submit_form_random_data(self, page: RegisterAccountPage, account_random, db_delete_customer_random):

        with allure.step("submit registration form"):
            account_random.password_2 = account_random.password_1
            page.submit_form(account_random)
            assert 'Your Account Has Been Created!' in page.page_src

        with allure.step("do logout"):
            page.click(account_dropdown)
            page.click(account_dropdown.logout)

    @allure.title("Try to submit registration form with 'privacy policy' checkbox unchecked")
    def test_submit_form_privacy_policy_unchecked(self, page: RegisterAccountPage, account_random):
        account_random.password_2 = account_random.password_1
        page.submit_form(account_random, agree=False)
        assert page.does_present(page.locator.LOCATOR_ALERT_DANGER)

    @allure.title("Try to register account with errors in the registration form")
    @pytest.mark.parametrize('field, expected', (('fname', RegisterAccountPageLocators.TEXT_FIRST_NAME_ERROR),
                                                 ('lname', RegisterAccountPageLocators.TEXT_LAST_NAME_ERROR),
                                                 ('email', RegisterAccountPageLocators.TEXT_EMAIL_ERROR),
                                                 ('phone', RegisterAccountPageLocators.TEXT_TELEPHONE_ERROR),
                                                 ('password_1', RegisterAccountPageLocators.TEXT_PASSWORD_ERROR)))
    def test_try_register_account_with_errors(self, page: RegisterAccountPage, account_random, field, expected):
        setattr(account_random, field, '')
        page.submit_form(account_random)
        assert expected in page.page_src

    @allure.title("Try to register account with mismatched passwords in the form")
    def test_register_passwords_mismatch(self, page: RegisterAccountPage, account_random):
        account_random.password_2 = ''
        page.submit_form(account_random)
        assert page.locator.TEXT_PASSWORDS_MISMATCH in page.page_src
