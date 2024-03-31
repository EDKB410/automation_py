import allure
from frame.base_locator import BaseLocator, Selector
from frame.base_page import BasePage
from frame.types import Currency
from selenium.webdriver.common.by import By


class ProductThumbnailsLocators(BaseLocator):

    LOCATOR_PRODUCT_THUMBNAILS = Selector(By.CSS_SELECTOR, ".product-thumb")
    LOCATOR_PRODUCT_THUMBNAIL_IMAGE = Selector(
        By.CSS_SELECTOR, ".product-thumb .image img")
    LOCATOR_PRODUCT_THUMBNAIL_HREF = Selector(
        By.CSS_SELECTOR, ".product-thumb .image a")
    LOCATOR_PRODUCT_THUMBNAIL_CAPTION_HREF = Selector(
        By.CSS_SELECTOR, ".product-thumb .caption h4 a")
    LOCATOR_PRODUCT_THUMBNAIL_CAPTION_DESCRIPTION = Selector(
        By.CSS_SELECTOR, "div.caption > p:nth-child(2)")
    LOCATOR_PRODUCT_THUMBNAIL_PRICE = Selector(
        By.CSS_SELECTOR, ".product-thumb p.price")
    LOCATOR_PRODUCT_THUMBNAIL_BUTTON_ADD_TO_CART = Selector(
        By.CSS_SELECTOR, ".button-group > button:nth-child(1)")
    LOCATOR_PRODUCT_THUMBNAIL_BUTTON_ADD_TO_WISH_LIST = Selector(
        By.CSS_SELECTOR, ".button-group > button:nth-child(2)")
    LOCATOR_PRODUCT_THUMBNAIL_BUTTON_ADD_TO_COMPARE = Selector(
        By.CSS_SELECTOR, ".button-group > button:nth-child(3)")


class ProductThumbnails(BasePage):

    locator = ProductThumbnailsLocators

    @allure.step("get thumbnails for all products")
    def get_products(self):
        self._logger.info("get thumbnails for all products")
        return self.find_elements(self.locator.LOCATOR_PRODUCT_THUMBNAILS)

    @allure.step("get {index} product's thumbnail")
    def get_product(self, index):
        self._logger.info("get %s product's thumbnail", index)
        return self.get_products()[index]

    @allure.step("extract a link to product's page from it's thumbnail")
    def get_product_link(self, product):
        self._logger.info(
            "extract a link to product's page from it's thumbnail")
        return product.find_element(*self.locator.LOCATOR_PRODUCT_THUMBNAIL_HREF)

    @allure.step("extract name from product's link")
    def get_product_name(self, product):
        self._logger.info("extract name from product's link")
        return product.find_element(*self.locator.LOCATOR_PRODUCT_THUMBNAIL_HREF).get_attribute('text')

    @allure.step("extract price value from product's thumbnail")
    def get_product_price(self, product):
        self._logger.info("extract price value from product's thumbnail")
        return product.find_element(*self.locator.LOCATOR_PRODUCT_THUMBNAIL_PRICE)

    @allure.step("extract price currency from product's thumbnail")
    def get_price_currency(self, product):
        self._logger.info("extract price currency from product's thumbnail")
        price = self.get_product_price(product)
        if price.text.startswith(Currency.USD.value):
            return Currency.USD.value.lower()
        elif price.text.endswith(Currency.EUR.value):
            return Currency.EUR.value.lower()
        elif price.text.startswith(Currency.GBP.value):
            return Currency.GBP.value.lower()

    @allure.step("extract description from product's thumbnail")
    def get_product_description(self, product):
        self._logger.info("extract description from product's thumbnail")
        return product.find_element(*self.locator.LOCATOR_PRODUCT_THUMBNAIL_CAPTION_DESCRIPTION)

    @allure.step("click on link extracted from product's thumbnail")
    def click_product_link(self, product):
        self._logger.info("click on link extracted from product's thumbnail")
        self.get_product_link(product).click()


if __name__ == '__main__':

    print(ProductThumbnails.locator.locators)
