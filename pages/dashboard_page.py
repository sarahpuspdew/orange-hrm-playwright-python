import re
import allure

from playwright.sync_api import Page, expect

class DashboardPage:
    def __init__(self, page: Page):
        self.page = page
        self.DASHBOARD_HEADER = self.page.locator("//h6[text()='Dashboard']")

    @allure.step("Verify dashboard page is loaded")
    def is_loaded(self):
        expect(self.page).to_have_url(re.compile(r".*/dashboard"))
        expect(self.DASHBOARD_HEADER).to_be_visible()