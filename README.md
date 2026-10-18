# OrangeHRM UI Test Automation - Playwright Python

End-to-end UI tests for the [OrangeHRM open-source demo](https://opensource-demo.orangehrmlive.com), built with **Python, Playwright and pytest** using the **Page Object Model**. Tests run in Docker, report with **Allure** and **pytest-html**, and run automatically on **GitHub Actions**.

## Project structure

```
orange-hrm/
├── .github/workflows/
│   └── playwright.yml        # CI pipeline
├── pages/                    # Page Objects (locators + actions per page)
│   ├── login_page.py
│   ├── dashboard_page.py
│   ├── sidebar_page.py
│   ├── pim_employee_list_page.py
│   └── pim_add_employee_page.py
├── tests/                    # Test cases
│   ├── test_01_login.py
│   └── test_02_pim.py
├── test_data/
│   └── test_data.py          # Credentials, etc
├── conftest.py               # Shared fixtures
├── pytest.ini                # pytest options and report settings
├── requirements.txt          # Pinned Python dependencies
├── Dockerfile                # Test image (based on the official Playwright image)
└── docker-compose.yml        # `tests` service and optional `allure` report service
```

## Test scenarios

### Login (`tests/test_01_login.py`)

| ID | Scenario | Expected result |
|----|----------|-----------------|
| TC_LOGIN_001 | Login with valid credentials | Redirected to the dashboard; dashboard header visible |
| TC_LOGIN_002 | Login with invalid credentials (wrong password, wrong username, both wrong, leading space in username, trailing space in password) | "Invalid credentials" alert is shown |
| TC_LOGIN_003 | Login with missing username | "Required" validation message |
| TC_LOGIN_004 | Login with missing password | "Required" validation message |
| TC_LOGIN_005 | Login with both fields empty | "Required" shown on every field |

### PIM - Employee List (`tests/test_02_pim.py`)

| ID | Scenario | Expected result |
|----|----------|-----------------|
| TC_PIM_001 | Open PIM > Employee List | URL, header, filter form, buttons and table are all displayed |
| TC_PIM_002 | Add an employee, then search for them by name | Exactly one matching row with the correct first/middle and last name |
| TC_PIM_003 | Search for the employee, delete them, and confirm | The employee no longer appears in the table |

> **Note:** `TC_PIM_003` deletes the employee created in `TC_PIM_002`, so these two tests depend on each other. Run the file in order and **do not** run it in parallel (`-n`).

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) with Docker Compose v2 (recommended), **or**
- Python 3.10+ if you want to run without Docker (see below)

## Running the tests

### With Docker (recommended)

```bash
# build the image (only needed the first time, or when requirements.txt / Dockerfile change)
docker compose build tests

# run the whole suite
docker compose run --rm tests

# run a single file
docker compose run --rm tests tests/test_01_login.py

# run login first, then the employee tests
docker compose run --rm tests tests/test_login.py tests/test_02_pim.py

# run a single test by name
docker compose run --rm tests -k test_valid_creds_login
```

### Without Docker

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium

pytest
```

## Reports and failure artifacts

### Allure report (live, local)

```bash
docker compose --profile report up -d allure
```

Then open <http://localhost:5050/allure-docker-service/latest-report>. The report refreshes automatically as new results appear in `allure-results/`. Stop it with `docker compose --profile report down`.

It shows each test with its steps, screenshots, history and timings.

### pytest-html report

After every run, open `reports/report.html` in a browser. It is a single self-contained file.

### Failure screenshots, videos and traces

On failure, Playwright saves a screenshot, a video and a trace under `test-results/`. To inspect a trace:

```bash
playwright show-trace test-results/<test-folder>/trace.zip
```

(Or drop the `trace.zip` onto <https://trace.playwright.dev>.)

### CI report (GitHub Actions)

Every push to `main`, every pull request, and manual runs (**Actions > Playwright Tests > Run workflow**) trigger the pipeline. It builds the Docker image, runs the tests, and generates a **single-file Allure report**.

To view it:

1. Open the repo's **Actions** tab and select a workflow run.
2. Scroll to **Artifacts** at the bottom of the summary page and download `allure-report`.
3. Unzip it and double-click `index.html`.

The artifact is kept for 14 days and is uploaded even when tests fail.
