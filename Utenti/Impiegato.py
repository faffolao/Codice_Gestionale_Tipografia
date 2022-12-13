from Utenti.Utente import Utente

class Impiegato(Utente):

    def __init__(self, id, nome, cognome, username, password, email, cellulare, data_nascita, is_admin):
        super().__init__(id, nome, cognome, username, password, email, cellulare, data_nascita)
        self.amministratore = is_admin

    def is_admin(self):
        return self.amministratore
