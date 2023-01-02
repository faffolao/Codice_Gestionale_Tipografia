from Gestione.Database import Database
from Gestione.GestioneTipografia import GestioneTipografia


class GestioneUtenti(GestioneTipografia):
    def __init__(self):
        super(GestioneUtenti).__init__()

    def carica_lista(self):
        db_con = Database("system.db")
        self.lista = db_con.get_lista_impiegati()

    def aggiungi(self, usr):
        db_con = Database("system.db")
        db_con.inserisci_utente(usr, "impiegato")

    def rimuovi(self, id):
        db_con = Database("system.db")
        db_con.rimuovi_utente(id)

    def ricerca(self, query):
        for usr in self.lista:
            if usr.get_username() == query:
                return usr

        return None
