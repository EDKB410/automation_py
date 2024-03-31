import pytest
from pom.element.store.search_string import SearchString
from pom.store.main_page import MainPage, MainPageLocators
from pom.store.search_page import SearchPageLocators
import allure


@pytest.fixture(scope='class', autouse=True)
def page(request, driver, base_url) -> MainPage:
    request.cls.driver = driver
    request.cls.url = base_url + MainPageLocators.URL
    page = MainPage(driver, request.cls.url)
    page.open()
    return page

@allure.feature("Customer-side scenarios")
@allure.story("Search a product")
class TestSearchFromMainPage:

    @allure.title("check if main page opened")
    def test_if_at_page(self, page: MainPage):
        page.go(page.url)
        assert page.at_page(MainPageLocators.TITLE_MAIN_PAGE)

    @allure.title("click Search button with no text entered")
    def test_click_search_button_no_text(self, page: MainPage):
        page.click(SearchString.locator.LOCATOR_BUTTON_SEARCH)
        assert page.at_page(SearchPageLocators.TITLE_SEARCH_PAGE)
        assert SearchPageLocators.LOCATOR_TEXT_SEARCH_FAIL in page.page_src

    @pytest.mark.parametrize('text, fail', (('iphone', False), ('huawey', True)), ids=('success', 'fail'))
    @allure.title("search product by {text} text")
    def test_search_product(self, text, fail, page: MainPage):
        SearchString(self.driver, self.url).do_search(text)
        assert page.at_page(f"Search - {text}")
        if fail:
            assert SearchPageLocators.LOCATOR_TEXT_SEARCH_FAIL in page.page_src
        else:
            assert SearchPageLocators.LOCATOR_TEXT_SEARCH_FAIL not in page.page_src
