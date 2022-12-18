from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow


class CarrelloView(QMainWindow):
    def __init__(self):
        # inizializzazione finestra
        super(CarrelloView, self).__init__()
        uic.loadUi('ui/carrello.ui', self)
