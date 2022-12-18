from ECommerce.Carrello import Carrello
from Utenti.Utente import Utente


class Cliente(Utente):
    def __init__(self, id, nome, cognome, username, password, email, cellulare, data_nascita):
        super().__init__(id, nome, cognome, username, password, email, cellulare, data_nascita)
        # inizializzazione carrello cliente
        self.carrello_prodotti = Carrello()

    def get_carrello_prodotti(self):
        return self.carrello_prodotti
