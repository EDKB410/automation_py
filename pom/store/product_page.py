import allure
from frame.base_locator import BaseLocator, Selector
from frame.base_page import BasePage
from selenium.webdriver.common.by import By


class ProductPageLocators(BaseLocator):

    URL = ''

    URL_PRODUCT_PAGE = URL

    TITLE_PRODUCT_PAGE = ''

    LOCATOR_PRICE = Selector(
        By.CSS_SELECTOR, "ul:nth-child(4) > li:nth-child(1) > h2")
    LOCATOR_INPUT_QUANTITY = Selector(By.ID, "input-quantity")
    LOCATOR_BUTTON_ADD_TO_CART = Selector(By.ID, "button-cart")
    LOCATOR_THUMBNAILS_UL = Selector(By.CSS_SELECTOR, "ul.thumbnails")
    LOCATOR_THUMBNAILS_LI = Selector(
        By.CSS_SELECTOR, "ul.thumbnails > li> a.thumbnail")
    LOCATOR_THUMBNAILS_BUTTON_CLOSE = Selector(
        By.CSS_SELECTOR, "button.mfp-close")


class ProductPage(BasePage):

    locator = ProductPageLocators

    @allure.step("get product price")
    def get_product_price(self):
        self._logger.info("get product price")
        return self.find_element(self.locator.LOCATOR_PRICE).text

    @allure.step("add product to shopping cart")
    def add_product_to_shopping_cart(self, quantity=0):
        self._logger.info("add product to shopping cart")
        input = self.find_element(
            self.locator.LOCATOR_INPUT_QUANTITY)
        input.clear()
        input.send_keys(quantity)
        self.click(self.locator.LOCATOR_BUTTON_ADD_TO_CART)

    @allure.step("get product's thumbnails (images)")
    def get_thumbnails(self):
        self._logger.info("get product's thumbnails (images)")
        return self.find_elements(self.locator.LOCATOR_THUMBNAILS_LI)

    @allure.step("click {index} product thumbnail")
    def click_thumbnail(self, index):
        self._logger.info("click %s product thumbnail", index)
        self.get_thumbnails()[index].click()

    @allure.step("close product thumbnail (image)")
    def close_thumbnail_image(self):
        self._logger.info("close product thumbnail (image)")
        self.click(self.locator.LOCATOR_THUMBNAILS_BUTTON_CLOSE)


if __name__ == '__main__':

    print(ProductPage.locator.locators)
