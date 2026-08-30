from playwright.sync_api import Page


def test_login_e_dashboard_visibile(authenticated_page: Page):
    assert "demo.example.com" in authenticated_page.url