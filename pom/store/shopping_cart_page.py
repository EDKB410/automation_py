import allure
from frame.base_locator import BaseLocator, Selector
from frame.base_page import BasePage
from selenium.webdriver.common.by import By


class ShoppingCartPageLocators(BaseLocator):

    URL = '/index.php?route=checkout/cart'

    TITLE_SHOPPING_CART_PAGE = "Shopping Cart"

    LOCATOR_BUTTON_CONTINUE = Selector(By.LINK_TEXT, "Continue")
    LOCATOR_HEADER_SHOPPING_CART = Selector(By.CSS_SELECTOR, "#content > h1")
    TEXT_SHOPPING_CART_EMPTY = 'Your shopping cart is empty!'


class ShoppingCartPage(BasePage):

    locator = ShoppingCartPageLocators

    @allure.step("click Continue button")
    def click_continue_button(self):
        self._logger.info("click Continue button")
        self.click(self.locator.LOCATOR_BUTTON_CONTINUE)

    @allure.step("check if Shopping cart is empty")
    def is_empty(self):
        self._logger.info("check if Shopping cart is empty")
        return self.locator.TEXT_SHOPPING_CART_EMPTY in self.page_src


if __name__ == '__main__':

    print(ShoppingCartPage.locator.locators)
