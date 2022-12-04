import sqlite3
import os.path
import hashlib

class DataBase:
    tables = [
        """Utente(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cognome TEXT NOT NULL,
        email TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        dataNascita INTEGER NOT NULL,
        telefono TEXT NOT NULL,
        ruolo TEXT NOT NULL
        )""",
        """Documento(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        idCliente INTEGER NOT NULL,
        tipoCarta INTEGER NOT NULL,
        tipoRilegatura INTEGER NOT NULL,
        nomeFile TEXT NOT NULL,
        dataOra INTEGER NOT NULL,
        FOREIGN KEY(idCliente) REFERENCES Utente(id)
        )""",
        """Ordine(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        idCliente INTEGER NOT NULL,
        ammonto INTEGER NOT NULL,
        dataOra INTEGER NOT NULL,
        via TEXT NOT NULL,
        numeroCivico INTEGER NOT NULL,
        citta TEXT NOT NULL,
        cap INTEGER NOT NULL,
        FOREIGN KEY(idCliente) REFERENCES Utente(id)
        )""",
        """Prodotto(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titolo TEXT NOT NULL,
        descrizione TEXT NOT NULL,
        immagine BLOB,
        quantita INTEGER NOT NULL,
        prezzo INTEGER NOT NULL
        )""",
        """CarrelloCliente(
        idCliente INTEGER NOT NULL,
        idProdotto INTEGER NOT NULL,
        quantita INTEGER NOT NULL,
        FOREIGN KEY(idCliente) REFERENCES Utente(id),
        FOREIGN KEY(idProdotto) REFERENCES Prodotto(id),
        PRIMARY KEY(idCliente, idProdotto)
        )""",
        """ProdottiOrdinati(
        idOrdine INTEGER NOT NULL,
        idProdotto INTEGER NOT NULL,
        quantita INTEGER NOT NULL,
        FOREIGN KEY(idProdotto) REFERENCES Prodotto(id),
        FOREIGN KEY(idOrdine) REFERENCES Ordine(id),
        PRIMARY KEY(idOrdine, idProdotto)
        )"""
    ]

    def __init__(self, dababase_path):

        if not os.path.exists(dababase_path):
            self.dbb = sqlite3.connect(dababase_path)
            self.cur = self.dbb.cursor()
            self.cur.execute("BEGIN TRANSACTION;")
            for table in self.tables:
                self.cur.execute(f"CREATE TABLE {table};")
            self.cur.execute("COMMIT TRANSACTION;")
        else:
            self.dbb = sqlite3.connect(dababase_path)
            self.cur = self.dbb.cursor()

    def query(self, query_string):
        if ';' in query_string:
            raise ValueError('Deve essere inviata UNA query senza delimitatore')
        self.cur.execute(f"{query_string};")

    def crittografia_psw_determ(self, passwd, salt):
        enc_psw = hashlib.pbkdf2_hmac('sha256', passwd.encode('utf-8'), salt, 177013)
        return salt.hex() + enc_psw.hex()

    def crittografia_psw(self, passwd):
        salt = os.urandom(16)
        out = self.crittografia_psw_determ(passwd, salt)
        return out

    def verifica_psw(self, guess, enc_psw):
        salt = bytes.fromhex(enc_psw[:16])
        enc_guess = self.crittografia_psw_determ(guess, salt)
        if enc_guess == enc_psw:
            return True
        else:
            return False

    def dump_db(self):
        return "\n".join(self.dbb.iterdump())