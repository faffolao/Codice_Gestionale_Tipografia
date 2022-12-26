from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QAbstractItemView, QDialog

from ECommerce.Catalogo import Catalogo
from Gestione.Database import Database
from Gestione.GestioneSessioneMarket import GestioneSessioneMarket
from view.CarrelloView import CarrelloView
from view.DettagliProdottoView import DettagliProdottoView
from view.MsgBoxView import MsgBox
from view.RicercaProdottoClienteView import RicercaProdottoClienteView


class CatalogoView(QMainWindow):
    def __init__(self, cliente):
        # inizializzazione finestra
        super(CatalogoView, self).__init__()
        self.gestione_market = GestioneSessioneMarket()

        uic.loadUi('ui/catalogo_prodotti.ui', self)

        # il prodotto che l'utente selezionerà dal catalogo sarà qui
        self.selected_prod_id = None
        # il cliente che fa acquisti è qui
        self.cliente = cliente
        self.cliente.get_carrello_prodotti().carica_carrello(self.cliente.get_id())
        # imposto la selezione a intera riga e non a cella singola nella tabella del catalogo
        self.table_catalogo.setSelectionBehavior(QAbstractItemView.SelectRows)
        # disabilito la possibilità di modificare le celle della tabella liberamente
        self.table_catalogo.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # evento selezione di una riga
        self.table_catalogo.cellClicked.connect(self.get_selected_prod)
        # eventi dei pulsanti
        self.btn_visualizza_dettagli.clicked.connect(self.get_dettagli_prod)
        self.btn_search_prod.clicked.connect(self.ricerca_prodotto)
        self.btn_open_carrello.clicked.connect(self.visualizza_carrello)
        self.btn_aggiungi_al_carrello.clicked.connect(self.aggiungi_al_carrello)
        self.btn_finalizza_ordine.clicked.connect(self.finalizza_ordine)

        # caricamento del catalogo
        self.catalogo = Catalogo()
        lista_prodotti = self.catalogo.get_lista_prodotti()
        # visualizzazione catalogo a schermo
        self.carica_catalogo(lista_prodotti)

    def carica_catalogo(self, lista_prodotti):
        # pulizia tabella (per aggiornamenti, ad esempio)
        self.table_catalogo.setRowCount(0)
        # ottengo il numero di righe che vanno inserite
        self.table_catalogo.setRowCount(len(lista_prodotti))
        # inserisco effettivamente le righe
        num_riga = 0
        for prod in lista_prodotti:
            # gli item della qtablewidget devono essere obbligatoriamente delle stringhe, quindi vado a castare
            # i valori numerici in stringhe per renderli visibili in tabella
            prod_id = QTableWidgetItem(str(prod.get_id()))
            prod_title = QTableWidgetItem(prod.get_titolo())
            prod_qta = QTableWidgetItem(str(prod.get_quantita()))
            prod_price = QTableWidgetItem(str(prod.get_prezzo()) + "€")

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
            prod_details_view = DettagliProdottoView(self, prod)
            prod_details_view.exec_()
        else:
            msg = MsgBox()
            msg.show_error_msg("Il prodotto non è stato trovato, probabilmente non è stato selezionato alcun prodotto.")

    def ricerca_prodotto(self):
        # ottenimento del nome
        self.search_dialog = RicercaProdottoClienteView(self)
        dialog_return = self.search_dialog.exec_()

        if dialog_return == QDialog.Accepted:
            nome = self.search_dialog.get_query()
            prod = self.catalogo.ricerca_per_nome(nome)

            if prod is not None:
                # faccio vedere i dettagli del prodotto trovato.
                prod_details_view = DettagliProdottoView(self, prod)
                prod_details_view.exec_()
                # il prodotto trovato viene impostato come selezionato.
                self.selected_prod_id = prod.get_id()
                # abilito i pulsanti disabilitati
                self.btn_visualizza_dettagli.setEnabled(True)
                self.btn_aggiungi_al_carrello.setEnabled(True)
            else:
                msg = MsgBox()
                msg.show_error_msg("Il prodotto non è stato trovato, probabilmente è stato inserito il nome di un "
                                   "prodotto inesistente.")

    def visualizza_carrello(self):
        self.carrello_view = CarrelloView(self.cliente, self)
        self.carrello_view.show()

    def aggiungi_al_carrello(self):
        # ottengo il prodotto dal catalogo
        prod = self.catalogo.ricerca_per_id(self.selected_prod_id)

        # controllo quantità prodotto
        if prod.get_quantita() <= 0:
            msg = MsgBox()
            msg.show_error_msg("Impossibile aggiungere il prodotto nel catalogo: il prodotto selezionato è esaurito.")
        else:
            self.cliente.get_carrello_prodotti().aggiungi(prod, self.cliente.get_id())

            prod.scala_quantita()
            db_con = Database("system.db")
            db_con.modifica_quantita_prodotto(prod)

            self.carica_catalogo(self.catalogo.get_lista_prodotti())

    def finalizza_ordine(self):
        if self.gestione_market.finalizza_acquisto(self.cliente.get_carrello_prodotti(), self.cliente.get_id()):
            msg = MsgBox()
            msg.show_info_msg("L'ordine è stato correttamente inviato.")
        else:
            msg = MsgBox()
            msg.show_error_msg("L'ordine è stato respinto: controlla: di avere almeno un prodotto nel carrello, "
                               "di avere saldo sufficiente e di non aver annullato l'ordine.")
