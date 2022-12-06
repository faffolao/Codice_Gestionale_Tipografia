import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow

from view.RegistrationView import RegistrationView


class LoginView(QMainWindow):
    def __init__(self, main_ctrl):
        super(LoginView, self).__init__()
        self.__controller = main_ctrl
        uic.loadUi('ui/login_form.ui', self)
        self.show()
        self.setFixedSize(self.size())
        self.btn_login.clicked.connect(self.login)
        self.btn_register.clicked.connect(self.registrazione)

    def login(self):
        nome = self.txt_username.text()
        self.__controller.login(nome, "password")

    def registrazione(self):
        print("ciao")
        register = RegistrationView(self.__controller)



