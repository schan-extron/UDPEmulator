import sys

from PyQt5.QtNetwork import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import json
import socket
from CustomJsonParser import customJsonParser


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'UDP/HTTP Emulator'
        self.listOfCommands = []
        self.initUI()
        self.IPAddr = socket.gethostbyname(socket.gethostname())
        self.port = '0'

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(300, 300, 720, 480)
        self.setWindowIcon(QIcon("icon.PNG"))
        self.statusBar().showMessage('Ready')
        self.setAcceptDrops(True)
        self.widget = QWidget()
        self.hbox = QHBoxLayout(self.widget)
        self.label = QLabel("Drop JSON file here")
        font = QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.hbox.addWidget(self.label)
        self.setCentralWidget(self.widget)

    def createSettings(self):
        self.setAcceptDrops(False)
        self.commandsVBox = QVBoxLayout()
        self.rightSide = QVBoxLayout()
        cmdLabelList = [QLabel(cmd) for cmd in self.listOfCommands]
        for c in cmdLabelList:
            c.setFixedWidth(300)
            self.commandsVBox.addWidget(c)
            self.commandsVBox.addWidget(QLineEdit())

        ipLineEdit = QLineEdit()
        ipLineEdit.setText(self.IPAddr)

        portLineEdit = QLineEdit()
        portLineEdit.setText(self.port)

        settingHBox = QHBoxLayout()
        flo = QFormLayout()
        flo.addRow("IP Address", ipLineEdit)
        flo.addRow("Port", portLineEdit)
        ipLineEdit.setMaxLength(15)
        # ipLineEdit.setFixedWidth(120)
        portLineEdit.setMaxLength(5)
        # portLineEdit.setFixedWidth(120)
        connectionVbox = QVBoxLayout()
        connectButton = QPushButton("Connect")
        connectButton.clicked.connect(self.connectClicked)
        disconnectButton = QPushButton("Disconnect")
        disconnectButton.clicked.connect(self.disconnectClicked)
        connectionVbox.addWidget(connectButton)
        connectionVbox.addWidget(disconnectButton)
        connectionVbox.addStretch(1)
        settingHBox.addLayout(flo)
        settingHBox.addLayout(connectionVbox)
        self.rightSide.addLayout(settingHBox)
        self.hbox.addLayout(self.commandsVBox)
        self.hbox.addSpacing(15)
        self.hbox.addLayout(self.rightSide)

        addCommandAction = QAction(QIcon('add.png'), 'Add Command', self)
        addCommandAction.setShortcut('Ctrl+1')
        addCommandAction.setStatusTip('Add Command')
        addCommandAction.triggered.connect(self.addCommandClicked)

        saveFileAction = QAction(QIcon('save.png'), 'Save', self)
        saveFileAction.setShortcut('Ctrl+2')
        saveFileAction.setStatusTip('Save current emulator file')
        saveFileAction.triggered.connect(self.saveFileClicked)

        toolbar = self.addToolBar('Add Command')
        toolbar.addAction(addCommandAction)
        toolbar.addAction(saveFileAction)

        traceVBox = QVBoxLayout()
        w = QWidget()
        w.resize(420, 200)
        receiveBox = QPlainTextEdit(w)
        receiveBox.setPlainText('Hello\rWorld')
        receiveBox.setReadOnly(True)
        receiveBox.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)
        transmitBox = QPlainTextEdit(w)
        transmitBox.setReadOnly(True)
        transmitBox.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)
        traceVBox.addWidget(QLabel('Receive'))
        traceVBox.addWidget(receiveBox)
        traceVBox.addWidget(QLabel('Transmit'))
        traceVBox.addWidget(transmitBox)
        self.rightSide.addLayout(traceVBox)

    def connectClicked(self):
        self.statusBar().showMessage("Connected")

    def disconnectClicked(self):
        self.statusBar().showMessage("Disconnected")

    def addCommandClicked(self):
        newCmdLineEdit = QLineEdit()
        newCmdLineEdit.setFixedWidth(300)
        self.commandsVBox.addWidget(newCmdLineEdit)

    def saveFileClicked(self):
        print('saved')

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        print(event.mimeData().text())
        with open(event.mimeData().text()[8:]) as file:
            data = json.load(file)

        json_parser_obj = customJsonParser(data)
        json_parser_obj.storeModelsAndCommands()

        self.listOfCommands = list(json_parser_obj.commands.keys())
        print('here', self.listOfCommands)
        print(data)
        self.port = str(data['Protocols'][1]['Port'])
        print(self.port)
        self.label.clear()
        self.createSettings()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Quit', "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class Label(QLabel):
    def __init__(self, title, parent):
        super().__init__(title, parent)


app = QApplication(sys.argv)
window = App()
window.show()
app.exec_()
