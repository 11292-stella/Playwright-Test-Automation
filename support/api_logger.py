"""
Helper per "abbinare" la scoperta degli endpoint (stessa logica di
support/discover_endpoints.py) a un test E2E già esistente, invece di
navigare a mano nel browser.

Uso: si aggancia a una Page già aperta (es. authenticated_page) prima
che il test faccia le sue azioni. Ogni request/response verso /v1/ o
/api/ viene stampata IN TEMPO REALE in console (stile >>>/<<<, come
discover_endpoints.py) e in più accumulata in memoria per un dump
finale su file come backup.
"""

import json
import re
from pathlib import Path

OUTPUT_DIR = Path("reports/api-discovery")


def _is_api_call(url: str) -> bool:
    return "/v1/" in url or "/api/" in url


def attach_api_logger(page) -> list:
    """
    Aggancia i listener request/response sulla page. Ogni chiamata API
    viene stampata subito in console (>>> per la request, <<< per la
    response) e in più accumulata nella lista (mutabile) restituita,
    così a fine test si può ancora fare un dump su file come backup.

    Va chiamata PRIMA che il test esegua le azioni da tracciare.
    """
    calls = []

    def log_request(request):
        if _is_api_call(request.url):
            entry = {"type": "request", "method": request.method, "url": request.url}
            if request.method in ("POST", "PUT", "PATCH"):
                try:
                    entry["payload"] = request.post_data
                except Exception:
                    pass
            calls.append(entry)
            payload = f" payload={entry.get('payload')}" if entry.get("payload") else ""
            print(f">>> {entry['method']} {entry['url']}{payload}")

    def log_response(response):
        if _is_api_call(response.url):
            calls.append({"type": "response", "status": response.status, "url": response.url})
            print(f"<<< {response.status} {response.url}")

    page.on("request", log_request)
    page.on("response", log_response)
    return calls


def dump_api_log(calls: list, test_nodeid: str) -> Path:
    """
    Scrive le chiamate accumulate su reports/api-discovery/<nome_test>.log
    come backup (una riga JSON per chiamata). La console resta comunque
    la fonte "live" durante l'esecuzione del test.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = re.sub(r"[^\w\-]", "_", test_nodeid)
    out_path = OUTPUT_DIR / f"{safe_name}.log"
    with out_path.open("w", encoding="utf-8") as f:
        for c in calls:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    return out_path