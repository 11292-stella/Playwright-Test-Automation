from playwright.sync_api import Page
from pages.mod_5_delivery.delivery_provider_page import DeliveryProviderPage


class Deliverect(DeliveryProviderPage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.path = "/delivery-integrations/deliverect"
        self.switch_provider = page.get_by_role("checkbox", name="Abilita Deliverect")
        self.input_account_brand = page.get_by_role("textbox", name="Account/Brand Deliverect (")
        self.input_location_id = page.get_by_role("textbox", name="Location ID Deliverect")

    def compila_id(self, dati_id: dict):
        self.input_location_id.fill(dati_id["id"])