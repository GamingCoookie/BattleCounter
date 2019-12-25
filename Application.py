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
        elements = ()

        window = QVBoxLayout()
        layouttop = QWidget()
        layoutbottom = QWidget()
        additemdiv = QHBoxLayout(layouttop)
        listbuttonsdiv = QHBoxLayout(layoutbottom)
        buttonsdiv = QVBoxLayout()
        inputline = QLineEdit()
        namelist = QListWidget()

        layoutsave = QWidget()
        savev = QVBoxLayout(layoutsave)
        saveh = QHBoxLayout()
        pathinput = QLineEdit()
        savelable = QLabel()
        doneb = Button("Done Save", pathinput, namelist, elements)

        savelable.setText("Please enter name of the file. It will be saved to a subdirectory called 'saves'")
        savev.addWidget(savelable)
        savev.addLayout(saveh)
        saveh.addWidget(pathinput)
        saveh.addWidget(doneb.button)

        layoutsave.setVisible(False)
        layoutsave.setWindowTitle("WoT-BattleCounter")

        elements = (layouttop, layoutbottom, layoutsave, savelable)

        additemdiv.addWidget(inputline)
        for button in buttons:
            buttonobject = Button(button, inputline, namelist, elements)

            if button == "Add":
                additemdiv.addWidget(buttonobject.button)
            else:
                buttonsdiv.addWidget(buttonobject.button)

        window.addWidget(layouttop)
        window.addWidget(layoutbottom)

        listbuttonsdiv.addWidget(namelist)
        listbuttonsdiv.addLayout(buttonsdiv)

        self.setLayout(window)
        self.show()
