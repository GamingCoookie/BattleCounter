try:
    import simplejson as json
except ImportError:
    import json
from Player import Player
import os

# initialize global variables
PlayersObjects = []
Players = []
running = True
loading_file = True
i = 0


# all the functions
def showhelp():
    print("All possible commands:\n\n"
          "help - shows this list\n"
          "showlist - shows the list of added names\n"
          "add - adds a new name to the list\n"
          "rm - removes a name from the list\n"
          "save - saves list\n"
          "load - loads list\n"
          "done - exits the name adding\n")


def showlist():
    for name in Players:
        if len(Players) == 0:
            print("The list is empty. Please add names")
        else:
            print(Players.index(name) + 1, name)


def add():
    global i
    if i < 100:
        name = str(input("Enter name:"))
        Players.append(name)
        i += 1
    else:
        print("The list is already full!")


def remove():
    global i
    index = int(input("Please enter the index number of the name to be removed.\n"
                      "You can find the indices with 'showlist':")) - 1
    del Players[index]
    i -= 1


def save():
    if "saves" not in os.listdir("./"):
        os.mkdir("saves")
    data = []
    path = "./saves/" + input("Please enter name of the file. It will be saved to a subdirectory: ") + ".json"
    file = open(path, "w+")
    for player in Players:
        data.append(player.name)

    file_data = json.dumps(data)
    file.write(file_data)
    file.close()
    print("Data has been written.")


def load():
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
                    Players[data.index(player)].name = player
                file.close()
            except FileNotFoundError:
                print("The given file doesn't exist. Please try again.")
        print("Data has been read.")
    else:
        print("No file to load.")


def listexit():
    global running
    running = False
    print("")


# Switch-Case
def switchcase(case):
    func = switch.get(case, "Not a valid command")
    return func()


switch = {
        "help": showhelp,
        "showlist": showlist,
        "add": add,
        "rm": remove,
        "save": save,
        "load": load,
        "done": listexit
    }

# Actual program code!
# Load the replays json file
while loading_file:
    path_battles = input("Please enter either the relative path or complete path to the battles file: ")
    try:
        battles_data_file = open(path_battles, "r+")
        loading_file = False
        battles_data = json.loads(battles_data_file.read())
        battles_data_file.close()
    except FileNotFoundError:
        print("The given file doesn't exist. Please try again.")


# CLI
print("Use help to open the help menu")
while running:
    command = input("Enter command: ")
    if command in switch:
        switchcase(command)
    else:
        print("Command not found, please try again.")

# Instantiate the player objects
for player in Players:
    playerobj = Player(player)
    PlayersObjects.append(playerobj)


# Determine battle amount
for battle in battles_data:
    for index in range(14):
        name = battle["BothTeams"][index]["Name"]
        for player in PlayersObjects:
            if name == player.name:
                player.battles += 1

# Print out results
for player in PlayersObjects:
    if player.battles >= 1:
        print(player.name, player.battles)

# Just here so the program doesn't terminate instantly
input("\nPress enter to terminate the program")