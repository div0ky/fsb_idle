import configparser
import os
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

config = configparser.ConfigParser()
config_file = os.path.expanduser("~") + f"/Documents/Firestone Bot/config.ini"
config.read(config_file)

window = None
party1 = None
party2 = None
party3 = None
party4 = None
party5 = None


class BotGUI:
    def __init__(self):

        self.window = Tk()
        self.window.title("Firestone Bot v3.1.0-stable")
        self.window.geometry("350x80")
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(2, weight=1)
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.main_menu = Menu(self.window)

        self.file_menu = Menu(self.main_menu, tearoff=0)
        # self.file_menu.add_command(label="Save")
        self.file_menu.add_command(label="Exit", command=self.menu_exit)

        self.help_menu = Menu(self.main_menu, tearoff=0)
        self.help_menu.add_command(label="About", command=self.menu_about)

        self.main_menu.add_cascade(label="File", menu=self.file_menu)
        self.main_menu.add_cascade(label="Help", menu=self.help_menu)

        self.window.config(menu=self.main_menu)

        self.btn1 = Button(self.window, text="GENERAL OPTIONS", command=self.options_win, width=40)
        self.btn1.grid(column=0, row=0, padx=15, pady=5, columnspan=2)

        self.btn2 = Button(self.window, text="CONFIGURE PARTY", command=self.party_win, width=40)
        self.btn2.grid(column=0, row=1, padx=15, pady=5, columnspan=2)

        self.window.bind('<Control-n>', self.party_win)

        self.window.mainloop()

    def options_win(self, e=None):
        self.options_win = Toplevel(self.window)
        self.options_win.title("Configure Options")
        self.options_win.geometry("350x220")
        self.options_win.grid_columnconfigure(0, weight=1)
        self.options_win.grid_columnconfigure(2, weight=1)
        self.options_win.resizable(False, False)

        self.options_text = Label(self.options_win, text="Use the boxes below to set your preferred options.")
        self.options_text.grid(column=0, row=0, padx=15, pady=5, columnspan=2)

        self.prestige_state = BooleanVar()
        if config['OPTIONS']['auto_prestige'] == "True":
            self.prestige_state.set(True)
        self.prestige_toggle = Checkbutton(self.options_win, text="Auto-Prestige?", var=self.prestige_state)
        self.prestige_toggle.grid(column=0, row=3, padx=15, pady=5, sticky="w")

        self.guild_state = BooleanVar()
        if config['OPTIONS']['in_guild'] == "True":
            self.guild_state.set(True)
        self.guild_toggle = Checkbutton(self.options_win, text="In Guild?", var=self.guild_state)
        self.guild_toggle.grid(column=1, row=3, padx=15, pady=10, sticky="w")

        self.guardian_label = Label(self.options_win, text="Which Guardian:")
        self.guardian_label.grid(column=0, row=1, padx=15, pady=2, sticky="w")

        self.guardian_choice = ttk.Combobox(self.options_win, state="readonly")
        self.guardian_choice['values'] = ("Fairy", "Dragon")
        if config['OPTIONS']['guardian'] == "1":
            self.guardian_choice.current(0)
        elif config['OPTIONS']['guardian'] == "2":
            self.guardian_choice.current(1)

        self.guardian_choice.grid(column=0, row=2, padx=15, pady=5, sticky="w")

        self.guild_missions_state = BooleanVar()
        self.guild_missions_state.set(True)
        self.guild_missions_toggle = Checkbutton(self.options_win, text="Guild Missions?", var=self.guild_missions_state)
        self.guild_missions_toggle.grid(column=1, row=4, padx=15, pady=5, sticky="w")

        self.prestige_level_label = Label(self.options_win, text="Prestige Multiplier:")
        self.prestige_level_label.grid(column=1, row=1, padx=15, pady=2, sticky="w")

        self.prestige_level = Entry(self.options_win)
        self.prestige_level.grid(column=1, row=2, padx=15, pady=5, sticky="w")
        self.prestige_level.insert(0, config['OPTIONS']['prestige_level'])

        self.g_btn = Button(self.options_win, text="SAVE", width=40, command=self.options_save)
        self.g_btn.grid(column=0, row=5, padx=15, pady=15, columnspan=2)

    def options_save(self, e=None):
        config['OPTIONS']['prestige_level'] = self.prestige_level.get()
        config['OPTIONS']['in_guild'] = str(self.guild_state.get())
        config['OPTIONS']['auto_prestige'] = str(self.prestige_state.get())

        if self.guardian_choice.get() == "Fairy":
            config['OPTIONS']['guardian'] = "1"
        elif self.guardian_choice.get() == "Dragon":
            config['OPTIONS']['guardian'] = "2"

        with open(config_file, 'w') as configfile:
            config.write(configfile)

        self.options_win.destroy()

    def party_win(self, e=None):
        self.party_win = Toplevel(self.window)
        self.party_win.title("Configure Party")
        self.party_win.geometry("350x275")
        self.party_win.grid_columnconfigure(0, weight=1)
        self.party_win.grid_columnconfigure(2, weight=1)
        self.party_win.resizable(False, False)

        """

        Begin building the GUI

        """

        self.party_text = Label(self.party_win, text="Use the boxes below to set your party options.")
        self.party_text.grid(column=0, row=0, padx=15, pady=5, columnspan=2)

        self.party1_label = Label(self.party_win, text="Party Slot 01:")
        self.party1_label.grid(column=0, row=1, padx=15, pady=5, sticky="w")

        self.party2_label = Label(self.party_win, text="Party Slot 02:")
        self.party2_label.grid(column=1, row=1, padx=15, pady=5, sticky="w")

        self.party1 = ttk.Combobox(self.party_win, state="readonly")
        self.party1['values'] = (
            config['PARTY']['party_slot_1'], config['PARTY']['party_slot_2'], config['PARTY']['party_slot_3'],
            config['PARTY']['party_slot_4'], config['PARTY']['party_slot_5'], config['PARTY']['party_slot_6'])
        self.party1.current(0)
        self.party1.grid(column=0, row=2, padx=15, pady=5, sticky="w")

        self.party2 = ttk.Combobox(self.party_win, state="readonly")
        self.party2['values'] = (
            config['PARTY']['party_slot_1'], config['PARTY']['party_slot_2'], config['PARTY']['party_slot_3'],
            config['PARTY']['party_slot_4'], config['PARTY']['party_slot_5'], config['PARTY']['party_slot_6'])
        self.party2.current(1)
        self.party2.grid(column=1, row=2, padx=15, pady=5, sticky="w")

        self.party3_label = Label(self.party_win, text="Party Slot 03:")
        self.party3_label.grid(column=0, row=3, padx=15, pady=5, sticky="w")

        self.party4_label = Label(self.party_win, text="Party Slot 04:")
        self.party4_label.grid(column=1, row=3, padx=15, pady=5, sticky="w")

        self.party3 = ttk.Combobox(self.party_win, state="readonly")
        self.party3['values'] = (
            config['PARTY']['party_slot_1'], config['PARTY']['party_slot_2'], config['PARTY']['party_slot_3'],
            config['PARTY']['party_slot_4'], config['PARTY']['party_slot_5'], config['PARTY']['party_slot_6'])
        self.party3.current(2)
        self.party3.grid(column=0, row=4, padx=15, pady=5, sticky="w")

        self.party4 = ttk.Combobox(self.party_win, state="readonly")
        self.party4['values'] = (
            config['PARTY']['party_slot_1'], config['PARTY']['party_slot_2'], config['PARTY']['party_slot_3'],
            config['PARTY']['party_slot_4'], config['PARTY']['party_slot_5'], config['PARTY']['party_slot_6'])
        self.party4.current(3)
        self.party4.grid(column=1, row=4, padx=15, pady=5, sticky="w")

        self.party5_label = Label(self.party_win, text="Party Slot 05:")
        self.party5_label.grid(column=0, row=5, padx=15, pady=5, sticky="w")

        self.party_size_label = Label(self.party_win, text="Party Size:")
        self.party_size_label.grid(column=1, row=5, padx=15, pady=5, sticky="w")

        self.party5 = ttk.Combobox(self.party_win, state="readonly")
        self.party5['values'] = (
            config['PARTY']['party_slot_1'], config['PARTY']['party_slot_2'], config['PARTY']['party_slot_3'],
            config['PARTY']['party_slot_4'], config['PARTY']['party_slot_5'], config['PARTY']['party_slot_6'])
        self.party5.current(4)
        self.party5.grid(column=0, row=6, padx=15, pady=5, sticky="w")

        self.party_size = ttk.Combobox(self.party_win, state="readonly")
        self.party_size['values'] = ("1", "2", "3", "4", "5")
        self.party_size.current(4)
        self.party_size.grid(column=1, row=6, padx=15, pady=5, sticky="w")

        self.btn = Button(self.party_win, text="SAVE", command=self.party_save, width=40)
        self.btn.grid(column=0, row=7, padx=15, pady=15, columnspan=2)

    def party_save(self):
        classes = ["Tank", "Warrior", "Ranger", "Mage", "Priest", "Rogue"]
        selections = []
        selections.extend([self.party2.get(), self.party3.get(), self.party4.get(), self.party5.get()])
        print(selections)

        if self.party1.get() in classes and self.party1.get() not in selections:
            config['PARTY']['party_slot_1'] = self.party1.get()
            classes.remove(self.party1.get())

        selections = []
        selections.extend([self.party1.get(), self.party3.get(), self.party4.get(), self.party5.get()])
        print(selections)

        if self.party2.get() in classes and self.party2.get() not in selections:
            config['PARTY']['party_slot_2'] = self.party2.get()
            classes.remove(self.party2.get())

        selections = []
        selections.extend([self.party1.get(), self.party2.get(), self.party4.get(), self.party5.get()])
        print(selections)

        if self.party3.get() in classes and self.party3.get() not in selections:
            config['PARTY']['party_slot_3'] = self.party3.get()
            classes.remove(self.party3.get())

        selections = []
        selections.extend([self.party1.get(), self.party2.get(), self.party3.get(), self.party5.get()])
        print(selections)

        if self.party4.get() in classes and self.party4.get() not in selections:
            config['PARTY']['party_slot_4'] = self.party4.get()
            classes.remove(self.party4.get())

        selections = []
        selections.extend([self.party1.get(), self.party2.get(), self.party3.get(), self.party4.get()])
        print(selections)

        if self.party5.get() in classes and self.party5.get() not in selections:
            config['PARTY']['party_slot_5'] = self.party5.get()
            classes.remove(self.party5.get())

        config['PARTY']['party_size'] = self.party_size.get()

        with open(config_file, 'w') as configfile:
            config.write(configfile)

        self.party_win.destroy()

    def menu_exit(self):
        exit(1)

    def menu_about(self):
        messagebox.showinfo("Firestone Bot v3.1.0-stable",
                            "Created by: div0ky\nhttp:\\\\github.com\\div0ky\n\nVersion 3.1.0-stable")

    def on_closing(self):
        self.window.quit()
        self.window.destroy()

if __name__ == "__main__":
    gui = BotGUI()
