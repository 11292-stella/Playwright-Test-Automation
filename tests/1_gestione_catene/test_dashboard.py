from pages.mod_1_gestione_catene.Dashboard_Page import DashboardPage

class TestDashboard:

    def test_apertura_dashboard_catena(self, authenticated_page):
        dashboard = DashboardPage(authenticated_page)
        dashboard.apri_dashboard()

    def test_filtro_catena_dashboard(self, authenticated_page):
        dashboard = DashboardPage(authenticated_page)
        dashboard.apri_dashboard()
        dashboard.filtra_per_catena("Catena Demo (reseller_demo_catena_demo)")



# per avviare il test: pytest tests/1_gestione_catene/test_dashboard.py --headed