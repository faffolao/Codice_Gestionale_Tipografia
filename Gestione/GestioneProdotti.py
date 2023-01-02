from Gestione.Database import Database
from Gestione.GestioneTipografia import GestioneTipografia
from view.MsgBoxView import MsgBox


class GestioneProdotti(GestioneTipografia):
    def __init__(self):
        super(GestioneProdotti).__init__()

    def aggiungi(self, prod):
        db_con = Database("system.db")
        db_con.inserisci_prodotto(prod)

    def carica_lista(self):
        db_con = Database("system.db")
        self.lista = db_con.get_catalogo()

    def rimuovi(self, prod_id):
        x = self.ricerca_per_id(prod_id)

        if x is None:
            msg = MsgBox()
            msg.show_error_msg("Il prodotto che si desidera rimuovere non è presente in catalogo.")
        else:
            db_con = Database("system.db")
            db_con.rimuovi_prodotto(prod_id)

    def ricerca_per_id(self, id):
        for prod in self.lista:
            if prod.get_id() == id:
                return prod

        return None

    def ricerca(self, nome):
        for prod in self.lista:
            # controllo se la sottostringa nome è contenuta all'interno del nome completo del prodotto (nome_prod)
            nome_prod = prod.get_titolo()
            if nome in nome_prod:
                return prod

        return None

    def modifica_prodotto(self, new_prod):
        db_con = Database("system.db")
        db_con.aggiorna_prodotto(new_prod)
