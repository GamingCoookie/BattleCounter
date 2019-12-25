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
            self.load()
        if v == "Done Save":
            self.save()

    def opensave(self):
        self.onscreen[2].setVisible(True)

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

        self.onscreen[2].setVisible(False)


        '''
        decision = input("Loading a list erases the current list, do you want to continue? Y/N: ")
        if decision == "Y" or "y":
            if len(os.listdir("./saves/")) > 0:
                load = True
                print("Available files to load: \n")
                for file in os.listdir("./saves/"):
                    print(file)
                while load:
                    path = "./saves/" + input("Please enter the name of the file you want to load: ")
                    try:
                        file = open(path, "r+")
                        data = json.loads(file.read())
                        for player in data:
                            print(player)
                        file.close()
                        load = False
                    except FileNotFoundError:
                        print("The given file doesn't exist. Please try again.")
                print("Data has been read.")
            else:
                print("No file to load.")
        '''