import allure
from playwright.sync_api import expect

from pages.pim_employee_list_page import PimEmployeeListPage
from pages.pim_add_employee_page import PimAddEmployeePage
from test_data.test_data import (EMPLOYEE_FULL_NAME)

class TestPim:
    first_name, middle_name, last_name = EMPLOYEE_FULL_NAME
    first_middle_name = " ".join(name for name in [first_name, middle_name] if name)
    employee_full_name = f"{first_middle_name} {last_name}"

    # ── TC_PIM_001 ── Verify Employee List Page ──────────────────────
    @allure.title("TC_PIM_001 - Verify Employee List Page")
    def test_employee_list(self, pim_page: PimEmployeeListPage):
        with allure.step("Verify user can see employee list page"):
            pim_page.is_loaded()
            screenshot = pim_page.page.screenshot()
            allure.attach(screenshot)

    # ── TC_PIM_002 ── Search Employee by Employee Name ──────────────────────
    @allure.title("TC_PIM_002 - Search Employee by Employee Name")
    def test_search_employee(self, base_url, pim_page: PimEmployeeListPage):
        # Add a new employee first
        pim_page.click_add()
        pim_add_page = PimAddEmployeePage(pim_page.page)
        pim_add_page.add_employee(self.first_name, self.middle_name, self.last_name)
        pim_add_page.check_save_success()
        pim_page.navigate_to_employee_list(base_url)
        
        with allure.step("User Search for the newly added employee"):
            pim_page.enter_employee_name(self.employee_full_name)
            pim_page.click_search()

        with allure.step("Verify employee can be seen in the table "):
            employee_row = pim_page.get_employee_row(self.first_middle_name, self.last_name)

            # Verify one matching row exists
            expect(employee_row).to_have_count(1)

            # Verify First (& Middle) Name
            expect(employee_row.get_by_role("cell").nth(2)).to_have_text(self.first_middle_name)

            # Verify Last Name
            expect(employee_row.get_by_role("cell").nth(3)).to_have_text(self.last_name)

            screenshot = pim_page.page.screenshot()
            allure.attach(screenshot)

    # ── TC_PIM_003 ── Delete Employee ──────────────────────
    @allure.title("TC_PIM_002 - Delete Employee")
    def test_delete_employee(self, pim_page: PimEmployeeListPage):
        with allure.step("Search for the existing employee"):
            pim_page.enter_employee_name(self.employee_full_name)
            pim_page.click_search()

        with allure.step("Delete the employee"):
            pim_page.click_delete_employee(self.first_middle_name, self.last_name)

        with allure.step("Confirm employee deletion"):
            pim_page.confirm_deletion()

        with allure.step("Verify employee is deleted"):
            employee_row = pim_page.get_employee_row(self.first_middle_name, self.last_name)
            expect(employee_row).to_have_count(0)