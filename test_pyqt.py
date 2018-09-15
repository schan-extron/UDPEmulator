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
        self.ethernetType = ''
        self.commandStateDict = {}
        self.commandStateButtonMap = {}

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(300, 300, 1200, 800)
        self.setWindowIcon(QIcon("icons\\icon.PNG"))
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

        # Create combo box for HTTP request type
        self.dropdownBox = QComboBox()
        self.dropdownBox.addItems(['GET', 'POST', 'PUT'])

        # Most-Outer Container Widget
        widget = QWidget()

        # Most-Outer VBoxLayout
        outtermostVBox = QVBoxLayout(self)

        # Layout of Container Widget
        commandsVBox = QVBoxLayout(self)
        # buttonsLayoutWidget = QGridLayout()

        for command in self.listOfCommands:
            if type(self.commandStateDict[command]) is dict:
                print(command + ' has a dict')
            else:
                commandLabel = QLabel(command)
                commandLabel.setFixedWidth(300)
                commandsVBox.addWidget(commandLabel)
                #commandsVBox.addWidget(QLineEdit())

                tempStateList = self.commandStateDict[command]

                buttonGroup = QButtonGroup()
                buttonGroup.setExclusive(True)
                for state in range(0, len(tempStateList)):
                    button = QPushButton(tempStateList[state], checkable=True)
                    self.saveStateButton(command + tempStateList[state], button)

                    buttonGroup.addButton(button)
                    button.clicked.connect(lambda: self.stateButtonClicked())
                    commandsVBox.addWidget(button)

                #commandsVBox.addWidget(buttonGroup)
                #buttonGroup.buttonClicked(lambda: self.stateButtonClicked())
        self.show()

        widget.setLayout(commandsVBox)

        # Scroll Area Properties
        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setWidgetResizable(False)
        scroll.setWidget(widget)

        # Scroll Area Layer add
        vLayout = QVBoxLayout(self)
        vLayout.addWidget(scroll)
        self.setLayout(vLayout)
        outtermostVBox.addLayout(vLayout)
        self.hbox.addLayout(outtermostVBox)

        # self.rightSide = QVBoxLayout()
        #
        # self.hbox.addLayout(vLayout)

        #self.hbox.addLayout(self.commandsVBox)
        # self.hbox.addSpacing(15)
        # self.hbox.addLayout(self.rightSide)

        w = QWidget()
        w.resize(300, 200)
        receiveBox = QPlainTextEdit(w)
        receiveBox.setPlainText('Receiving\rstuff')
        receiveBox.setReadOnly(True)
        receiveBox.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)
        receiveVBox = QVBoxLayout()
        receiveVBox.addWidget(QLabel('Receive'))
        receiveVBox.addWidget(receiveBox)

        transmitBox = QPlainTextEdit(w)
        transmitBox.setPlainText('transmitting\rstuff')
        transmitBox.setReadOnly(True)
        transmitBox.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)
        transmitVBox = QVBoxLayout()
        transmitVBox.addWidget(QLabel('Transmit'))
        transmitVBox.addWidget(transmitBox)

        splitter1 = QSplitter()

        splitter1.setStyleSheet("handle{image:url(icons\\dottedline.png)}")
        splitter1.addWidget(QPushButton("hello"))
        splitter1.addWidget(QPushButton("world"))
        traceHBox = QHBoxLayout()
        traceHBox.addWidget(splitter1)
        # traceHBox.addLayout(receiveVBox)
        # traceHBox.addLayout(transmitVBox)

        outtermostVBox.addLayout(traceHBox)

        self.initializeToolBar()

    def initializeToolBar(self):
        # Create Add Button
        #########################################################################################################
        addCommandAction = QAction(QIcon('icons\\add.png'), 'Add Command', self)
        addCommandAction.setShortcut('Ctrl+1')
        addCommandAction.setStatusTip('Add Command')
        addCommandAction.triggered.connect(self.addCommandClicked)

        # Create Delete Button
        #########################################################################################################
        removeCommandAction = QAction(QIcon('icons\\remove.png'), 'Remove Command', self)
        removeCommandAction.setShortcut('Ctrl+2')
        removeCommandAction.setStatusTip('Remove Command')
        removeCommandAction.triggered.connect(self.removeCommandClicked)

        # Create Open Button
        #########################################################################################################
        openFileAction = QAction(QIcon('icons\\open.png'), 'Open Emulator File', self)
        openFileAction.setShortcut('Ctrl+3')
        openFileAction.setStatusTip('Open Emulator File')
        openFileAction.triggered.connect(self.openFileClicked)

        # Create Save Button
        #########################################################################################################
        saveFileAction = QAction(QIcon('icons\\save.png'), 'Save', self)
        saveFileAction.setShortcut('Ctrl+4')
        saveFileAction.setStatusTip('Save Emulator File')
        saveFileAction.triggered.connect(self.saveFileClicked)

        # IP AND PORT Label and LineEdit
        #########################################################################################################
        ipAddressLabel = QLabel("IP Address:")
        ipAddressLineEdit = QLineEdit()
        ipAddressLineEdit.setMaxLength(15)
        ipAddressLineEdit.setFixedWidth(120)
        ipPortLabel = QLabel("Port:")
        ipPortLineEdit = QLineEdit()
        ipPortLineEdit.setMaxLength(5)
        ipPortLineEdit.setFixedWidth(120)
        connectButton = QPushButton("Connect")
        disconnectButton = QPushButton("Disconnect")
        connectButton.clicked.connect(self.connectClicked)
        disconnectButton.clicked.connect(self.disconnectClicked)

        #########################################################################################################
        toolbar = self.addToolBar('Add Command')
        toolbar.addAction(addCommandAction)
        toolbar.addAction(removeCommandAction)
        toolbar.addAction(openFileAction)
        toolbar.addAction(saveFileAction)
        toolbar.addWidget(ipAddressLabel)
        toolbar.addWidget(ipAddressLineEdit)
        toolbar.addWidget(ipPortLabel)
        toolbar.addWidget(ipPortLineEdit)
        toolbar.addWidget(connectButton)
        toolbar.addWidget(disconnectButton)
        toolbar.setStyleSheet("QLabel{margin-left:5px} QPushButton{margin-left:5px;padding:4px}")

    def stateButtonClicked(self):
        print(self.sender().text())

    def saveStateButton(self, keyName, buttonObject):
        self.commandStateButtonMap[keyName] = buttonObject

    def connectClicked(self):
        self.statusBar().showMessage("Connected")

    def disconnectClicked(self):
        self.statusBar().showMessage("Disconnected")

    def addCommandClicked(self):
        newCmdLineEdit = QLineEdit()
        newCmdLineEdit.setFixedWidth(300)
        self.commandsVBox.addWidget(newCmdLineEdit)

    def removeCommandClicked(self):
        pass

    def openFileClicked(selfs):
        pass

    def saveFileClicked(self):
        pass

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
        json_parser_obj.storePortAndType()

        self.commandStateDict = json_parser_obj.commands
        # Remove Connection Status key
        del self.commandStateDict['Connection Status']
        print(self.commandStateDict)
        self.listOfCommands = list(self.commandStateDict.keys())
        self.port = json_parser_obj.port
        self.ethernetType = json_parser_obj.ethernetType

        if self.ethernetType == 'HTTP':
            self.setWindowTitle('HTTP Emulator')
        else:
            self.setWindowTitle('UDP Emulator')

        self.label.clear()
        self.createSettings()

    # def closeEvent(self, event):
    #     reply = QMessageBox.question(self, 'Quit', "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    #     if reply == QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()


class Label(QLabel):
    def __init__(self, title, parent):
        super().__init__(title, parent)


app = QApplication(sys.argv)
window = App()
window.show()
app.exec_()
