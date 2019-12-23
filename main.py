try:
    import simplejson as json
except ImportError:
    import json
from classes import getnames


# print("Please enter the complete path to the file with the battles")
# path_battles = input()
# battles_data_file = open(path_battles, "r+")
# battles_data = json.loads(battles_data_file.read())

getnames()

'''
for battle in battles_data:
    for index in range(14):
        name = battle["BothTeams"][index]["Name"]
        for player in Players:
            if name == player.name:
                player.battles += 1


for player in Players:
    if player.battles >= 1:
        print(player.name, player.battles)
'''
