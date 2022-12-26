from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

from view.MsgBoxView import MsgBox


class FinalizzaAcquistoView(QDialog):
    def __init__(self):
        # inizializzazione finestra
        super(FinalizzaAcquistoView, self).__init__()
        uic.loadUi('ui/finalizza_acquisto.ui', self)

        self.btn_finalizza_acquisto.clicked.connect(self.conferma_dati_spedizione)
        self.btn_annulla_ordine.clicked.connect(self.annulla_ordine)

    def get_dati_spedizione(self):
        ds = {
            "via": self.txt_via.text(),
            "num_civico": self.txt_num_civico.text(),
            "cap": self.txt_cap.text(),
            "citta": self.txt_citta.text()
        }

        return ds

    def annulla_ordine(self):
        msg = MsgBox()
        if msg.show_yes_no_msg("Desideri annullare l'ordine?"):
            self.reject()

    def conferma_dati_spedizione(self):
        via = self.txt_via.text()
        num_civico = self.txt_num_civico.text()
        cap = self.txt_cap.text()
        citta = self.txt_citta.text()

        if not via or not num_civico or not cap or not citta:
            msg = MsgBox()
            msg.show_error_msg("Per procedere con l'ordine è necessario riempire tutti i campi di questa finestra.")
        else:
            self.accept()
