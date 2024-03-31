import allure
from frame.base_locator import BaseLocator
from frame.base_page import BasePage
from frame.node import Node
from selenium.webdriver.common.by import By


class AdminProductPageLocators(BaseLocator):

    class product(Node):

        name = (By.CSS_SELECTOR, "#form-product > * #input-name1")
        description = (By.CSS_SELECTOR, "#form-product > * div.note-editable")
        meta_tag_title = (
            By.CSS_SELECTOR, "#form-product > * #input-meta-title1")
        model = (By.CSS_SELECTOR, "#form-product > * #input-model")
        price = (By.CSS_SELECTOR, "#form-product > * #input-price")
        quantity = (By.CSS_SELECTOR, "#form-product > * #input-quantity")
        manufacturer = (By.CSS_SELECTOR,
                        "#form-product > * #input-manufacturer")
        categories = (By.CSS_SELECTOR, "#form-product > * #input-category")

    class filter(Node):

        name = (By.CSS_SELECTOR, "#filter-product > * #input-name")
        model = (By.CSS_SELECTOR, "#filter-product > * #input-model")
        price = (By.CSS_SELECTOR, "#filter-product > * #input-price")
        quantity = (By.CSS_SELECTOR, "#filter-product > * input-quantity")
        status = (By.CSS_SELECTOR, "#filter-product > * input-status")
        button = (By.CSS_SELECTOR, "#filter-product > * #button-filter")

    class product_row(Node):

        self = (By.CSS_SELECTOR, "#form-product > * table > tbody > tr")
        checkbox = (
            By.CSS_SELECTOR, "#form-product > * table > tbody > tr > td > input[type='checkbox']")
        name = (By.CSS_SELECTOR,
                "#form-product > div > table > tbody > tr > td:nth-child(2)")
        no_result = (By.CSS_SELECTOR,
                     "#form-product > * table > tbody  > tr > td[colspan='8']")


class AdminProductPage(BasePage):

    locator = AdminProductPageLocators

    @allure.step("set product name as {name}")
    def set_product_name(self, name):
        self._logger.info("set product name as %s", name)
        self.enter_text(self.locator.product.name, name)

    @allure.step("set product description as {description}")
    def set_product_description(self, description):
        self._logger.info("set product description as %s", description)
        self.enter_text(self.locator.product.description, description)

    @allure.step("set product meta tag title as {tag}")
    def set_meta_tag_title(self, tag):
        self._logger.info("set product meta tag title as %s", tag)
        self.enter_text(self.locator.product.meta_tag_title, tag)

    @allure.step("set product model as {model}")
    def set_product_model(self, model):
        self._logger.info("set product model as %s", model)
        self.enter_text(self.locator.product.model, model)

    @allure.step("set product price as {price}")
    def set_product_price(self, price):
        self._logger.info("set product price as %s", price)
        self.enter_text(self.locator.product.price, price)

    @allure.step("set product quantity as {quantity}")
    def set_product_quantity(self, quantity):
        self._logger.info("set product quantity as %s", quantity)
        self.enter_text(self.locator.product.quantity, quantity)

    @allure.step("set product category as {category}")
    def set_product_category(self, category):
        self._logger.info("set product category as %s", category)
        self.enter_text_with_dropdown(
            self.locator.product.categories, category)

    @allure.step("set product manufacturer as {manufacturer}")
    def set_product_manufacturer(self, manufacturer):
        self._logger.info("set product manufacturer as %s", manufacturer)
        self.enter_text_with_dropdown(
            self.locator.product.manufacturer, manufacturer)

    @allure.step("set name as {name} in Filter form")
    def set_filter_name(self, name):
        self._logger.info("set name as %s in Filter form", name)
        self.enter_text(self.locator.filter.name, name)

    @allure.step("set model as {model} in Filter form")
    def set_filter_model(self, model):
        self._logger.info("set model as %s in Filter form", model)
        self.enter_text(self.locator.filter.model, model)

    @allure.step("set price as {price} in Filter form")
    def set_filter_price(self, price):
        self._logger.info("set price as %s in Filter form", price)
        self.enter_text(self.locator.filter.model, price)

    @allure.step("set quantity as {quantity} in Filter form")
    def set_filter_quantity(self, quantity):
        self._logger.info("set quantity as %s in Filter form", quantity)
        self.enter_text(self.locator.filter.model, quantity)

    def set_filter_status(self, status):
        # TBD
        pass

    @allure.step("click Filter button")
    def click_filter(self):
        self._logger.info("click Filter button")
        self.click(self.locator.filter.button)

    @allure.step("get all products from list")
    def get_products(self):
        self._logger.info("get all products from list")
        if self.does_not_present(self.locator.product_row.no_result):
            return self.find_elements(self.locator.product_row.self)

    @allure.step("get product name")
    def get_product_name(self, product):
        self._logger.info("get product name")
        return product.find_element(*self.locator.product_row.name).text

    @allure.step("check if product selected")
    def is_product_selected(self, product):
        self._logger.info("check if product selected")
        return product.find_element(*self.locator.product_row.checkbox).get_attribute('checked')

    @allure.step("select product")
    def select_product(self, product):
        self._logger.info("select product")
        if not self.is_product_selected(product):
            product.find_element(*self.locator.product_row.checkbox).click()

    @allure.step("unselect product")
    def unselect_product(self, product):
        self._logger.info("unselect product")
        if self.is_product_selected(product):
            product.find_element(*self.locator.product_row.checkbox).click()
