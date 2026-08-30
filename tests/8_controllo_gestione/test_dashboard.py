from pages.mod_8_controllo_gestione.DashboardPage import Dashboard

class TestDashboard:
    def test_dash(self,authenticated_page):
        dash = Dashboard(authenticated_page)
        dash.apri_controllo_gestione()
        dash.salva_html_pagina("dashboard")

        dash.scegli_filtro()

        dash.genera_e_aggiorna_dati()


# per avviare il test: - pytest tests/8_controllo_gestione/test_dashboard.py --headed
# per avviare il test di tutta la cartella: - pytest tests/8_controllo_gestione
# per aprire il report finale: - start reports\report.html