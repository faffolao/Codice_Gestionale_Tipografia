from PyQt5 import uic
from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import QMainWindow, QFileDialog

from Gestione.GestioneSessioneStampa import GestioneSessioneStampa
from Stampa.Documento import Documento
from view.MsgBoxView import MsgBox


class StampaDocumentoView(QMainWindow):
    def __init__(self, cliente_obj, print_session_manager):
        # inizializzazione finestra
        super(StampaDocumentoView, self).__init__()

        self.cliente = cliente_obj
        self.sessione_stampa = print_session_manager

        uic.loadUi('ui/stampa_documento.ui', self)
        self.setFixedSize(self.size())

        self.btn_scegli_doc.clicked.connect(self.seleziona_file)
        self.btn_elimina_doc.clicked.connect(self.elimina_doc)
        self.btn_invia_stampa.clicked.connect(self.invia_stampa)

        self.combo_tipo_carta.currentTextChanged.connect(self.set_tipo_carta)
        self.combo_rilegatura.currentTextChanged.connect(self.set_tipo_rilegatura)

    def seleziona_file(self):
        # Apro un dialog per selezionare il file da stampare. È settato per poter scegliere solamente file pdf, docx,
        # png, jpeg, ovvero i file che abbiamo impostato come stampabili dalla tipografia.
        selected_file = QFileDialog.getOpenFileName(self, 'Seleziona documento da stampare', "",
                                                    "Documenti stampabili (*.pdf *.docx *.png *.jpeg)")

        # ottengo il nome del file a partire dal file selezionato
        filename = QFileInfo(selected_file[0]).fileName()

        if filename:
            doc = Documento(filename, self.cliente.get_id())
            self.sessione_stampa.set_doc(doc)
            self.sessione_stampa.set_carta(self.combo_tipo_carta.currentText())
            self.sessione_stampa.set_rilegatura(self.combo_rilegatura.currentText())

            self.lbl_selected_doc.setText(filename)

            self.combo_tipo_carta.setEnabled(True)
            self.combo_rilegatura.setEnabled(True)

            self.btn_invia_stampa.setEnabled(True)
            self.btn_elimina_doc.setEnabled(True)

    def invia_stampa(self):
        msg = MsgBox()

        if self.sessione_stampa.invia_stampa():
            msg.show_info_msg("La tua stampa è stata inviata correttamente alla coda.")
            self.close()
        else:
            msg.show_error_msg("Non è stato possibile inviare la stampa. Probabilmente la stampa è stata annullata o "
                               "si è verificato un problema con il pagamento o con l'invio nella coda.")

    def elimina_doc(self):
        question = MsgBox()
        delete_doc = question.show_yes_no_msg("Desideri rimuovere il documento selezionato?")

        if delete_doc:
            self.sessione_stampa.rimuovi_doc()

            self.lbl_selected_doc.setText("Nessun file selezionato.")

            self.combo_tipo_carta.setEnabled(False)
            self.combo_rilegatura.setEnabled(False)

            self.btn_invia_stampa.setEnabled(False)
            self.btn_elimina_doc.setEnabled(False)

    def set_tipo_carta(self, value):
        self.sessione_stampa.set_carta(value)

    def set_tipo_rilegatura(self, value):
        self.sessione_stampa.set_rilegatura(value)
