from PyQt5 import uic
from PyQt5.QtWidgets import QDialog


class RicercaUtenteView(QDialog):
    def __init__(self, parent):
        # inizializzazione finestra
        super(RicercaUtenteView, self).__init__(parent)
        uic.loadUi('ui/ricerca_utente.ui', self)

        self.btn_search.clicked.connect(self.conferma)
        self.btn_cancel.clicked.connect(lambda: self.reject())

    def get_query(self):
        return self.txt_query.text()

    def conferma(self):
        if self.txt_query.text() != '':
            self.accept()
