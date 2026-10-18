import re
import allure

from playwright.sync_api import Page, expect

class PimAddEmployeePage():
    def __init__(self, page: Page):
        self.page = page
        self.FIRST_NAME_INPUT = page.locator("[name='firstName']")
        self.MIDDLE_NAME_INPUT = page.locator("[name='middleName']")
        self.LAST_NAME_INPUT = page.locator("[name='lastName']")
        self.EMPLOYEE_ID = page.locator(".oxd-input-group").filter(has_text="Employee Id").locator("input")
        self.CANCEL_BUTTON = page.get_by_role("button", name="Cancel")
        self.SAVE_BUTTON = page.get_by_role("button", name="Save")
        self.SUCCESS_TOAST = page.locator("div.oxd-toast.oxd-toast--success.oxd-toast-container--toast")

    @allure.step("Verify PIM - add employee page is loaded")
    def is_loaded(self):
        expect(self.page).to_have_url(re.compile(r".*/pim/addEmployee$"))
        expect(self.FIRST_NAME_INPUT).to_be_visible()
        expect(self.MIDDLE_NAME_INPUT).to_be_visible()
        expect(self.LAST_NAME_INPUT).to_be_visible()
        expect(self.EMPLOYEE_ID).to_be_visible()
        expect(self.CANCEL_BUTTON).to_be_visible()
        expect(self.SAVE_BUTTON).to_be_visible()

    @allure.step("Enter first name='{first_name}'")
    def enter_first_name(self, first_name: str):
        self.FIRST_NAME_INPUT.fill(first_name)

    @allure.step("Enter middle name='{middle_name}'")
    def enter_middle_name(self, middle_name: str):
        self.MIDDLE_NAME_INPUT.fill(middle_name)

    @allure.step("Enter last name='{last_name}'")
    def enter_last_name(self, last_name: str):
        self.LAST_NAME_INPUT.fill(last_name)

    @allure.step("Enter employee id='{employee_id}'")
    def enter_employee_id(self, employee_id: int):
        self.EMPLOYEE_ID_INPUT.fill(employee_id)

    @allure.step("Add employee")
    def add_employee(self, first_name, middle_name, last_name):
        self.enter_first_name(first_name)
        self.enter_middle_name(middle_name)
        self.enter_last_name(last_name)
        self.SAVE_BUTTON.click()

    @allure.step("Verify success adding new employee")
    def check_save_success(self):
        expect(self.SUCCESS_TOAST).to_be_visible()

    