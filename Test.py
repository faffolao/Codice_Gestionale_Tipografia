import datetime
import string
import sys
import time
import unittest

from ECommerce.Catalogo import Catalogo
from ECommerce.Prodotto import Prodotto
from Gestione.Database import Database
from Utenti.Cliente import Cliente

OUTPUT_DEBUG = True

"""Colori per la print di debug"""


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


"""Funzione per il debug, impostare OUTPUT_DEBUG a True se si vuole stampare a schermo, false altrimenti"""


def out(num: int, msg: str) -> None:
    if OUTPUT_DEBUG:
        if num is not None:
            print(bcolors.HEADER + "<Test " + str(num) + ">" + bcolors.ENDC + msg)
        else:
            print("\t" + msg)


class TestDatabase(unittest.TestCase):
    database_path = "system.db"
    database = Database(database_path)

    """Testo la connessione al database controllando se viene eseguita una query
     che non necessita di tabelle"""

    def test_db_connection(self):
        out(1, "Controllo connessione database:")

        res = self.database.query("SELECT 1")
        self.assertEqual(res.fetchone()[0], 1, "Problema di connessione al DB")  # add assertion here

        out(1, "Done!")

    """Controllo se le tabelle esistenti nel database sono tutte"""

    def test_db_table(self):
        out(2, "Controllo tabelle del database:")

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
            out(None, table[0])
            self.assertEqual(table[0], tables[i][0])
            if table[0] == tables[i][0]:
                raws = self.database.query("PRAGMA table_info(" + table[0] + ")")
                j = 0
                for col in raws:
                    out(None, "verifico : " + tables[i][1][j] + " = " + col[1])
                    self.assertEqual(col[1], tables[i][1][j])
                    j = j + 1
            i = i + 1

        out(2, "Done!")

    """Testo l'inserimento e la rimozione di un utente di prova e confronto se l'oggetto originale e quello scritto 
    nel db sono identici"""

    def test_crd_cliente(self):
        out(3, "Inserimento, verifica uguaglianza ed eliminazione di un Cliente:")

        # inserisco l'utente nel db
        cliente = Cliente(1, "Test", "Test", "Test", "Test", "Test@Test.it", 1111111111, datetime.datetime(2001, 1, 1))
        self.assertTrue(self.database.inserisci_utente(cliente, "cliente"), "Problema nell'inserimento dell'utente")

        # lo confronto con un altro
        db_cliente = self.database.get_dettagli_utente(cliente.username)
        # devo cifrare la psw per poter confrontarla con quella nel db manualmente
        salt = bytes.fromhex(db_cliente.get_password()[:32])
        enc_guess = self.database.crittografia_psw_determ(cliente.get_password(), salt)
        cliente.password = enc_guess

        out(None, "Confronto")
        out(None, "".join(str(cliente.__dir__())))
        out(None, "".join(str(db_cliente.__dir__())))
        self.assertTrue(cliente.__eq__(db_cliente), "L'utente inserito nel DB non corrisponde a quello di Test")

        # rimuovo l'utente dal db
        self.database.query("BEGIN TRANSACTION")
        self.database.query("DELETE FROM Utente WHERE id = ? ", (db_cliente.id,))
        self.assertTrue(self.database.query("COMMIT TRANSACTION"))

        # test finito
        out(3, "Done!")

    def test_prodotto(self):
        out(4, "Verifica di un Prodotto...")

        # creo l'oggetto prodotto
        # inserire qui sotto l'id e i dettagli del prodotto da testare
        prod_test_id = 1
        prod_test_title = str(time.time())
        prod_test_description = string.printable
        prod_test_price = sys.float_info.max

        prod_test = Prodotto(prod_test_description, prod_test_id, None, prod_test_price, 1, prod_test_title)
        self.database.inserisci_prodotto(prod_test)

        # ottengo dal db il prodotto che ha lo stesso id di quello sopra
        prod_from_db = self.database.query(
            "SELECT * FROM Prodotto WHERE Prodotto.titolo = '" + prod_test.get_titolo() + "'")
        print("SELECT * FROM Prodotto WHERE Prodotto.titolo = '" + prod_test.get_titolo() + "'")

        if prod_from_db is not None:
            prod_from_db = prod_from_db.fetchall()
            print(prod_from_db)
            # confronto tra i due prodotti
            out(None, "verifico titolo prodotto...")

            self.assertEqual(prod_from_db[0][1], prod_test.get_titolo(),
                             "Il prodotto prelevato dal database ha un titolo differente")
            out(None, "verifico descrizione prodotto:")
            self.assertEqual(prod_from_db[0][2], prod_test.get_descrizione(),
                             "Il prodotto prelevato dal "
                             "database ha una descrizione "
                             "differente")
            out(None, "verifico prezzo prodotto...")
            self.assertEqual(prod_from_db[0][5], prod_test.get_prezzo(),
                             "Il prodotto prelevato dal database ha "
                             "un prezzo differente")

        else:
            # dico che il test è fallito perchè il prodotto da esaminare non è stato trovato nel db
            self.fail("Test non superato: il prodotto non esiste nel catalogo e nel database")

        self.database.rimuovi_prodotto(prod_from_db[0][0])
        prod_from_db = self.database.query(
            "SELECT * FROM Prodotto WHERE Prodotto.titolo = '" + prod_test.get_titolo() + "'")
        out(None, "Verifico corretta cancellazione prodotto...")
        self.assertIsNone(prod_from_db.fetchone())
        # test finito
        out(4, "Done!")


if __name__ == '__main__':
    unittest.main()
