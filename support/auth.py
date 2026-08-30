from playwright.sync_api import Page
from support.config import EMAIL, PASSWORD, BASE_URL, TENANT_LABEL


def login_app(page: Page):
    page.context.clear_cookies()
    page.goto(BASE_URL)

    page.locator("#username").fill(EMAIL)
    page.locator("#password").fill(PASSWORD)
    page.locator("#password").press("Enter")

    page.wait_for_load_state("networkidle")

    seleziona_tenant(page)   # <-- selezione subito dopo il login


def seleziona_tenant(page: Page):
    """Seleziona il tenant corretto nel combobox 'Impersona Tenant'."""
    page.get_by_label("Impersona Tenant", exact=True).click()
    page.get_by_role("option", name=TENANT_LABEL, exact=True).click()


