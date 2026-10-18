import re
import allure

from playwright.sync_api import Page, expect

class PimEmployeeListPage():
    def __init__(self, page: Page):
        self.page = page
        self.PIM_HEADER = page.get_by_role("heading", name="PIM")
        self.FILTER_TABLE = page.locator("div.oxd-table-filter")
        self.EMPLOYEE_NAME_INPUT = page.locator(".oxd-input-group").filter(has_text="Employee Name").locator("input")
        self.SUPERVISOR_NAME_INPUT = page.locator(".oxd-input-group").filter(has_text="Supervisor Name").locator("input")
        self.EMPLOYEE_ID_INPUT = page.locator(".oxd-input-group").filter(has_text="Employee Id").get_by_role("textbox")
        self.JOB_TITLE_DROPDOWN = page.locator(".oxd-input-group").filter(has_text="Job Title").locator(".oxd-select-text-input")
        self.EMPLOYMENT_STATUS_DROPDOWN = page.locator(".oxd-input-group").filter(has_text="Employment Status").locator(".oxd-select-text-input")
        self.SUB_UNIT_DROPDOWN = page.locator(".oxd-input-group").filter(has_text="Sub Unit").locator(".oxd-select-text-input")
        self.INCLUDE_DROPDOWN = page.locator(".oxd-input-group").filter(has_text="Include").locator(".oxd-select-text-input")
        self.RESET_BUTTON = page.get_by_role("button", name="Reset")
        self.SEARCH_BUTTON = page.get_by_role("button", name="Search")
        self.ADD_BUTTON = page.get_by_role("button", name="Add")
        self.RECORDS_TEXT = page.locator(".orangehrm-horizontal-padding").locator(".oxd-text")
        
        self.EMPLOYEE_TABLE = page.locator(".orangehrm-employee-list")
        self.EMPLOYEE_TABLE_HEADER = self.EMPLOYEE_TABLE.get_by_role("columnheader")
        self.EMPLOYEE_TABLE_ROW = self.EMPLOYEE_TABLE.locator(".oxd-table-body .oxd-table-row")

        self.DELETION_POPUP = page.locator(".orangehrm-dialog-popup")
        self.DELETION_CANCEL_BUTTON = self.DELETION_POPUP.get_by_role("button", name="No, Cancel")
        self.DELETION_DELETE_BUTTON = self.DELETION_POPUP.get_by_role("button", name="Yes, Delete")
        self.SUCCESS_DELETE_TOAST = page.locator(".oxd-toast-container--bottom")

    @allure.step("Verify PIM - employee list page is loaded")
    def is_loaded(self):
        expect(self.page).to_have_url(re.compile(r".*/pim/viewEmployeeList$"))
        expect(self.PIM_HEADER).to_be_visible()
        expect(self.FILTER_TABLE).to_be_visible()
        expect(self.EMPLOYEE_NAME_INPUT).to_have_attribute("placeholder", "Type for hints...")
        expect(self.SUPERVISOR_NAME_INPUT).to_have_attribute("placeholder", "Type for hints...")
        expect(self.EMPLOYEE_ID_INPUT).to_be_visible()
        expect(self.JOB_TITLE_DROPDOWN).to_have_text("-- Select --")
        expect(self.EMPLOYMENT_STATUS_DROPDOWN).to_have_text("-- Select --")
        expect(self.SUB_UNIT_DROPDOWN).to_have_text("-- Select --")
        expect(self.INCLUDE_DROPDOWN).to_have_text("Current Employees Only")
        expect(self.RESET_BUTTON).to_be_visible()
        expect(self.SEARCH_BUTTON).to_be_visible()
        expect(self.ADD_BUTTON).to_be_visible()
        expect(self.RECORDS_TEXT).to_contain_text("Records Found")
        expect(self.EMPLOYEE_TABLE).to_be_visible()

    @allure.step("Navigate to Employee List")
    def navigate_to_employee_list(self, base_url: str):    
        self.page.goto(f"{base_url}/web/index.php/pim/viewEmployeeList")

    @allure.step("Enter employee name")
    def enter_employee_name(self, employee_name):
        self.EMPLOYEE_NAME_INPUT.fill(employee_name)

    @allure.step("Click search button")
    def click_search(self):
        self.SEARCH_BUTTON.click()

    @allure.step("Click add button")
    def click_add(self):
        self.ADD_BUTTON.click()

    def get_employee_row(self, first_middle_name, last_name):
        return self.EMPLOYEE_TABLE_ROW.filter(has=self.page.get_by_text(first_middle_name, exact=True)).filter(
            has=self.page.get_by_text(last_name, exact=True)
        )

    def click_delete_employee(self, first_middle_name, last_name):
        employee_row = self.get_employee_row(first_middle_name, last_name)
        employee_row.get_by_role("button").nth(1).click()

    def confirm_deletion(self):
        self.DELETION_DELETE_BUTTON.click()


    