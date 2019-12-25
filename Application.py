import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Button import Button


class Application(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WoT-BattleCounter")
        self.createapp()

    def createapp(self):
        buttons = ("Add", "Remove", "Load", "Save", "Done")

        window = QVBoxLayout()
        additemdiv = QHBoxLayout()
        listbuttonsdiv = QHBoxLayout()
        buttonsdiv = QVBoxLayout()
        inputline = QLineEdit()
        namelist = QListWidget()

        additemdiv.addWidget(inputline)
        listbuttonsdiv.addWidget(namelist)

        for button in buttons:
            buttonobject = Button(button, inputline, namelist)

            if button == "Add":
                additemdiv.addWidget(buttonobject.button)
            else:
                buttonsdiv.addWidget(buttonobject.button)

        window.addLayout(additemdiv)
        window.addLayout(listbuttonsdiv)
        listbuttonsdiv.addLayout(buttonsdiv)

        self.setLayout(window)
        self.show()
