from collections import namedtuple

import allure
import pytest
from frame.utils import Utils
from pom.element.store.breadcrumb import Breadcrumb
from pom.element.store.navbar import navbar
from pom.element.store.product import product
from pom.element.store.thumbnails import ProductThumbnails
from pom.store.catalog_page import CatalogPage
from pom.store.main_page import MainPageLocators


@pytest.fixture(scope='class', autouse=True)
def page(request, driver, base_url) -> CatalogPage:
    request.cls.driver = driver
    request.cls.url = base_url + '/tablet'
    page = CatalogPage(driver, request.cls.url)
    page.open()
    return page


@allure.feature("Customer-side scenarios")
@allure.story("Catalog page expirience")
class TestCatalogPage:

    @allure.title("check if catalog page opened")
    def test_if_at_page(self, page: CatalogPage):
        assert page.at_page('Tablets')

    @allure.title("go to {title} with navbar")
    @pytest.mark.parametrize('item, title', ((navbar.desktops.pc, 'PC'),
                                             (navbar.desktops.mac, 'Mac'),
                                             (navbar.desktops.all, 'Desktops')))
    def test_navbar_with_subcats(self, item, title, page: CatalogPage):
        page.hover(navbar.desktops)
        page.click(item)
        assert page.at_page(title)

    @allure.title("use navbar")
    @pytest.mark.parametrize('p, l', [(p, l) for p in navbar.items for l in [p, *p.items]], ids=lambda x: navbar.item_name(x))
    def test_navbar(self, page: CatalogPage, p, l):
        allure.dynamic.title(
            f"with navbar go to {navbar.item_name(p)} / {navbar.item_name(l)}")
        page.click(p)
        page.click(l)

    @allure.title("use menu")
    @pytest.mark.parametrize('p, l', [(p, l) for p in product.items for l in [p, *p.items]], ids=lambda x: product.item_name(x))
    def test_menu(self, page: CatalogPage, p, l):
        allure.dynamic.title(
            f"with menu go to {product.item_name(p)} / {product.item_name(l)}")
        page.click(p)
        page.click(l)

    @allure.title("go to home page using breadcrumb")
    def test_breadcrumb_go_home(self, page: CatalogPage):
        assert page.at_page('Tablets')
        Breadcrumb(self.driver).go_home()
        assert page.at_page(MainPageLocators.TITLE_MAIN_PAGE)

    @allure.title("walking using breadcrumb")
    def test_breadcrumb_walk(self, page: CatalogPage):
        assert page.at_page('Tablets')
        page.click(product.components)
        page.click(product.components.monitors)
        assert page.at_page('Monitors')
        bc = Breadcrumb(self.driver)
        while not page.at_page(MainPageLocators.TITLE_MAIN_PAGE):
            bc.back()
        assert page.at_page(MainPageLocators.TITLE_MAIN_PAGE)

    @allure.title("products list view")
    def test_view_list(self, page: CatalogPage):
        page.click(product.cameras)
        page.click_button_view_list()
        assert len(page.get_view_list_elements())

    @allure.title("products grid view")
    def test_view_grid(self, page: CatalogPage):
        page.click(product.cameras)
        page.click_button_view_grid()
        assert len(page.get_view_grid_elements())

    @allure.title("sort products by {selected}")
    @pytest.mark.parametrize('selected', (CatalogPage.select_sort_options.keys()))
    def test_select_sort(self, selected, page: CatalogPage):
        page.select_sort_set_by_text(selected)
        assert page.get_sort_selected_option().text == selected

    @allure.title("show {selected} products per page")
    @pytest.mark.parametrize('selected', (CatalogPage.select_show_options.keys()))
    def test_select_show(self, selected, page: CatalogPage):
        page.select_show_set_by_text(selected)
        assert page.get_show_selected_option().text == selected

    def select_sort_data():
        options = {'Default': 'Canon',
                   'Name (A - Z)': 'Canon',
                   'Name (Z - A)': 'Nikon',
                   'Price (Low > High)': 'Canon',
                   'Price (High > Low)': 'Nikon',
                   'Rating (Highest)': 'Nikon',
                   'Rating (Lowest)': 'Canon',
                   'Model (A - Z)': 'Canon',
                   'Model (Z - A)': 'Nikon'
                   }
        Option = namedtuple('Option', ('text', 'value'))
        return [Option(*item) for item in options.items()]

    @allure.title("test sorting modes")
    @pytest.mark.parametrize('selected', (select_sort_data()), ids=lambda v: v.text)
    def test_select_sort_cameras(self, selected, page: CatalogPage):
        allure.dynamic.title(f"sorted by {selected.text}")
        page.click(product.cameras)
        page.select_sort_set_by_text(selected.text)
        assert page.get_sort_selected_option().text == selected.text
        assert selected.value in ProductThumbnails(
            self.driver).get_products().pop(0).text
