import requests, os, tempfile, shutil
from time import sleep
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.withdraw()

__version__ = "1.0.0.0"

update = "http://div0ky.com/repo/"
update_check = "http://div0ky.com/repo/fsb_ver.txt"
s = requests.Session()

def download_file(url, file_path):

    reply = s.get(url, stream=True, auth=('wildfireajs', 'alien25'))
    with open(file_path, 'wb+') as file:
        for chunk in reply.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)

rands = os.urandom(24).hex()
dir = tempfile.gettempdir() + "\\" + rands + "\\"
os.mkdir(dir)

current_version = dir + "fsb_ver.txt"

download_file(update_check, current_version)

with open(current_version, "r+") as f:
    ver = f.read()

if ver > __version__:
    print("We need to update.")
    messagebox.askokcancel("Update Available", "New version available. Update?")
    installer = dir + ver + ".exe"
    link = update + ver + ".exe"
    download_file(link, installer)
    os.startfile(dir)
else:
    print("We're up-to-date.")

sleep(3)
shutil.rmtree(dir, ignore_errors=True)