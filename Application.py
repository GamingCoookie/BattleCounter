from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QListWidget, QLabel
from Button import Button


class Application(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WoT-BattleCounter")
        self.createapp()

    def createapp(self):
        buttons = ("Add", "Remove", "Clear", "Save", "Load", "Next")
        # Create main window and elements
        window = QVBoxLayout()
        layouttop = QWidget()
        layoutbottom = QWidget()
        additemdiv = QHBoxLayout(layouttop)
        listbuttonsdiv = QHBoxLayout(layoutbottom)
        buttonsdiv = QVBoxLayout()
        inputline = QLineEdit()
        namelist = QListWidget()
        # Create pop-up window and elements
        layoutpopup = QWidget()
        popupvertical = QVBoxLayout(layoutpopup)
        popuphorizontal = QHBoxLayout()
        popuppathinput = QLineEdit()
        popuplabel = QLabel()
        donepopup = Button("", popuppathinput, namelist, None)
        # Hide pop-up window and set basic properties
        layoutpopup.hide()
        layoutpopup.setMinimumWidth(375)
        layoutpopup.setWindowTitle("WoT-BattleCounter")
        # set elements tuple with variables to be used by functions in Button class
        elements = (None, None, layoutpopup, popuplabel, popupvertical, popuphorizontal, donepopup,
                    popuppathinput)

        donepopup.onscreen = elements
        # Add layouts and widgets to main window
        window.addWidget(layouttop)
        window.addWidget(layoutbottom)
        additemdiv.addWidget(inputline)

        for button in buttons:
            buttonobject = Button(button, inputline, namelist, elements)
            if button == "Add":
                additemdiv.addWidget(buttonobject.button)
            else:
                buttonsdiv.addWidget(buttonobject.button)

        listbuttonsdiv.addWidget(namelist)
        listbuttonsdiv.addLayout(buttonsdiv)
        # Show the main window
        self.setLayout(window)
        self.show()
