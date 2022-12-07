from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

from view.RegistrationView import RegistrationView
from view.MsgBoxView import MsgBox


class LoginView(QMainWindow):
    def __init__(self, access_ctrl):
        # inizializzazione finestra
        super(LoginView, self).__init__()

        # associazione controller a questa vista
        self.__controller = access_ctrl

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

        self.__controller.login(username, password, self)

    def registrazione(self):
        register = RegistrationView(self.__controller, self)
        register.exec_()
        self.close()
