try:
    import simplejson as json
except ImportError:
    import json
import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Button:
    def __init__(self, text, input, list, onscreen):
        self.button = QPushButton(str(text))
        self.text = text
        self.button.clicked.connect(lambda: self.handleinput(self.text))
        self.input = input
        self.list = list
        self.onscreen = onscreen

    def handleinput(self, v):
        print("Pressed:", v)
        if v == "Add":
            name = self.input.text()
            self.list.addItem(name)
            self.input.setText("")
        if v == "Remove":
            selection = self.list.currentRow()
            self.list.takeItem(selection)
        if v == "Save":
            self.opensave()
        if v == "Load":
            self.openload()
        if v == "Done Save":
            self.save()
        if v == "Done Load":
            self.load()

    def opensave(self):
        self.onscreen[2].show()

    def save(self):
        if "saves" not in os.listdir("./"):
            os.mkdir("saves")
        data = []
        filename = self.input.text()
        path = "./saves/" + filename + ".json"

        row = 0
        saving = True

        while saving:
            amount_items = self.list.count()
            if row+1 > amount_items:
                saving = False
            else:
                item = self.list.item(row)
                name = item.text()
                data.append(name)
                row += 1

        file_data = json.dumps(data)
        file = open(path, "w+")
        file.write(file_data)
        file.close()

        self.onscreen[2].hide()

    def openload(self):
        self.onscreen[3].show()

    def load(self):
        filename = self.input.text()
        path = "./saves/" + filename + ".json"
        self.loadfile(path)
        self.onscreen[3].hide()

    def loadfile(self, path):
        try:
            file = open(path, "r+")
            data = json.loads(file.read())
            self.list.clear()
            for player in data:
                self.list.addItem(player)
            file.close()
        except FileNotFoundError:
            self.onscreen[4].setText("File not found. Please try again.")
