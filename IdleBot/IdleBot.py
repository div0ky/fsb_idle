#! python3
"""
IdleBot.py
====================================
The core module of Firestone Idle Bot
"""

import os
import sys

import keyboard
from pyautogui import FailSafeException
from threading import Thread
from threading import enumerate as thread_enumerate

from bot_functions.AdvancedFunctions import *
from bot_functions.LiteFunctions import *
from bot_internals.GUI import Interface
from bot_internals.Launcher import Setup
from bot_internals.MouseLock import MouseLock
from bot_functions.GuildFunctions import guild_expeditions
from bot_functions.silver_functions import guardian_training, open_chests
from bot_internals.Authentication import keep_alive


class MainBot:
    """This is the primary class that does things and stuff?"""
    def __init__(self):
        os.system('cls')  # clear the console for debug
        log.info(f'{__name__} has been initialized.')
        self.start_time = 0
        keyboard.add_hotkey('ctrl+p', callback=self.hotkey_pause, suppress=True, trigger_on_release=True)
        keyboard.add_hotkey('shift+esc', callback=self.hotkey_quit, suppress=True, trigger_on_release=True)
        keyboard.add_hotkey('ctrl+g', callback=self.hotkey_go, suppress=True, trigger_on_release=True)

        # Let's start some instances from other modules and configure some things.

        # self.mouse_lock = MouseLock()  # Locks the mouse down to the primary screen
        self.setup = Setup()
        while not database.updater_finished:
            time.sleep(0.5)
        self.interface = Thread(target=Interface, daemon=True, name='Interface') # All GUI instances we should need
        self.interface.start()
        self.interface.join()
        # self.interface = Interface()

        # Get a Tk instance going so we can use message boxes.
        # TODO: How to handle message boxes. Likely create function in the Interface module?

    def hotkey_pause(self):
        """This does a thing."""
        database.paused = True
        log.warning(f"Pausing operations...")

    def hotkey_quit(self):
        log.warning(f"Exit hotkeys were pressed. Terminating.")
        sys.exit()
        # database.running = False

    def hotkey_go(self):
        database.paused = False
        log.info(f"Resuming operations...")

    def save_runtime(self):
        _runtime_in_seconds = time.time() - self.start_time
        # runtime = str(timedelta(seconds=_runtime_in_seconds))
        runtime = time.strftime('%Hh %Mm %Ss', time.gmtime(_runtime_in_seconds))
        database.save_stat('total_runtime', database.total_runtime + _runtime_in_seconds)
        log.info(f'Bot has run for {runtime}')
        return

    @staticmethod
    def _check_thread_status():
        thread_names = ['keep alive']

        for thrd in thread_enumerate():
            if thrd.name.lower() in thread_names:
                thread_names.remove(thrd.name.lower())

        for i in thread_names:
            if i == 'keep alive':
                msg = 'Keep Alive; Thread Crashed'
                log.error(msg)
                Thread(target=keep_alive, daemon=True, name='Keep Alive').start()

    def run(self):
        self.start_time = time.time()
        database.save_option('upgrade_status', 'x1')
        change_upgrade_progression('Milestone')
        while True:
            if database.running:
                if not database.paused:
                    try:
                        guardian_click()
                        buy_upgrades()
                        farm_gold()
                        if 'SILVER' or 'GOLD' in database.edition:
                            guardian_training()
                            open_chests()
                        if 'GOLD' in database.edition:
                            map_missions()
                            guild_expeditions()
                            auto_prestige()
                        self.save_runtime()
                        self._check_thread_status()
                    except FailSafeException:
                        log.info('Fail-safe triggered. Terminating.')
                        break
                else:
                    time.sleep(1)
            else:
                self.save_runtime()
                sys.exit()

if __name__ == "__main__":
    bot = MainBot()
    bot.run()
    sys.exit()
