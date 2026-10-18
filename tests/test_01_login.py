import allure

from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from test_data.test_data import (
    VALID_USERNAME, VALID_PASSWORD,
    INVALID_CREDS
)

class TestLogin:
    # ── TC_LOGIN_001 ── Valid Credentials Login ──────────────────────
    @allure.title("TC_LOGIN_001 - Login with correct credentials")

    def test_valid_creds_login(self, login_page: LoginPage):
        with allure.step("User enter valid username and password"):
            login_page.login(VALID_USERNAME, VALID_PASSWORD)

        dashboard = DashboardPage(login_page.page)

        with allure.step("Verify user is directed to dashboard"):
            dashboard.is_loaded()
            screenshot = dashboard.page.screenshot()
            allure.attach(screenshot)

    # ── TC_LOGIN_002 ── Invalid Credentials Login ──────────────────────
    @allure.title("TC_LOGIN_002 - Login with wrong credentials")
    def test_invalid_creds_login(self, login_page: LoginPage):
        for username, password in INVALID_CREDS:
            login_page.login(username, password)
            login_page.click_login()

            with allure.step("Verify validation error is shown"):
                expect(login_page.VALIDATION_ERROR).to_be_visible()
                expect(login_page.VALIDATION_ERROR).to_contain_text("Invalid credentials")

    # ── TC_LOGIN_003 ── Missing Username Login ──────────────────────
    @allure.title("TC_LOGIN_003 - Login with missing username")
    def test_missing_username_login(self, login_page: LoginPage):
        login_page.enter_password(VALID_PASSWORD)
        login_page.click_login()

        with allure.step("Verify error message is shown"):
            expect(login_page.ERROR_MESSAGE).to_be_visible()
            expect(login_page.ERROR_MESSAGE).to_contain_text("Required")

    # ── TC_LOGIN_004 ── Missing Password Login ──────────────────────
    @allure.title("TC_LOGIN_004 - Login with missing password")
    def test_missing_password_login(self, login_page: LoginPage):
        login_page.enter_username(VALID_USERNAME)
        login_page.click_login()

        with allure.step("Verify error message is shown"):
            expect(login_page.ERROR_MESSAGE).to_be_visible()
            expect(login_page.ERROR_MESSAGE).to_contain_text("Required")

    # ── TC_LOGIN_005 ── Missing Credentials Login ──────────────────────
    @allure.title("TC_LOGIN_005 - Login with missing credentials")
    def test_missing_cred_login(self, login_page: LoginPage):
        login_page.click_login()

        with allure.step("Verify error message is shown"):
            for message in login_page.ERROR_MESSAGE.all():
                expect(message).to_be_visible()
                expect(message).to_contain_text("Required")