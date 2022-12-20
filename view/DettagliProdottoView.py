from PyQt5 import uic
from PyQt5.QtWidgets import QDialog


class DettagliProdottoView(QDialog):
    def __init__(self, parent, prodotto):
        # inizializzazione finestra
        super(DettagliProdottoView, self).__init__(parent)
        uic.loadUi('ui/dettagli_prodotto.ui', self)
        self.btn_close.clicked.connect(lambda: self.close())

        # caricamento dei dettagli del prodotto
        # TODO: in particolar modo mi rivolgo a luca, come faccio a far vedere l'immagine del prodotto?
        self.lbl_prod_title.setText(prodotto.get_titolo())
        self.lbl_prod_price.setText(str(prodotto.get_prezzo()) + "€")
        self.lbl_prod_details.setText(f"ID: {prodotto.get_id()} - {prodotto.get_quantita()} pezzi rimasti in magazzino")
        self.lbl_prod_description.setText(prodotto.get_descrizione())
        self.prod_image.setPixmap(prodotto.get_immagine_rendered())
