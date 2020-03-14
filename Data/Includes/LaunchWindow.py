import queue
import random
import threading
import time
from tkinter import Tk, Menu, Label, Button, Toplevel, BooleanVar, messagebox, HORIZONTAL, simpledialog
from tkinter.ttk import Combobox, Checkbutton, Entry, Progressbar, Style

from Data.Includes.IdleBotDB import IdleBotDB
from Data.Includes.ver import version_info

db = IdleBotDB()

version_info = version_info()

if version_info.vStage == "stable":
    current_version = version_info.version
else:
    current_version = version_info.full_version

class GUIPart:
    def __init__(self, master, queue, endCommand):
        self.queue = queue
        # Setup the GUI
        console = Button(master, text='Done', command=endCommand)
        console.grid(column=0, row=2)
        self.total_label = Label(master, text="Authenticating...".upper())
        self.total_label.grid(column=0, row=0, padx=15, pady=5)
        progress = Progressbar(master, orient=HORIZONTAL, length=300, mode='determinate')
        progress.grid(column=0, row=1, padx=15, pady=10)
        # Add more GUI stuff here depending on your needs

    def process_incoming(self):
        # Handle all messages currently in the queue, if any.

        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                # Check contents of message and do whatever is needed. As simple, print it.
                print(msg)
                self.total_label.config(text=msg)
            except queue.Empty:
                pass

    def on_closing(self):
        window.quit()
        window.destroy()
        exit()

class ThreadedClient:
    """ Launch the main part of the GUI and the worker thread. periodicCall and endApplication could reside in
    the GUI part, but putting them here means that you have all the thread controls in a single place."""

    def __init__(self, master):
        self.master = master

        # Create the queue
        self.queue = queue.Queue()

        # Setup the GUI part
        self.gui = GUIPart(master, self.queue, self.end_application)
        window.protocol("WM_DELETE_WINDOW",self.end_application)

        # Setup the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary
        self.running = 1
        self.thread1 = threading.Thread(target=self.worker_thread)
        self.thread1.start()

        # Start the periodic call in the GUI to check if the queue contains anything
        self.periodic_call()

    def periodic_call(self):
        # Check every 200ms if there is something new in the queue.
        self.gui.process_incoming()
        if not self.running:
            # This is the brutal stop of the system. I may need to do some cleanup first.
            exit(1)
        self.master.after(200, self.periodic_call)

    def worker_thread(self):
        """
        This is where we handle the asynchronous I/O. For example, it may be
        a 'select(  )'. One important thing to remember is that the thread has
        to yield control pretty regularly, by select or otherwise.
        """
        while self.running:
            # To simulate asynch I/O we create a random number at random intervals.
            time.sleep(rand.random()*1.5)
            msg = rand.random()
            self.queue.put(msg)

    def end_application(self):
        self.running = 0


rand = random.Random()
window = Tk()
window.title(f"Firestone Bot v5")
window.geometry("380x225")
window.minsize(380, 200)
window.wait_visibility(window)
windowWidth = window.winfo_reqwidth()
windowHeight = window.winfo_reqheight()
# Gets both half the screen width/height and window width/height
positionRight = int(window.winfo_screenwidth() / 2 - windowWidth / 2)
positionDown = int(window.winfo_screenheight() / 2 - windowHeight / 2)
window.geometry("+{}+{}".format(positionRight, positionDown))

window.grid_columnconfigure(0, weight=1)
window.resizable(0, 0)


# window.pack_propagate(0)
window.attributes("-topmost", True)

# window.protocol("WM_DELETE_WINDOW", on_closing)

client = ThreadedClient(window)
window.mainloop()























# from tkinter import Tk, Menu, Label, Button, Toplevel, BooleanVar, messagebox, HORIZONTAL, simpledialog
# from tkinter.ttk import Combobox, Checkbutton, Entry, Progressbar, Style
# from Data.Includes.IdleBotDB import IdleBotDB
# from Data.Includes.ver import version_info
# import requests, time
#
#
# db = IdleBotDB()
#
# version_info = version_info()
#
# if version_info.vStage == "stable":
#     current_version = version_info.version
# else:
#     current_version = version_info.full_version
#
# class LaunchProcess:
#     def __init__(self):
#         self.auth_win = Tk()
#         self.auth_win.geometry("325x70")
#         self.auth_win.title(f"Firestone Bot v{current_version}")
#         self.total_label = Label(self.auth_win, text="Authenticating...".upper())
#         self.total_label.grid(column=0, row=0, padx=15, pady=5)
#         self.auth_win.grid_columnconfigure(0, weight=1)
#         rootWidth = self.auth_win.winfo_reqwidth()
#         rootHeight = self.auth_win.winfo_reqheight()
#         # Gets both half the screen width/height and window width/height
#         positionRight = int(self.auth_win.winfo_screenwidth() / 2 - rootWidth / 2)
#         positionDown = int(self.auth_win.winfo_screenheight() / 2 - rootHeight / 2)
#         self.auth_win.geometry("+{}+{}".format(positionRight, positionDown))
#         self.auth_win.resizable(0, 0)
#         self.auth_win.attributes("-topmost", True)
#         self.progress = Progressbar(self.auth_win, orient=HORIZONTAL, length=300, mode='determinate')
#         self.progress.grid(column=0, row=1, padx=15, pady=10)
#         self.auth_win.update()
#         # self.authenticate()
#         self.auth_win.after(10, self.authenticate)
#         self.auth_win.mainloop()
#
#
#     def authenticate(self, key=None):
#         if db.license_key or key is not None:
#             if key is None:
#                 response = requests.get(f'https://api.div0ky.com/authenticate?key={db.license_key}&id={db.public_id}&version={version_info.full_version}')
#             else:
#                 response = requests.get(f'https://api.div0ky.com/authenticate?key={key}&id={db.public_id}&version={version_info.full_version}')
#
#             print(response.text)
#             data = response.json()
#             if data['success']:
#                 db.token = data['token']
#                 db.email = data['email']
#                 db.authenticated = True
#                 print(response.url)
#                 self.progress['value'] = 50
#                 self.total_label.config(text="SUCCESS")
#                 self.auth_win.update()
#                 time.sleep(2)
#                 self.auth_win.destroy()
#             elif data['message'] == 'Somebody is already using that license key!':
#                 messagebox.showerror(f'Firestone Bot v{current_version}', data['message'])
#                 exit()
#             else:
#                 messagebox.showerror(f'Firestone Bot v{current_version}', data['message'])
#                 return False
#         else:
#             messagebox.showerror(f'Firestone Bot v{current_version}', 'LICENSE KEY IS INVALID OR NOT FOUND.')
#             self.notLicensed()
#             return False
#
#     def notLicensed(self):
#         lkey = None
#         valid = False
#         while lkey is None and valid == False:
#             lkey = simpledialog.askstring(title=f'Firestone Bot v{current_version}',
#                                           prompt='       PLEASE ENTER YOUR LICENSE KEY:       ')
#             print(lkey)
#             if lkey is not None:
#                 db.save_option('license_key', lkey)
#                 check = self.authenticate(key=lkey)
#                 if check:
#                     db.save_option('license_key', lkey)
#                     valid = True
#                 else:
#                     messagebox.showwarning(f'Firestone Bot v{current_version}', 'Key is invalid.')
#             else:
#                 messagebox.showwarning(f'Firestone Bot v{current_version}', 'LICENSE KEY IS INVALID.')
#                 exit()
#
#
# if __name__ == "__main__":
#     win = LaunchProcess()
