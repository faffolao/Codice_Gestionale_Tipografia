from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QAbstractItemView, QDialog
from ECommerce.Catalogo import Catalogo
import view.AggiungiProdottoView as APV
import view.ModificaProdottoView as MPV
from Gestione.GestioneProdotti import GestioneProdotti
from view.MsgBoxView import MsgBox
from view.RicercaProdottoImpiegatoView import RicercaProdottoImpiegatoView


class GestioneProdottiView(QMainWindow):
    def __init__(self):
        super(GestioneProdottiView, self).__init__()
        uic.loadUi('ui/gestione_prodotti.ui', self)

        self.selected_prod_id = None
        self.prod_manager = GestioneProdotti()
        self.prod_manager.carica_lista()

        self.table_prodotti.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_prodotti.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.btn_add_prod.clicked.connect(self.aggiungi_prodotto)
        self.btn_delete_selected.clicked.connect(self.rimuovi_prodotto)
        self.btn_edit_selected.clicked.connect(self.modifica_prodotto)
        self.btn_search_prod.clicked.connect(self.ricerca_prodotto)
        # evento selezione di una riga
        self.table_prodotti.cellClicked.connect(self.get_selected_prod)

        self.carica_catalogo(self.prod_manager.get_lista())

    def carica_catalogo(self, lista_prodotti):
        # pulizia tabella (per aggiornamenti, ad esempio)
        self.table_prodotti.setRowCount(0)
        # ottengo il numero di righe che vanno inserite
        self.table_prodotti.setRowCount(len(lista_prodotti))
        # inserisco effettivamente le righe
        num_riga = 0
        for prod in lista_prodotti:
            # gli item della qtablewidget devono essere obbligatoriamente delle stringhe, quindi vado a castare
            # i valori numerici in stringhe per renderli visibili in tabella
            prod_id = QTableWidgetItem(str(prod.get_id()))
            prod_title = QTableWidgetItem(prod.get_titolo())
            prod_qta = QTableWidgetItem(str(prod.get_quantita()))
            prod_price = QTableWidgetItem(str(prod.get_prezzo()) + "€")
            prod_descr = QTableWidgetItem(prod.get_descrizione())

            self.table_prodotti.setItem(num_riga, 0, prod_id)
            self.table_prodotti.setItem(num_riga, 1, prod_title)
            self.table_prodotti.setItem(num_riga, 2, prod_qta)
            self.table_prodotti.setItem(num_riga, 3, prod_price)
            self.table_prodotti.setItem(num_riga, 4, prod_descr)

            num_riga += 1

    def aggiungi_prodotto(self):
        aggiunta_prodotto = APV.AggiungiProdottoView(self.prod_manager)
        if aggiunta_prodotto.exec():
            self.prod_manager.carica_lista()
            self.carica_catalogo(self.prod_manager.get_lista())

    def rimuovi_prodotto(self):
        conferma = MsgBox()
        if conferma.show_yes_no_msg("Desideri rimuovere il prodotto selezionato?"):
            # rimozione prodotto
            self.prod_manager.rimuovi(self.selected_prod_id)
            # ricaricamento lista prodotti
            self.prod_manager.carica_lista()
            self.carica_catalogo(self.prod_manager.get_lista())
            # nessun prodotto ora è più selezionato
            self.selected_prod_id = None

    def modifica_prodotto(self):
        # ottenimento prodotto che si desidera modificare
        prod_da_modificare = self.prod_manager.ricerca_per_id(self.selected_prod_id)

        if prod_da_modificare is None:
            msg = MsgBox()
            msg.show_error_msg("Il prodotto che si desidera modificare non è presente in catalogo.")
        else:
            mod_prodotto = MPV.ModificaProdottoView(self.prod_manager, prod_da_modificare)
            if mod_prodotto.exec():
                # ricaricamento lista prodotti
                self.prod_manager.carica_lista()
                self.carica_catalogo(self.prod_manager.get_lista())

    def get_selected_prod(self):
        # ottengo l'id del prodotto selezionato
        selected_row = self.table_prodotti.currentRow()
        self.selected_prod_id = int(self.table_prodotti.item(selected_row, 0).text())

        # abilito il pulsante per modificare o rimuovere un prodotto
        self.btn_edit_selected.setEnabled(True)
        self.btn_delete_selected.setEnabled(True)

    def ricerca_prodotto(self):
        self.ricerca_view = RicercaProdottoImpiegatoView(self)
        dialog_return = self.ricerca_view.exec_()

        if dialog_return == QDialog.Accepted:
            query = self.ricerca_view.get_query()
            search_by = self.ricerca_view.get_search_type()

            if search_by == self.ricerca_view.SEARCH_BY_ID:
                result = self.prod_manager.ricerca_per_id(int(float(query)))
            elif search_by == self.ricerca_view.SEARCH_BY_NAME:
                result = self.prod_manager.ricerca(query)

            msg = MsgBox()
            if result is None:
                msg.show_error_msg("Il prodotto desiderato non è stato trovato.")
            else:
                msg.show_info_msg(f"Prodotto trovato: {result.get_titolo()}, ID {result.get_id()}, "
                                  f"prezzo {result.get_prezzo()}€, {result.get_quantita()} giacenze in magazzino.")
                self.selected_prod_id = result.get_id()
