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
        savepathinput = QLineEdit()
        savelabel = QLabel()
        dones = Button("Done Save", savepathinput, namelist, None)

        savelabel.setText("Please enter name of the file. It will be saved to a subdirectory called 'saves'")
        savev.addWidget(savelabel)
        savev.addLayout(saveh)
        saveh.addWidget(savepathinput)
        saveh.addWidget(dones.button)

        layoutsave.hide()
        layoutsave.setWindowTitle("WoT-BattleCounter")

        layoutload = QWidget()
        loadv = QVBoxLayout(layoutload)
        loadh = QHBoxLayout()
        loadpathinput = QLineEdit()
        loadlabel = QLabel()
        donel = Button("Done Load", loadpathinput, namelist, None)

        loadlabel.setText("Please enter name of the file. Loading a list will replace the current list. \n"
                          "Close this window to not load a list.")
        loadv.addWidget(loadlabel)
        loadv.addLayout(loadh)
        loadh.addWidget(loadpathinput)
        loadh.addWidget(donel.button)

        layoutload.hide()
        layoutload.setMinimumWidth(375)
        layoutload.setWindowTitle("WoT-BattleCounter")

        elements = (layouttop, layoutbottom, layoutsave, layoutload, loadlabel)

        dones.onscreen = elements
        donel.onscreen = elements

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
