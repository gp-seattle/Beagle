import os
from PyQt6.QtGui import (
    QAction,
)
from PyQt6.QtWidgets import (
    QDialog,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

class UpdateApp(QAction):
    def __init__(self, parent):
        super().__init__("Update App", parent)
        self.parent = parent
        self.triggered.connect(UpdateDialog(parent).exec)

class UpdateDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        isApp = None
        exStr = None
        
        if os.path.exists("pyinstaller.sh"): # In Main Directory
            isApp = False
        elif os.path.exists("../../../../pyinstaller.sh"): # In Dist Directory
            isApp = True
        else:
            exStr = "Not in valid Directory. To update, app needs to be in dist/ directory of a properly set up repo."

        if exStr is None:
            vlayout = QVBoxLayout()

            vlayout.addWidget(QLabel("Update App to Latest Version\n(Expect this to take approx 1 minute)"))

            vlayout.addWidget(UpdateButton(parent, isApp))

            self.setLayout(vlayout)
        else:
            vlayout = QVBoxLayout()
            label = QLabel(exStr)
            label.setStyleSheet("color:red")
            vlayout.addWidget(label)
            self.setLayout(vlayout)

class UpdateButton(QPushButton):
    def __init__(self, parent, isApp):
        super().__init__("Update", parent)
        self.parent = parent
        self.isApp = isApp

        self.pressed.connect(self.onPressed)
    
    def onPressed(self):
        statusCode = os.system("git pull > update.log")
        statusLine = ""
        with open("update.log") as file:
            statusLine = file.readline().strip()
        os.system("rm update.log")

        if statusLine == "Already up to date.":
            dlg = QMessageBox(self.parent)
            dlg.setWindowTitle("Update App")
            dlg.setText("Already up to date.")
            dlg.exec()
        elif statusCode == 0:
            if self.isApp:
                os.system("../../../../pyinstaller.sh")
            else:
                os.system("./pyinstaller.sh")

            dlg = QMessageBox(self.parent)
            dlg.setWindowTitle("Update App")
            dlg.setText("App Updated. Quitting App now. Please open again.")
            if dlg.exec():
                os._exit(os.EX_OK)
        else:
            dlg = QMessageBox(self.parent)
            dlg.setWindowTitle("Update App")
            dlg.setText("Error Updating. Please check logs for details.")
            dlg.exec()