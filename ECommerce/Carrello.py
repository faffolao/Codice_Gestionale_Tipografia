import Gestione.Database as DB


class Carrello:
    def __init__(self):
        self.prodotti = []

    def get_lista_prodotti(self):
        return self.prodotti

    def carica_carrello(self, id):
        db_con = DB.Database("system.db")
        self.prodotti = db_con.get_carrello_cliente(id)
        print(self.prodotti)
