from PyQt5.QtGui import QPixmap


class Prodotto:

    # nota di sviluppo: l'attributo immagine è di tipo blob
    def __init__(self, descrizione, id, immagine, prezzo, quantita, titolo):
        self.descrizione = descrizione
        self.id = int(id)
        self.immagine = immagine
        self.prezzo = prezzo
        self.quantita = quantita
        self.titolo = titolo

    def get_descrizione(self):
        return self.descrizione

    # questo metodo ritorna l'immagine del prodotto sottoforma di QPixmap, che ne permette la rappresentazione nelle
    # GUI QT5.
    def get_immagine_rendered(self):
        pix = QPixmap()
        pix.loadFromData(format="JPG", buf=self.immagine)

    # questo metodo ritorna l'immagine del prodotto sottoforma di blob (sequenza di byte che rappresenta l'immagine)
    def get_immagine(self):
        return self.immagine

    def get_prezzo(self):
        return self.prezzo

    def get_quantita(self):
        return self.quantita

    def get_titolo(self):
        return self.titolo

    def get_id(self):
        return self.id

    def scala_quantita(self):
        pass
