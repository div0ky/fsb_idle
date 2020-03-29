import os, sys
from bot_internals.DatabaseManager import database as db
from bot_internals.version_info import *
from tkinter import Tk, messagebox
import semver
import requests
from bot_internals.BotLog import log

class Updater:
    def __init__(self):
        if db.authenticated:
            if db.channel == "Development":
                response = requests.get("http://div0ky.com/repo/development/latest.txt")
            elif db.channel == "Staging":
                response = requests.get("http://div0ky.com/repo/staging/latest.txt")
            else:
                response = requests.get("http://div0ky.com/repo/stable/latest.txt")
            latest = response.text

            print(f"Current Version is {current_version}\nLatest Version is {latest}")

            if semver.compare(latest, current_version) > 0:
                root = Tk()
                root.withdraw()
                ask_update = messagebox.askyesno(title=f"FIB v{current_version}",
                                                 message=f"A new version is availble. You're running v{current_version}. The latest version is v{latest}.\n\nDo you want to download & update?", parent=root)
                root.destroy()

                if ask_update:
                    update = f"http://div0ky.com/repo/Firestone_Bot_v{latest}.exe"
                    with open(os.getenv('LOCALAPPDATA') + f"/Firestone Idle Bot/Firestone_Bot_v{latest}.exe", 'wb') as f:
                        response = requests.get(update, stream=True)
                        total_size = response.headers.get('content-length')
                        if total_size is None:
                            f.write(response.content)
                        else:
                            dl = 0
                            total_size = int(total_size)
                            adj_size = round(int(total_size) / 1000, 2)
                            for data in response.iter_content(chunk_size=4096):
                                dl += int(len(data))
                                adj_dl = round(dl / 1000, 2)
                                f.write(data)
                                done = int(100 * dl / total_size)
                                db.launch_progress = done
                                db.launch_text = f"{adj_dl}KB / {adj_size}KB"
                                if not db.launch_running:
                                    break
                                # print("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                        if db.launch_running:
                            db.launch_text = "DOWNLOAD COMPLETE"
                        # messagebox.showinfo(title="DOWNLOAD COMPLETE", message="Download Complete. Launching Installer...")
                    if db.launch_running:
                        log.info(f"Updated to v{latest}")
                        os.startfile(os.getenv('LOCALAPPDATA') + f"/Firestone Idle Bot/Firestone_Bot_v{latest}.exe")
                    sys.exit()

                else:
                    db.updater_finished = True