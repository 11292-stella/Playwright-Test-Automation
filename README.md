# Playwright E2E Testing – Demo Project

Suite di test end-to-end scritta con **Playwright + pytest** per un'applicazione
web gestionale (SaaS multi-tenant), con pipeline CI/CD completa su **GitLab CI**.

> Questo repository è una versione dimostrativa/anonimizzata di un progetto di
> test automation realizzato in ambito lavorativo: URL, credenziali, nomi
> tenant e dati aziendali sono stati sostituiti con valori fittizi. La
> struttura, le tecniche e la pipeline sono invece quelle realmente usate.

## Stack

- **Playwright** (Python) — automazione browser
- **pytest** + **pytest-playwright** — test runner
- **Allure** + **pytest-html** — reportistica
- **GitLab CI** — pipeline automatizzata, containerizzata con l'immagine
  Docker ufficiale Playwright

## Struttura del progetto

```
tests/                     # test organizzati per modulo funzionale
  0_stabilita_moduli_cypress/
  1_gestione_catene/
  2_gestione_locale_nuovi_moduli/
  3_configurazione_ristorante_mod_webapp/
  4_email_marketing/
  5_delivery/
  6_fidelity/
  7_report_e_analytics/
  8_controllo_gestione/
  conftest.py               # fixture di autenticazione condivisa (storage state)
pages/                     # Page Object Model: una classe per pagina/sezione UI,
  base_page.py             # con i selettori e le azioni, separati dalla logica di test
  mod_1_gestione_catene/
  mod_...
utils/
  test_data.py             # generatori di dati di test (nomi prodotti, categorie, ecc.)
support/
  auth.py                   # logica di login riutilizzabile
  config.py                 # lettura configurazione da variabili d'ambiente
.gitlab-ci.yml               # pipeline CI multi-job con report JUnit/Allure
pytest.ini
requirements.txt
.env.example
```

## Punti di interesse tecnico

- **Page Object Model**: ogni schermata/sezione dell'app ha una classe dedicata in
  `pages/` con selettori e azioni; i file in `tests/` restano leggibili come una
  sequenza di passi (`catalogo.apri_catalogo()`, `catalogo.crea_nuovo_prodotto()`)
  senza selettori CSS/XPath sparsi nei test.
- **Autenticazione una tantum**: il login viene eseguito una sola volta per
  sessione di test e lo stato (cookie/localStorage) viene salvato su disco e
  riutilizzato da tutti i test (`storage_state`), evitando di rifare login ad
  ogni singolo test.
- **Screenshot automatico sui fallimenti**: un hook pytest (`pytest_runtest_makereport`)
  cattura uno screenshot e lo allega al report Allure solo quando un test fallisce.
- **Pipeline modulare**: ogni cartella di `tests/` ha un job GitLab CI dedicato,
  incatenati in sequenza (per non far girare più browser in parallelo sullo
  stesso runner), ciascuno con il proprio report JUnit visibile nella UI di GitLab.
- **Job manuale "singolo spec"**: tramite un `spec:inputs` configurabile dalla UI
  di GitLab, è possibile lanciare un singolo file di test senza eseguire l'intera suite.
- **Anti-pipeline duplicate**: una regola di `workflow` evita che lo stesso commit
  generi due pipeline identiche (una da push diretto, una da Merge Request).
- **Commento automatico in Merge Request**: a fine suite, un job chiama le API
  di GitLab per lasciare un commento con l'esito nella MR.

## Setup locale

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # poi valorizza .env con i tuoi dati
pytest
```

## Esecuzione in CI

La pipeline gira su un'immagine Docker Playwright ufficiale (browser già
pre-installati) e legge le credenziali da CI/CD Variables protette/mascherate
(`EMAIL`, `PASSWORD`, `TENANT_LABEL`), mai committate nel repository.
