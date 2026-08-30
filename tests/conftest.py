import pytest
from support.auth import login_app
from support.config import BASE_URL
import allure

STORAGE_STATE_PATH = "support/storage_state.json"


@pytest.fixture(scope="session")
def storage_state_path(browser):
    """
    Fa il login UNA VOLTA per l'intera sessione di test e salva
    cookie/localStorage su file. Equivalente di cy.session().
    """
    context = browser.new_context()
    page = context.new_page()
    login_app(page)
    context.storage_state(path=STORAGE_STATE_PATH)
    context.close()
    return STORAGE_STATE_PATH


@pytest.fixture
def authenticated_page(browser, storage_state_path):
    """
    Ogni test che chiede questo fixture ottiene una pagina già loggata,
    senza rifare login. Equivalente di richiamare cy.session() nei
    singoli test.
    """
    context = browser.new_context(storage_state=storage_state_path)
    page = context.new_page()
    page.goto(BASE_URL)   # <-- AGGIUNTA: naviga verso l'app appena apri la pagina
    
    yield page
    page.pause()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("authenticated_page") or item.funcargs.get("page")
        if page:
            try:
                screenshot = page.screenshot()
                allure.attach(screenshot, name="screenshot-failure", attachment_type=allure.attachment_type.PNG)
            except Exception:
                pass