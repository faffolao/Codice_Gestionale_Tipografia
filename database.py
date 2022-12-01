import sqlite3
import os.path

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
