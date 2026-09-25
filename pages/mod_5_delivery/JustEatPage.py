from playwright.sync_api import Page
from pages.mod_5_delivery.delivery_provider_page import DeliveryProviderPage


class JustEat(DeliveryProviderPage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.path = "/delivery-integrations/justeat"
        self.switch_provider = page.get_by_role("checkbox", name="Abilita Just Eat")
        self.input_partner_brand = page.get_by_role("textbox", name="ID Partner / Brand (opzionale)")
        self.input_id_ristorante = page.get_by_role("textbox", name="ID Ristorante Just Eat")

    def compila_id(self, dati_id: dict):
        self.input_id_ristorante.fill(dati_id["id"])