try:
    import simplejson as json
except ImportError:
    import json
from classes import Player


player1 = Player("")
player2 = Player("")
player3 = Player("")
player4 = Player("")
player5 = Player("")
player6 = Player("")
player7 = Player("")
player8 = Player("")
player9 = Player("")
player10 = Player("")
player11 = Player("")
player12 = Player("")
player13 = Player("")
player14 = Player("")
player15 = Player("")
player16 = Player("")
player17 = Player("")
player18 = Player("")
player19 = Player("")
player20 = Player("")
player21 = Player("")
player22 = Player("")
player23 = Player("")
player24 = Player("")
player25 = Player("")
player26 = Player("")
player27 = Player("")
player28 = Player("")
player29 = Player("")
player30 = Player("")
player31 = Player("")
player32 = Player("")
player33 = Player("")
player34 = Player("")
player35 = Player("")
player36 = Player("")
player37 = Player("")
player38 = Player("")
player39 = Player("")
player40 = Player("")
player41 = Player("")
player42 = Player("")
player43 = Player("")
player44 = Player("")
player45 = Player("")
player46 = Player("")
player47 = Player("")
player48 = Player("")
player49 = Player("")
player50 = Player("")
player51 = Player("")
player52 = Player("")
player53 = Player("")
player54 = Player("")
player55 = Player("")
player56 = Player("")
player57 = Player("")
player58 = Player("")
player59 = Player("")
player60 = Player("")
player61 = Player("")
player62 = Player("")
player63 = Player("")
player64 = Player("")
player65 = Player("")
player66 = Player("")
player67 = Player("")
player68 = Player("")
player69 = Player("")
player70 = Player("")
player71 = Player("")
player72 = Player("")
player73 = Player("")
player74 = Player("")
player75 = Player("")
player76 = Player("")
player77 = Player("")
player78 = Player("")
player79 = Player("")
player80 = Player("")
player81 = Player("")
player82 = Player("")
player83 = Player("")
player84 = Player("")
player85 = Player("")
player86 = Player("")
player87 = Player("")
player88 = Player("")
player89 = Player("")
player90 = Player("")
player91 = Player("")
player92 = Player("")
player93 = Player("")
player94 = Player("")
player95 = Player("")
player96 = Player("")
player97 = Player("")
player98 = Player("")
player99 = Player("")
player100 = Player("")

Players = (player1, player2, player3, player4, player5, player6, player7, player8, player9, player10, player11,
           player12, player13, player14, player15, player16, player17, player18, player19, player20, player21,
           player22,
           player23, player24, player25, player26, player27, player28, player29, player30, player31, player32,
           player33,
           player34, player35, player36, player37, player38, player39, player40, player41, player42, player43,
           player44,
           player45, player46, player47, player48, player49, player50, player51, player52, player53, player54,
           player55,
           player56, player57, player58, player59, player60, player61, player62, player63, player64, player65,
           player66,
           player67, player68, player69, player70, player71, player72, player73, player74, player75, player76,
           player77,
           player78, player79, player80, player81, player82, player83, player84, player85, player86, player87,
           player88,
           player89, player90, player91, player92, player93, player94, player95, player96, player97, player98,
           player99,
           player100)

path_battles = input("Please enter either the relative path or complete path to the battles file: ")
battles_data_file = open(path_battles, "r+")
battles_data = json.loads(battles_data_file.read())

running = True
i = 0
previous_i = 0
print("Use help to open the help menu")
while running:
    command = input("Enter Command:")

    if command == "help":
        print("All possible commands:\n"
              "help - shows this list\n"
              "showlist - shows the list of added names\n"
              "add - adds a new name to the list\n"
              "rm - removes a name from the list\n"
              "save - saves list\n"
              "exit - exits the name adding")
    elif command == "showlist":
        for name in Players:
            if len(name.name) >= 1:
                print(Players.index(name) + 1, name.name)
            elif len(name.name) == 0 and Players.index(name) == 0:
                print("The list is empty. Please add names")
    elif command == "add":
        if i < 100:
            if previous_i == 0:
                name = input("Enter name:")
                Players[i].name = name
                i += 1
            else:
                name = input("Enter name:")
                Players[i].name = name
                i = previous_i
        else:
            print("The list is already full!")
    elif command == "rm":
        index = int(input("Please enter the index number of the name to be removed.\n"
                          "You can find the indices with 'showlist':")) - 1
        Players[index].name = ""
        previous_i = i
        i = index
    elif command == "save":
        data = []
        path = "./saves/" + input("Please enter name of the file. It will be saved to a subdirectory: ") + ".json"
        file = open(path, "w+")
        for player in Players:
            data.append(player.name)

        file_data = json.dumps(data)
        file.write(file_data)
        file.close()
        print("Data has been written.")
    elif command == "load":
        path = "./saves/" + input("Please enter the name of the file you want to load: ") + ".json"
        file = open(path, "r+")
        data = json.loads(file.read())
        for player in data:
            Players[data.index(player)].name = player
        print("Data has been read.")
    elif command == "exit":
        running = False
        break

for battle in battles_data:
    for index in range(14):
        name = battle["BothTeams"][index]["Name"]
        for player in Players:
            if name == player.name:
                player.battles += 1


for player in Players:
    if player.battles >= 1:
        print(player.name, player.battles)
