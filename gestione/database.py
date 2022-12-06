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
        username TEXT NOT NULL UNIQUE,
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
        return self.cur.execute(f"{query_string};")

    def get_lista_utenti(self):
        return self.query("SELECT id,username,email FROM Utente").fetchall()

    def get_coda_stampa(self):
        return self.query("SELECT * from Documento").fetchall()

    def inserisci_doc(self, documento):
        idCliente = documento.get_id_cliente()
        tipoCarta = documento.get_tipo_carta()
        tipoRilegatura = documento.get_tipo_rilegatura()
        nomeFile = documento.get_nome_file()
        dataOra = round(documento.get_data().mktime())
        self.query(f"""INSERT INTO Documento(idCliente, tipoCarta, tipoRilegatura, nomeFile, dataOra)
        VALUES({idCliente}, {tipoCarta},{tipoRilegatura}, {nomeFile}, {dataOra})""")

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
        self.query(f"""INSERT INTO Ordine(idCliente, ammonto, quantita, dataOra, via, numeroCivico, citta, cap)
        VALUES({idCliente}, {ammonto}, {quantita}, {dataOra}, {via}, {numeroCivico}, {citta}, {cap})""")

    def inserisci_utente(self, utente, ruolo):
        nome = utente.get_nome()
        cognome = utente.get_cognome()
        email = utente.get_email()
        username = utente.get_username()
        password = self.crittografia_psw(utente.get_password())
        dataNascita = utente.get_data_nascita().mktime()
        telefono = utente.get_telefono()
        self.query(f"""INSERT INTO Ordine(nome, cognome, email, username, password, dataNascita, telefono, ruolo)
        VALUES({nome},{cognome},{email},{username},{password},{dataNascita},{telefono},{ruolo})""")

    def inserisci_prodotto(self, prodotto):
        titolo = prodotto.get_titolo()
        descrizione = prodotto.get_descrizione()
        immagine = prodotto.get_immagine()
        quantita = prodotto.get_quantita()
        prezzo = prodotto.get_prezzo()
        self.query(f"""INSERT INTO Prodotto(titolo, descrizione, immagine, quantita, prezzo)
        VALUES({titolo},{descrizione},{immagine},{quantita},{prezzo})""")

    def rimuovi_prodotto(self, id):
        self.query(f"DELETE FROM Prodotto WHERE id={int(id)}")

    def rimuovi_utente(self, id):
        iid = int(id)
        self.query("BEGIN TRANSACTION")
        self.query(f"DELETE FROM CarrelloCliente WHERE idCliente={iid}")
        self.query(f"""DELETE PO FROM ProdottiOrdinati as PO INNER JOIN Ordine ON PO.idOrdine=Ordine.id
        WHERE Ordine.idUtente={iid}""")
        self.query(f"DELETE FROM Ordine WHERE idUtente={iid}")
        self.query(f"DELETE FROM Documento WHERE idUtente={iid}")
        self.query(f"DELETE FROM Utente WHERE id={iid}")
        self.query("COMMIT TRANSACTION")

    def svuota_carrello(self, id):
        iid = int(id)
        self.query("BEGIN TRANSACTION")
        self.query(f"DELETE FROM CarrelloCliente WHERE idCliente={iid}")
        self.query("COMMIT TRANSACTION")

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

    alfabeto = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_1234567890"

    def verify_user(self, username, guess_pass):
        for ch in username:
            if ch not in self.alfabeto:
                return False
        enc_pass = self.query(f"SELECT password FROM Utente WHERE username={username}").fetchone()[0]
        return self.verifica_psw(guess_pass, enc_pass)

    def chiudi_connessione(self):
        self.dbb.close()

    def dump_db(self):
        return "\n".join(self.dbb.iterdump())