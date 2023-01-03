from datetime import datetime

from Gestione.Database import Database


class GestioneBackup:
    def effettua_backup(self):
        db_con = Database("system.db")
        dump_text = db_con.dump_db()

        self.salva_su_file(dump_text)

    def salva_su_file(self, content):
        with open("backup-" + datetime.now().strftime("%d-%m-%Y_%H%M%S") + ".sql", "w") as f:
            f.write(content)
