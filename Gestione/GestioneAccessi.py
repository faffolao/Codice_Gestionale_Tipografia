from PyQt5.QtCore import QObject
from Utenti.Utente import Utente
from view.MsgBoxView import MsgBox


# [!!!!!!!] sono ardu: a cosa serve usare QObject qui? [!!!!!!]

# eredito dalla classe QObject e lo inizializzo come controller
class GestioneAccessi(QObject):
    def __init__(self, db_connection):
        super().__init__()
        self.db_con = db_connection

    utente_connesso = None

    def get_utente_connesso(self):
        return self.utente_connesso

    def login(self, username, password) -> bool:
        login_accepted = self.db_con.verify_user(username, password)
        if login_accepted:
            print("Login effettuato correttamente!")
        elif not login_accepted:
            msg = MsgBox()
            msg.show_error_msg("Nome utente o password errati.")

    def logout(self):
        self.utente_connesso = None

    def registrazione(self, utente: Utente):
        self.db_con.inserisci_utente(utente, "cliente")
