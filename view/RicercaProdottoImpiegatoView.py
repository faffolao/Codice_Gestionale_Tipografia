from PyQt5 import uic
from PyQt5.QtWidgets import QDialog


class RicercaProdottoImpiegatoView(QDialog):
    SEARCH_BY_ID = 0
    SEARCH_BY_NAME = 1

    def __init__(self, parent):
        # inizializzazione finestra
        super(RicercaProdottoImpiegatoView, self).__init__(parent)
        uic.loadUi('ui/ricerca_prodotto_impiegato.ui', self)
        # uso i segnali di ritorno di QDialog: accept significa che ciò che il dialog ha chiesto è stato inserito,
        # in questo caso la query di ricerca; reject il contrario, ovvero che il dialog è stato rifiutato ed è stato
        # premuto annulla.
        self.btn_search.clicked.connect(self.conferma)
        self.btn_cancel.clicked.connect(lambda: self.reject())

    def get_search_type(self):
        if self.radio_search_by_name.isChecked():
            return self.SEARCH_BY_NAME
        elif self.radio_search_by_id.isChecked():
            return self.SEARCH_BY_ID

    def get_query(self):
        return self.txt_search_query.text()

    def conferma(self):
        if self.txt_search_query.text() != '':
            self.accept()
