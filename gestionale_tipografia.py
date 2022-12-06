import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow


class Ui(QMainWindow):

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('ui/login_form.ui', self)
        self.show()
        self.setFixedSize(self.size())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()
