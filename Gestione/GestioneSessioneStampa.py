from Gestione.GestionePagamento import GestionePagamento
from Stampa.CodaStampa import CodaStampa
from view.MsgBoxView import MsgBox


class GestioneSessioneStampa:
    def __init__(self):
        self.doc = None

    def set_doc(self, doc):
        self.doc = doc

    def rimuovi_doc(self):
        self.doc = None

    def set_carta(self, carta):
        self.doc.set_carta(carta)

    def set_rilegatura(self, rilegatura):
        self.doc.set_rilegatura(rilegatura)

    def invia_stampa(self):
        # confermo l'invio della stampa
        conferma = self.conferma_stampa()

        if not conferma:
            return False

        # effettuo il pagamento della stampa
        msg = MsgBox()
        msg.show_info_msg("Verrai reindirizzato al servizio di pagamento per la stampa.")

        pagamento = GestionePagamento()
        doc_pagato = pagamento.paga_documento()
        if not doc_pagato:
            msg.show_error_msg("Non c'è saldo sufficiente per pagare il documento. La stampa verrà annullata.")
            return False

        # salvo il documento sul database
        coda_stampa = CodaStampa()
        coda_stampa.inserisci_doc(self.doc)

        # stampa inviata correttamente
        return True

    def conferma_stampa(self):
        msg = MsgBox()
        conferma = msg.show_yes_no_msg("Confermi l'invio della stampa alla coda?")
        return conferma
