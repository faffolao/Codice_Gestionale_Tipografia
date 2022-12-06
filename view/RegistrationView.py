import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QDialog, QWidget


class RegistrationView(QWidget):
    def __init__(self, main_ctrl):
        print("ciao2")
        super(RegistrationView, self).__init__()
        self.__controller = main_ctrl
        uic.loadUi('ui/reg2.ui', self)
        self.show()
        self.setFixedSize(self.size())
        #self.btn_login.clicked.connect(self.login)
