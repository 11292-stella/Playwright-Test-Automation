import os
import pytest
from support.auth import login_utente
from support.config import BASE_URL
from support.api_logger import attach_api_logger, dump_api_log
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
    login_utente(page)
    context.storage_state(path=STORAGE_STATE_PATH)
    context.close()
    return STORAGE_STATE_PATH


@pytest.fixture
def authenticated_page(browser, storage_state_path, request):
    """
    Ogni test che chiede questo fixture ottiene una pagina già loggata,
    senza rifare login. Equivalente di richiamare cy.session() nei
    singoli test.

    Se la variabile d'ambiente API_DISCOVERY è impostata, aggancia anche
    il logger delle chiamate API (stessa logica di
    support/discover_endpoints.py) e le scrive su
    reports/api-discovery/<nome_test>.log a fine test — utile per
    scoprire gli endpoint usati da un modulo E2E già scritto invece di
    navigare a mano nel browser. Di default è disattivato e il
    comportamento resta identico a prima (compreso il page.pause()).
    """
    context = browser.new_context(storage_state=storage_state_path)
    page = context.new_page()

    discovery_enabled = bool(os.getenv("API_DISCOVERY"))
    calls = attach_api_logger(page) if discovery_enabled else None

    page.goto(BASE_URL)   # <-- AGGIUNTA: naviga verso l'app appena apri la pagina

    yield page

    if discovery_enabled:
        out_path = dump_api_log(calls, request.node.nodeid)
        print(f"\n[api-discovery] {len(calls)} chiamate salvate in {out_path}\n")
    else:
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