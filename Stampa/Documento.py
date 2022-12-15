class Documento:
    # questo costruttore viene usato nell'area della coda di stampa
    def __init__(self, id, id_cliente, nome_file, tipo_carta, tipo_rilegatura, data):
        self.id = id
        self.id_cliente = id_cliente
        self.nome_file = nome_file
        self.tipo_carta = tipo_carta
        self.tipo_rilegatura = tipo_rilegatura
        self.data = data

    # questo costruttore viene usato nell'area di stampa del documento
    def __init__(self, nome_file, id_cliente):
        self.nome_file = nome_file
        self.id_cliente = id_cliente

    def get_data(self):
        return self.data

    def get_id(self):
        return self.id

    def get_id_cliente(self):
        return self.id_cliente

    def get_nome_file(self):
        return self.nome_file

    def get_tipo_carta(self):
        return self.tipo_carta

    def get_tipo_rilegatura(self):
        return self.tipo_rilegatura

    def set_carta(self, tipo_carta):
        self.tipo_carta = tipo_carta

    def set_rilegatura(self, tipo_rilegatura):
        self.tipo_rilegatura = tipo_rilegatura