from json import dumps, loads
from os import path, listdir
from re import compile, search
from struct import unpack
from ttkthemes import ThemedStyle
from tkinter import filedialog, messagebox, Menu, Listbox, Label, StringVar, IntVar, HORIZONTAL, Tk
from tkinter.ttk import Frame, Entry, Button, Scrollbar, Progressbar
from Player import Player


class App(Tk):
    def __init__(self, master=None):
        super().__init__(master)
        self.style = ThemedStyle(self)
        self.style.set_theme('elegance')
        self.iconbitmap(r'data\app.ico')

        self.title('WoT Battle Counter')
        self.menu_bar = Menu(self)
        self.content = Frame(self)
        self.entry = Entry(self.content)
        self.player_list = Listbox(self.content)
        self.count_button = Button(self)
        self.scrollbar = Scrollbar(self.content, orient='vertical')
        self.progress_frame = Frame(self)
        self.progress_info = Label(self.progress_frame)
        self.progress_info_var = StringVar()
        self.progress_bar = Progressbar(self.progress_frame)
        self.progress_bar_var = IntVar()

        self.PlayerObjects = []
        self.replays = []

    def create_app(self):
        # Config menu entries and attach them
        self.menu_bar.add_command(label='Open skirmish files', command=self.open_skirmish_files)
        self.menu_bar.add_command(label='Open list', command=self.load_list)
        self.menu_bar.add_command(label='Save list', command=self.save_list)
        self.menu_bar.add_command(label='About', command=self.about)
        self.config(menu=self.menu_bar)

        # Config main content window
        self.content.config(width=500, height=350)
        self.content.pack(fill='both', expand=1)

        # Config Text Entry + bind enter key
        self.entry.config(width=50)
        self.entry.pack(fill='x')
        self.entry.bind('<Return>', self.add_player)

        # Config Listbox + bind delete key
        self.player_list.config(width=50, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.player_list.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.player_list.pack(side='left', fill='both', expand=1)
        self.player_list.bind('<Delete>', self.remove_player)

        # Config button at the bottom
        self.count_button.config(text='Count!', command=self.decode_replays)
        self.count_button.pack(side='right', padx=20, pady=10)
        self.count_button.state(['disabled'])

        # Config the progress frame + bar + label
        self.progress_frame.pack(side='left', fill='both', pady=5)
        self.progress_info.config(height=1, textvariable=self.progress_info_var)
        self.progress_info.pack(side='top', fill='both')
        self.progress_bar.config(mode='determinate', orient=HORIZONTAL, length=220, variable=self.progress_bar_var)
        self.progress_bar.pack(side='bottom', fill='both')
        self.progress_bar_var.set([0])

        # Config the window
        self.mainloop()

    def add_player(self, event):
        name = self.entry.get()
        self.player_list.insert('end', name)
        self.entry.delete(0, 'end')
        playerobj = Player(name)
        self.PlayerObjects.append(playerobj)

    def remove_player(self, event):
        select = self.player_list.curselection()
        name = self.player_list.get(select)
        self.player_list.delete(select)
        for player in self.PlayerObjects:
            if name == player.name:
                self.PlayerObjects.remove(player)

    def open_skirmish_files(self):
        path = filedialog.askdirectory()
        self.replays = self.list_dir(path)
        self.count_button.state(['!disabled'])

    def save_list(self):
        file_path = filedialog.asksaveasfilename(defaultextension='.json')
        players = list()
        for player in self.PlayerObjects:
            players.append(player.name)
        if path.exists(file_path):
            f = open(file_path, 'w')
        else:
            f = open(file_path, 'x')
        f.seek(0)
        f.write(dumps(players))

    def load_list(self):
        file_path = filedialog.askopenfilename(filetypes=[('json-file', '*.json'), ('all files', '*.*')])
        if path.isfile(file_path):
            self.player_list.delete(0, 'end')
            f = open(file_path, 'r')
            players = loads(f.read())
            for name in players:
                self.player_list.insert('end', name)
                player_obj = Player(name)
                self.PlayerObjects.append(player_obj)
        else:
            pass

    def about(self):
        message = 'WorldOfTanks-BattleCounter 1.0 \n' \
                  '\n' \
                  'Replay decoding works due to code from: \n' \
                  'Phalynx WoT-Replay-To-JSON application on Github'

        messagebox.showinfo('About', message, default='ok')

    def list_dir(self, path):
        entries = listdir(path)
        re_replay = compile('\.wotreplay')
        re_file = compile('\.')
        replays = []
        # recursive function for searching in subdirectories for .wotreplay files and putting them into a list
        for entry in entries:
            if not search(re_file, entry):
                new_path = path + "/" + entry
                new_replays = self.list_dir(new_path)
                for replay in new_replays:
                    replays.append(replay)
            elif search(re_replay, entry):
                replays.append((path + '/' + entry))
            elif not search(re_replay, entry) and search(re_file, entry):
                continue
        return replays

    def decode_replays(self):
        # setup progress bar
        self.progress_bar.config(maximum=len(self.replays))
        self.progress_bar_var = 0

        player_names = list()

        for replay in range(len(self.replays)):
            # update progress bar + info
            self.progress_info_var.set((str(replay+1) + '/' + str(len(self.replays))))
            self.progress_bar.step()
            self.update_idletasks()

            filename_source = self.replays[replay]
            f = open(filename_source, 'rb')
            f.seek(8)
            size = f.read(4)
            data_block_size = unpack('I', size)[0]
            f.seek(12)
            my_block = f.read(int(data_block_size))

            # Convert binary data into a json and then into an iterable tuple
            json_replay = loads(my_block)
            players_dict = [(v, k) for (k, v) in dict.items(json_replay['vehicles'])]

            # Extract names and append to a list
            for player_id in players_dict:
                player_name = player_id[0]['name']
                player_names.append(player_name)

        # COUNTING TIME!
        for name in player_names:
            for player in self.PlayerObjects:
                if name == player.name:
                    player.battles += 1

        # Insert names together with battle count back into the list
        self.player_list.delete(0, 'end')
        for player in self.PlayerObjects:
            self.player_list.insert('end', (player.name, player.battles))
