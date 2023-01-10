from PyQt6.QtWidgets import (
    QComboBox,
    QLabel,
)

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