from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow


class HomePageClienteView(QMainWindow):
    def __init__(self, access_ctrl):
        # inizializzazione finestra
        super(HomePageClienteView, self).__init__()

        # associazione controller a questa vista
        self.__controller = access_ctrl

        uic.loadUi('ui/home_page_cliente.ui', self)
        self.show()
        self.setFixedSize(self.size())

        # mapping delle funzioni agli eventi click dei pulsanti
        '''
        self.btn_logout.clicked.connect(self.login)
        self.btn_stampa_doc.clicked.connect(self.login)
        self.btn_open_market.clicked.connect(self.login)
        '''
