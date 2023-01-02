from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QDialog, QFileDialog
from view.MsgBoxView import MsgBox
from ECommerce.Prodotto import Prodotto


class AggiungiProdottoView(QDialog):
    def __init__(self, prod_manager):
        super(AggiungiProdottoView, self).__init__()
        uic.loadUi('ui/aggiungi_prodotto.ui', self)

        self.prod_manager = prod_manager

        self.btn_select_image.clicked.connect(self.select_image)
        self.btn_aggiungi_prod.clicked.connect(self.aggiungi)
        self.btn_annulla.clicked.connect(self.annulla)

    def aggiungi(self):
        titolo = self.txt_prod_title.text()
        descrizione = self.txt_prod_description.text()
        prezzo = self.txt_prezzo.value()
        quantita = self.txt_prod_quantita.value()

        if not titolo or not descrizione or not prezzo or not quantita or not self.dati_immagine:
            msg = MsgBox()
            msg.show_error_msg("Per poter inserire un prodotto è necessario compilare tutti i campi richiesti.")
            return
        else:
            prodotto = Prodotto(descrizione, 0, self.dati_immagine, prezzo, quantita, titolo)
            self.prod_manager.aggiungi(prodotto)

        self.accept()

    def annulla(self):
        self.reject()

    def select_image(self):
        filename, _ = QFileDialog.getOpenFileName(self)
        with open(filename, "rb") as file_immagine:
            self.dati_immagine = file_immagine.read()

        pix = QPixmap()
        pix.loadFromData(self.dati_immagine)
        self.lbl_selected_img.setPixmap(pix.scaledToHeight(101))
