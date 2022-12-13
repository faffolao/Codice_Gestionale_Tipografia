from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from view.LoginView import LoginView

class HomePageClienteView(QMainWindow):
    def __init__(self, login_manager_model):
        # inizializzazione finestra
        super(HomePageClienteView, self).__init__()

        # associazione controller a questa vista
        self.login_manager = login_manager_model

        uic.loadUi('ui/home_page_cliente.ui', self)
        self.setFixedSize(self.size())

        self.lbl_titolo.setText("Benvenuto, " + self.login_manager.get_utente_connesso().get_nome())
        self.lbl_user_email.setText(self.login_manager.get_utente_connesso().get_email())

        self.btn_logout.clicked.connect(self.logout)

        self.show()

    def logout(self):
        self.login_manager.logout()
        self.login_form = LoginView(self.login_manager)
        self.login_form.show()
        self.close()