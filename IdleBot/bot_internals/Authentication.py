import sys
import time
from tkinter import simpledialog, Tk, messagebox
from threading import Thread

import requests

from bot_internals.BotLog import log
from bot_internals.DatabaseManager import database
from bot_internals.version_info import *

# api_address = 'http://127.0.0.1:5000'
api_address = 'https://rest.div0ky.com'

class API:
    def __init__(self):
        log.info(f'{__name__} has been initialized.')
        self.license_was_empty = True
        if database.license_key:
            self.license_was_empty = False
            log.debug('License Key found in database.')
            database.launch_progress = 33
            if database.token:
                log.debug('Token found in database.')
                database.launch_progress = 66
                if not self.validate():
                    log.warning('Unable to validate the token. Trying to get a new one.')
                    if self.get_token():
                        log.info('Got a new token. Attempting to validate it.')
                        self.validate()
            else:
                self.get_token()
                self.validate()
        else:
            if self.get_license_key():
                if self.get_token():
                    self.validate()
            else:
                log.warning('We were unable to authenticate.')
                sys.exit()

        if database.authenticated:
            self.map_nodes()
            Thread(target=self.keep_alive, daemon=True, name='Keep Alive').start()

    @staticmethod
    def validate():
        response = requests.post(f'{api_address}/firestone/validate?token={database.token}')
        # print(response.text)
        message = response.json()
        if message['success']:
            log.info('Token is valid.')
            database.launch_progress = 99
            database.authenticated = True
            database.launch_text = 'Authenticated!'
            return True
        else:
            return False

    def get_token(self):
        response = requests.get(f'{api_address}/firestone/token?key={database.license_key}&id={database.public_id}&version={full_version}')
        print(response.text)
        message = response.json()
        if message['success']:
            log.info('We received a fresh token.')
            database.save_option('token', message['token'])
            database.save_option('email', message['email'])
            if self.license_was_empty:
                database.save_option('license_key', database.license_key)
            return True
        elif message['message'] == 'That is not a valid license key.':
            root = Tk()
            root.withdraw()
            database.launch_show_window = False
            messagebox.showwarning(f'Firestone Bot v{current_version}', 'Invalid license key.')
            root.destroy()
            sys.exit()
            return False

    @staticmethod
    def get_license_key():
        database.license_key_needed = True
        root = Tk()
        root.withdraw()
        database.launch_show_window = False
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
            time.sleep(30)
            response = requests.post(f'{api_address}/firestone/alive?token={database.token}&total_chests_opened={database.total_chests_opened}&total_clicks={database.total_clicks}&total_daily_checkins={database.total_daily_checkins}&total_guardian_trainings={database.total_guardian_trainings}&total_guild_expeditions={database.total_guild_expeditions}&total_map_missions={database.total_map_missions}&total_prestiges={database.total_prestiges}&total_restarts={database.total_restarts}&total_runtime={database.total_runtime}&total_stages_farmed={database.total_stages_farmed}&total_tavern_cards={database.total_tavern_cards}&total_upgrades_purchased={database.total_upgrades_purchased}')
            print(response.text)
            message = response.json()
            if message['success']:
                log.info(message['message'])
                return True
            else:
                return False

    # Load in the latest map nodes from API
    @staticmethod
    def map_nodes():
        response = requests.get(f'{api_address}/firestone/map?token={database.token}')
        # print(response.text)
        message = response.json()
        if message['success']:
            log.info('Succesfully loaded in latest map nodes.')
            _nodes = message['nodes']
            if _nodes != database.map_nodes:
                database.save_option('map_nodes', message['nodes'])
            else:
                log.info('We appear to have the latest map nodes.')


if __name__ == "__main__":
    verify = API()
    # verify.keep_alive()