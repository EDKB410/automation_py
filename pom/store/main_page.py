import allure
from frame.base_locator import BaseLocator, Selector
from frame.base_page import BasePage
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


class MainPageLocators(BaseLocator):

    URL = ''

    URL_MAIN_PAGE = URL
    TITLE_MAIN_PAGE = "Your Store"
    LOCATOR_SLIDESHOW = Selector(By.CSS_SELECTOR, "#slideshow0")
    LOCATOR_SLIDESHOW_NEXT = Selector(
        By.CSS_SELECTOR, ".slideshow .swiper-button-next")
    LOCATOR_SLIDESHOW_PREV = Selector(
        By.CSS_SELECTOR, ".slideshow .swiper-button-prev")
    LOCATOR_FEATURED = Selector(By.CSS_SELECTOR, "h3")
    LOCATOR_CAROUSEL = Selector(By.CSS_SELECTOR, "#carousel0")


class MainPage(BasePage):

    locator = MainPageLocators

    @allure.step("click slideshow Next >")
    def click_slideshow_next(self):
        self._logger.info("click slideshow Next >")
        self.hover(self.locator.LOCATOR_SLIDESHOW)
        el = self.is_clickable(self.locator.LOCATOR_SLIDESHOW_NEXT)
        self.actions.move_to_element(el).pause(0.2).click(el).perform()

    @allure.step("click slideshow < Prev")
    def click_slideshow_prev(self):
        self._logger.info("click slideshow < Prev")
        self.hover(self.locator.LOCATOR_SLIDESHOW)
        el = self.is_clickable(self.locator.LOCATOR_SLIDESHOW_PREV)
        self.actions.move_to_element(el).pause(0.2).click(el).perform()

    @allure.step("click on slideshow")
    def click_slideshow(self):
        self._logger.info("click on slideshow")
        self.hover(self.locator.LOCATOR_SLIDESHOW)
        el = self.is_clickable(self.locator.LOCATOR_SLIDESHOW)
        self.actions.move_to_element(el).pause(0.2).click(el).perform()


if __name__ == '__main__':

    print(MainPage.locator.locators)
