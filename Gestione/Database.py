import sqlite3
import os.path
import hashlib
import time
import datetime
from Utenti.Utente import Utente
from Utenti.Cliente import Cliente
from Utenti.Impiegato import Impiegato


class Database:
    tables = [
        """Utente(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cognome TEXT NOT NULL,
        email TEXT NOT NULL,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        dataNascita INTEGER,
        telefono TEXT,
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
        quantita INTEGER NOT NULL,
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
    alfabeto = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_1234567890"

    def __init__(self, database_path):

        if not os.path.exists(database_path):
            self.dbb = sqlite3.connect(database_path)
            self.cur = self.dbb.cursor()
            self.cur.execute("BEGIN TRANSACTION;")
            for table in self.tables:
                self.cur.execute(f"CREATE TABLE {table};")
            self.cur.execute("""INSERT INTO Utente(nome, cognome, email, username, password, ruolo)
            VALUES('System', 'Administrator', 'root@admin.com', 'admin', 'deadbeefdeadbeefdeadbeefdeadbeef32d5051379c2292d13f3b022c3847d6f81791d458e7d1a80c1b4898bcbc2f7b2', 'admin')""")
            self.cur.execute("COMMIT TRANSACTION;")
        else:
            self.dbb = sqlite3.connect(database_path)
            self.cur = self.dbb.cursor()

    def query(self, query_string, values=()):
        if ';' in query_string:
            raise ValueError('Deve essere inviata UNA query senza delimitatore')
        return self.cur.execute(f"{query_string};", values)

    def get_lista_utenti(self):
        return self.query("SELECT id,username,email FROM Utente").fetchall()

    def get_coda_stampa(self):
        return self.query("SELECT * from Documento").fetchall()

    def inserisci_doc(self, documento):
        idCliente = documento.get_id_cliente()
        tipoCarta = documento.get_tipo_carta()
        tipoRilegatura = documento.get_tipo_rilegatura()
        nomeFile = documento.get_nome_file()
        dataOra = round(time.mktime(documento.get_data().timetuple()))
        self.query("""INSERT INTO Documento(idCliente, tipoCarta, tipoRilegatura, nomeFile, dataOra)
        VALUES(?, ?, ?, ?, ?)""", (idCliente, tipoCarta, tipoRilegatura, nomeFile, dataOra))
        self.query("COMMIT TRANSACTION")

    def inserisci_ordine_market(self, ordine):
        datiSpedizione = ordine.get_dati_spedizione()
        idCliente = ordine.get_id_cliente()
        ammonto = ordine.get_ammonto()
        dataOra = round(ordine.get_data())
        via = datiSpedizione["via"]
        numeroCivico = datiSpedizione["numeroCivico"]
        citta = datiSpedizione["citta"]
        cap = datiSpedizione["cap"]
        quantita = ordine.get_quantita()
        self.query("""INSERT INTO Ordine(idCliente, ammonto, quantita, dataOra, via, numeroCivico, citta, cap)
        VALUES(?, ?, ?, ?, ?, ?, ?,?)""", (idCliente, ammonto, quantita, dataOra, via, numeroCivico, citta, cap))
        self.query("COMMIT TRANSACTION")

    def inserisci_utente(self, utente: Utente, ruolo):
        nome = utente.get_nome()
        cognome = utente.get_cognome()
        email = utente.get_email()
        username = utente.get_username()
        password = self.crittografia_psw(utente.get_password())
        dataNascita = time.mktime(utente.get_data_nascita().timetuple())
        telefono = utente.get_cellulare()
        ddt = (nome, cognome, email, username, password, dataNascita, telefono, ruolo)
        self.query("""INSERT INTO Utente(nome, cognome, email, username, password, dataNascita, telefono, ruolo)
        VALUES(?,?,?,?,?,?,?,?)""", ddt)
        self.query("COMMIT TRANSACTION")

    def inserisci_prodotto(self, prodotto):
        titolo = prodotto.get_titolo()
        descrizione = prodotto.get_descrizione()
        immagine = prodotto.get_immagine()
        quantita = prodotto.get_quantita()
        prezzo = prodotto.get_prezzo()
        self.query(f"""INSERT INTO Prodotto(titolo, descrizione, immagine, quantita, prezzo)
        VALUES(?,?,?,?,?)""", (titolo, descrizione, immagine, quantita, prezzo))
        self.query("COMMIT TRANSACTION")

    def rimuovi_prodotto(self, id):
        self.query(f"DELETE FROM Prodotto WHERE id=?", (id,))
        self.query("COMMIT TRANSACTION")

    def rimuovi_utente(self, id):
        self.query("BEGIN TRANSACTION")
        self.query("DELETE FROM CarrelloCliente WHERE idCliente=?", (id,))
        self.query("""DELETE PO FROM ProdottiOrdinati as PO INNER JOIN Ordine ON PO.idOrdine=Ordine.id
        WHERE Ordine.idUtente=?""",(id,))
        self.query("DELETE FROM Ordine WHERE idUtente=?",(id,))
        self.query("DELETE FROM Documento WHERE idUtente=?", (id,))
        self.query("DELETE FROM Utente WHERE id=?", (id,))
        self.query("COMMIT TRANSACTION")

    def get_dettagli_utente(self, username:str):
        for ch in username:
            if ch not in self.alfabeto:
                return None
        dati = self.query("SELECT * FROM Utente WHERE username=?", (username,)).fetchone()
        if dati is None:
            return None

        id = dati[0]
        nome = dati[1]
        cognome = dati[2]
        email = dati[3]
        password = dati[5]
        dataNascita = dati[6]
        telefono = dati[7]
        ruolo = dati[8]
        if ruolo == "cliente":
            return Cliente(id, nome, cognome, username, password, email, telefono, dataNascita)
        elif ruolo == "admin":
            return Impiegato(id, nome, cognome, username, password, email, telefono, dataNascita, True)
        elif ruolo == "impiegato":
            return Impiegato(id, nome, cognome, username, password, email, telefono, dataNascita, False)
        else:
            return Utente(id, nome, cognome, username, password, email, telefono, dataNascita)

    def svuota_carrello(self, id):
        self.query("BEGIN TRANSACTION")
        self.query("DELETE FROM CarrelloCliente WHERE idCliente=?", (id,))
        self.query("COMMIT TRANSACTION")

    def crittografia_psw_determ(self, passwd, salt):
        enc_psw = hashlib.pbkdf2_hmac('sha256', passwd.encode('utf-8'), salt, 177013)
        return salt.hex() + enc_psw.hex()

    def crittografia_psw(self, passwd):
        salt = os.urandom(16)
        out = self.crittografia_psw_determ(passwd, salt)
        return out

    def verifica_psw(self, guess, enc_psw):
        salt = bytes.fromhex(enc_psw[:32])
        enc_guess = self.crittografia_psw_determ(guess, salt)
        if enc_guess == enc_psw:
            return True
        else:
            return False

    def verify_user(self, username, guess_pass):
        for ch in username:
            if ch not in self.alfabeto:
                return False

        enc_pass_wrap = self.query("SELECT password FROM Utente WHERE username=?",(username,)).fetchone()

        if enc_pass_wrap is None:
            return False

        enc_pass = enc_pass_wrap[0]
        return self.verifica_psw(guess_pass, enc_pass)

    def chiudi_connessione(self):
        self.dbb.close()

    def dump_db(self):
        return "\n".join(self.dbb.iterdump())


if __name__ == '__main__':
    database = Database()
