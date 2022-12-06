import sys
from PyQt5.QtWidgets import QApplication
from Utenti.Utente import Utente
from Gestione.GestioneAccessi import GestioneAccessi
from view.LoginView import LoginView


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        # Connect everything together
        self.main_ctrl = GestioneAccessi()
        self.main_view = LoginView(self.main_ctrl)
        self.main_view.show()


if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())
