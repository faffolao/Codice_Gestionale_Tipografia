import Gestione.Database as DB
from ECommerce.Prodotto import Prodotto


class Carrello:
    def __init__(self):
        self.prodotti = []

    def get_lista_prodotti(self):
        return self.prodotti

    def carica_carrello(self, id):
        db_con = DB.Database("system.db")
        self.prodotti = db_con.get_carrello_cliente(id)

    def get_num_prod(self):
        return len(self.prodotti)

    def get_prod(self, id):
        for prod in self.prodotti:
            if prod.get_id() == id:
                return prod

        return None

    def aggiungi(self, prod, id_user):
        x = self.get_prod(prod.get_id())
        if x is not None:
            x.incrementa_quantita()
        else:
            prod_da_ins = Prodotto(prod.get_descrizione(), prod.get_id(), prod.get_immagine(), prod.get_prezzo(), 1,
                                   prod.get_titolo())
            self.prodotti.append(prod_da_ins)

        db_con = DB.Database("system.db")
        db_con.aggiorna_carrello(self, id_user)

    def rimuovi(self, prod_id, user_id):
        # ottengo prodotto selezionato
        prod = self.get_prod(prod_id)

        # se il prodotto selezionato ha quantità > 1...
        if prod.get_quantita() > 1:
            # ...gli scalo 1 quantità, senza toglierlo dal carrello
            prod.scala_quantita()
        elif prod.get_quantita() <= 1:
            # ricerco il prodotto da rimuovere dal carrello...
            for x in self.prodotti:
                if x.get_id() == prod_id:
                    # ... e lo rimuovo
                    self.prodotti.remove(x)

        # aggiorno il carrello sul database
        db_con = DB.Database("system.db")
        db_con.aggiorna_carrello(self, user_id)