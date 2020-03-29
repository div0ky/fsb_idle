import sys
import time
from tkinter import simpledialog, Tk, messagebox
from threading import Thread

import requests

from bot_internals.BotLog import log
from bot_internals.DatabaseManager import database
from bot_internals.version_info import *

# api_address = 'http://div.local:5000'
api_address = 'https://firestone.div0ky.com'

class API:
    def __init__(self):
        log.info(f'{__name__} has been initialized.')
        if not database.license_key:
            self.get_license_key()
        else:
            self.map_nodes()
            Thread(target=self.keep_alive, daemon=True, name='Keep Alive').start()


    @staticmethod
    def get_license_key():
        log.debug('Attempting to get license key from user.')
        database.license_key_needed = True
        root = Tk()
        root.withdraw()
        # database.launch_show_window = False
        lkey = simpledialog.askstring(parent=root, title=f'Firestone Bot v{current_version}', prompt='       PLEASE ENTER YOUR LICENSE KEY:       ')
        database.launch_show_window = True
        root.destroy()
        if lkey is not None:
            database.license_key = lkey
            log.info('User entered a license key.')
            return True
        else:
            return False

    @staticmethod
    def keep_alive():
        while True:
            response = requests.get(f'{api_address}/alive?key={database.license_key}')
            # print(response.text)
            message = response.json()
            if message['success']:
                log.info(message['message'])
                if database.edition != '':
                    database.save_option('edition', message['edition'])
            else:
                log.error(message['message'])
            time.sleep(180)

    # Load in the latest map nodes from API
    @staticmethod
    def map_nodes():
        response = requests.get(f'{api_address}/map?key={database.license_key}')
        print(response.text)
        message = response.json()
        if message['success']:
            log.info('Succesfully loaded in latest map nodes.')
            _nodes = message['nodes']
            if _nodes != database.map_nodes:
                database.save_option('map_nodes', message['nodes'])
            else:
                log.info('We appear to have the latest map nodes.')
        else:
            log.error('Unable to access latest map nodes from API')


if __name__ == "__main__":
    verify = API()
    while True:
        time.sleep(1)
    # verify.keep_alive()
