from urllib.parse import urlparse
from support.config import BASE_URL
from playwright.sync_api import Page


def test_login_e_dashboard_visibile(authenticated_page: Page):
    assert urlparse(BASE_URL).netloc in authenticated_page.url