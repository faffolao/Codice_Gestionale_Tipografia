import sys
from PyQt5.QtWidgets import QApplication

from Gestione.Database import Database
from Gestione.GestioneAccessi import GestioneAccessi
from view.LoginView import LoginView


class App(QApplication):
    def __init__(self, sys_argv):
        # inizializzazione app
        super(App, self).__init__(sys_argv)

        # inizializzazione database
        self.db_con = Database("system.db")

        # inizializzazione controller iniziale -> permetterà la comunicazione tra le viste e le classi Model
        # (Gestione, Utenti, E-Commerce, Stampa)
        self.main_ctrl = GestioneAccessi(self.db_con)

        # inizializzazione vista iniziale -> login form
        self.main_view = LoginView(self.main_ctrl)
        self.main_view.show()


if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())
