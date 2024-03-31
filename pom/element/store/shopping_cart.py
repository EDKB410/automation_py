import allure
from frame.base_locator import BaseLocator, Selector
from frame.base_page import BasePage
from selenium.webdriver.common.by import By


class ShoppingCartButtonLocators(BaseLocator):

    LOCATOR_BUTTON_SHOPPING_CART = Selector(
        By.CSS_SELECTOR, "#cart > button")
    LOCATOR_TEXT_SHOPPING_CART_EMPTY = Selector(
        By.CSS_SELECTOR, "#cart > ul > li > p")
    LOCATOR_TEXT_SHOPPING_CART_NOT_EMPTY = Selector(
        By.CSS_SELECTOR, "#cart-total")


class ShoppingCartButton(BasePage):

    locator = ShoppingCartButtonLocators

    @allure.step("click Shopping cart button")
    def click_button(self):
        self._logger.info("click Shopping cart button")
        return self.click(self.locator.LOCATOR_BUTTON_SHOPPING_CART)

    @allure.step("get total for Shopping cart")
    def get_total(self):
        self._logger.info("get total Shopping cart")
        return self.find_element(self.locator.LOCATOR_TEXT_SHOPPING_CART_NOT_EMPTY).text

    @allure.step("check if Shopping cart is empty")
    def is_empty(self):
        self._logger.info("check if Shopping cart is empty")
        return self.find_element(self.locator.LOCATOR_TEXT_SHOPPING_CART_EMPTY)

    @allure.step("check if Shopping cart is not empty")
    def is_not_empty(self):
        self._logger.info("check if Shopping cart is not empty")
        return self.find_element(self.locator.LOCATOR_TEXT_SHOPPING_CART_NOT_EMPTY)
