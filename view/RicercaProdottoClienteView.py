from PyQt5 import uic
from PyQt5.QtWidgets import QDialog


class RicercaProdottoClienteView(QDialog):
    def __init__(self, parent):
        # inizializzazione finestra
        super(RicercaProdottoClienteView, self).__init__(parent)
        uic.loadUi('ui/ricerca_prodotto_cliente.ui', self)
        # uso i segnali di ritorno di QDialog: accept significa che ciò che il dialog ha chiesto è stato inserito,
        # in questo caso la query di ricerca; reject il contrario, ovvero che il dialog è stato rifiutato ed è stato
        # premuto annulla.
        self.btn_search.clicked.connect(lambda: self.accept())
        self.btn_cancel.clicked.connect(lambda: self.reject())

    def get_query(self):
        return self.txt_query.text()
