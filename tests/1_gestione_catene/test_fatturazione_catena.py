from pages.mod_1_gestione_catene.Fatturazione_catenaPage import FatturazionePage


class TestFattureModello:

    def test_compila_modello(self, authenticated_page):
        fatture = FatturazionePage(authenticated_page)
        fatture.apri_fatture()
        fatture.filtra_per_catena("Catena Demo (reseller_demo_catena_demo)")

        fatture.form_fatture_catena({
            "modello": "Royalty (% fatturato)",
            "iva": "22",
            "royalty": "25",
            "ciclo": "Mensile"
        })
        # fatture.salva_modello_fatturazione()  # disabilitato: vedi BUG NOTO nel metodo


class TestFattureGenerate:

    def test_genera_fatture(self, authenticated_page):
        fatture = FatturazionePage(authenticated_page)
        fatture.apri_fatture()
        fatture.filtra_per_catena("Catena Demo (reseller_demo_catena_demo)")
        fatture.genera_fatture("2026-07-08", "2026-07-16")


# per avviare il test: pytest tests/1_gestione_catene/test_fatturazione_catena.py --headed