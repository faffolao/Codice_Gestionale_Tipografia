from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

import view.HomePageClienteView as HPCV
from Utenti.Cliente import Cliente
from Utenti.Impiegato import Impiegato

from view.RegistrationView import RegistrationView
from view.MsgBoxView import MsgBox


class LoginView(QMainWindow):
    def __init__(self, login_manager_model):
        # inizializzazione finestra
        super(LoginView, self).__init__()

        # associazione controller a questa vista
        self.login_manager = login_manager_model

        uic.loadUi('ui/login_form.ui', self)
        self.show()
        self.setFixedSize(self.size())

        # mapping delle funzioni agli eventi click dei pulsanti
        self.btn_login.clicked.connect(self.login)
        self.btn_register.clicked.connect(self.registrazione)

    def login(self):
        # ottengo i dati inseriti
        username = self.txt_username.text()
        password = self.txt_password.text()

        if not username or not password:
            msg = MsgBox()
            msg.show_error_msg("Inserire nome utente e/o password.")

            return

        if self.login_manager.login(username, password):
            user_type = self.login_manager.get_utente_connesso()

            if isinstance(user_type, Cliente):
                self.customer_home = HPCV.HomePageClienteView(self.login_manager)
                self.customer_home.show()
            elif isinstance(user_type, Impiegato):
                print("la parte del'impiegato arriverà più avanti...")

            self.close()

    def registrazione(self):
        register = RegistrationView(self.login_manager, self)
        register.show()
