from tkinter import Label, HORIZONTAL, Tk, Entry, Button
from tkinter.ttk import Progressbar
from bot_internals.version_info import *
from threading import Thread
from bot_internals.Authentication import API
from bot_internals.Updater import Updater
from bot_internals.BotLog import log
from bot_internals.DatabaseManager import database
import sys
import time


class Setup:
    def __init__(self):
        log.info(f'{__name__} has been initialized.')
        self.auth_win = None
        self.progress = None
        self.status_text = None
        self.key_entry = None
        self.okay_button = None

        self.startup = Thread(target=self.startup_procedures, daemon=True, name='Authentication GUI').start()
        # self.startup_procedures()
        self.auth = API()
        self.updater = Updater()
        database.updater_finished = True
        # self.update = Thread(target=Updater, daemon=True, name='Updater')
        # self.update.start()
        # self.update.join()
        # sys.exit()


    def startup_procedures(self, key=None):
        self.auth_win = Tk()
        self.auth_win.geometry("375x90")
        self.auth_win.title(f"Firestone Bot v{current_version}")
        self.auth_win.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.status_text = Label(self.auth_win, text=database.launch_text.upper())
        self.status_text.grid(column=0, row=0, padx=15, pady=5)
        self.auth_win.grid_columnconfigure(0, weight=1)
        rootWidth = self.auth_win.winfo_reqwidth()
        rootHeight = self.auth_win.winfo_reqheight()
        # Gets both half the screen width/height and window width/height
        positionRight = int(self.auth_win.winfo_screenwidth() / 2 - rootWidth / 2)
        positionDown = int(self.auth_win.winfo_screenheight() / 2 - rootHeight / 2)
        self.auth_win.geometry("+{}+{}".format(positionRight, positionDown))
        self.auth_win.resizable(0, 0)
        # self.auth_win.attributes("-topmost", True)
        self.progress = Progressbar(self.auth_win, orient=HORIZONTAL, length=300, mode='determinate')
        self.progress.grid(column=0, row=1, padx=15, pady=10)
        # self.key_entry =  Entry(self.auth_win)
        # self.key_entry.grid(column=0, row=1, padx=15, pady=10)
        # self.key_entry.grid_remove()
        # self.okay_button = Button(self.auth_win, text='SUBMIT', command=self.submit_key)
        # self.okay_button.grid(column=0, row=2, padx=15, pady=10, sticky='EW')

        Thread(target=self.progress_updates, daemon=True, name='Progress Updater').start()
        # self.auth_win.update_idletasks()
        self.auth_win.update()
        self.auth_win.mainloop()

    def progress_updates(self):
            while self.progress['value'] < 100 and database.launch_running:
                # print('progress updater is running')
                self.progress['value'] = database.launch_progress
                self.status_text.config(text=database.launch_text.upper())
                if database.updater_finished:
                    self.auth_win.withdraw()
                    self.auth_win.destroy()
            sys.exit()



    def submit_key(self):
        pass

    def on_closing(self):
        database.launch_running = False
        sys.exit()


if __name__ == "__main__":
    setup = Setup()
    while database.launch_running:
        time.sleep(0.1)
        if not database.launch_running:
            sys.exit()
