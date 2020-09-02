from json import dumps, loads
from os import path, listdir
from re import compile, search
from struct import unpack
from ttkthemes import ThemedStyle
from tkinter import filedialog, messagebox, Menu, Listbox, Tk, IntVar, Toplevel, HORIZONTAL
from tkinter.ttk import Frame, Entry, Button, Scrollbar, Checkbutton, Labelframe, Label, Style, Progressbar
from Player import Player
from threading import Thread
from functools import partial
from queue import Queue
from time import sleep


def validate_config_entry(text):
    if text == '':
        return True
    try:
        int(text)
        return True
    except (AttributeError, ValueError):
        return False


def about():
    message = 'WorldOfTanks-BattleCounter 1.2 \n' \
              '\n' \
              'Replay decoding works due to code from: \n' \
              'Phalynx WoT-Replay-To-JSON application on Github'
    messagebox.showinfo('About', message, default='ok')


def config_cancel(window):
    window.destroy()


class App(Tk):
    def __init__(self, master=None):
        super().__init__(master)
        self.style = ThemedStyle(self)
        self.style.set_theme('elegance')
        self.iconbitmap(r'data\app.ico')
        self.minsize(450, 300)

        self.title('WoT Battle Counter')
        self.menu_bar = Menu(self)
        self.content = Frame(self)
        self.entry = Entry(self.content)
        self.player_list = Listbox(self.content)
        self.count_button = Button(self)
        self.scrollbar = Scrollbar(self.content)
        self.buttons_frame = Frame(self)
        self.sort_button = Checkbutton(self.buttons_frame)
        self.progressbar = Progressbar(self.buttons_frame)
        self.sort_variable = IntVar(self)
        self.PlayerObjects = []
        self.replays = []
        self.player_names = []
        self.offset = 0
        self.skirmish_value = 1
        self.advance_value = 1
        self.clan_war_value = 3

    def create_app(self):
        # Config menu entries and attach them
        self.menu_bar.add_command(label='Config', command=self.open_config_window)
        self.menu_bar.add_command(label='Open replay files', command=self.open_skirmish_files)
        self.menu_bar.add_command(label='Open list', command=self.load_list)
        self.menu_bar.add_command(label='Save list', command=self.save_list)
        self.menu_bar.add_command(label='Export to file', command=self.export_to_file)
        self.menu_bar.add_command(label='About', command=about)
        self.config(menu=self.menu_bar)

        # Config main content window
        self.content.pack(fill='both', expand=1)

        # Config Text Entry + bind enter key
        self.entry.config(exportselection=0)
        self.entry.pack(fill='x')
        self.entry.bind('<Return>', self.add_player)

        # Config Listbox + bind delete key
        self.player_list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.player_list.yview, orient='vertical')
        self.scrollbar.pack(side='right', fill='y')
        self.player_list.pack(side='left', fill='both', expand=1)
        self.player_list.bind('<Delete>', self.remove_player)

        # Count button at the bottom
        self.count_button.config(text='Count!', command=Thread(target=self.decode_replays).start)
        self.count_button.pack(side='right', padx=10, pady=10)
        self.count_button.state(['disabled'])

        # Config button frame + button + progressbar
        self.buttons_frame.pack(side='left', fill='both', pady=5, padx=5, expand=1)
        self.sort_button.config(text="Sort the list", variable=self.sort_variable)
        self.sort_button.pack(anchor='nw', pady=3, padx=3)
        self.progressbar.config(length=360, mode='indeterminate', orient=HORIZONTAL, maximum=10)
        self.progressbar.pack(anchor='e', pady=3, padx=3)

        # Config the style
        Style().configure('TEntry', background='white')
        Style().configure('TButton', font=('Roboto', 12))
        Style().configure('OK.TButton', font=('Roboto', 12, 'bold'))

        # Loading configuration
        self.load_config()

        # Start the app
        self.mainloop()

    def add_player(self, event):
        name = self.entry.get()
        self.entry.delete(0, 'end')
        player_obj = Player(name)
        self.PlayerObjects.append(player_obj)
        if self.sort_variable.get() == 1:
            self.PlayerObjects.sort(key=lambda player: player.name.lower())
            self.player_list.delete(0, 'end')
            for player in self.PlayerObjects:
                self.player_list.insert('end', (self.PlayerObjects.index(player)+self.offset+1, player.name))
        else:
            self.player_list.delete(0, 'end')
            for player in self.PlayerObjects:
                self.player_list.insert('end', (self.PlayerObjects.index(player)+self.offset+1, player.name))

    def remove_player(self, event):
        select = self.player_list.curselection()
        name = self.player_list.get(select)
        self.player_list.delete(select)
        for player in self.PlayerObjects:
            if name.split()[1] == player.name:
                self.PlayerObjects.remove(player)

        self.player_list.delete(0, 'end')
        for player in self.PlayerObjects:
            self.player_list.insert('end', (self.PlayerObjects.index(player)+self.offset+1, player.name))

    def open_skirmish_files(self):
        directory_path = filedialog.askdirectory()
        if not path.exists(directory_path):
            return
        self.replays = self.list_dir(directory_path)
        self.count_button.state(['!disabled'])

    def save_list(self):
        file_path = filedialog.asksaveasfilename(defaultextension='.json')
        if not path.exists(file_path):
            return
        players = list()
        for player in self.PlayerObjects:
            players.append(player.name)
        if path.isfile(file_path):
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
                player_obj = Player(name)
                self.PlayerObjects.append(player_obj)
            for player in self.PlayerObjects:
                self.player_list.insert('end', (self.PlayerObjects.index(player)+self.offset+1, player.name))

    def export_to_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension='.txt')
        if path.isfile(file_path):
            f = open(file_path, 'w')
        elif path.exists(file_path):
            f = open(file_path, 'x')
        else:
            return
        data = str()
        for player in self.PlayerObjects:
            if player.battles >= 100:
                data += f'{player.battles}  {player.name} \n'
            elif player.battles >= 10:
                data += f'{player.battles}   {player.name} \n'
            elif player.battles > 0:
                data += f'{player.battles}    {player.name} \n'
        f.seek(0)
        f.write(data)

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
        self.progressbar.start()
        thread_queue = Queue()
        replay_list_1 = [self.replays[x] for x in range(0, round(len(self.replays) / 4))]
        replay_list_2 = [self.replays[x] for x in range(round(len(self.replays) / 4), round(len(self.replays) / 4) * 2)]
        replay_list_3 = [self.replays[x] for x in range(round(len(self.replays) / 4) * 2, round(len(self.replays) / 4) * 3)]
        replay_list_4 = [self.replays[x] for x in range(round(len(self.replays) / 4) * 3, len(self.replays))]

        thread_1 = Thread(target=self.convert_binary_data, args=(replay_list_1, thread_queue))
        thread_2 = Thread(target=self.convert_binary_data, args=(replay_list_2, thread_queue))
        thread_3 = Thread(target=self.convert_binary_data, args=(replay_list_3, thread_queue))
        thread_4 = Thread(target=self.convert_binary_data, args=(replay_list_4, thread_queue))

        threads = (thread_1, thread_2, thread_3, thread_4)

        for thread in threads:
            thread.start()

        sleep(1)
        if self.listen_for_result(threads):
            self.player_names = thread_queue.get()
            for name in thread_queue.get():
                self.player_names.append(name)
            for name in thread_queue.get():
                self.player_names.append(name)
            for name in thread_queue.get():
                self.player_names.append(name)

        # COUNTING TIME!
        for name in self.player_names:
            for player in self.PlayerObjects:
                if name[0] == player.name:
                    player.battles += name[1]

        # Insert names together with battle count back into the list
        self.player_list.delete(0, 'end')
        for player in self.PlayerObjects:
            if player.battles > 0:
                self.player_list.insert('end',
                                        (self.PlayerObjects.index(player)+self.offset+1, player.name, player.battles))
            else:
                continue
        self.progressbar.stop()

    def listen_for_result(self, threads):
        # Check if all replay results have come in
        alive_threads = 0
        for thread in threads:
            thread.join(0.1)
        for thread in threads:
            if thread.is_alive():
                print("thread not ded")
                alive_threads += 1
        if alive_threads > 0:
            if self.listen_for_result(threads):
                return True
        return True

    def convert_binary_data(self, replays, queue):
        player_names = list()
        for replay in range(len(replays)):
            filename_source = replays[replay]
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
                if json_replay['battleType'] == 20:
                    player_names.append((player_name, self.skirmish_value))
                elif json_replay['battleType'] == 13:
                    player_names.append((player_name, self.clan_war_value))
                else:
                    player_names.append((player_name, 1))
        queue.put(player_names)

    def open_config_window(self):
        config_window = Toplevel(self)
        config_window.iconbitmap(r'data\app.ico')
        config_window.minsize(500, 350)

        config_frame = Labelframe(config_window)
        config_frame.config(text="App Configuration", relief='groove', borderwidth=5)
        config_frame.pack(expand=1, fill='both', padx=5, pady=5)

        offset_title = Label(config_frame)
        offset_title.config(text='Numbering offset (Default 0)')
        offset_title.pack(anchor='nw', padx=5, pady=5)

        offset_entry = Entry(config_frame)
        offset_entry.config(width=10, exportselection=0, validate='key',
                            validatecommand=(offset_entry.register(validate_config_entry), '%P'))
        offset_entry.pack(anchor='nw', padx=5, pady=5)

        battle_value_frame = Labelframe(config_frame)
        battle_value_frame.config(text='Battle weighting', relief='groove', borderwidth=5)
        battle_value_frame.pack(anchor='nw', fill='both', expand=1, padx=5, pady=5)

        descriptor_frame = Frame(battle_value_frame)
        descriptor_frame.pack(side='left', fill='both', expand=1)

        entry_frame = Frame(battle_value_frame)
        entry_frame.pack(side='left', fill='both', expand=1)

        skirmish_title = Label(descriptor_frame)
        skirmish_title.config(text='Skirmish weighting (Default = 1):')
        skirmish_title.pack(anchor='nw', padx=5, pady=7)

        skirmish_entry = Entry(entry_frame)
        skirmish_entry.config(width=10, exportselection=0, validate='key',
                              validatecommand=(skirmish_entry.register(validate_config_entry), '%P'))
        skirmish_entry.pack(anchor='nw', padx=5, pady=5)

        advance_title = Label(descriptor_frame)
        advance_title.config(text='Advance weighting (Default = 1):')
        advance_title.pack(anchor='nw', padx=5, pady=10)

        advance_entry = Entry(entry_frame)
        advance_entry.config(width=10, exportselection=0, validate='key',
                             validatecommand=(advance_entry.register(validate_config_entry), '%P'))
        advance_entry.pack(anchor='nw', padx=5, pady=5)

        clan_war_title = Label(descriptor_frame)
        clan_war_title.config(text='Clan War weighting (Default = 3):')
        clan_war_title.pack(anchor='nw', padx=5, pady=6)

        clan_war_entry = Entry(entry_frame)
        clan_war_entry.config(width=10, exportselection=0, validate='key',
                              validatecommand=(clan_war_entry.register(validate_config_entry), '%P'))
        clan_war_entry.pack(anchor='nw', padx=5, pady=5)

        buttons_frame = Frame(config_frame)
        buttons_frame.pack(anchor='sw', fill='both', expand=0)

        apply_button = Button(buttons_frame)
        apply_button.config(text='Apply', command=partial(self.config_apply, offset_entry, skirmish_entry, advance_entry
                                                          , clan_war_entry))
        apply_button.pack(side='right', padx=5, pady=5)

        cancel_button = Button(buttons_frame)
        cancel_button.config(text='Cancel', command=lambda: config_window.destroy())
        cancel_button.pack(side='right', padx=5, pady=5)

        ok_button = Button(buttons_frame)
        ok_button.config(text='OK', style='OK.TButton', command=partial(self.config_ok, offset_entry,
                                                                        skirmish_entry, advance_entry,
                                                                        clan_war_entry, config_window))
        ok_button.pack(side='right', padx=5, pady=5)

        offset_entry.insert('end', self.offset)
        skirmish_entry.insert('end', self.skirmish_value)
        advance_entry.insert('end', self.advance_value)
        clan_war_entry.insert('end', self.clan_war_value)

    def config_ok(self, offset, skirmish, advance, clan_war, window):
        self.offset = int(offset.get())
        self.skirmish_value = int(skirmish.get())
        self.advance_value = int(advance.get())
        self.clan_war_value = int(clan_war.get())
        data = {'offset': offset.get(), 'skirmish_value': skirmish.get(), 'advance_value': advance.get(),
                'clan_war_value': clan_war.get()}
        if path.isfile(r'config.json'):
            f = open(r'config.json', 'w')
        else:
            f = open(r'config.json', 'x')
        f.seek(0)
        f.write(dumps(data))
        window.destroy()

    def config_apply(self, offset, skirmish, advance, clan_war):
        self.offset = int(offset.get())
        self.skirmish_value = int(skirmish.get())
        self.advance_value = int(advance.get())
        self.clan_war_value = int(clan_war.get())
        data = {'offset': offset.get(), 'skirmish_value': skirmish.get(), 'advance_value': advance.get(),
                'clan_war_value': clan_war.get()}
        if path.isfile(r'config.json'):
            f = open(r'config.json', 'w')
        else:
            f = open(r'config.json', 'x')
        f.seek(0)
        f.write(dumps(data))

    def load_config(self):
        if path.isfile(r'config.json'):
            f = open(r'config.json', 'r')
            data = loads(f.read())
            print(data)
            self.offset = int(data['offset'])
            self.skirmish_value = int(data['skirmish_value'])
            self.advance_value = int(data['advance_value'])
            self.clan_war_value = int(data['clan_war_value'])
        else:
            pass
