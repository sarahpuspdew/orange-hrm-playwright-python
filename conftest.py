import pytest
import os
from dotenv import load_dotenv
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.sidebar_page import SidebarPage
from pages.pim_employee_list_page import PimEmployeeListPage
from pages.pim_add_employee_page import PimAddEmployeePage
from test_data.test_data import VALID_USERNAME, VALID_PASSWORD, EMPLOYEE_FULL_NAME

load_dotenv()

@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("BASE_URL", "https://opensource-demo.orangehrmlive.com")

@pytest.fixture
def login_page(page: Page, base_url: str) -> LoginPage:
    login_page = LoginPage(page)
    login_page.go_to(base_url)
    return login_page

@pytest.fixture
def logged_in(login_page: LoginPage) -> DashboardPage:
    login_page.login(VALID_USERNAME, VALID_PASSWORD)
    dashboard_page = DashboardPage(login_page.page)
    return dashboard_page

@pytest.fixture
def pim_page(logged_in: DashboardPage) -> PimEmployeeListPage:
    sidebar_page = SidebarPage(logged_in.page)
    sidebar_page.click_PIM_OPTION()
    pim_page = PimEmployeeListPage(logged_in.page)
    return pim_page