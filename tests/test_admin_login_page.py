import allure
import pytest
from pom.admin.login_page import AdminLoginPage, AdminLoginPageLocators


@pytest.fixture(scope='class', autouse=True)
def page(request, driver, base_url):
    request.cls.driver = driver
    request.cls.url = base_url + AdminLoginPageLocators.URL
    page = AdminLoginPage(driver, request.cls.url)
    page.open()
    return page


@allure.feature("Admin-side scenarios")
@allure.story("Admin login page expirience")
class TestAdminLoginPage:

    @allure.title("check if login page is accessible")
    def test_if_at_page(self, page):
        assert page.at_page(AdminLoginPageLocators.TITLE_ADMIN_LOGIN_PAGE)

    @pytest.mark.parametrize('login,password,expected', (('user', 'bitnami', AdminLoginPageLocators.TITLE_ADMIN_PAGE),
                                                         ('user', 'bitnomi', AdminLoginPageLocators.TITLE_ADMIN_LOGIN_PAGE)),
                             ids=('SUCCESS', 'FAIL'))
    @allure.title("login with login {login} and password {password}")
    def test_admin_login(self, login, password, expected, page: AdminLoginPage):
        assert page.at_page(AdminLoginPageLocators.TITLE_ADMIN_LOGIN_PAGE)
        page.admin_login_with(login, password)
        assert page.at_page(expected)

    @allure.title("successfull admin login with {valid_creds}")
    def test_admin_login_successful(self, valid_creds, page: AdminLoginPage):
        assert page.at_page(AdminLoginPageLocators.TITLE_ADMIN_LOGIN_PAGE)
        page.admin_login_with(*valid_creds)
        assert page.at_page(AdminLoginPageLocators.TITLE_ADMIN_PAGE)

    @allure.title("failed admin login with {invalid_creds}")
    def test_admin_login_failed(self, invalid_creds, page: AdminLoginPage):

        with allure.step(f"login with {invalid_creds}"):
            assert page.at_page(AdminLoginPageLocators.TITLE_ADMIN_LOGIN_PAGE)
            page.admin_login_with(*invalid_creds)
            assert page.at_page(AdminLoginPageLocators.TITLE_ADMIN_LOGIN_PAGE)

        with allure.step("close raised alert"):
            assert page.does_present_alert_danger()
            page.close_alert()
            assert page.does_not_present_alert_danger()

    @allure.title("cancel to reset admin's password")
    def test_admin_reset_password_cancel(self, page: AdminLoginPage):

        with allure.step("go to reset forgotten password page"):
            assert page.at_page(AdminLoginPageLocators.TITLE_ADMIN_LOGIN_PAGE)
            page.click_forgotten_password_link()
            assert page.at_page(
                AdminLoginPageLocators.TITLE_FORGOTTEN_PASSWORD_PAGE)

        with allure.step("cancel to reset password"):
            page.click_forgotten_password_cancel_button()
            assert page.at_page(AdminLoginPageLocators.TITLE_ADMIN_LOGIN_PAGE)

    @allure.title("submit incorrect email while reset admin's password")
    def test_admin_reset_password_submit_invalid_email(self, page: AdminLoginPage):

        with allure.step("go to reset forgotten password page"):
            assert page.at_page(AdminLoginPageLocators.TITLE_ADMIN_LOGIN_PAGE)
            page.click_forgotten_password_link()
            assert page.at_page(
                AdminLoginPageLocators.TITLE_FORGOTTEN_PASSWORD_PAGE)

        with allure.step("submit incorrect email"):
            page.enter_email('user@otus.ru')
            page.click_forgotten_password_reset_button()
            assert page.at_page(
                AdminLoginPageLocators.TITLE_FORGOTTEN_PASSWORD_PAGE)
        
        with allure.step("handle danger alert"):
            assert page.does_present_alert_danger()
            page.close_alert()
        
        with allure.step("cancel to reset password"):
            page.click_forgotten_password_cancel_button()

    @allure.title("reset admin's password")
    def test_admin_reset_password_submit_valid_email(self, page: AdminLoginPage):
        
        with allure.step("go to reset forgotten password page"):
            assert page.at_page(AdminLoginPageLocators.TITLE_ADMIN_LOGIN_PAGE)
            page.click_forgotten_password_link()
            assert page.at_page(
                AdminLoginPageLocators.TITLE_FORGOTTEN_PASSWORD_PAGE)
        
        with allure.step("submit correct admin's email"):
            page.enter_email('user@example.com')
            page.click_forgotten_password_reset_button()
            assert page.at_page(AdminLoginPageLocators.TITLE_ADMIN_LOGIN_PAGE)
        
        with allure.step("handle successfull alert"):
            assert page.does_present_alert_success()
            page.close_alert()
            assert page.does_not_present_alert_success()
