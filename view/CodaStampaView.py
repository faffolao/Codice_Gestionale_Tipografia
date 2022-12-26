import datetime

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem

from Gestione.Database import Database
from Stampa.CodaStampa import CodaStampa


class CodaStampaView(QMainWindow):
    def __init__(self):
        super(CodaStampaView, self).__init__()
        uic.loadUi('ui/coda_stampa.ui', self)

        # caricamento della coda di stampa
        self.coda_stampa = CodaStampa()
        self.coda_stampa.carica_coda_stampa()

        # visualizzazione numero di documenti nella coda
        self.lbl_num_docs.setText(f"Ci sono {len(self.coda_stampa.get_coda_stampa())} documenti nella coda di stampa.")

        # associazione evento click al tasto chiudi
        self.btn_close.clicked.connect(lambda: self.close())

        # visualizzazione coda di stampa
        self.table_coda_stampa.setRowCount(len(self.coda_stampa.get_coda_stampa()))
        # inserisco effettivamente le righe
        num_riga = 0
        db_con = Database("system.db")
        for doc in self.coda_stampa.get_coda_stampa():
            # gli item della qtablewidget devono essere obbligatoriamente delle stringhe, quindi vado a castare
            # i valori numerici in stringhe per renderli visibili in tabella
            document_time = datetime.datetime.fromtimestamp(int(doc.get_data()))

            doc_id = QTableWidgetItem(str(doc.get_id()))
            doc_username = QTableWidgetItem(db_con.get_username(doc.get_id_cliente())[0])
            doc_filename = QTableWidgetItem(doc.get_nome_file())
            doc_datetime = QTableWidgetItem(document_time.strftime("%d/%m/%Y %H:%M"))
            doc_tipo_carta = QTableWidgetItem(doc.get_tipo_carta())
            doc_tipo_rilegatura = QTableWidgetItem(doc.get_tipo_rilegatura())

            self.table_coda_stampa.setItem(num_riga, 0, doc_id)
            self.table_coda_stampa.setItem(num_riga, 1, doc_username)
            self.table_coda_stampa.setItem(num_riga, 2, doc_filename)
            self.table_coda_stampa.setItem(num_riga, 3, doc_datetime)
            self.table_coda_stampa.setItem(num_riga, 4, doc_tipo_carta)
            self.table_coda_stampa.setItem(num_riga, 5, doc_tipo_rilegatura)

            num_riga += 1