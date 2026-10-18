import allure

from playwright.sync_api import Page

class SidebarPage:
    def __init__(self, page: Page):
        self.page = page
        self.PIM_OPTION = page.get_by_role("link", name="PIM")

    @allure.step("Click PIM menu")
    def click_PIM_OPTION(self):
        self.PIM_OPTION.click()