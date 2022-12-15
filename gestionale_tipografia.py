import sys
from PyQt5.QtWidgets import QApplication

from Gestione.Database import Database
from Gestione.GestioneAccessi import GestioneAccessi
from view.LoginView import LoginView


class App(QApplication):
    def __init__(self, sys_argv):
        # inizializzazione app
        super(App, self).__init__(sys_argv)

        self.using_model = GestioneAccessi()

        # inizializzazione vista iniziale -> login form
        self.login_view = LoginView(self.using_model)
        self.login_view.show()


if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())
