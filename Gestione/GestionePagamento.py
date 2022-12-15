class GestionePagamento:
    # DISCLAIMER:
    # Come detto nel progetto, non è prevista la memorizzazione dei dati di pagamento; in un contesto ideale, sarebbe
    # gestita da un servizio esterno di pagamento, che si preoccuperebbe di prendere i dati per il pagamento e
    # processarlo.
    # Per simulare un comportamento tale anche in ambito didattico abbiamo creato questa classe che simula il conto
    # di un utente e permette così di simulare le operazioni di pagamento delle stampe e degli ordini.
    # È possibile cambiare il saldo iniziale fittizio e il costo delle stampe modificando queste costanti.
    SALDO = 100
    COSTO_DOC = 5

    def __init__(self):
        self.saldo = self.SALDO

    def paga_documento(self):
        if self.SALDO >= self.COSTO_DOC:
            self.saldo -= self.COSTO_DOC
            return True
        else:
            return False
