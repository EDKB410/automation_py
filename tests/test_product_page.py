import allure
import pytest
from pom.element.store.navbar import navbar
from pom.element.store.shopping_cart import ShoppingCartButton
from pom.element.store.thumbnails import ProductThumbnails
from pom.store.product_page import ProductPage, ProductPageLocators


@pytest.fixture(scope='class', autouse=True)
def page(request, driver, base_url) -> ProductPage:
    request.cls.driver = driver
    request.cls.url = base_url + ProductPageLocators.URL
    page = ProductPage(driver, request.cls.url)
    page.open()
    return page


@allure.feature("Customer-side scenarios")
@allure.story("Product page expirience")
class TestProductPage:

    @allure.title("select product from catalog")
    def test_select_product_from_catalog(self, page: ProductPage):

        with allure.step("go to Monitors page"):
            page.hover(navbar.components)
            page.click(navbar.components.monitors)

        with allure.step("click on the first product thumbnail"):
            tn = ProductThumbnails(self.driver, self.url)
            product = tn.get_products().pop()
            tn.click_product_link(product)
            assert 'monitor/samsung-syncmaster-941bw' in page.current_url
            assert page.at_page('Samsung SyncMaster 941BW')

    @allure.title("select product {expr} from featured")
    @pytest.mark.parametrize('index, expr', ((0, 'macbook'),
                                             (1, 'iphone'),
                                             (2, 'test'),
                                             (3, 'canon-eos-5d')))
    def test_select_product_from_featured(self, index, expr, page: ProductPage):
        tn = ProductThumbnails(self.driver)
        tn.get_product_link(
            tn.get_product(index)).click()
        assert expr in page.current_url

    @allure.title("add product to shopping cart")
    def test_add_product_to_shopping_cart(self, page: ProductPage):

        with allure.step("click on product's thumbnail"):
            tn = ProductThumbnails(self.driver)
            tn.get_product(1).click()
            assert page.at_page('iPhone')

        with allure.step("add product to shopping cart"):
            page.add_product_to_shopping_cart(1)
            assert page.get_product_price() in ShoppingCartButton(self.driver).get_total()

    @allure.title("view images of the product")
    @pytest.mark.parametrize('item', range(0, 4), ids=('MacBook', 'iPhone', 'Apple Cinema 30"', 'Canon EOS 5D'))
    def test_view_product_images(self, item, page: ProductPage):
        # https://github.com/allure-framework/allure-python/issues/512
        tn = ProductThumbnails(self.driver)
        tn.click_product_link(tn.get_product(item))
        for t in page.get_thumbnails():
            t.click()
            page.close_thumbnail_image()
