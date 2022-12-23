from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QAbstractItemView

from Gestione.Database import Database
from view.MsgBoxView import MsgBox


class CarrelloView(QMainWindow):
    def __init__(self, cliente_obj, parent):
        # inizializzazione finestra
        super(CarrelloView, self).__init__(parent)
        uic.loadUi('ui/carrello.ui', self)
        self.cliente = cliente_obj

        # carico il carrello
        self.carrello = cliente_obj.get_carrello_prodotti()
        self.carrello.carica_carrello(cliente_obj.get_id())

        # impostazioni per la visualizzazione degli elementi nella tabella
        self.table_carrello.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_carrello.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # mapping click pulsante elimina dal carrello
        self.btn_remove_prod.clicked.connect(self.elimina_dal_carrello)

        # evento selezione di una riga
        self.table_carrello.cellClicked.connect(self.get_selected_prod)

        # visualizzo il carrello a schermo
        self.carica_carrello()

    def carica_carrello(self):
        self.table_carrello.setRowCount(0)
        self.table_carrello.setRowCount(self.carrello.get_num_prod())

        num_riga = 0
        for prod in self.carrello.get_lista_prodotti():
            # gli item della qtablewidget devono essere obbligatoriamente delle stringhe, quindi vado a castare
            # i valori numerici in stringhe per renderli visibili in tabella
            prod_id = QTableWidgetItem(str(prod.get_id()))
            prod_title = QTableWidgetItem(prod.get_titolo())
            prod_qta = QTableWidgetItem(str(prod.get_quantita()))
            prod_price = QTableWidgetItem(str(prod.get_prezzo()) + "€")

            self.table_carrello.setItem(num_riga, 0, prod_id)
            self.table_carrello.setItem(num_riga, 1, prod_title)
            self.table_carrello.setItem(num_riga, 2, prod_qta)
            self.table_carrello.setItem(num_riga, 3, prod_price)

            num_riga += 1

    def elimina_dal_carrello(self):
        msg = MsgBox()
        if msg.show_yes_no_msg("Desideri rimuovere il prodotto selezionato dal carrello?"):
            # rimuovo il prodotto dal carrello
            self.carrello.rimuovi(self.selected_prod_id, self.cliente.get_id())
            # aggiorno l'elenco dei prodotti in carrello
            self.carica_carrello()
            # aumento la quantità del prodotto rimosso dal carrello
            prod_da_aumentare = self.parent().catalogo.ricerca_per_id(self.selected_prod_id)
            prod_da_aumentare.incrementa_quantita()

            db_con = Database("system.db")
            db_con.modifica_quantita_prodotto(prod_da_aumentare)
            # aggiorno l'elenco dei prodotti nel catalogo
            self.parent().carica_catalogo(self.parent().catalogo.get_lista_prodotti())

    def get_selected_prod(self):
        # ottengo l'id del prodotto selezionato
        selected_row = self.table_carrello.currentRow()
        self.selected_prod_id = int(self.table_carrello.item(selected_row, 0).text())

        # abilito il pulsante per rimuovere un prodotto dal carrello
        self.btn_remove_prod.setEnabled(True)
