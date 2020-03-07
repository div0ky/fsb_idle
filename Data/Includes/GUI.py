#! python3
import configparser
import http.client
import json
import os
import sys
import urllib
from tkinter import Tk, Menu, Label, Button, Toplevel, BooleanVar, messagebox, HORIZONTAL, simpledialog
from tkinter.ttk import Combobox, Checkbutton, Entry, Progressbar, Style

import requests
import semver
from requests import get

from Data.Includes.ver import version_info

config = configparser.ConfigParser()
config_file = os.getenv('LOCALAPPDATA') + "/Firestone Bot/config.ini"
config.read(config_file)

version_info = version_info()

if version_info.vStage == "stable":
    current_version = version_info.version
else:
    current_version = version_info.full_version

window = None
party1 = None
party2 = None
party3 = None
party4 = None
party5 = None


def push(msg):
    ip = get('https://api.ipify.org').text
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
                 urllib.parse.urlencode({
                     "token": "anj13d6adu8s3hm66pfmiwacjxwt36",
                     "user": "uGUQThApDAJfvscP5Levk419xn7yyx",
                     "message": f"{ip} - {msg}",
                 }), {"Content-type": "application/x-www-form-urlencoded"})
    conn.getresponse()


class BotGUI:
    def __init__(self):

        self.key_info = None
        try:
            self.license_key = str(config['OPTIONS']['license_key'])
        except:
            self.license_key = ''

        """
        DEFINE VERSION INFO
        """

        self.window = Tk()
        self.window.title(f"Firestone Bot v{current_version}")
        self.window.geometry("380x225")
        self.style = Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
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
        # self.window.pack_propagate(0)
        self.window.attributes("-topmost", True)

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

        self.window.after(300, self.status_win)
        self.verifyLicense(self.license_key)
        self.window.after(300, self.checkVersion)
        # Thread(target=self.status_win, name="StatusWindow", daemon=True).start()

        self.window.mainloop()

    def ready_set_go(self):
        self.window.quit()
        self.window.withdraw()
        # self.window.destroy()
        # push(f"A Firestone Bot with v{current_version} was started!")

    def options_win(self, e=None):
        self.window.withdraw()
        self.options_win = Toplevel(self.window)
        self.options_win.protocol("WM_DELETE_WINDOW", self.options_on_close)
        self.options_win.title(f"Firestone Bot v{current_version}")
        self.options_win.geometry("350x250")
        self.options_win.grid_columnconfigure(0, weight=1)
        self.options_win.grid_columnconfigure(2, weight=1)
        self.options_win.resizable(0, 0)
        # self.options_win.pack_propagate(0)
        self.options_win.attributes("-topmost", True)
        self.options_win.geometry("+{}+{}".format(self.positionRight, self.positionDown))

        self.options_text = Label(self.options_win, text="Use the boxes below to set your preferred options.")
        self.options_text.grid(column=0, row=0, padx=15, pady=5, columnspan=2)

        # Toggle if you want the bot to automatically prestige for you

        self.prestige_state = BooleanVar()
        if config['OPTIONS']['auto_prestige'] == "True":
            self.prestige_state.set(True)
        self.prestige_toggle = Checkbutton(self.options_win, text="Auto-Prestige?", var=self.prestige_state)
        self.prestige_toggle.grid(column=0, row=5, padx=15, pady=5, sticky="w")

        # Selection for update channel

        self.updates_label = Label(self.options_win, text="Updates Channel:")
        self.updates_label.grid(column=0, row=3, padx=15, pady=2, sticky="w")

        self.channel_choice = Combobox(self.options_win, state="readonly")
        self.channel_choice['values'] = ("Stable", "Development")
        if config['OPTIONS']['channel'] == "Stable":
            self.channel_choice.current(0)
        elif config['OPTIONS']['channel'] == "Development":
            self.channel_choice.current(1)
        else:
            self.channel_choice['values'] = self.channel_choice['values'] + (config['OPTIONS']['channel'],)
            self.channel_choice.current(2)
        self.channel_choice.grid(column=0, row=4, padx=15, pady=5, sticky="w")

        # Toggle for if the user is in a guild or not

        # self.guild_state = BooleanVar()
        # if config['OPTIONS']['in_guild'] == "True":
        #    self.guild_state.set(True)
        # self.guild_toggle = Checkbutton(self.options_win, text="In Guild?", var=self.guild_state)
        # self.guild_toggle.grid(column=1, row=3, padx=15, pady=10, sticky="w")

        # Select which guardian the user is using

        self.guardian_label = Label(self.options_win, text="Which Guardian:")
        self.guardian_label.grid(column=0, row=1, padx=15, pady=2, sticky="w")

        self.guardian_choice = Combobox(self.options_win, state="readonly")
        self.guardian_choice['values'] = ("Fairy", "Dragon")
        if config['OPTIONS']['guardian'] == "1":
            self.guardian_choice.current(0)
        elif config['OPTIONS']['guardian'] == "2":
            self.guardian_choice.current(1)
        self.guardian_choice.grid(column=0, row=2, padx=15, pady=5, sticky="w")

        self.guild_missions_state = BooleanVar()
        if config['OPTIONS']['guild_missions'] == "True":
            self.guild_missions_state.set(True)
        self.guild_missions_toggle = Checkbutton(self.options_win, text="Guild Missions?",
                                                 var=self.guild_missions_state)
        self.guild_missions_toggle.grid(column=1, row=5, padx=15, pady=5, sticky="w")

        self.prestige_level_label = Label(self.options_win, text="Prestige Multiplier:")
        self.prestige_level_label.grid(column=1, row=1, padx=15, pady=2, sticky="w")

        self.prestige_level = Entry(self.options_win)
        self.prestige_level.grid(column=1, row=2, padx=15, pady=5, sticky="w")
        self.prestige_level.insert(0, config['OPTIONS']['prestige_level'])

        self.g_btn = Button(self.options_win, text="SAVE", width=40, command=self.options_save)
        self.g_btn.grid(column=0, row=6, padx=15, pady=15, columnspan=2)

    def options_save(self, e=None):
        config['OPTIONS']['prestige_level'] = self.prestige_level.get()
        # config['OPTIONS']['in_guild'] = str(self.guild_state.get())
        config['OPTIONS']['auto_prestige'] = str(self.prestige_state.get())
        config['OPTIONS']['guild_missions'] = str(self.guild_missions_state.get())

        if self.guardian_choice.get() == "Fairy":
            config['OPTIONS']['guardian'] = "1"
        elif self.guardian_choice.get() == "Dragon":
            config['OPTIONS']['guardian'] = "2"

        with open(config_file, 'w') as configfile:
            config.write(configfile)

        self.window.deiconify()
        self.options_win.destroy()

    def party_win(self, e=None):
        self.window.withdraw()
        self.party_win = Toplevel(self.window)
        self.party_win.protocol("WM_DELETE_WINDOW", self.party_on_close)
        self.party_win.title(f"Firestone Bot v{current_version}")
        self.party_win.geometry("350x275")
        self.party_win.grid_columnconfigure(0, weight=1)
        self.party_win.grid_columnconfigure(2, weight=1)
        self.party_win.resizable(0, 0)
        # self.party_win.pack_propagate(0)
        self.party_win.attributes("-topmost", True)
        self.party_win.geometry("+{}+{}".format(self.positionRight, self.positionDown))

        """

        Begin building the GUI

        """
        # TODO: Add support for the Rogue
        self.party_text = Label(self.party_win, text="Use the boxes below to set your party options.")
        self.party_text.grid(column=0, row=0, padx=15, pady=5, columnspan=2)

        self.party1_label = Label(self.party_win, text="Party Slot 01:")
        self.party1_label.grid(column=0, row=1, padx=15, pady=5, sticky="w")

        self.party2_label = Label(self.party_win, text="Party Slot 02:")
        self.party2_label.grid(column=1, row=1, padx=15, pady=5, sticky="w")

        self.party1 = Combobox(self.party_win, state="readonly")
        self.party1['values'] = (
            config['PARTY']['party_slot_1'], config['PARTY']['party_slot_2'], config['PARTY']['party_slot_3'],
            config['PARTY']['party_slot_4'], config['PARTY']['party_slot_5'])
        self.party1.current(0)
        self.party1.grid(column=0, row=2, padx=15, pady=5, sticky="w")

        self.party2 = Combobox(self.party_win, state="readonly")
        self.party2['values'] = (
            config['PARTY']['party_slot_1'], config['PARTY']['party_slot_2'], config['PARTY']['party_slot_3'],
            config['PARTY']['party_slot_4'], config['PARTY']['party_slot_5'])
        self.party2.current(1)
        self.party2.grid(column=1, row=2, padx=15, pady=5, sticky="w")

        self.party3_label = Label(self.party_win, text="Party Slot 03:")
        self.party3_label.grid(column=0, row=3, padx=15, pady=5, sticky="w")

        self.party4_label = Label(self.party_win, text="Party Slot 04:")
        self.party4_label.grid(column=1, row=3, padx=15, pady=5, sticky="w")

        self.party3 = Combobox(self.party_win, state="readonly")
        self.party3['values'] = (
            config['PARTY']['party_slot_1'], config['PARTY']['party_slot_2'], config['PARTY']['party_slot_3'],
            config['PARTY']['party_slot_4'], config['PARTY']['party_slot_5'])
        self.party3.current(2)
        self.party3.grid(column=0, row=4, padx=15, pady=5, sticky="w")

        self.party4 = Combobox(self.party_win, state="readonly")
        self.party4['values'] = (
            config['PARTY']['party_slot_1'], config['PARTY']['party_slot_2'], config['PARTY']['party_slot_3'],
            config['PARTY']['party_slot_4'], config['PARTY']['party_slot_5'])
        self.party4.current(3)
        self.party4.grid(column=1, row=4, padx=15, pady=5, sticky="w")

        self.party5_label = Label(self.party_win, text="Party Slot 05:")
        self.party5_label.grid(column=0, row=5, padx=15, pady=5, sticky="w")

        self.party_size_label = Label(self.party_win, text="Party Size:")
        self.party_size_label.grid(column=1, row=5, padx=15, pady=5, sticky="w")

        self.party5 = Combobox(self.party_win, state="readonly")
        self.party5['values'] = (
            config['PARTY']['party_slot_1'], config['PARTY']['party_slot_2'], config['PARTY']['party_slot_3'],
            config['PARTY']['party_slot_4'], config['PARTY']['party_slot_5'])
        self.party5.current(4)
        self.party5.grid(column=0, row=6, padx=15, pady=5, sticky="w")

        self.party_size = Combobox(self.party_win, state="readonly")
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
        else:
            messagebox.showerror(title="ERROR", message="PARTY SLOT 1: Invalid selection choice.")

        selections = []
        selections.extend([self.party1.get(), self.party3.get(), self.party4.get(), self.party5.get()])
        print(selections)

        if self.party2.get() in classes and self.party2.get() not in selections:
            config['PARTY']['party_slot_2'] = self.party2.get()
            classes.remove(self.party2.get())
        else:
            messagebox.showerror(title="ERROR", message="PARTY SLOT 2: Invalid selection choice.")

        selections = []
        selections.extend([self.party1.get(), self.party2.get(), self.party4.get(), self.party5.get()])
        print(selections)

        if self.party3.get() in classes and self.party3.get() not in selections:
            config['PARTY']['party_slot_3'] = self.party3.get()
            classes.remove(self.party3.get())
        else:
            messagebox.showerror(title="ERROR", message="PARTY SLOT 3: Invalid selection choice.")

        selections = []
        selections.extend([self.party1.get(), self.party2.get(), self.party3.get(), self.party5.get()])
        print(selections)

        if self.party4.get() in classes and self.party4.get() not in selections:
            config['PARTY']['party_slot_4'] = self.party4.get()
            classes.remove(self.party4.get())
        else:
            messagebox.showerror(title="ERROR", message="PARTY SLOT 4: Invalid selection choice.")

        selections = []
        selections.extend([self.party1.get(), self.party2.get(), self.party3.get(), self.party4.get()])
        print(selections)

        if self.party5.get() in classes and self.party5.get() not in selections:
            config['PARTY']['party_slot_5'] = self.party5.get()
            classes.remove(self.party5.get())
        else:
            messagebox.showerror(title="ERROR", message="PARTY SLOT 5: Invalid selection choice.")

        config['PARTY']['party_size'] = self.party_size.get()

        with open(config_file, 'w') as configfile:
            config.write(configfile)

        self.window.deiconify()
        self.party_win.destroy()

    def status_win(self, e=None):
        # self.window.withdraw()
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
        sys.exit()

    def menu_about(self):
        if self.key_info:
            user = self.key_info['purchase']['email']
        else:
            user = "UNLICENSED"
        messagebox.showinfo(f"ABOUT",
                            f"FIRESTONE IDLE BOT v{current_version}\n\nLicensed to {user}\n\nThank you for supporting Firestone Idle Bot!")

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
        sys.exit()

    def verifyLicense(self, key):
        data = {
            'product_permalink': 'hqKje',
            'license_key': key,
            'increment_uses_count': 'false'
        }

        response = requests.post('https://api.gumroad.com/v2/licenses/verify', data=data)
        self.key_info = json.loads(response.text)

        if self.key_info['success'] == True and self.key_info['purchase']['refunded'] == False:
            return True
        else:
            self.window.withdraw()
            messagebox.showerror(f'Firestone Bot v{current_version}', 'LICENSE KEY IS INVALID OR NOT FOUND.')
            self.notLicensed()
            return False

    def notLicensed(self):
        lkey = None
        valid = False
        while lkey is None and valid == False:
            lkey = simpledialog.askstring(title=f'Firestone Bot v{current_version}', prompt='       PLEASE ENTER YOUR LICENSE KEY:       ')

            if lkey is not None:
                check = self.verifyLicense(lkey)
                if check:
                    # messagebox.showinfo('SUCCESS', 'Key is valid!')
                    self.license_key = self.key_info['purchase']['license_key']
                    config['OPTIONS']['license_key'] = self.license_key
                    with open(config_file, 'w') as configfile:
                        config.write(configfile)
                    valid = True
                    self.window.deiconify()
                else:
                    messagebox.showwarning('INVALID', 'Key is invalid.')
            else:
                messagebox.showwarning('INVALID', 'LICENSE KEY IS INVALID.')
                exit()

    def checkVersion(self):
        print(config['OPTIONS']['channel'])
        if config['OPTIONS']['channel'] == "Development":
            response = requests.get("http://div0ky.com/repo/development/latest.txt")
        elif config['OPTIONS']['channel'] == "Staging":
            response = requests.get("http://div0ky.com/repo/staging/latest.txt")
        else:
            response = requests.get("http://div0ky.com/repo/stable/latest.txt")
        latest = response.text


        print(f"Current Version is {current_version}\nLatest Version is {latest}")

        if semver.compare(latest, current_version) > 0:
            self.window.withdraw()
            root = Tk()
            root.geometry("325x70")
            root.title(f"Firestone Bot v{latest} Updater")
            total_label = Label(root, text="Download Pending...")
            total_label.grid(column=0, row=0, padx=15, pady=5)
            root.grid_columnconfigure(0, weight=1)
            rootWidth = root.winfo_reqwidth()
            rootHeight = root.winfo_reqheight()
            # Gets both half the screen width/height and window width/height
            positionRight = int(root.winfo_screenwidth() / 2 - rootWidth / 2)
            positionDown = int(root.winfo_screenheight() / 2 - rootHeight / 2)
            root.geometry("+{}+{}".format(positionRight, positionDown))
            root.resizable(0, 0)
            # root.pack_propagate(0)
            root.attributes("-topmost", True)
            progress = Progressbar(root, orient=HORIZONTAL, length=300, mode='determinate')
            progress.grid(column=0, row=1, padx=15, pady=10)
            root.withdraw()

            ask_update = messagebox.askyesno(title=f"Firestone Bot v{current_version}",
                                             message=f"A new version is availble. You're running v{current_version}. The latest version is v{latest}.\n\nDo you want to download & update?")

            if ask_update:
                root.deiconify()
                update = f"http://div0ky.com/repo/Firestone_Bot_v{latest}.exe"
                with open(os.getenv('LOCALAPPDATA') + f"/Firestone Bot/Firestone_Bot_v{latest}.exe", 'wb') as f:
                    response = requests.get(update, stream=True)
                    total_size = response.headers.get('content-length')
                    if total_size is None:
                        f.write(response.content)
                    else:
                        dl = 0
                        total_size = int(total_size)
                        adj_size = round(int(total_size) / 1000, 2)
                        for data in response.iter_content(chunk_size=4096):
                            dl += len(data)
                            adj_dl = round(dl / 1000, 2)
                            f.write(data)
                            done = int(100 * dl / total_size)
                            progress['value'] = done
                            total_label.config(text=f"{adj_dl}KB / {adj_size}KB")
                            root.update()
                            # print("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                    total_label.config(text="DOWNLOAD COMPLETE")
                    # messagebox.showinfo(title="DOWNLOAD COMPLETE", message="Download Complete. Launching Installer...")
                    root.destroy()
                push(f"Updated to v{latest}")
                os.startfile(os.getenv('LOCALAPPDATA') + f"/Firestone Bot/Firestone_Bot_v{latest}.exe")
                sys.exit()

            else:
                root.destroy()
                self.window.deiconify()
                # sys.exit(1)


if __name__ == "__main__":
    gui = BotGUI()
