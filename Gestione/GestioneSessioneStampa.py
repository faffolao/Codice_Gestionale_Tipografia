from Gestione.GestionePagamento import GestionePagamento
from view.MsgBoxView import MsgBox


class GestioneSessioneStampa:
    def __init__(self, db_con):
        self.doc = None
        self.db_con = db_con

    def set_doc(self, doc):
        self.doc = doc

    def get_doc(self):
        return self.doc

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

        doc_pagato = GestionePagamento.paga_documento()
        if not doc_pagato:
            msg.show_error_msg("Non c'è saldo sufficiente per pagare il documento. La stampa verrà annullata.")
            return False

    def conferma_stampa(self):
        msg = MsgBox()
        conferma = msg.show_yes_no_msg("Confermi l'invio della stampa alla coda?")
        return conferma
