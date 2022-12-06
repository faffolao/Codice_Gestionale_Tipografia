from PyQt5.QtWidgets import QMessageBox


class MsgBox(QMessageBox):
    def __init__(self):
        super().__init__()

    def show_error_msg(self, msg):
        self.setIcon(QMessageBox.Critical)
        self.setText("Si è verificato un errore:")
        self.setInformativeText(msg)
        self.setWindowTitle("Errore!")
        self.exec_()
