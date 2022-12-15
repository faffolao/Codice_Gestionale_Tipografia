from Gestione.Database import Database


# DISCLAIMER:
# La coda di stampa è simulata per motivi didattici; conterrà solamente i nomi dei file che devono essere stampati
# per i clienti che li richiedono.
class CodaStampa:
    def __init__(self):
        self.lista_documenti = []

    def inserisci_doc(self, doc):
        db_con = Database("system.db")
        db_con.inserisci_doc(doc)
