from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

import view.LoginView as LV
from Gestione.GestioneSessioneStampa import GestioneSessioneStampa
from view.CatalogoView import CatalogoView
from view.StampaDocumentoView import StampaDocumentoView


class HomePageClienteView(QMainWindow):
    def __init__(self, login_manager_model):
        # inizializzazione finestra
        super(HomePageClienteView, self).__init__()

        self.login_manager = login_manager_model

        uic.loadUi('ui/home_page_cliente.ui', self)
        self.setFixedSize(self.size())

        self.lbl_titolo.setText("Benvenuto, " + self.login_manager.get_utente_connesso().get_nome())
        self.lbl_user_email.setText(self.login_manager.get_utente_connesso().get_email())

        self.btn_logout.clicked.connect(self.logout)
        self.btn_stampa_doc.clicked.connect(self.apri_sezione_stampa)
        self.btn_open_market.clicked.connect(self.apri_ecommerce)

        self.show()

    def logout(self):
        self.login_manager.logout()

        self.login_form = LV.LoginView(self.login_manager)
        self.login_form.show()

        self.close()

    def apri_sezione_stampa(self):
        print_session_manager = GestioneSessioneStampa()
        self.stampa_view = StampaDocumentoView(self.login_manager.get_utente_connesso(), print_session_manager)
        self.stampa_view.show()

    def apri_ecommerce(self):
        self.catalogo_view = CatalogoView(self.login_manager.get_utente_connesso())
        self.catalogo_view.show()
