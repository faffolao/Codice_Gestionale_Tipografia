from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
import view.GestioneProdottiView as GPV
import view.LoginView as LV
from view.CodaStampaView import CodaStampaView
from view.GestioneUtentiView import GestioneUtentiView
from view.ListaOrdiniView import ListaOrdiniView


class HomePageImpiegatoView(QMainWindow):
    def __init__(self, login_manager_model):
        super(HomePageImpiegatoView, self).__init__()

        self.login_manager = login_manager_model

        uic.loadUi('ui/home_page_impiegato.ui', self)
        self.setFixedSize(self.size())

        self.lbl_title.setText("Benvenuto, " + self.login_manager.get_utente_connesso().get_nome())
        self.lbl_impiegato_connesso.setText(
            f"impiegato connesso: {self.login_manager.get_utente_connesso().get_nome()} {self.login_manager.get_utente_connesso().get_cognome()}")

        # mapping pulsanti a eventi
        self.btn_gestione_prodotti.clicked.connect(self.gestione_prod)
        self.btn_logout.clicked.connect(self.logout)
        self.btn_show_coda_stampa.clicked.connect(self.apri_coda_stampa)
        self.btn_show_ordini.clicked.connect(self.apri_lista_ordini)
        self.btn_gestione_utenti.clicked.connect(self.gestione_utenti)

        # se l'impiegato connesso ha i privilegi di admin, abilito il pulsante backup
        if self.login_manager.get_utente_connesso().is_admin():
            self.btn_run_backup.setEnabled(True)

    def gestione_prod(self):
        self.gestione_prodotti_view = GPV.GestioneProdottiView()
        self.gestione_prodotti_view.show()

    def logout(self):
        self.login_manager.logout()
        self.login_form = LV.LoginView(self.login_manager)
        self.login_form.show()
        self.close()

    def apri_coda_stampa(self):
        self.coda_stampa = CodaStampaView()
        self.coda_stampa.show()

    def apri_lista_ordini(self):
        self.lista_ordini = ListaOrdiniView()
        self.lista_ordini.show()

    def gestione_utenti(self):
        self.gestione_utenti = GestioneUtentiView()
        self.gestione_utenti.show()
