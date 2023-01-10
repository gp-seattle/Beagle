from datetime import datetime
from PyQt6.QtCore import (
    pyqtSignal,
    pyqtSlot,
    Qt,
)
from PyQt6.QtWidgets import (
    QComboBox,
    QLabel,
    QTextEdit,
)

class LogBox(QTextEdit):
    addLine = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setFixedHeight(150)
        self.setReadOnly(True)
        self.setLineWrapMode(self.LineWrapMode.NoWrap)
        self.setTabStopDistance(40)

        self.addLine.connect(self.onAddLine)

    @pyqtSlot(str)
    def onAddLine(self, text):
        super().append(str(datetime.now()) + "\t" + text)

class AddressBox(QComboBox):
    def __init__(self, initVal, options = None):
        super().__init__()
        self.status = QLabel()
        self.status.setFixedWidth(80)

        self.currentState = {
            "text": initVal,
            "statusText": "",
            "statusStyle": ""
        }

        self.setEditable(True)
        if options is not None:
            self.addItems(options)
        self.setCurrentText(initVal)
        self.currentTextChanged.connect(self.onChange)
    
    def connected(self):
        self.currentState["text"] = self.currentText()
        self.currentState["statusText"] = "Connected!"
        self.currentState["statusStyle"] = "color: green"
        self.status.setText(self.currentState["statusText"])
        self.status.setStyleSheet(self.currentState["statusStyle"])

    def invalid(self):
        self.currentState["text"] = self.currentText()
        self.currentState["statusText"] = "INVALID"
        self.currentState["statusStyle"] = "color: red"
        self.status.setText(self.currentState["statusText"])
        self.status.setStyleSheet(self.currentState["statusStyle"])

    def onChange(self, text):
        if text == self.currentState["text"]:
            self.status.setText(self.currentState["statusText"])
            self.status.setStyleSheet(self.currentState["statusStyle"])
        else:
            self.status.setText("Modified")
            self.status.setStyleSheet("color: gray")
    
    def addItems(self, texts):
        super().addItems(texts)
        super().setCurrentText(self.currentState["text"])
        self.status.setText(self.currentState["statusText"])
        self.status.setStyleSheet(self.currentState["statusStyle"])