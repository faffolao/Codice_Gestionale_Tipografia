import sched
import time

from PyQt5.QtCore import QThread

import Gestione.GestioneBackup


class BackupWorker(QThread):
    '''
    Worker thread
    '''

    def __init__(self):
        super(BackupWorker, self).__init__()
        self.backup = Gestione.GestioneBackup.GestioneBackup()

    def run(self):
        self.s = sched.scheduler(time.time, time.sleep)
        self.s.enter(1, 1, self.updateBackup, (self.s,))
        self.s.run()

    def updateBackup(self, sc):
        self.backup.effettua_backup()
        sc.enter(600, 1, self.updateBackup, (sc,))
