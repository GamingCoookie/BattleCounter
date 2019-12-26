try:
    import simplejson as json
except ImportError:
    import json
import os
from PyQt5.QtWidgets import *
from Player import Player
# global list
PlayerObjects = []


class Button:
    def __init__(self, text, input, list, onscreen):
        self.text = text
        self.button = QPushButton(self.text)
        self.button.clicked.connect(lambda: self.handleinput(self.text))
        self.input = input
        self.list = list
        self.onscreen = onscreen

    # Basically switch-case function
    def handleinput(self, pressedbutton):
        if pressedbutton == "Add":
            self.addname()
        elif pressedbutton == "Remove":
            self.removename()
        elif pressedbutton == "Save":
            self.opensave()
        elif pressedbutton == "Load":
            self.openload()
        elif pressedbutton == "Done Save":
            self.save()
        elif pressedbutton == "Done Load":
            self.load()
        elif pressedbutton == "Next":
            self.opennext()
        elif pressedbutton == "Count!":
            self.next()
        elif pressedbutton == "Clear":
            self.list.clear()

    def addname(self):
        global PlayerObjects
        name = self.input.text()
        self.list.addItem(name)
        self.input.setText("")
        playerobj = Player(name)
        PlayerObjects.append(playerobj)

    def removename(self):
        global PlayerObjects
        selection = self.list.currentRow()
        name = self.list.item(selection).text()
        for player in PlayerObjects:
            if name == player.name:
                PlayerObjects.remove(player)
        self.list.takeItem(selection)

    # prepare pop-up window for save function
    def opensave(self):
        self.onscreen[2].show()
        self.onscreen[3].setText("Please enter name of the file. It will be saved to a subdirectory called 'saves'")
        self.onscreen[4].addWidget(self.onscreen[3])
        self.onscreen[4].addLayout(self.onscreen[5])
        self.onscreen[5].addWidget(self.onscreen[7])
        self.onscreen[5].addWidget(self.onscreen[6].button)
        self.onscreen[6].text = "Done Save"
        self.onscreen[6].button.setText("Done Save")
        self.onscreen[7].setText("")

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

    # prepare pop-up window for load function
    def openload(self):
        self.onscreen[2].show()
        if self.onscreen[3].text() != "File not found. Please try again.":
            self.onscreen[3].setText("Please enter name of the file. Loading a list will replace the current list. \n"
                                     "Close this window to not load a list.")
        self.onscreen[4].addWidget(self.onscreen[3])
        self.onscreen[4].addLayout(self.onscreen[5])
        self.onscreen[5].addWidget(self.onscreen[7])
        self.onscreen[5].addWidget(self.onscreen[6].button)
        self.onscreen[6].text = "Done Load"
        self.onscreen[6].button.setText("Done Load")
        self.onscreen[7].setText("")

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
            self.onscreen[3].setText("File not found. Please try again.")

    # prepare pop-up window for next function
    def opennext(self):
        self.onscreen[2].show()
        if self.onscreen[3].text() != "File not found. Please try again.":
            self.onscreen[3].setText("Please enter complete name of the file. Don't worry after pressing 'Count!'.\n"
                                     "It takes a while to load!")
        self.onscreen[4].addWidget(self.onscreen[3])
        self.onscreen[4].addLayout(self.onscreen[5])
        self.onscreen[5].addWidget(self.onscreen[7])
        self.onscreen[5].addWidget(self.onscreen[6].button)
        self.onscreen[6].text = "Count!"
        self.onscreen[6].button.setText("Count!")
        self.onscreen[7].setText("")

    def next(self):
        filename = self.input.text()
        path = filename
        self.count(path)
        self.onscreen[2].hide()

    def count(self, path):
        try:
            file = open(path, "r+")
            data = json.loads(file.read())
            file.close()
            for battle in data:
                for index in range(14):
                    name = battle["BothTeams"][index]["Name"]
                    for player in PlayerObjects:
                        if name == player.name:
                            player.battles += 1
            self.list.clear()
            for player in PlayerObjects:
                self.list.addItem(player.name + " " + str(player.battles) + " battles fought")
            file.close()
        except FileNotFoundError:
            self.onscreen[3].setText("File not found. Please try again.")
