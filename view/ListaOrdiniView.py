from datetime import datetime

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem

from Gestione.Database import Database
from Gestione.GestioneOrdini import GestioneOrdini


class ListaOrdiniView(QMainWindow):
    def __init__(self):
        super(ListaOrdiniView, self).__init__()
        uic.loadUi('ui/lista_ordini.ui', self)

        self.gestione_ordini = GestioneOrdini()
        self.gestione_ordini.carica_lista_ordini()

        self.lbl_num_ordini.setText(f"Ci sono {self.gestione_ordini.conta_ordini()} ordini nella lista.")
        self.btn_close.clicked.connect(lambda: self.close())

        db_con = Database("system.db")
        self.table_ordini.setRowCount(self.gestione_ordini.conta_ordini())

        num_riga = 0
        for ordine in self.gestione_ordini.get_lista_ordini():
            order_id = QTableWidgetItem(str(ordine.get_id()))
            order_cliente = QTableWidgetItem(db_con.get_username(ordine.get_id_cliente())[0])
            order_date = QTableWidgetItem(datetime.fromtimestamp(int(ordine.get_data())).strftime("%d/%m/%Y %H:%M"))
            order_ammonto = QTableWidgetItem(str(ordine.get_ammonto()) + "€")

            ds = ordine.get_dati_spedizione()
            order_dati_spedizione = f"{ds.get('citta')} - via {ds.get('via')} {ds.get('num_civico')}"

            prod_list = ordine.get_lista_prodotti()
            order_prodotti = ""
            for p in prod_list:
                order_prodotti += f"{p.get_quantita()}x {p.get_titolo()} - "

            item_dati_spedizione = QTableWidgetItem(order_dati_spedizione)
            item_prodotti = QTableWidgetItem(order_prodotti)

            self.table_ordini.setItem(num_riga, 0, order_id)
            self.table_ordini.setItem(num_riga, 1, order_cliente)
            self.table_ordini.setItem(num_riga, 2, order_date)
            self.table_ordini.setItem(num_riga, 3, order_ammonto)
            self.table_ordini.setItem(num_riga, 4, item_dati_spedizione)
            self.table_ordini.setItem(num_riga, 5, item_prodotti)

            num_riga += 1