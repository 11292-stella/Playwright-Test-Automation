## Generatore di dati dinamici con faker per ogni modulo

import random
import re
import uuid
from faker import Faker
from datetime import timedelta

fake = Faker('it_IT')

class ChainTestData:
    @staticmethod
    def genera_dati_nuova_catena():
        """Genera un dataset completo per la modale 'Nuova catena'."""
        azienda = fake.company()

        # Puliamo il nome per creare uno slug valido (es. "Rossi-Spa-12")
        slug_clean = re.sub(r'[^a-zA-Z0-9]', '-', azienda).lower()
        slug_dinamico = f"{slug_clean[:10]}-{fake.random_int(100, 999)}"

        return {
            "slug": slug_dinamico,
            "nome": f"Catena {azienda}",
            "max_negozi": str(fake.random_int(5, 50))
        }

    @staticmethod
    def genera_dati_nuovo_prodotto_catalogo_catena():
        """Genera un dataset completo per la modale 'Nuovo Prodotto' del catalogo catena."""

        # Lista di piatti realistici della cucina italiana
        piatti = [
            "Pasta alla Norma", "Pasta alla Carbonara", "Pasta all'Amatriciana",
            "Pasta al Pesto", "Pasta alla Gricia", "Pasta alla Puttanesca",
            "Pasta al Forno", "Pasta Alfredo", "Pasta al Tartufo",
            "Cotoletta alla Milanese", "Cotoletta ai Funghi", "Cotoletta alla Valdostana",
            "Risotto ai Funghi Porcini", "Risotto alla Milanese", "Risotto ai Frutti di Mare",
            "Lasagna alla Bolognese", "Parmigiana di Melanzane", "Saltimbocca alla Romana",
            "Ossobuco alla Milanese", "Bistecca alla Fiorentina", "Involtini di Melanzane",
            "Gnocchi al Gorgonzola", "Gnocchi alla Sorrentina", "Tagliatelle al Ragù",
            "Spaghetti alle Vongole", "Orecchiette alle Cime di Rapa", "Trofie al Pesto",
            "Polpette al Sugo", "Pollo alla Cacciatora", "Vitello Tonnato",
            "Bruschetta al Pomodoro", "Caprese di Bufala", "Tiramisù"
        ]

        nome_prodotto = random.choice(piatti)
        sku_dinamico = f"SKU-{fake.random_int(100000, 999999)}"

        return {
            "sku": sku_dinamico,
            "nome_prodotto": nome_prodotto,
            "descrizione": fake.sentence(nb_words=8),
            "prezzo_vendita": round(random.uniform(3.5, 25.0), 2),
            "costo": round(random.uniform(1.0, 10.0), 2),
        }

    @staticmethod
    def genera_dati_nuova_categoria_catena():
        """Genera un dataset completo per la modale 'Nuova Categoria' del catalogo catena."""

        categorie = ["Primi Piatti", "Secondi Piatti", "Antipasti", "Contorni", "Dolci", "Bevande"]

        nome_categoria = random.choice(categorie)

        return {
            "nome_categoria": nome_categoria,
            "descrizione": fake.sentence(nb_words=8),
        }

    @staticmethod
    def genera_dati_nuovo_ingrediente_catena():
        """Genera un dataset completo per la modale 'Nuovo Ingrediente' del catalogo catena."""

        ingredienti = [
            "funghi",
            "pomodoro",
            "mozzarella",
            "basilico",
            "aglio",
            "cipolla",
            "olio d'oliva",
            "sale",
            "pepe",
            "peperoni",
            "zucchine",
            "melanzane",
            "prosciutto",
            "parmigiano",
            "ricotta",
            "spinaci",
            "carote",
            "patate",
            "limone",
            "prezzemolo"
        ]

        sku_dinamico = f"SKU-{fake.random_int(100000, 999999)}"
        nome_prodotto = random.choice(ingredienti)

        return {
            "sku_ingrediente": sku_dinamico,
            "nome_prodotto": nome_prodotto,
            "descrizione_ingrediente": fake.sentence(nb_words=8),
            "costo_standard": round(random.uniform(1.0, 10.0), 2),
            "costo_unitario": round(random.uniform(3.5, 25.0), 2),
            "densita": round(random.uniform(3.5, 25.0), 2),
        }

    @staticmethod
    def genera_dati_nuova_variante_catena():

        variante = [
            "cotta bene",
            "senza pomodoro",
            "con olio al tartufo",
            "poco cotta",
            "senza glutine",
            "piccante",
            "senza aglio",
            "con doppia mozzarella",
            "senza sale",
            "vegetariana",
            "con bordo ripieno",
            "senza cipolla",
            "extra formaggio",
            "leggera (poco olio)",
            "con farina integrale"
        ]

        nome_variante = random.choice(variante)

        return {
            "nome_variante": nome_variante,
            "descrizione_variante": fake.sentence(nb_words=8),
            "delta_quantita": round(random.uniform(3.5, 25.0), 2),
        }

    @staticmethod
    def genera_dati_nuovo_listino_catena():

        nome = [
            "Menu Pasqua",
            "Menu Halloween",
            "Menu Natale",
            "Menu Capodanno",
            "Menu San Valentino",
            "Menu Ferragosto",
            "Menu Estate",
            "Menu Autunno",
            "Menu Carnevale",
            "Menu Festa della Mamma",
            "Menu Black Friday",
            "Menu Weekend",
            "Menu Degustazione",
            "Menu Bambini",
            "Menu Aperitivo",
        ]
        nome_listino = random.choice(nome)
        codice_listino = f"SKU_{fake.random_int(100000, 999999)}"

        return {
            "codice_listino": codice_listino,
            "nome_listino": nome_listino,
            "descrizione_listino": fake.sentence(nb_words=8),
            "data_dal": "2026-08-10",
            "data_al": "2026-12-31",
        }
    @staticmethod
    def genera_dati_nuova_catena():

        nome_catena = f"Catena {fake.company()}"
        slug_base = re.sub(r"[^a-z0-9]", "", nome_catena.lower())[:15]
        slug = f"{slug_base}{random.randint(100, 999)}"

        return{
            "slug": slug,
            "nome": nome_catena,
            "max_negozi": str(random.randint(5, 50)),
        }

    @staticmethod
    def genera_dati_nuova_ricetta_prodotto():

        return {
            "quantita": round(random.uniform(3.5, 25.0), 2),
            "descrizione_ricetta": fake.sentence(nb_words=8),
            "resa_ricetta": round(random.uniform(3.5, 25.0), 2),
            "tempo_ricetta": random.randint(5, 120),
        }

    @staticmethod
    def genera_dati_nuovo_fornitore_prodotto():

        codice_articolo = f"SKU_{fake.random_int(100000, 999999)}"

        conf_acquisto = [
            "12 (cartone da 12 pezzi)",
            "6 (confezione da 6 pezzi)",
            "24 (cartone da 24 bottiglie)",
            "1 (pezzo singolo)",
            "10 (cassa da 10 kg)",
            "20 (scatola da 20 pezzi)",
            "4 (confezione da 4 lattine)",
            "50 (sacco da 50 kg)",
            "8 (vaschetta da 8 pezzi)",
            "100 (fusto da 100 lt)",
        ]

        return {
            "codice_articolo": codice_articolo,
            "prezzo_unitario": round(random.uniform(3.5, 25.0), 2),
            "quantita_minima": round(random.uniform(3.5, 25.0), 2),
            "lead_time": random.randint(5, 120),
            "conf_acquisto": conf_acquisto,
            "fattore_conv": random.randint(5, 120),
        }

    @staticmethod
    def genera_dati_categorie_prodotto():

        categorie = ["Primi Piatti", "Secondi Piatti", "Antipasti", "Contorni", "Dolci", "Bevande"]

        icone = [
            "mdi-food",
            "mdi-food-fork-drink",
            "mdi-food-variant",
            "mdi-silverware-fork-knife",
            "mdi-pasta",
            "mdi-pizza",
            "mdi-hamburger",
            "mdi-cupcake",
            "mdi-cake-variant",
            "mdi-coffee",
            "mdi-cup",
            "mdi-glass-cocktail",
            "mdi-bottle-soda",
            "mdi-fruit-watermelon",
            "mdi-carrot",
        ]

        nome_categoria = random.choice(categorie)

        return {
            "nome_categoria": nome_categoria,
            "descrizione": fake.sentence(nb_words=8),
            "ordine": random.randint(5, 120),
            "icona": random.choice(icone),
            "colore": fake.hex_color(),
        }

    @staticmethod
    def genera_dati_specializzazione_personale():
        icone = [
            "mdi-account-star",
            "mdi-chef-hat",
            "mdi-glass-wine",
            "mdi-coffee",
            "mdi-cash-register",
            "mdi-silverware-fork-knife",
            "mdi-food",
            "mdi-bottle-wine",
            "mdi-account-hard-hat",
            "mdi-star",
        ]

        nome_base = random.choice(ChainTestData.SPECIALIZZAZIONI_PERSONALE)
        nome_specializzazione = f"{nome_base} {fake.random_int(1000, 9999)}"

        return {
            "nome_specializzazione": nome_specializzazione,
            "descrizione_specializzazione": fake.sentence(nb_words=8),
            "icona_specializzazione": random.choice(icone),
            "ordine_specializzazione": random.randint(0, 20),
        }

    @staticmethod
    def genera_dati_nuovo_operatore_con_specializzazione():

        nome = fake.first_name()
        cognome = fake.last_name()
        pin = str(fake.random_int(1000, 9999))

        return {
            "nome": nome,
            "cognome": cognome,
            "pin": pin,
            "costo": round(random.uniform(8.0, 20.0), 2),
        }

    SPECIALIZZAZIONI_PERSONALE = [
        "Barista",
        "Pizzaiolo",
        "Sommelier",
        "Pasticcere",
        "Cucina Vegana",
        "Cucina Senza Glutine",
        "Gestione Cassa",
        "Servizio ai Tavoli",
        "Preparazione Cocktail",
        "Gestione Magazzino",
        "Griglia e Brace",
        "Panificazione",
        "Servizio Delivery",
        "Formazione Nuovo Personale",
        "Gestione Reclami Clienti",
    ]

    @staticmethod
    def genera_dati_mod_successivo():

        return {
            "descrizione_mod": fake.sentence(nb_words=8),
        }

    @staticmethod
    def genera_dati_campi_personalizzati_nuovo_campo():

        etichette = [
            "Allergie",
            "Preferenze Alimentari",
            "Numero Tessera Fedeltà",
            "Referente Aziendale",
            "Note Interne",
            "Codice Fiscale",
            "Partita IVA",
            "Data di Nascita",
            "Provenienza Cliente",
            "Canale di Acquisizione",
        ]

        gruppi = [
            "Anagrafica",
            "Contatti",
            "Preferenze",
            "Fatturazione",
            "Note Operative",
        ]

        formati = [
            "^[A-Za-z]+$",
            "^[0-9]{5}$",
            "^[A-Z]{2}[0-9]{7}$",
            "",  # nessun formato richiesto (campo facoltativo)
        ]

        return {
            "etichetta": random.choice(etichette),
            "gruppo": random.choice(gruppi),
            "descrizione": fake.sentence(nb_words=10),
            "lunghezza": random.randint(10, 100),
            "formato": random.choice(formati),
        }

    @staticmethod
    def genera_dati_campi_personalizzati_nuovo_campo_univoco():
        """Come sopra, ma con etichetta resa univoca: da usare SOLO nel test
        che salva davvero, per evitare conflitti di duplicazione."""
        dati = ChainTestData.genera_dati_campi_personalizzati_nuovo_campo()
        dati["etichetta"] = f"{dati['etichetta']} {uuid.uuid4().hex[:6]}"
        return dati

    @staticmethod
    def genera_dati_campi_aggiuntivi_tipo_dato(n_opzioni: int = 3):
        return {
            "valore_minimo": random.randint(0, 10),
            "valore_massimo": random.randint(50, 200),
            "etichette_opzioni": [fake.word() for _ in range(n_opzioni)],
            "selezioni_minime": random.randint(1, 2),
            "selezioni_massime": random.randint(3, 5),
            "caratteri_per_voce": random.randint(50, 99),
            "voci_conservate": random.randint(1, 10),
        }

    @staticmethod
    def genera_dati_app_asporto():

        username = fake.user_name()

        return{
            "facebook": f"https://facebook.com/{username}",
            "instagram": f"https://instagram.com/{username}",
            "tik_tok": f"https://tiktok.com/@{username}",
            "google_maps": f"https://maps.google.com/?q={fake.city()}+{fake.street_name()}"
        }

    @staticmethod
    def genera_dati_app_asporto_tab_testi():

        return{
            "slogan": fake.catch_phrase(),
            "mess_benvenuto": fake.sentence(nb_words=6),
            "mess_orario_chiusura": "Siamo chiusi. " + fake.sentence(nb_words=5),
            "testo_footer": f"© {fake.company()} - {fake.year()}",
            "info_consegna": fake.paragraph(nb_sentences=2),
            "note_legali": fake.paragraph(nb_sentences=3),
        }

    @staticmethod
    def genera_dati_app_asporto_tab_loghi_e_immagini():

        return{
            "logo_principale": "https://picsum.photos/512/512",
            "logo_secondario": "https://picsum.photos/200/60",
            "favicon": "https://picsum.photos/32/32",
            "immagine_hero": "https://picsum.photos/1920/600",
            "pattern_sfondo": "https://picsum.photos/400/400",
        }

    @staticmethod
    def genera_dati_catalogo_app():

        return{
            "nome_menu_it": f"Menù {fake.word().capitalize()}",
            "nome_menu_ing": f"{fake.word().capitalize()} Menu",
            "prezzo_fisso": round(random.uniform(9.9, 39.9), 2),
            "descrizione_it": fake.sentence(nb_words=10),
            "url_img": "https://picsum.photos/400/300",
        }

    @staticmethod
    def genera_dati_date_disponibilita():
        """Genera un intervallo di date valido (inizio prima di fine) in formato YYYY-MM-DD."""
        data_inizio = fake.date_between(start_date="today", end_date="+30d")
        data_fine = fake.date_between(start_date=data_inizio, end_date="+90d")

        return {
            "data_inizio": data_inizio.strftime("%Y-%m-%d"),
            "data_fine": data_fine.strftime("%Y-%m-%d"),
        }

    @staticmethod
    def genera_dati_web_app_tavolo_catalogo():

        return{
            "descrizione": fake.sentence(nb_words=10),
            "ordine": random.randint(0, 10),
        }

    @staticmethod
    def genera_dati_registrazione_testi():
        """Genera un dataset di testi per il tab Testi di Webapp Registrazione Clienti."""

        return {
            "tagline": fake.catch_phrase(),
            "messaggio_benvenuto": fake.sentence(nb_words=6),
            "titolo_form": "Registrati ora",
            "titolo_successo": "Registrazione completata!",
            "messaggio_successo": fake.sentence(nb_words=8),
            "consenso_marketing": fake.sentence(nb_words=10),
            "footer": f"© {fake.company()} - {fake.year()}",
            "note_legali": fake.paragraph(nb_sentences=3),
        }

    @staticmethod
    def genera_dati_stampa_qr():

        return{
            "testo":fake.sentence(nb_words=8),
        }

    @staticmethod
    def genera_dati_nuova_campagna():

        attiva_dal = fake.date_between(start_date="+1d", end_date="+30d")
        fino_al = attiva_dal + timedelta(days=random.randint(30, 180))

        return{
        "nome_campagna": fake.catch_phrase(),
        "oggetto": fake.sentence(nb_words=6).rstrip("."),
        "nome_mittente": fake.name(),
        "rispondi_a": fake.company_email(),
        "riga_anteprima": fake.sentence(nb_words=8).rstrip("."),
        "messaggio": fake.paragraph(nb_sentences=3),
        "orario_invio": f"{random.randint(7, 20):02d}:{random.choice(['00', '15', '30', '45'])}",
        "attiva_dal": attiva_dal.strftime("%Y-%m-%d"),
        "fino_al": fino_al.strftime("%Y-%m-%d"),
        }

    @staticmethod
    def genera_dati_nuovo_segmento():

        punti_da = random.randint(0, 500)
        punti_a = punti_da + random.randint(50, 1000) 
        iscritti_dal = fake.date_between(start_date="-2y", end_date="-30d")
        iscritti_fino_al = iscritti_dal + timedelta(days=random.randint(1, 365))

        return{

            "nome": f"Segmento {fake.word().capitalize()} {random.randint(1000, 9999)}",
            "descrizione": fake.sentence(nb_words=10),
            "tag": fake.word(),
            "gruppo_cliente": random.choice(["VIP", "Standard", "Occasionali", "Fidelizzati", "Nuovi clienti"]),
            "citta": fake.city(),
            "punti_da": punti_da,
            "punti_a": punti_a,
            "iscritti_dal": iscritti_dal.strftime("%Y-%m-%d"),
            "iscritti_fino_al": iscritti_fino_al.strftime("%Y-%m-%d"),

        }
    @staticmethod
    def genera_dati_programma_ora_e_data():
        data = fake.date_time_between(start_date="+1d", end_date="+60d")
        return {
            "data_e_ora": data.strftime("%Y-%m-%dT%H:%M")
        }

    

    @staticmethod
    def genera_dati_deliveroo():

        fake = Faker("it_IT")
        TENANT_DEMO = "Bistrot Demo (reseller_demo_tenant_001)"

        return{
            "id": TENANT_DEMO,
            "tempo_preparazione": str(fake.random_int(min=10, max=60)),
            "ricarico_prezzo": str(fake.random_int(min=0, max=20)),
            "url_foto": fake.image_url(width=1920, height=1080),
        }

    @staticmethod
    def genera_dati_just_eat():

        fake = Faker("it_IT")
        TENANT_DEMO = "Bistrot Demo (reseller_demo_tenant_001)"

        return{
            "id": TENANT_DEMO,
            "tempo_preparazione": str(fake.random_int(min=10, max=60)),
            "ricarico_prezzo": str(fake.random_int(min=0, max=20)),
            "url_foto": fake.image_url(width=1920, height=1080),
        }

    @staticmethod
    def genera_dati_uber_eats():

        fake = Faker("it_IT")
        TENANT_DEMO = "Bistrot Demo (reseller_demo_tenant_001)"

        return{
            "id": TENANT_DEMO,
            "tempo_preparazione": str(fake.random_int(min=10, max=60)),
            "ricarico_prezzo": str(fake.random_int(min=0, max=20)),
            "url_foto": fake.image_url(width=1920, height=1080),
        }

    @staticmethod
    def genera_dati_glovo():

        fake = Faker("it_IT")
        TENANT_DEMO = "Bistrot Demo (reseller_demo_tenant_001)"

        return{
            "id": TENANT_DEMO,
            "tempo_preparazione": str(fake.random_int(min=10, max=60)),
            "ricarico_prezzo": str(fake.random_int(min=0, max=20)),
            "url_foto": fake.image_url(width=1920, height=1080),
        }

    @staticmethod
    def genera_dati_deliverect():

        fake = Faker("it_IT")
        TENANT_DEMO = "Bistrot Demo (reseller_demo_tenant_001)"

        return{
            "id": TENANT_DEMO,
            "tempo_preparazione": str(fake.random_int(min=10, max=60)),
            "ricarico_prezzo": str(fake.random_int(min=0, max=20)),
            "url_foto": fake.image_url(width=1920, height=1080),
        }
    @staticmethod
    def genera_dati_carta_fidelity():
        fake = Faker("it_IT")

        CLIENTI_DEMO = [
            "Becker, Crooks and Skiles",
            "Farrell, Ryan and Connelly",
            "Greenfelder, Mann and Schowalter",
            "Hane - Wisozk",
            "Heller - Bergnaum",
            "Hodkiewicz - Kulas",
            "Koelpin, Reichert and Klocko",
            "Legros LLC",
            "Mayer, Daugherty and Fahey",
            "Mayer, Denesik and Lakin",
            "McClure - Blanda",
            "Monahan, Harris and Huel",
            "Mraz Inc",
            "Murazik - West",
            "Nienow, Carroll and Koepp",
            "Quitzon LLC",
        ]

        punti = random.randint(0, 500)

        return {
            # workaround bug backend: barcode sempre valorizzato per evitare
            # E11000 duplicate key su barcode_unique_sparse (vedi nota bug)
            "barcode": f"BC{fake.unique.random_number(digits=10)}",
            "cliente": random.choice(CLIENTI_DEMO),
            "punti": punti,
            "credito": round(random.uniform(9.9, 39.9), 2),
            "moltiplicatore":random.randint(10, 100),
        }

    @staticmethod
    def genera_dati_campagna():
        fake = Faker("it_IT")

        attiva_dal = fake.date_between(start_date="+1d", end_date="+30d")
        fino_al = attiva_dal + timedelta(days=random.randint(30, 180))

        return {
            "nome": f"Campagna {fake.catch_phrase()}",
            "descrizione": fake.sentence(nb_words=10),
            "priorita": random.randint(0, 10),
            "attiva_dal": attiva_dal.strftime("%Y-%m-%d"),
            "fino_al": fino_al.strftime("%Y-%m-%d"),
        }

    @staticmethod
    def genera_dati_fascia_oraria():
        """Genera un intervallo orario valido (inizio prima di fine) in formato HH:MM,
        da usare per compilare una riga 'Fascia Oraria' in Programmazione Campagne."""
        ora_inizio_h = random.randint(6, 20)
        ora_inizio_m = random.choice(["00", "15", "30", "45"])
        ora_fine_h = random.randint(ora_inizio_h + 1, min(ora_inizio_h + 6, 23))
        ora_fine_m = random.choice(["00", "15", "30", "45"])

        return {
            "ora_inizio": f"{ora_inizio_h:02d}:{ora_inizio_m}",
            "ora_fine": f"{ora_fine_h:02d}:{ora_fine_m}",
        }

    @staticmethod
    def genera_dati_targeting_campagna():
        """Genera limiti di utilizzo realistici per il tab Targeting.
        Tutte le chiavi sono opzionali per compila_limiti_utilizzo, ma qui
        le generiamo sempre per esercitare i 4 campi nel test."""
        return {
            "max_utilizzi_totali": random.randint(50, 5000),
            "max_utilizzi_cliente": random.randint(1, 10),
            "importo_minimo_carrello": round(random.uniform(0, 30.0), 2),
            "sconto_massimo": round(random.uniform(5.0, 50.0), 2),
        }

    @staticmethod
    def genera_dati_premio():
        return {
            "nome": f"Premio {fake.word().capitalize()} {fake.word().capitalize()}",
            "descrizione": fake.sentence(nb_words=8),
            "punti_richiesti": random.randint(50, 5000),
            "valore_sconto": round(random.uniform(5, 100), 2),
            "stock": random.choice([-1, 10, 25, 50, 100]),
        }

    @staticmethod
    def genera_dati_premio_con_prodotti_gratis():
        return {
            "nome": f"Premio {fake.word().capitalize()} {fake.word().capitalize()}",
            "descrizione": fake.sentence(nb_words=8),
            "punti_richiesti": random.randint(50, 5000),
            "stock": random.choice([-1, 10, 25, 50, 100]),
            "max_utilizzi": random.choice([-1, 10, 25, 50, 100]),
            "valore": random.randint(50, 5000),
            "ordine minimo":round(random.uniform(0, 30.0), 2),
            "validita_giorni": random.randint(0, 29),
        }

    @staticmethod
    def genera_dati_nuovo_coupon():

        return{
            "valore": random.randint(50, 5000),
            "ordine minimo":round(random.uniform(0, 30.0), 2),
            "max_utilizzi": random.choice([-1, 10, 25, 50, 100]),
            "validita_giorni": random.randint(0, 29),
        }

    @staticmethod
    def genera_dati_buono():
     return {
        "valore": random.randint(10, 500),
        "validita_giorni": random.randint(1, 365),
        
    }

    @staticmethod
    def genera_dati_tier():

        return{
        "nome": f"Tier {fake.word().capitalize()}",
        "livello": random.randint(1, 10),
        "soglia_punti": random.randint(0, 5000),
        "moltiplicatore": round(random.uniform(1.0, 3.0), 1),
        "sconto": random.randint(0, 50),
        "mesi": random.choice([6, 12, 24]),
        "colore": random.choice(["grey", "blue", "green", "amber", "purple", "teal"]),
        "icona": random.choice(["mdi-medal", "mdi-star", "mdi-crown", "mdi-trophy", "mdi-shield-star"]),

        }

    @staticmethod
    def genera_dati_prepagata():
        """Genera limiti coerenti per il tab 'Prepagate' di Impostazioni Fidelity.

        Vincoli rilevati dall'HTML (Vuetify number field):
        - importo_minimo_ricarica: min=1, step=1 (default UI: 1)
        - importo_massimo_ricarica: min=1, step=1 (default UI: 250)
        - saldo_massimo_carta: min=1, step=1 (default UI: 2500)
        - scadenza_credito_mesi: min=0, step=1 (0 = nessuna scadenza, default UI: 0)

        Manteniamo minimo < massimo <= saldo massimo per evitare che il form
        rifiuti valori logicamente incoerenti (anche se la UI non lo valida
        esplicitamente, evitiamo falsi negativi nei test smoke).
        """

        importo_minimo_ricarica = random.randint(1, 10)
        importo_massimo_ricarica = random.randint(importo_minimo_ricarica + 50, importo_minimo_ricarica + 300)
        saldo_massimo_carta = random.randint(importo_massimo_ricarica + 500, importo_massimo_ricarica + 5000)
        scadenza_credito_mesi = random.choice([0, 6, 12, 24, 36])

        return {
            "importo_minimo_ricarica": importo_minimo_ricarica,
            "importo_massimo_ricarica": importo_massimo_ricarica,
            "saldo_massimo_carta": saldo_massimo_carta,
            "scadenza_credito_mesi": scadenza_credito_mesi,
        }
    @staticmethod
    def genera_dati_report_page():
        """Genera un dataset per 'Impostazioni Template', 'Test Parametri' e
        'Personalizza Header e Footer' dell'editor Report."""

        tipi_dataset = [
            "SALES_MASTER", "SALES_TRENDS", "PRODUCT_MIX", "INVENTORY_LOG",
            "STAFF_PERFORMANCE", "FIDELITY_INSIGHTS", "CUSTOMER_SEGMENT",
            "HOURLY_PERFORMANCE", "BOOKINGS",
        ]

        data_da = fake.date_between(start_date="-90d", end_date="-30d")
        data_a = fake.date_between(start_date="-29d", end_date="today")

        return {
            "nome_template": f"Report {fake.catch_phrase()}",
            "tipo_dataset": random.choice(tipi_dataset),
            "master_template": random.choice(["default-master.html", "minimal-master.html"]),
            "descrizione": fake.sentence(nb_words=10),
            "data_da": data_da.strftime("%Y-%m-%d"),
            "data_a": data_a.strftime("%Y-%m-%d"),
            "granularita": random.choice(["day", "week", "month"]),
            "limite_righe": random.choice([50, 100, 200, 500]),
            "titolo_report": f"Report {fake.word().capitalize()}",
            "sottotitolo": f"Periodo dal {data_da.strftime('%d/%m/%Y')} al {data_a.strftime('%d/%m/%Y')}",
            "url_logo": "",  # vuoto = usa logo del tenant (comportamento di default documentato in UI)
            "allineamento_header": random.choice(["left", "center", "right"]),
            "testo_footer": fake.sentence(nb_words=6),
            "mostra_data_generazione": True,
            "mostra_numero_pagina": True,
        }
    @staticmethod
    def genera_dati_schedulazione_nuova():
        faker = Faker("it_IT")
        return {
            "nome": f"Schedulazione {faker.word().capitalize()} {faker.random_int(100, 999)}",
            "seleziona_template": True,
            "canali_invio_extra": [],
            "destinatari_email": [faker.company_email() for _ in range(random.randint(1, 3))],
            "frequenza": None,
            "espressione_cron": None,
            "formato_report": None,
            "abilitato": True,
            "oggetto_email": f"Report {faker.word().capitalize()} del {{{{meta.scheduledAt}}}}",
            "corpo_email": faker.paragraph(nb_sentences=2),
        }
    @staticmethod
    def genera_dati_nuovo_spreco():

        faker = Faker("it_IT")

        return{
            "quantita": round(random.uniform(3.5, 25.0), 2),
            "note": faker.paragraph(nb_sentences=2),
        }


        