from Gestione.Database import Database


class Catalogo:
    def __init__(self):
        self.db_con = Database("system.db")
        self.lista_prodotti = self.db_con.get_catalogo()

    def get_lista_prodotti(self):
        return self.lista_prodotti

    def ricerca_per_id(self, id):
        for prodotto in self.lista_prodotti:
            if prodotto.get_id() == id:
                return prodotto

        return None
