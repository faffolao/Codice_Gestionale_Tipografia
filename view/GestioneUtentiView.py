from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QAbstractItemView, QTableWidgetItem, QDialog

from Gestione.GestioneUtenti import GestioneUtenti
from view.AggiungiUtenteView import AggiungiUtenteView
from view.MsgBoxView import MsgBox
from view.RicercaUtenteView import RicercaUtenteView


class GestioneUtentiView(QMainWindow):
    def __init__(self):
        super(GestioneUtentiView, self).__init__()
        uic.loadUi('ui/gestione_utenti.ui', self)

        self.selected_user_id = None
        self.usr_manager = GestioneUtenti()
        self.usr_manager.carica_lista()

        self.table_utenti.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_utenti.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.btn_add_user.clicked.connect(self.aggiungi_utente)
        self.btn_delete_selected.clicked.connect(self.elimina_utente)
        self.btn_search_user.clicked.connect(self.ricerca_utente)
        self.table_utenti.cellClicked.connect(self.get_selected_usr)

        self.carica_lista_utenti(self.usr_manager.get_lista())

    def carica_lista_utenti(self, lista_utenti):
        # pulizia tabella (per aggiornamenti, ad esempio)
        self.table_utenti.setRowCount(0)
        # ottengo il numero di righe che vanno inserite
        self.table_utenti.setRowCount(len(lista_utenti))
        # inserisco effettivamente le righe
        num_riga = 0
        for usr in lista_utenti:
            # gli item della qtablewidget devono essere obbligatoriamente delle stringhe, quindi vado a castare
            # i valori numerici in stringhe per renderli visibili in tabella
            usr_id = QTableWidgetItem(str(usr.get_id()))
            usr_username = QTableWidgetItem(usr.get_username())
            usr_nome = QTableWidgetItem(usr.get_nome())
            usr_cognome = QTableWidgetItem(usr.get_cognome())
            usr_email = QTableWidgetItem(usr.get_email())
            usr_cellulare = QTableWidgetItem(usr.get_cellulare())

            data_nascita = usr.get_data_nascita()
            if data_nascita is None:
                data_nascita_val = "non presente"
            else:
                data_nascita_val = data_nascita.strftime("%d/%m/%Y")
            usr_data_nascita = QTableWidgetItem(data_nascita_val)

            self.table_utenti.setItem(num_riga, 0, usr_id)
            self.table_utenti.setItem(num_riga, 1, usr_username)
            self.table_utenti.setItem(num_riga, 2, usr_nome)
            self.table_utenti.setItem(num_riga, 3, usr_cognome)
            self.table_utenti.setItem(num_riga, 4, usr_email)
            self.table_utenti.setItem(num_riga, 5, usr_cellulare)
            self.table_utenti.setItem(num_riga, 6, usr_data_nascita)

            num_riga += 1

    def aggiungi_utente(self):
        self.aggiungi_utente_dialog = AggiungiUtenteView(self.usr_manager, self)
        dialog_result = self.aggiungi_utente_dialog.exec_()

        if dialog_result == QDialog.Accepted:
            self.usr_manager.carica_lista()
            self.carica_lista_utenti(self.usr_manager.get_lista())

    def get_selected_usr(self):
        # ottengo l'id dell'utente selezionato
        selected_row = self.table_utenti.currentRow()
        self.selected_user_id = int(self.table_utenti.item(selected_row, 0).text())

        # abilito il pulsante per rimuovere un utente
        self.btn_delete_selected.setEnabled(True)

    def elimina_utente(self):
        # chiedo conferma
        conferma = MsgBox()
        if conferma.show_yes_no_msg("Desideri eliminare l'utente selezionato?"):
            # rimuovo l'utente
            self.usr_manager.rimuovi(self.selected_user_id)
            # ricarico la lista
            self.usr_manager.carica_lista()
            self.carica_lista_utenti(self.usr_manager.get_lista())
            # nessun utente ora è selezionato
            self.selected_user_id = None

    def ricerca_utente(self):
        self.ricerca_utente_dialog = RicercaUtenteView(self)
        dialog_result = self.ricerca_utente_dialog.exec_()

        if dialog_result == QDialog.Accepted:
            usr = self.usr_manager.ricerca(self.ricerca_utente_dialog.get_query())

            msg = MsgBox()
            if usr is None:
                msg.show_error_msg("L'utente desiderato non è stato trovato.")
            else:
                msg.show_info_msg(f"Utente trovato: {usr.get_nome()} {usr.get_cognome()} (username: {usr.get_username()}), "
                                  f"con ID {usr.get_id()} - Email: {usr.get_email()}")
                self.selected_user_id = usr.get_id()
