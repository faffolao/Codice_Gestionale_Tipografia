import sqlite3
import os.path
import hashlib
import time
import datetime

from ECommerce.Prodotto import Prodotto
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
            self.cur.execute("INSERT INTO Prodotto(titolo, descrizione, immagine, quantita, prezzo) Values(?,?,?,?,?)",(
                "molluschi al vapore",
                "un pranzo gustoso",
                bytes.fromhex("FFD8FFE000104A46494600010101004800480000FFDB004300110C0D0F0D0B110F0E0F131211151A2B1C1A18181A3526281F2B3F3742413E373C3B454E635445495E4B3B3C5676575E676A6F706F43537A83796C82636D6F6BFFDB0043011213131A171A331C1C336B473C476B6B6B6B6B6B6B6B6B6B6B6B6B6B6B6B6B6B6B6B6B6B6B6B6B6B6B6B6B6B6B6B6B6B6B6B6B6B6B6B6B6B6B6B6B6B6B6B6B6BFFC90011080031004A03012200021101031101FFCC000A0010100501101105FFDA000C03010002110311003F00C8BA3854FC3315C0171BE18A6FFE6194D4909D14C99B9C8D90B1F1B0CBE525B6E81076FBFE6F29C544A61F1D745DEA0A20A0BBDDDEFD9C4E989994A0535AED34DB3E21AA2A68BA524BC0E1F20425CA4C0B84EA9BC947BB93FEF26D4E348DD48EABF9C0A54412BA033425BC9125B4F62786103741EFF456626A1B67DBFE7B3DA17BC336A2DC7ACE77EFA090C1D208A652AF1B9EDEA664B3AD996948AB81D568595051DA6C7B299199BFEF6C642BEE501738870872AE026AE15B0B502860D0763FC0EAD007EDF81AC5931C1204C44BB6C63B4536B179E073A2A9279B53AEF24CCC18CCFE214D7CB9ABFEA198EE73A3AFECBA7C171897582E2A25EAF29305199111C0F6B0A375852ADBA55C14BE883160AA6B3798A3FB2BA54052822DA3D7F2FC0CF135F6A2F650CDA68BF3F4CD21CA25F3E67259C27249FCF2B80B783BCDC207E3040007165AA8444F5FA5758FD88FC583A0FB97F2903B1329D7813A941043FF00964C5CD74011DFB124BA0E7D78262E1E7D70CFAEEEA38E74DE86C21B57C5505069C1BAE1969C89FE3F736C64E45AB659F90E537ACBE01FF1B4294137CB31814D01CE1BFF00B6813E77C016A7C5D06D33403902BF6B96804801331DCED723AB13A00D86BDA7D859BB0C2C69228E2BEB7460E0A9C371E31E4008DFE0E72D57FAE3F318EE6743A028D2F56154F61150B6C590C2F918B1DDBBF91960B2B06AB9D8BC3DC4BA49B9E5D613EFBD1CDC794BB881F72B68C7D233AAF1390135C9683A4DAC4A7D9F4A945691043333BF8B7214C177A49287C46AE4FF00E821320CD211661856C4A08D2581EEFA22D3DE73BC2924E83CFC8761DC69B0A5DA7F2F8C281511955B664179D146C37E1F21B659ACDF427A3FF316CEB67FD07C68ADEB4DCDE07FBFFA20E1AA998AA5BFF8690A9D1BA1C551B8B0747F0900236A77B2B220CBBDDC807A13C0FFD9"),
                42,
                69
            ))
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
        dataOra = round(time.time())
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
        immagine = prodotto.get_dati_immagine()
        quantita = prodotto.get_quantita()
        prezzo = prodotto.get_prezzo()
        self.query(f"""INSERT INTO Prodotto(titolo, descrizione, immagine, quantita, prezzo)
        VALUES(?,?,?,?,?)""", (titolo, descrizione, immagine, quantita, prezzo))
        self.query("COMMIT TRANSACTION")

    def rimuovi_prodotto(self, id):
        self.query(f"DELETE FROM Prodotto WHERE id=?", id)
        self.query("COMMIT TRANSACTION")

    def rimuovi_utente(self, id):
        self.query("BEGIN TRANSACTION")
        self.query("DELETE FROM CarrelloCliente WHERE idCliente=?", (id,))
        self.query("""DELETE PO FROM ProdottiOrdinati as PO INNER JOIN Ordine ON PO.idOrdine=Ordine.id
        WHERE Ordine.idUtente=?""", (id,))
        self.query("DELETE FROM Ordine WHERE idUtente=?", (id,))
        self.query("DELETE FROM Documento WHERE idUtente=?", (id,))
        self.query("DELETE FROM Utente WHERE id=?", (id,))
        self.query("COMMIT TRANSACTION")

    def get_dettagli_utente(self, username: str):
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
        data_nascita_unix = dati[6]
        if data_nascita_unix is None:
            data_nascita_unix = 0
        dataNascita = datetime.datetime.fromtimestamp(data_nascita_unix)
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

        enc_pass_wrap = self.query("SELECT password FROM Utente WHERE username=?", (username,)).fetchone()

        if enc_pass_wrap is None:
            return False

        enc_pass = enc_pass_wrap[0]
        return self.verifica_psw(guess_pass, enc_pass)

    def chiudi_connessione(self):
        self.dbb.close()

    def dump_db(self):
        return "\n".join(self.dbb.iterdump())

    def get_catalogo(self):
        query_list = self.query("SELECT * FROM Prodotto").fetchall()

        prodotto_list = []
        for tupla in query_list:
            prodotto_list.append(Prodotto(tupla[2], tupla[0], tupla[3], tupla[5], tupla[4], tupla[1]))

        return prodotto_list

    def get_carrello_cliente(self, id_cliente):
        query_list = self.query(
            "SELECT Prodotto.descrizione, Prodotto.id, Prodotto.immagine, Prodotto.prezzo, CarrelloCliente.quantita, Prodotto.titolo "
            "FROM CarrelloCliente "
            "JOIN Prodotto ON CarrelloCliente.idProdotto = Prodotto.id "
            "JOIN Utente ON CarrelloCliente.idCliente = Utente.id "
            "WHERE Utente.id = ?", (id_cliente,)).fetchall()

        prodotti_list = []
        for tupla in query_list:
            prodotti_list.append(Prodotto(tupla[0], tupla[1], tupla[2], tupla[3], tupla[4], tupla[5]))

        return prodotti_list


if __name__ == '__main__':
    database = Database()
