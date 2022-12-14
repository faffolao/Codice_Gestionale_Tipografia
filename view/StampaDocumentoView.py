from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow


class StampaDocumentoView(QMainWindow):
    def __init__(self, cliente_obj):
        # inizializzazione finestra
        super(StampaDocumentoView, self).__init__()

        self.cliente = cliente_obj

        uic.loadUi('ui/stampa_documento.ui', self)
        self.setFixedSize(self.size())

        self.btn_scegli_doc.clicked.connect(self.seleziona_file)
        self.btn_invia_stampa.clicked.connect(self.invia_stampa)

    def seleziona_file(self):
        pass

    def invia_stampa(self):
        pass
