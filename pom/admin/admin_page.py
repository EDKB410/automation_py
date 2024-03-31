import allure
from frame.base_locator import BaseLocator, Selector
from frame.base_page import BasePage
from frame.node import Node
from selenium.webdriver.common.by import By


class AdminPageLocators(BaseLocator):

    LOCATOR_ADD = Selector(By.CSS_SELECTOR, "a[data-original-title='Add New']")
    LOCATOR_COPY = Selector(
        By.CSS_SELECTOR, "button[data-original-title='Copy'")
    LOCATOR_DELETE = Selector(
        By.CSS_SELECTOR, "button[data-original-title='Delete']")
    LOCATOR_SAVE = Selector(
        By.CSS_SELECTOR, "button[data-original-title='Save']")
    LOCATOR_CANCEL = Selector(
        By.CSS_SELECTOR, "a[data-original-title='Cancel']")
    LOCATOR_ALERT_DANGER_MESSAGE = Selector(
        By.CSS_SELECTOR, "div.alert.alert-danger.alert-dismissible")
    LOCATOR_ALERT_SUCCESS_MESSAGE = Selector(
        By.CSS_SELECTOR, "div.alert.alert-success.alert-dismissible")
    LOCATOR_BUTTON_ALERT_CLOSE = Selector(By.CSS_SELECTOR, "button.close")

    class tabs(Node):
        general = (By.LINK_TEXT, 'General')
        data = (By.LINK_TEXT, 'Data')
        links = (By.LINK_TEXT, 'Links')
        attribute = (By.LINK_TEXT, 'Attribute')
        option = (By.LINK_TEXT, 'Option')
        recurring = (By.LINK_TEXT, 'Recurring')
        discount = (By.LINK_TEXT, 'Discount')
        special = (By.LINK_TEXT, 'Special')
        image = (By.LINK_TEXT, 'Image')
        reward_points = (By.LINK_TEXT, 'Reward Points')
        seo = (By.LINK_TEXT, 'SEO')
        design = (By.LINK_TEXT, 'Design')


class AdminPage(BasePage):

    locator = AdminPageLocators

    @allure.step("click Add button")
    def click_add(self):
        self._logger.info("click Add button")
        self.click(self.locator.LOCATOR_ADD)

    @allure.step("click Copy button")
    def click_copy(self):
        self._logger.info("click Copy button")
        self.click(self.locator.LOCATOR_COPY)

    @allure.step("click Delete button")
    def click_delete(self):
        self._logger.info("click Delete button")
        self.click(self.locator.LOCATOR_DELETE)

    @allure.step("click Save button")
    def click_save(self):
        self._logger.info("click Save button")
        self.click(self.locator.LOCATOR_SAVE)

    @allure.step("switch to tab {tab}")
    def click_tab(self, tab):
        self._logger.info("switch to tab %s", tab)
        self.click(self.locator.tabs.get_item_by_name(tab.lower()))

    @allure.step("check if danger alert is present")
    def does_present_alert_danger(self):
        self._logger.info("check if danger alert is present")
        return self.does_present(self.locator.LOCATOR_ALERT_DANGER_MESSAGE)

    @allure.step("check if danger alert is not present")
    def does_not_present_alert_danger(self):
        self._logger.info("check if danger alert is not present")
        return self.does_not_present(self.locator.LOCATOR_ALERT_DANGER_MESSAGE)

    @allure.step("check if success alert is present")
    def does_present_alert_success(self):
        self._logger.info("check if success alert is present")
        return self.does_present(self.locator.LOCATOR_ALERT_SUCCESS_MESSAGE)

    @allure.step("check if alert success is not present")
    def does_not_present_alert_success(self):
        self._logger.info("check if success alert is not present")
        return self.does_not_present(self.locator.LOCATOR_ALERT_SUCCESS_MESSAGE)

    @allure.step("close alert")
    def close_alert(self):
        self._logger.info("close alert")
        self.click(self.locator.LOCATOR_BUTTON_ALERT_CLOSE)
