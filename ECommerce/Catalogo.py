from Gestione.Database import Database


class Catalogo:
    def __init__(self):
        self.db_con = Database("system.db")
        self.lista_prodotti = self.db_con.get_catalogo()

    def get_lista_prodotti(self):
        return self.lista_prodotti

    def ricerca_per_id(self, id):
        for prod in self.lista_prodotti:
            id_prod = prod.get_id()
            if id_prod == id:
                return prod

        return None

    def ricerca_per_nome(self, nome):
        for prod in self.lista_prodotti:
            # controllo se la sottostringa nome è contenuta all'interno del nome completo del prodotto (nome_prod)
            nome_prod = prod.get_titolo()
            if nome in nome_prod:
                return prod

        return None
