from Gestione.Database import Database
from Stampa.Documento import Documento


# DISCLAIMER:
# La coda di stampa è simulata per motivi didattici; conterrà solamente i nomi dei file che devono essere stampati
# per i clienti che li richiedono.
class CodaStampa:
    def __init__(self):
        self.lista_documenti = []

    def inserisci_doc(self, doc):
        db_con = Database("system.db")
        db_con.inserisci_doc(doc)

    def carica_coda_stampa(self):
        db_con = Database("system.db")
        list = db_con.get_coda_stampa()

        for stampa in list:
            self.lista_documenti.append(Documento(id=stampa[0], id_cliente=stampa[1], nome_file=stampa[4], data=stampa[5],
                                                  tipo_carta=stampa[2], tipo_rilegatura=stampa[3]))

    def get_coda_stampa(self):
        return self.lista_documenti
