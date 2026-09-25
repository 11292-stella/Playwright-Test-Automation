"""
Script di utilità (NON un test pytest) per scoprire velocemente gli
endpoint API usati da un flusso, senza aprire il Network tab a mano.

Uso da terminale, dalla root del progetto:
    python -m support.discover_endpoints

Apre un browser visibile, già loggato. Ogni richiesta verso l'API
(qualsiasi path con /v1/ o /api/) viene stampata in tempo reale con
metodo, URL, status e - se presente - il payload della richiesta.

Naviga a mano nell'app e fai l'azione che ti interessa (es. cerca un
fornitore, crea un DDT, ecc). Quando hai visto quello che ti serve,
chiudi la finestra del browser per terminare lo script.
"""

from playwright.sync_api import sync_playwright
from support.auth import login_utente
from support.config import BASE_URL


def _is_api_call(url: str) -> bool:
    return "/v1/" in url or "/api/" in url


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        def log_request(request):
            if _is_api_call(request.url):
                print(f"\n>>> {request.method} {request.url}")
                if request.method in ("POST", "PUT", "PATCH"):
                    try:
                        print(f"    payload: {request.post_data}")
                    except Exception:
                        pass

        def log_response(response):
            if _is_api_call(response.url):
                print(f"<<< {response.status} {response.url}")

        page.on("request", log_request)
        page.on("response", log_response)

        login_utente(page)
        page.goto(BASE_URL)

        print("\n=== Browser pronto. Naviga e fai le azioni che ti interessano. ===")
        print("=== Chiudi la finestra del browser per terminare lo script.    ===\n")

        page.wait_for_event("close", timeout=0)
        browser.close()


if __name__ == "__main__":
    main()