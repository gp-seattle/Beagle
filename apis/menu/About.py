from PyQt6.QtGui import (
    QAction,
)
from PyQt6.QtWidgets import (
    QMessageBox,
)
from util.constants import VERSION

class About(QAction):
    def __init__(self, s):
        super().__init__("&About Beagle", s)
        self.s = s

        dlg = QMessageBox(self.s)
        dlg.setWindowTitle("About Beagle")
        dlg.setText("Version: " + VERSION)

        self.triggered.connect(dlg.exec)