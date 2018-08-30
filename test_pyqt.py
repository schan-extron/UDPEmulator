import sys

from PyQt5.QtNetwork import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import json
import socket


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
        self.commandsVBox = QVBoxLayout()
        settingTraceVBox = QVBoxLayout()
        cmdLabelList = [QLineEdit(cmd) for cmd in self.listOfCommands]
        for c in cmdLabelList:
            c.setFixedWidth(300)
            self.commandsVBox.addWidget(c)

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
        self.hbox.addLayout(self.commandsVBox)
        self.hbox.addLayout(settingHBox)

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
        self.listOfCommands = data['Models']['General']['AvailableItems']['Commands']
        self.port = str(data['Protocols'][0]['Port'])
        print(self.port)
        print(self.listOfCommands)
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
