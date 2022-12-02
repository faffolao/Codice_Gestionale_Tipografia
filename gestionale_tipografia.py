from PyQt5 import QtWidgets, uic
import sys
from PyQt5.QtWidgets import QPushButton, QDialog, QMainWindow

from model.Registrazione import Registrazione


class Ui(QMainWindow):

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('ui/login_form.ui', self)
        self.show()
        self.setFixedSize(self.size())
        self.btn_register.clicked.connect(self.register)

    def register(self):
        self.register = Registrazione()
        self.register.exec()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()
