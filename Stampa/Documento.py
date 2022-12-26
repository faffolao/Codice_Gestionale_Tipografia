class Documento:
    def __init__(self,  id_cliente, nome_file, id=None, tipo_carta=None, tipo_rilegatura=None, data=None):
        self.id = id
        self.id_cliente = id_cliente
        self.nome_file = nome_file
        self.tipo_carta = tipo_carta
        self.tipo_rilegatura = tipo_rilegatura
        self.data = data

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