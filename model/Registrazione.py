from PyQt5.QtWidgets import QDialog


class Registrazione(QDialog):

    def __init__(self):
        super(Registrazione, self).__init__()
        self.loadUi('../ui/registrazione.ui', self)
