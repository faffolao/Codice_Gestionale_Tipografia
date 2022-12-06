from Utenti.Utente import Utente


class Cliente(Utente):
    def __init__(self, id, nome, cognome, username, password, email, cellulare, data_nascita):
        super.__init__(id, nome, cognome, username, password, email, cellulare, data_nascita)

    # dovrà arrivare il carrello...
