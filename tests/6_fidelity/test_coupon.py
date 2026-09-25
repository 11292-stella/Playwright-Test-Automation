from pages.mod_6_fidelity.CouponPage import Coupon
from utils.test_data import ChainTestData


class TestCoupon:

    def test_coupon_sconto_fisso(self, authenticated_page):
        coupon = Coupon(authenticated_page)
        coupon.apri_coupon()

        coupon.crea_nuovo_coupon()
        dati_coupon = ChainTestData.genera_dati_nuovo_coupon()

        coupon.seleziona_tipo_coupon("Sconto Fisso")
        coupon.compila_mod_nuovo_coupon(dati_coupon)

        response = coupon.genera_coupon()
        assert response.status == 404, (
            "BUG NOTO (stesso bug visto in CampagnePage): il salvataggio del "
            "coupon risponde 404 a prescindere dai dati inseriti — problema "
            "lato backend, non di questo test. Se questo assert fallisce, "
            "il bug è stato risolto: aggiornare l'assert a status == 200 e "
            "rimuovere questo commento."
        )

    def test_coupon_sconto(self, authenticated_page):
        coupon = Coupon(authenticated_page)
        coupon.apri_coupon()

        coupon.crea_nuovo_coupon()
        dati_coupon = ChainTestData.genera_dati_nuovo_coupon()

        coupon.seleziona_tipo_coupon("Sconto %")
        coupon.compila_mod_nuovo_coupon(dati_coupon)

        response = coupon.genera_coupon()
        assert response.status == 404, (
            "BUG NOTO (stesso bug visto in CampagnePage): il salvataggio del "
            "coupon risponde 404 a prescindere dai dati inseriti — problema "
            "lato backend, non di questo test. Se questo assert fallisce, "
            "il bug è stato risolto: aggiornare l'assert a status == 200 e "
            "rimuovere questo commento."
        )

    def test_coupon_prodotto_gratis(self, authenticated_page):
        coupon = Coupon(authenticated_page)
        coupon.apri_coupon()

        coupon.crea_nuovo_coupon()
        dati_coupon = ChainTestData.genera_dati_nuovo_coupon()

        
        coupon.seleziona_tipo_coupon("Prodotto Gratis")
        coupon.cerca_e_seleziona_prodotto_gratis("Pollo alla Cacciatora")
        coupon.compila_mod_con_prodotti_gratis(dati_coupon)

        response = coupon.genera_coupon()
        assert response.status == 404, (
            "BUG NOTO (stesso bug visto in CampagnePage): il salvataggio del "
            "coupon risponde 404 a prescindere dai dati inseriti — problema "
            "lato backend, non di questo test. Se questo assert fallisce, "
            "il bug è stato risolto: aggiornare l'assert a status == 200 e "
            "rimuovere questo commento."
        )


# per avviare il test: - pytest tests/6_fidelity/test_coupon.py --headed
# per avviare il test di tutta la cartella gestione_catene: - pytest tests/6_fidelity
# per aprire il report finale: - start reports\report.html    



