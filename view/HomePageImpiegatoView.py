from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
import view.GestioneProdottiView as GPV
import view.LoginView as LV

class HomePageImpiegatoView(QMainWindow):
    def __init__(self, login_manager_model):
        super(HomePageImpiegatoView, self).__init__()

        self.login_manager = login_manager_model

        uic.loadUi('ui/home_page_impiegato.ui', self)
        self.setFixedSize(self.size())

        self.lbl_title.setText("Benvenuto, " + self.login_manager.get_utente_connesso().get_nome())
        self.lbl_impiegato_connesso.setText(f"impiegato connesso: {self.login_manager.get_utente_connesso().get_nome()} {self.login_manager.get_utente_connesso().get_cognome()}")

        self.btn_gestione_prodotti.clicked.connect(self.gestione_prod)
        self.btn_logout.clicked.connect(self.logout)

    def gestione_prod(self):
        self.gestione_prodotti_view = GPV.GestioneProdottiView()
        self.gestione_prodotti_view.show()

    def logout(self):
        self.login_manager.logout()
        self.login_form = LV.LoginView(self.login_manager)
        self.login_form.show()
        self.close()
