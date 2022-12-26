class Ordine:
    def __init__(self, ammonto, data, dati_spedizione, id, id_cliente, lista_prodotti):
        self.ammonto = ammonto
        self.data = data
        self.dati_spedizione = dati_spedizione
        self.id = id
        self.id_cliente = id_cliente
        self.lista_prodotti = lista_prodotti

    def get_ammonto(self):
        return self.ammonto

    def get_data(self):
        return self.data

    def get_dati_spedizione(self):
        return self.dati_spedizione

    def get_id(self):
        return self.id

    def get_id_cliente(self):
        return self.id_cliente

    def get_lista_prodotti(self):
        return self.lista_prodotti
