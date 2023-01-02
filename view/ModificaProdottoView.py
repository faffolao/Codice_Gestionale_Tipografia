from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtCore import Qt
from ECommerce.Prodotto import Prodotto
from ECommerce.Catalogo import Catalogo


class ModificaProdottoView(QDialog):
    def __init__(self, prod_manager, prodotto):
        super(ModificaProdottoView, self).__init__()
        uic.loadUi('ui/modifica_prodotto.ui', self)

        self.prod_manager = prod_manager
        self.prodotto = prodotto

        self.txt_prod_title.setText(self.prodotto.get_titolo())
        self.txt_prod_description.setText(self.prodotto.get_descrizione())
        self.txt_prezzo.setValue(self.prodotto.get_prezzo())
        self.txt_prod_quantita.setValue(self.prodotto.get_quantita())
        self.immagine_prodotto = prodotto.get_immagine()
        self.lbl_selected_img.setPixmap(prodotto.get_immagine_rendered(181, 101))

        self.btn_annulla.clicked.connect(self.reject)
        self.btn_edit_prod.clicked.connect(self.accetta_modifiche)
        self.btn_select_image.clicked.connect(self.select_image)

    def accetta_modifiche(self):
        self.prodotto.titolo = self.txt_prod_title.text()
        self.prodotto.descrizione = self.txt_prod_description.text()
        self.prodotto.prezzo = self.txt_prezzo.value()
        self.prodotto.quantita = self.txt_prod_quantita.value()
        self.prodotto.immagine = self.immagine_prodotto

        self.prod_manager.modifica_prodotto(self.prodotto)

        self.accept()

    def select_image(self):
        filename, _ = QFileDialog.getOpenFileName(self)
        with open(filename, "rb") as file_immagine:
            self.immagine_prodotto = file_immagine.read()

        pix = QPixmap()
        pix.loadFromData(self.immagine_prodotto)
        self.lbl_selected_img.setPixmap(pix.scaled(181, 101, Qt.KeepAspectRatio))
