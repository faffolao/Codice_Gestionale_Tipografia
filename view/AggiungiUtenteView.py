from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

from Utenti.Impiegato import Impiegato
from view.MsgBoxView import MsgBox


class AggiungiUtenteView(QDialog):
    def __init__(self, usr_manager, parent):
        super(AggiungiUtenteView, self).__init__(parent)
        uic.loadUi('ui/aggiungi_utente.ui', self)

        self.usr_manager = usr_manager

        self.btn_cancel.clicked.connect(lambda: self.reject())
        self.btn_add_new_user.clicked.connect(self.aggiungi_utente)

    def aggiungi_utente(self):
        # controllo che i campi fondamentali siano stati inseriti
        username = self.txt_username.text()
        password = self.txt_password.text()
        nome = self.txt_nome.text()
        cognome = self.txt_cognome.text()
        email = self.txt_email.text()

        data_nascita = self.txt_data_nascita.text()
        cell = self.txt_cell.text()

        if username == "" or password == "" or nome == "" or cognome == "" or email == "":
            msg = MsgBox()
            msg.show_error_msg("Riempire tutti i campi obbligatori, presenti nella sezione Dati principali.")
        else:
            self.usr_manager.aggiungi(Impiegato(1, nome, cognome, username, password, email, cell, data_nascita, False))
            self.accept()
