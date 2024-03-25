from selenium.webdriver.common.by import By
from frame.base_locator import Selector, BaseLocator
from frame.base_page import BasePage


class ComparisionPageLocators(BaseLocator):

    URL = '/index.php?route=product/compare'

    URL_COMPARISION_PAGE = URL

    TITLE_COMPARISION_PAGE = "Search"
    LOCATOR_HEADER_COMPARISION_PAGE = Selector(
        By.CSS_SELECTOR, "#content > h1")


class ComparisionPage(BasePage):

    locator = ComparisionPageLocators


if __name__ == '__main__':

    print(ComparisionPage.locator.locators)
