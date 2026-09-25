from playwright.sync_api import Page
from pages.mod_5_delivery.delivery_provider_page import DeliveryProviderPage


class Glovo(DeliveryProviderPage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.path = "/delivery-integrations/glovo"
        self.switch_provider = page.get_by_role("checkbox", name="Abilita Glovo")
        self.input_store_id_opzionale = page.get_by_role("textbox", name="Store ID Glovo (opzionale)")
        self.input_store_id = page.get_by_role("textbox", name="Store ID Glovo", exact=True)

    def compila_id(self, dati_id: dict):
        self.input_store_id.fill(dati_id["id"])