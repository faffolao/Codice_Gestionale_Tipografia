from Gestione.Database import Database


class GestioneOrdini:
    def __init__(self):
        self.lista_ordini = []

    def carica_lista_ordini(self):
        db_con = Database("system.db")
        self.lista_ordini = db_con.get_lista_ordini()

    def conta_ordini(self):
        return len(self.lista_ordini)

    def get_lista_ordini(self):
        return self.lista_ordini