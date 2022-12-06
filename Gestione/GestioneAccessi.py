from PyQt5.QtCore import QObject

from Utenti.Utente import Utente


#   eredito dalla classe QObject e lo inizializzo come controller
class GestioneAccessi(QObject):
    def __init__(self):
        super().__init__()

    utente_connesso = None

    def get_utente_connesso(self):
        return self.utente_connesso

    def login(self, str, str1) -> bool:
        print(str)

    def logout(self):
        self.utente_connesso = None

    def registrazione(self, utente: Utente) -> bool:
        return True
