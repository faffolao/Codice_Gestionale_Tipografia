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

    def show_yes_no_msg(self, msg):
        selection = self.question(self, "Domanda", msg, QMessageBox.Yes | QMessageBox.No)

        if selection == self.Yes:
            return True
        elif selection == self.No:
            return False

    def show_info_msg(self, msg):
        self.setIcon(QMessageBox.Information)
        self.setText("Informazione:")
        self.setInformativeText(msg)
        self.setWindowTitle("Messaggio dal sistema")
        self.exec_()
