from PyQt5.QtGui import QPixmap

class Prodotto:

    def __init__(self, descrizione, id, immagine, prezzo, quantita, titolo):
        self.descrizione = descrizione
        self.id = id
        self.immagine = immagine
        self.prezzo = prezzo
        self.quantita = quantita
        self.titolo = titolo

    def get_descrizione(self):
        return self.descrizione
    def get_immagine(self):
        pix = QPixmap()
        pix.loadFromData(format="JPG", buf=self.immagine)
    def get_dati_immagine(self):
        return self.immagine
    def get_prezzo(self):
        return self.prezzo
    def get_quantita(self):
        return self.quantita
    def get_titolo(self):
        return self.titolo
    def scala_quantita(self):
        pass
