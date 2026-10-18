VALID_USERNAME = "Admin"
VALID_PASSWORD = "admin123"

INVALID_CREDS = [
    ("Admin",        "wrongpass"),  # wrong password
    ("wronguser",    "admin123"),   # wrong username
    ("wronguser",    "wrongpass"),  # wrong userpass
    (" Admin",       "admin123"),   # leading space
    ("Admin",        "admin123 "),  # trailing space
]

EMPLOYEE_FULL_NAME = ("Leo", "Scott", "Kennedy")