#! python3
import sys
from tkinter import Tk, Menu, Label, Button, Toplevel, BooleanVar, messagebox
from tkinter.ttk import Combobox, Checkbutton, Entry, Style

from bot_internals.BotLog import log
from bot_internals.DatabaseManager import database
from bot_internals.version_info import *


class Interface:
    def __init__(self):
        log.info(f'{__name__} has been initialized.')

        self.window = Tk()
        self.window.title(f"Firestone Bot v{current_version}")
        self.window.geometry("380x225")
        self.style = Style()
        # if sys.platform == "win32":
        #     self.style.theme_use('winnative')
        self.window.minsize(380, 200)
        self.window.wait_visibility(self.window)
        self.windowWidth = self.window.winfo_reqwidth()
        self.windowHeight = self.window.winfo_reqheight()
        # Gets both half the screen width/height and window width/height
        self.positionRight = int(self.window.winfo_screenwidth() / 2 - self.windowWidth / 2)
        self.positionDown = int(self.window.winfo_screenheight() / 2 - self.windowHeight / 2)
        self.window.geometry("+{}+{}".format(self.positionRight, self.positionDown))
        self.window.grid_columnconfigure(0, weight=1)
        self.window.resizable(0, 0)
        self.window.attributes("-topmost", True)

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.main_menu = Menu(self.window)

        self.file_menu = Menu(self.main_menu, tearoff=0)
        # self.file_menu.add_command(label="Save")
        self.file_menu.add_command(label="Exit", command=self.menu_exit)

        self.help_menu = Menu(self.main_menu, tearoff=0)
        self.help_menu.add_command(label="About", command=self.menu_about)
        self.help_menu.add_command(label="Change License Key", command=self.menu_change_license)

        self.main_menu.add_cascade(label="File", menu=self.file_menu)
        self.main_menu.add_cascade(label="Help", menu=self.help_menu)

        self.window.config(menu=self.main_menu)

        self.info_label = Label(self.window, text="STOP BOT: SHIFT + ESC", font=("Helvetica", 16))
        self.info_label.grid(column=0, row=0, padx=15, pady=10, columnspan=2)

        self.btn1 = Button(self.window, text="GENERAL OPTIONS", command=self.options_win, width=50)
        self.btn1.grid(column=0, row=1, padx=15, pady=5, columnspan=2)

        self.btn2 = Button(self.window, text="CONFIGURE PARTY", command=self.party_win, width=50)
        self.btn2.grid(column=0, row=2, padx=15, pady=0, columnspan=2)

        self.gobtn = Button(self.window, text="<---    START    --->", command=self.ready_set_go, width=50)
        self.gobtn.config(foreground="white", background="blue")
        self.gobtn.grid(column=0, row=3, padx=15, pady=20, columnspan=2)

        # self.window.bind('<Control-n>', self.party_win)

        # self.window.after(300, self.status_win)

        self.window.mainloop()

    def ready_set_go(self):
        self.window.quit()
        self.window.withdraw()
        self.window.destroy()
        database.paused = False
        log.info(f"Firestone Bot v{current_version} was started!")

    def options_win(self, e=None):
        self.window.withdraw()
        self.options_win = Toplevel(self.window)
        self.options_win.protocol("WM_DELETE_WINDOW", self.options_on_close)
        self.options_win.title(f"Firestone Bot v{current_version}")
        # self.options_win.geometry("400x315")
        self.options_win.minsize(width=400, height=315)
        self.options_win.maxsize(width=400, height=315)
        self.options_win.grid_columnconfigure(0, weight=1)
        self.options_win.grid_columnconfigure(2, weight=1)
        self.options_win.resizable(width=False, height=False)
        # self.options_win.pack_propagate(0)
        self.options_win.attributes("-topmost", True)
        self.options_win.geometry("+{}+{}".format(self.positionRight, self.positionDown))



        self.options_text = Label(self.options_win, text="Use the boxes below to set your preferred options.")
        self.options_text.grid(column=0, row=0, padx=15, pady=5, columnspan=2)

        # Toggle if you want the bot to automatically prestige for you

        self.prestige_state = BooleanVar(self.options_win)
        if database.auto_prestige:
            self.prestige_state.set(True)
        self.prestige_toggle = Checkbutton(self.options_win, text="Auto-Prestige?", var=self.prestige_state)
        self.prestige_toggle.grid(column=0, row=5, padx=15, pady=5, sticky="w")

        # Selection for update channel

        self.updates_label = Label(self.options_win, text="Updates Channel:")
        self.updates_label.grid(column=0, row=3, padx=15, pady=2, sticky="w")

        self.channel_choice = Combobox(self.options_win, state="readonly")
        self.channel_choice['values'] = ("Stable", "Development")
        if database.channel == "Stable":
            self.channel_choice.current(0)
        elif database.channel == "Development":
            self.channel_choice.current(1)
        else:
            self.channel_choice['values'] = self.channel_choice['values'] + (database.channel,)
            self.channel_choice.current(2)
        self.channel_choice.grid(column=0, row=4, padx=15, pady=5, sticky="w")

        self.guardian_label = Label(self.options_win, text="Which Guardian:")
        self.guardian_label.grid(column=0, row=1, padx=15, pady=2, sticky="w")

        self.guardian_choice = Combobox(self.options_win, state="readonly")
        self.guardian_choice['values'] = [x for x in database.read_option('guardians').split(',')]
        if database.guardian == "Fairy":
            self.guardian_choice.current(0)
        elif database.guardian == "Dragon":
            self.guardian_choice.current(1)
        self.guardian_choice.grid(column=0, row=2, padx=15, pady=5, sticky="w")

        self.guild_missions_state = BooleanVar(self.options_win)
        if database.guild_missions:
            self.guild_missions_state.set(True)
        self.guild_missions_toggle = Checkbutton(self.options_win, text="Guild Missions?",
                                                 var=self.guild_missions_state)
        self.guild_missions_toggle.grid(column=1, row=5, padx=15, pady=5, sticky="w")

        self.prestige_level_label = Label(self.options_win, text="Prestige Multiplier:")
        self.prestige_level_label.grid(column=1, row=1, padx=15, pady=2, sticky="w")

        self.prestige_level = Entry(self.options_win)
        self.prestige_level.grid(column=1, row=2, padx=15, pady=5, sticky="w")
        self.prestige_level.insert(0, database.prestige_level)

        self.g_btn = Button(self.options_win, text="SAVE", width=40, command=self.options_save)
        self.g_btn.grid(column=0, row=6, padx=15, pady=15, columnspan=2)
        self.g_btn.config(foreground="white", background="blue")

    def options_save(self, e=None):
        database.save_option('prestige_level', self.prestige_level.get())
        # config['OPTIONS']['in_guild'] = str(self.guild_state.get())
        database.save_option('auto_prestige', self.prestige_state.get())
        database.save_option('guild_missions', self.guild_missions_state.get())
        database.save_option('guardian', self.guardian_choice.get())

        self.window.deiconify()
        self.options_win.destroy()

    def party_win(self, e=None):
        self.window.withdraw()
        self.party_win = Toplevel(self.window)
        self.party_win.protocol("WM_DELETE_WINDOW", self.party_on_close)
        self.party_win.title(f"Firestone Bot v{current_version}")
        # self.party_win.geometry("350x275")
        self.party_win.minsize(width=400, height=350)
        self.party_win.maxsize(width=400, height=350)
        self.party_win.resizable(width=False, height=False)
        self.party_win.grid_columnconfigure(0, weight=1)
        self.party_win.grid_columnconfigure(2, weight=1)
        self.party_win.attributes("-topmost", True)
        self.party_win.geometry("+{}+{}".format(self.positionRight, self.positionDown))

        """

        Begin building the GUI

        """
        self.party_text = Label(self.party_win, text="Use the boxes below to set your party options.")
        self.party_text.grid(column=0, row=0, padx=15, pady=5, columnspan=2)

        self.party1_label = Label(self.party_win, text="Party Slot 01:")
        self.party1_label.grid(column=0, row=1, padx=15, pady=5, sticky="w")

        self.party2_label = Label(self.party_win, text="Party Slot 02:")
        self.party2_label.grid(column=1, row=1, padx=15, pady=5, sticky="w")

        self.party1 = Combobox(self.party_win, state="readonly")
        self.party1['values'] = [x for x in database.heroes]
        self.party1.current(4)
        self.party1.grid(column=0, row=2, padx=15, pady=5, sticky="w")

        self.party2 = Combobox(self.party_win, state="readonly")
        self.party2['values'] = [x for x in database.heroes]
        self.party2.current(10)
        self.party2.grid(column=1, row=2, padx=15, pady=5, sticky="w")

        self.party3_label = Label(self.party_win, text="Party Slot 03:")
        self.party3_label.grid(column=0, row=3, padx=15, pady=5, sticky="w")

        self.party4_label = Label(self.party_win, text="Party Slot 04:")
        self.party4_label.grid(column=1, row=3, padx=15, pady=5, sticky="w")

        self.party3 = Combobox(self.party_win, state="readonly")
        self.party3['values'] = [x for x in database.heroes]
        self.party3.current(5)
        self.party3.grid(column=0, row=4, padx=15, pady=5, sticky="w")

        self.party4 = Combobox(self.party_win, state="readonly")
        self.party4['values'] = [x for x in database.heroes]
        self.party4.current(2)
        self.party4.grid(column=1, row=4, padx=15, pady=5, sticky="w")

        self.party5_label = Label(self.party_win, text="Party Slot 05:")
        self.party5_label.grid(column=0, row=5, padx=15, pady=5, sticky="w")

        self.party_size_label = Label(self.party_win, text="Party Size:")
        self.party_size_label.grid(column=1, row=5, padx=15, pady=5, sticky="w")

        self.party5 = Combobox(self.party_win, state="readonly")
        self.party5['values'] = [x for x in database.heroes]
        self.party5.current(3)
        self.party5.grid(column=0, row=6, padx=15, pady=5, sticky="w")

        self.party_size = Combobox(self.party_win, state="readonly")
        self.party_size['values'] = ("1", "2", "3", "4", "5")
        self.party_size.current(4)
        self.party_size.grid(column=1, row=6, padx=15, pady=5, sticky="w")

        self.btn = Button(self.party_win, text="SAVE", command=self.party_save, width=40)
        self.btn.grid(column=0, row=7, padx=15, pady=15, columnspan=2)
        self.btn.config(foreground="white", background="blue")

    def party_save(self):
        heroes = database.heroes.copy()
        selections = []
        selections.extend([self.party2.get(), self.party3.get(), self.party4.get(), self.party5.get()])
        print(selections)

        party_slot_1 = self.party1.get()
        if party_slot_1 in heroes and party_slot_1 not in selections:
            database.save_option('party_slot_1', party_slot_1)
            heroes.remove(party_slot_1)
        else:
            messagebox.showerror(title="ERROR", message="PARTY SLOT 1: Invalid selection choice.")

        selections = []
        selections.extend([self.party1.get(), self.party3.get(), self.party4.get(), self.party5.get()])
        print(selections)

        party_slot_2 = self.party2.get()
        if party_slot_2 in heroes and party_slot_2 not in selections:
            database.save_option('party_slot_2', party_slot_2)
            heroes.remove(party_slot_2)
        else:
            messagebox.showerror(title="ERROR", message="PARTY SLOT 2: Invalid selection choice.")

        selections = []
        selections.extend([self.party1.get(), self.party2.get(), self.party4.get(), self.party5.get()])
        print(selections)

        party_slot_3 = self.party3.get()
        if party_slot_3 in heroes and party_slot_3 not in selections:
            database.save_option('party_slot_3', party_slot_3)
            heroes.remove(party_slot_3)
        else:
            messagebox.showerror(title="ERROR", message="PARTY SLOT 3: Invalid selection choice.")

        selections = []
        selections.extend([self.party1.get(), self.party2.get(), self.party3.get(), self.party5.get()])
        print(selections)

        party_slot_4 = self.party4.get()
        if party_slot_4 in heroes and party_slot_4 not in selections:
            database.save_option('party_slot_4', party_slot_4)
            heroes.remove(party_slot_4)
        else:
            messagebox.showerror(title="ERROR", message="PARTY SLOT 4: Invalid selection choice.")

        selections = []
        selections.extend([self.party1.get(), self.party2.get(), self.party3.get(), self.party4.get()])
        print(selections)

        party_slot_5 = self.party5.get()
        if party_slot_5 in heroes and party_slot_5 not in selections:
            database.save_option('party_slot_5', party_slot_5)
            heroes.remove(party_slot_5)
        else:
            messagebox.showerror(title="ERROR", message="PARTY SLOT 5: Invalid selection choice.")

        database.save_option('party_size', self.party_size.get())

        self.window.deiconify()
        self.party_win.destroy()

    def status_win(self, e=None):
        # self.window.withdraw()
        print('Deploy status window')
        self.status_win = Toplevel(self.window)
        self.status_win.configure(background="black")
        self.status_win.overrideredirect(1)
        self.status_win.protocol("WM_DELETE_WINDOW", self.status_on_close)
        self.status_win.title(f"Idle Bot Status")
        self.status_win.geometry("350x35")
        self.status_win.grid_columnconfigure(0, weight=1)
        self.status_win.grid_columnconfigure(0, weight=2)
        self.status_win.resizable(0, 0)
        # self.status_win.pack_propagate(0)
        self.status_win.attributes("-topmost", True)
        self.status_win.geometry("+{}+{}".format(0, 0))

        self.status_text = Label(self.status_win, foreground="white", background="black", text="IDLE BOT: Verify my settings before we get started.")
        self.status_text.grid(column=0, row=0, padx=5, pady=5, columnspan=2, sticky="w")

    def update_status(self, status):
        self.status_text.config(text=f"IDLE BOT: {status}")
        self.status_win.update()

    def menu_exit(self):
        self.window.quit()
        self.window.destroy()
        database.running = False

    def menu_change_license(self):
        self.change_license()

    def menu_about(self):
        if database.email:
            user = database.email
        else:
            user = "UNLICENSED"

        messagebox.showinfo(f"ABOUT", f"FIRESTONE IDLE BOT v{current_version}\n\nLICENSED TO: {user}\n\nThank you for supporting Firestone Idle Bot!", parent=self.window)

    def options_on_close(self):
        self.window.deiconify()
        self.options_win.destroy()


    def status_on_close(self):
        self.status_win.destroy()

    def party_on_close(self):
        self.window.deiconify()
        self.party_win.destroy()

    def on_closing(self):
        self.window.quit()
        self.window.destroy()
        database.running = False


if __name__ == "__main__":
    gui = Interface()
