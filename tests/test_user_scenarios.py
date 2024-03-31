import allure
import pytest
from frame.types import Currency
from pom.element.store.account import account
from pom.element.store.account_dropdown import account_dropdown
from pom.element.store.currency import currency
from pom.element.store.navbar import navbar
from pom.element.store.thumbnails import ProductThumbnails
from pom.store.account_login_page import AccountLoginPage
from pom.store.account_page import AccountPage, AccountPageLocators
from pom.store.main_page import MainPage, MainPageLocators
from pom.store.register_account_page import (RegisterAccountPage,
                                             RegisterAccountPageLocators)

from tests.conftest import AccountData


@allure.feature("Customer-side scenarios")
@allure.story("Customer expiriense with UI")
class TestUserScenarios:

    @allure.title("User changes currency")
    @pytest.mark.parametrize('cur', (c.name for c in Currency))
    def test_change_currency(self, driver, base_url, cur):

        with allure.step(f"set currency on main page to {cur}"):
            page = MainPage(driver, base_url + MainPageLocators.URL)
            page.open()
            page.click(currency.button)
            page.click(getattr(currency, cur.lower()))
            assert page.find_element(
                currency.selected).text == Currency[cur].value

        with allure.step(f"check if currency of a product price is {cur}"):
            page.click(navbar.tablets)
            assert page.at_page('Tablets')
            tn = ProductThumbnails(driver)
            assert tn.get_price_currency(
                tn.get_product(0)) == Currency[cur].value

    @allure.title("Register a new customer account")
    def test_register_user_account(self, driver, base_url, account_random: AccountData, db_delete_customer_random):

        with allure.step("got to Register Account page"):
            page = RegisterAccountPage(driver, base_url + RegisterAccountPageLocators.URL)
            page.open()

        with allure.step(f"submit new account data at {page.title}"):
            account_random.password_2 = account_random.password_1  # valid input
            page.submit_form(account_random, agree=True)

        with allure.step(f"redirect to account page and logout"):
            assert page.at_page(
                RegisterAccountPageLocators.TEXT_ACCOUNT_CREATED)
            page.click(account.logout)
            AccountPage(driver).click_continue()
            assert page.at_page(MainPageLocators.TITLE_MAIN_PAGE)

    @allure.title("Test a valid customer login and logout")
    def test_user_login_and_logout(self, driver, base_url, account_valid: AccountData, db_customer_valid):

        with allure.step("login from main page"):
            page = MainPage(driver, base_url + MainPageLocators.URL)
            page.open()
            page.click(account_dropdown)
            page.click(account_dropdown.login)
            AccountLoginPage(driver).login_with(
                account_valid.email, account_valid.password_1)

        with allure.step("redirect to account page and logout from there"):
            assert page.at_page(AccountPageLocators.TITLE)
            page.click(account_dropdown)
            page.click(account_dropdown.logout)
            AccountPage(driver).click_continue()
            assert page.at_page(MainPageLocators.TITLE_MAIN_PAGE)
