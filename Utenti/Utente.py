from datetime import datetime


class Utente:
    def __init__(self, id, nome, cognome, username, password, email, cellulare, data_nascita):
        self.id = id
        self.nome = nome
        self.cognome = cognome
        self.username = username
        self.password = password
        self.email = email
        self.cellulare = cellulare
        if type(data_nascita) is str:
            self.data_nascita = datetime.strptime(data_nascita, '%d/%m/%y')
        elif type(data_nascita) is datetime:
            self.data_nascita = data_nascita
        else:
            raise TypeError("data_nascita deve essere un'oggetto datetime o una stringa")
    """
    def __init__(self, id, nome, cognome, username, password, email, cellulare, data_nascita: datetime):
        self.id = id
        self.nome = nome
        self.cognome = cognome
        self.username = username
        self.password = password
        self.email = email
        self.cellulare = cellulare
        self.data_nascita = data_nascita
    """

    def get_cellulare(self):
        return self.cellulare

    def get_cognome(self):
        return self.cognome

    def get_data_nascita(self) -> datetime:
        return self.data_nascita

    def get_email(self):
        return self.email

    def get_id(self):
        return self.id

    def get_nome(self):
        return self.nome

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password
