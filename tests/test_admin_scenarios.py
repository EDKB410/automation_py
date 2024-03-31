from pom.admin.admin_page import AdminPage
from pom.admin.login_page import AdminLoginPage, AdminLoginPageLocators
from pom.admin.product_page import AdminProductPage
from pom.element.admin.common import AdminCommonElements
from pom.element.admin.navigation import navigation

from tests.conftest import ProductData
import time
import allure

@allure.feature("Admin-side scenarios")
@allure.story("Managing products")
class TestAdminScenarios:

    @allure.title("add a new product")
    def test_add_product(self, driver, base_url, account_admin_valid, product_random: ProductData, db_delete_product):
        
        with allure.step("do login"):
            AdminLoginPage(driver, base_url + AdminLoginPageLocators.URL,
                        open=True).admin_login_with(*account_admin_valid)
        
        with allure.step("go to product list and click Add button"):
            admin_page = AdminPage(driver)
            product_page = AdminProductPage(driver)
            admin_page.click(navigation.catalog)
            admin_page.click(navigation.catalog.products)
            admin_page.click_add()

        with allure.step("switch to 'General' tab and fill in the data"):
            admin_page.click_tab('General')
            product_page.set_product_name(product_random.name)
            product_page.set_product_description(product_random.description)
            product_page.set_meta_tag_title(product_random.name)

        with allure.step("switch to 'Data' tab and fill in the data"):
            admin_page.click_tab('Data')
            product_page.set_product_model(product_random.name)
            product_page.set_product_price(product_random.price)
            product_page.set_product_quantity(product_random.quantity)

        with allure.step("switch to 'Links' tab and select the product category"):
            admin_page.click_tab('Links')
            product_page.set_product_category(
                product_random.categories.capitalize())

        with allure.step("save new product"):
            admin_page.click_save()
            assert admin_page.does_present_alert_success()
            admin_page.close_alert()
        
        with allure.step("do logout"):
            AdminCommonElements(driver).click_logout()

    @allure.title("delete product")
    def test_delete_product(self, driver, base_url, account_admin_valid, db_product_random):
        with allure.step(f"do login with {account_admin_valid}"):
            AdminLoginPage(driver, base_url +  AdminLoginPageLocators.URL,
                        open=True).admin_login_with(*account_admin_valid)
        
        with allure.step("go to product list"):
            admin_page = AdminPage(driver)
            product_page = AdminProductPage(driver)

            admin_page.click(navigation.catalog)
            admin_page.click(navigation.catalog.products)

        with allure.step("select products with models as 'test_'"):
            product_page.set_filter_model('test_')
            product_page.click_filter()
            products = product_page.get_products()

        with allure.step("delete all selected products"):
            if products:
                for p in products:
                    product_page.select_product(p)
                admin_page.click_delete()
                if admin_page.does_alert_present():
                    admin_page.alert_accept()
                assert admin_page.does_present_alert_success()
                admin_page.close_alert()

        with allure.step("do logout"):
            AdminCommonElements(driver).click_logout()
