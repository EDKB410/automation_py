from frame.base_locator import BaseLocator
from frame.base_page import BasePage


class SearchPageLocators(BaseLocator):

    URL = '/index.php?route=product/search'

    URL_SEARCH_PAGE = URL

    TITLE_SEARCH_PAGE = "Search"

    LOCATOR_TEXT_SEARCH_FAIL = "There is no product that matches the search criteria."


class SearchPage(BasePage):

    locator = SearchPageLocators


if __name__ == '__main__':

    print(SearchPage.locator.locators)
