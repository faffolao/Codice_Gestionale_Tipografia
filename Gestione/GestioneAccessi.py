from PyQt5.QtCore import QObject

from Gestione.Database import Database
from Utenti.Utente import Utente
from view.MsgBoxView import MsgBox


class GestioneAccessi(QObject):
    def __init__(self):
        super().__init__()

    utente_connesso = None

    def get_utente_connesso(self):
        return self.utente_connesso

    def login(self, username: str, password: str) -> bool:
        db_con = Database("system.db")
        login_accepted = db_con.verify_user(username, password)

        if login_accepted:
            self.utente_connesso = db_con.get_dettagli_utente(username)
            return True
        elif not login_accepted:
            msg = MsgBox()
            msg.show_error_msg("Nome utente o password errati.")
            return False

    def logout(self):
        self.utente_connesso = None

    def registrazione(self, utente: Utente):
        db_con = Database("system.db")
        db_con.inserisci_utente(utente, "cliente")

        self.utente_connesso = db_con.get_dettagli_utente(utente.get_username())
