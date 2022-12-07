from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QWidget

from Utenti.Utente import Utente
from view.HomePageClienteView import HomePageClienteView
from view.MsgBoxView import MsgBox


# [!!!!!!!] sono ardu: a cosa serve usare QObject qui? [!!!!!!]
# [!!!!!!!] sono Rocco: vediti https://www.html.it/pag/72800/la-classe-qobject/ [!!!!!!]


# eredito dalla classe QObject e lo inizializzo come controller
class GestioneAccessi(QObject):
    def __init__(self, db_connection):
        super().__init__()
        self.currentView = None
        self.db_con = db_connection

    utente_connesso = None

    def get_utente_connesso(self):
        return self.utente_connesso

    def login(self, username: str, password: str, parent: QWidget) -> bool:
        login_accepted = self.db_con.verify_user(username, password)
        if login_accepted:
            print("Login effettuato correttamente!")
            self.currentView = HomePageClienteView(self)
            parent.close()
            '''
            if():
                self.homePage = HomePageClienteView(self)
            else if():
                self.homePage = HomePageImpiegatoView(self)
            '''
        elif not login_accepted:
            msg = MsgBox()
            msg.show_error_msg("Nome utente o password errati.")

    def logout(self):
        self.utente_connesso = None

    def registrazione(self, utente: Utente):
        self.db_con.inserisci_utente(utente, "cliente")
        print(self.db_con.get_lista_utenti())
