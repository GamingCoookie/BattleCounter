try:
    import simplejson as json
except ImportError:
    import json
import os, sys
from PyQt5.QtWidgets import *
from Application import Application
from Button import Button


# initialize global variables
PlayersObjects = []
running = True
loading_file = True


# all the functions


def done():
    global running
    running = False
    decision = input("Do you want to sort the list alphanumerical? Y/N ")
    if decision == "Y" or "y":
        PlayersObjects.sort()
    print("")


# Switch-Case

# Actual program code!
# Load the replays json file
app = QApplication(sys.argv)
window = Application()

sys._excepthook = sys.excepthook


def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook
try:
    sys.exit(app.exec_())
except:
    print("Exiting")

'''
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
'''
