import allure
import pytest
from pom.element.store.common import CommonElements, CommonElementsLocators
from pom.element.store.shopping_cart import ShoppingCartButton
from pom.store.main_page import MainPage, MainPageLocators
from pom.store.shopping_cart_page import (ShoppingCartPage,
                                          ShoppingCartPageLocators)

from conftest import skip_if


@pytest.fixture(scope='class', autouse=True)
def page(request, driver, base_url) -> MainPage:
    request.cls.driver = driver
    request.cls.url = base_url + MainPageLocators.URL
    page = MainPage(driver, request.cls.url)
    page.open()
    return page

@allure.feature("Customer-side scenarios")
@allure.story("Main page expirience")
class TestMainPage:

    @allure.title("check if main page is opened")
    def test_if_at_page(self, page: MainPage):
        assert page.at_page(page.locator.TITLE_MAIN_PAGE)

    @allure.title("checkout with empty shopping cart")
    def test_checkout_with_empty_cart(self):
        common_elements = CommonElements(self.driver)
        common_elements.click_checkout()
        page = ShoppingCartPage(self.driver)
        assert page.at_page(
            ShoppingCartPageLocators.TITLE_SHOPPING_CART_PAGE)
        assert page.is_empty()
        page.click_continue_button()
        assert page.at_page(MainPageLocators.TITLE_MAIN_PAGE)

    @allure.title("click on empty shopping cart")
    def test_click_on_empty_shopping_cart(self):
        cart = ShoppingCartButton(self.driver)
        cart.click_button()
        assert cart.is_empty()

    @allure.title("click on 'Powered by' link")
    def test_click_on_powered_by(self, base_url, page: MainPage):
        CommonElements(self.driver).click_powered_by()
        assert page.at_page(CommonElementsLocators.TITLE_OPENCART_SITE)
        page.url = base_url

    @allure.title("check if Copyright is present")
    def test_copyright_should_present(self, page):
        assert CommonElementsLocators.TEXT_COPYRIGHT in page.find_element(
            CommonElementsLocators.LOCATOR_COPYRIGHT).text

    @skip_if('headless')
    @allure.title("use of slideshow on the main page")
    def test_slideshow_next_prev_click(self, page: MainPage):
        target = 'Samsung Galaxy Tab 10.1'
        page.click_slideshow_next()
        page.click_slideshow_prev()
        page.click_slideshow()
        assert page.at_page(target)
        page.back()
        assert page.at_page(MainPageLocators.TITLE_MAIN_PAGE)
        page.click_slideshow_prev()
        page.click_slideshow_next()
        page.click_slideshow()
        assert page.at_page(target)
