from datetime import datetime

from PyQt5.QtWidgets import QDialog

from ECommerce.Ordine import Ordine
from Gestione.Database import Database
from Gestione.GestionePagamento import GestionePagamento
from view.FinalizzaAcquistoView import FinalizzaAcquistoView
from view.MsgBoxView import MsgBox


class GestioneSessioneMarket:
    def __init__(self):
        self.dati_spedizione = {}

    def finalizza_acquisto(self, carrello, id_cliente):
        # controllo quanti prodotti ho in carrello
        num_prod = carrello.get_num_prod()
        if num_prod <= 0:
            return False

        # vado a richiedere i dati di spedizione
        self.dati_spedizione_view = FinalizzaAcquistoView()
        dialog_return = self.dati_spedizione_view.exec_()

        if dialog_return == QDialog.Rejected:
            return False
        else:
            self.set_dati_spedizione(self.dati_spedizione_view.get_dati_spedizione())

        # vado a richiedere conferma dell'ordine
        conferma = self.conferma_ordine()
        if not conferma:
            return False

        # pagamento dell'ordine
        prezzo = carrello.get_totale_prodotti()
        pagamento = GestionePagamento()
        ordine_pagato = pagamento.paga_ordine(prezzo)
        if not ordine_pagato:
            return False

        # creazione dell'ordine
        ordine = Ordine(prezzo, datetime.now(), self.dati_spedizione, None, id_cliente, carrello.get_lista_prodotti())
        db_con = Database("system.db")
        db_con.inserisci_ordine_market(ordine)

        # svuotamento carrello cliente
        carrello.svuota(id_cliente)

        # ordine inviato correttamente
        return True

    def set_dati_spedizione(self, ds):
        self.dati_spedizione = ds

    def conferma_ordine(self):
        msg = MsgBox()
        return msg.show_yes_no_msg("Desideri confermare l'ordine?")
