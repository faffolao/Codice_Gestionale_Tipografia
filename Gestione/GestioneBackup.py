import os
from datetime import datetime

from Gestione.Database import Database


class GestioneBackup:
    def effettua_backup(self):
        db_con = Database("system.db")
        dump_text = db_con.dump_db()

        self.salva_su_file(dump_text)

    def salva_su_file(self, content):
        # cartella dove salvare i dump
        dir = "Backup"
        # ottengo il percorso completo dove salvare i dump generati
        absolute_path = os.getcwd()
        relative_path = dir
        full_path = os.path.join(absolute_path, relative_path)
        # se la cartella non esiste la creo
        if not os.path.exists(full_path):
            os.mkdir(full_path)
        # il file avrà questo nome
        filename = "backup-" + datetime.now().strftime("%d-%m-%Y_%H%M%S") + ".sql"

        # scrivo il file sulla cartella
        with open(os.path.join(full_path, filename), "w") as f:
            f.write(content)
