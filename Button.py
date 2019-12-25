import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Button:
    def __init__(self, text, input, list):
        self.button = QPushButton(str(text))
        self.text = text
        self.button.clicked.connect(lambda: self.handleinput(self.text))
        self.input = input
        self.list = list

    def handleinput(self, v):
        print("Pressed:", v)
        if v == "Add":
            name = self.input.text()
            self.list.addItem(name)
            self.input.setText("")
        if v == "Remove":
            selection = self.list.currentRow()
            self.list.takeItem(selection)
