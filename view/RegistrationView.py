from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

from Utenti.Cliente import Cliente
import view.HomePageClienteView as HPCV
from view.MsgBoxView import MsgBox


class RegistrationView(QDialog):
    def __init__(self, login_manager_model, parent):
        super(RegistrationView, self).__init__(parent)

        uic.loadUi('ui/registrazione.ui', self)
        self.setFixedSize(self.size())

        self.login_manager = login_manager_model

        self.btn_registrati.clicked.connect(self.registrazione_utente)
        self.btn_annulla.clicked.connect(lambda: self.close())

    def registrazione_utente(self):
        username = self.txt_username.text()
        password = self.txt_password.text()
        nome = self.txt_nome.text()
        cognome = self.txt_cognome.text()
        email = self.txt_email.text()
        cellulare = self.txt_cellulare.text()
        data_nascita = self.data_nascita_input.text()

        if self.check_fields(username, password, nome, cognome, email, cellulare):
            usr = Cliente(None, nome, cognome, username, password, email, cellulare, data_nascita)
            self.login_manager.registrazione(usr)

            self.home_page_customer = HPCV.HomePageClienteView(self.login_manager)
            self.home_page_customer.show()

            self.close()
            self.parent().close()
        else:
            msg = MsgBox()
            msg.show_error_msg("Per potersi registrare è necessario riempire i campi obbligatori (sono obbligatori "
                               "tutti i campi eccetto Data di nascita).")

    def check_fields(self, username, password, nome, cognome, email, cellulare):
        # nota: le stringhe vuote sono considerate come dei valori False
        if not username or not password or not nome or not cognome or not email or not cellulare:
            return False
        else:
            return True
