from playwright.sync_api import Page
import allure

class LoginPage():
    def __init__(self, page: Page):
        self.page = page
        self.USERNAME_FIELD = page.locator("input[name='username']")
        self.PASSWORD_INPUT = page.locator("input[name='password']")
        self.LOGIN_BUTTON = page.locator("button[type='submit']")
        self.ERROR_MESSAGE = page.locator(".oxd-input-field-error-message")
        self.VALIDATION_ERROR = page.locator(".oxd-alert-content-text")
        self.FORGOT_PASSWORD = page.locator("//p[text()='Forgot your password? ']")
        self.LOGO = page.locator(".orangehrm-login-logo")
        self.PAGE_TITLE = page.locator(".orangehrm-login-title")
    
    @allure.step("Open login page")
    def go_to(self, base_url: str):
        self.page.goto(f"{base_url}/web/index.php/auth/login")

    @allure.step("Enter username")
    def enter_username(self, username: str):
        self.USERNAME_FIELD.fill(username)
    
    @allure.step("Enter password")
    def enter_password(self, password: str):
       self.PASSWORD_INPUT.fill(password)

    @allure.step("Click Login button")
    def click_login(self):
        self.LOGIN_BUTTON.click()

    @allure.step("Login with username='{username}' and password='{password}'")
    def login(self, username: str, password: str):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
