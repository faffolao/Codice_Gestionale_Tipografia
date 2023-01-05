from typing import Iterable

from ECommerce.Carrello import Carrello
from Utenti.Utente import Utente


class Cliente(Utente):
    def __init__(self, id, nome, cognome, username, password, email, cellulare, data_nascita):
        super().__init__(id, nome, cognome, username, password, email, cellulare, data_nascita)
        # inizializzazione carrello cliente
        self.carrello_prodotti = Carrello()

    def get_carrello_prodotti(self):
        return self.carrello_prodotti

    def __eq__(self, other):
        if not isinstance(other, Cliente):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.nome == other.nome and self.cognome == other.cognome and self.username == other.username and self.password == other.password and self.email == other.email and int(self.cellulare) == int(other.cellulare) and self.data_nascita == other.data_nascita

    def __dir__(self) -> Iterable[str]:
        return [self.nome, self.cognome, self.username, self.password, self.email, self.cellulare, self.data_nascita]
