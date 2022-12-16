from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QAbstractItemView, QTableWidget

from ECommerce.Catalogo import Catalogo
from view.MsgBoxView import MsgBox


class CatalogoView(QMainWindow):
    def __init__(self):
        # inizializzazione finestra
        super(CatalogoView, self).__init__()

        uic.loadUi('ui/catalogo_prodotti.ui', self)

        # imposto la selezione a intera riga e non a cella singola nella tabella del catalogo
        self.table_catalogo.setSelectionBehavior(QAbstractItemView.SelectRows)
        # disabilito la possibilità di modificare le celle della tabella liberamente
        self.table_catalogo.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # evento selezione di una riga
        self.table_catalogo.cellClicked.connect(self.get_selected_prod)
        # eventi dei pulsanti
        self.btn_visualizza_dettagli.clicked.connect(self.get_dettagli_prod)

        # caricamento del catalogo
        self.catalogo = Catalogo()
        lista_prodotti = self.catalogo.get_lista_prodotti()

        # visualizzazione catalogo a schermo
        self.table_catalogo.setRowCount(len(lista_prodotti))
        num_riga = 0
        for prod in lista_prodotti:
            # gli item della qtablewidget devono essere obbligatoriamente delle stringhe, quindi vado a castare
            # i valori numerici in stringhe per renderli visibili in tabella
            prod_id = QTableWidgetItem(str(prod.get_id()))
            prod_title = QTableWidgetItem(prod.get_titolo())
            prod_qta = QTableWidgetItem(str(prod.get_quantita()))
            prod_price = QTableWidgetItem(str(prod.get_prezzo()))

            self.table_catalogo.setItem(num_riga, 0, prod_id)
            self.table_catalogo.setItem(num_riga, 1, prod_title)
            self.table_catalogo.setItem(num_riga, 2, prod_qta)
            self.table_catalogo.setItem(num_riga, 3, prod_price)

            num_riga += 1

    def get_selected_prod(self):
        # ottengo l'id del prodotto selezionato
        selected_row = self.table_catalogo.currentRow()
        self.selected_prod_id = int(self.table_catalogo.item(selected_row, 0).text())

        # abilito i pulsanti disabilitati
        self.btn_visualizza_dettagli.setEnabled(True)
        self.btn_aggiungi_al_carrello.setEnabled(True)

    def get_dettagli_prod(self):
        prod = self.catalogo.ricerca_per_id(self.selected_prod_id)

        if prod is not None:
            # TODO: mettere la vista dettagli prodotto
            print(prod)
        else:
            msg = MsgBox()
            msg.show_error_msg("Il prodotto non è stato trovato, probabilmente non è stato selezionato alcun prodotto")
