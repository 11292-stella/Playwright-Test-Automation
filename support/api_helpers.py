"""
Helper comuni per i test API (Playwright APIRequestContext).
Evita di riscrivere sempre le stesse asserzioni/pattern in ogni
file test_*_api.py sotto tests/api/.
"""


def debug_body(response):
    """Estrae il body in modo sicuro, anche se la risposta non è JSON valido."""
    try:
        return response.json()
    except Exception:
        return response.text()


def assert_status(response, expected_status: int):
    """
    Verifica lo status code. Se fallisce, il body della risposta compare
    già nel messaggio di errore di pytest: non serve più aggiungere un
    print() e rilanciare con -s per vedere cosa ha risposto il backend.
    """
    assert response.status == expected_status, (
        f"Atteso status {expected_status}, ricevuto {response.status}. "
        f"Body: {debug_body(response)}"
    )


def assert_unauthorized(context_no_auth, method: str, path: str, **kwargs):
    """
    Esegue una richiesta senza autenticazione e verifica 401.
    Uso:
        assert_unauthorized(api_context_no_auth, "post", "/api/x", data=payload)
        assert_unauthorized(api_context_no_auth, "get", "/api/x")
    """
    request_method = getattr(context_no_auth, method.lower())
    response = request_method(path, **kwargs)
    assert_status(response, 401)
    return response


def assert_field(body: dict, field: str, expected_value=None):
    """
    Verifica che un campo esista nel body e, opzionalmente, che abbia
    un valore preciso. Messaggio d'errore già leggibile senza dover
    ristampare tutto il body a mano.
    """
    assert field in body, f"Campo '{field}' assente nel body: {body}"
    if expected_value is not None:
        assert body[field] == expected_value, (
            f"Campo '{field}' atteso={expected_value!r}, "
            f"ottenuto={body[field]!r}"
        )