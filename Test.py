import sqlite3
import unittest
import os

from Gestione.Database import Database

OUTPUT_DEBUG = True



def out(msg:str) -> None:
    if OUTPUT_DEBUG:
        print(msg)



class TestDatabase(unittest.TestCase):
    database_path = "system.db"
    database = Database(database_path)

    """Testo la connessione al database controllando se viene eseguita una queri
     che non necessita di tabelle"""

    def test_db_connection(self):
        res = self.database.query("SELECT 1")
        self.assertEqual(res.fetchone()[0], 1)  # add assertion here

    """Controllo se le tabelle esistenti nel database sono tutte"""

    def test_db_table(self):
        tables = [
            ["Utente", ["id", "nome", "cognome", "email", "username", "password", "dataNascita", "telefono", "ruolo"]],
            ["Prodotto", ["id", "titolo", "descrizione", "immagine", "quantita", "prezzo"]],
            ["ProdottiOrdinati", ["idOrdine", "idProdotto", "quantita"]],
            ["Ordine", ["id", "idCliente", "ammonto", "dataOra", "via", "numeroCivico", "citta", "cap"]],
            ["Documento", ["id", "idCliente", "tipoCarta", "tipoRilegatura", "nomeFile", "dataOra"]],
            ["CarrelloCliente", ["idCliente", "idProdotto", "quantita"]]

        ]
        res = self.database.query(
            "SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%' ORDER BY name DESC")
        i = 0
        for table in res.fetchall():
            out("----> " + table[0])
            self.assertEqual(table[0], tables[i][0])
            if table[0] == tables[i][0]:
                raws = self.database.query("PRAGMA table_info(" + table[0] + ")")
                j = 0
                for col in raws:
                    out("verifico : " + tables[i][1][j] + " = " + col[1])
                    self.assertEqual(col[1], tables[i][1][j])
                    j = j + 1
            i = i + 1


if __name__ == '__main__':
    unittest.main()
