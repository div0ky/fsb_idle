#! python3
"""

Firestone Idle RPG Bot

A bot to handle auto upgrading party members and such as it progresses.

"""
from bot_internals.BotLog import log
import os
import time
from bot_internals.GUI import Interface
from bot_internals.GameCoords import game_coords
from bot_internals.MouseLock import MouseLock
from bot_internals.DatabaseManager import database
from bot_functions.LiteFunctions import *
from bot_functions.AdvancedFunctions import *
import sys
import keyboard
from pyautogui import FailSafeException


class IdleBot:
    def __init__(self):
        os.system('cls')  # clear the console for debug
        log.info(f'{__name__} has been initialized.')
        self.paused = False
        keyboard.add_hotkey('ctrl+p', callback=self.hotkey_pause, suppress=True, trigger_on_release=True)
        keyboard.add_hotkey('shift+esc', callback=self.hotkey_quit, suppress=True, trigger_on_release=True)
        keyboard.add_hotkey('ctrl+g', callback=self.hotkey_go, suppress=True, trigger_on_release=True)

        """
        Let's start some instances from other modules and configure some things.
        """
        # self.mouse_lock = MouseLock()  # Locks the mouse down to the primary screen
        # self.interface = Interface()  # All GUI instances we should need

        """
        Get a Tk instance going so we can use message boxes.
        """
        # TODO: How to handle message boxes. Likely create function in the Interface module?

    def hotkey_pause(self):
        self.paused = True
        log.warning(f"Pausing operations...")

    @staticmethod
    def hotkey_quit():
        log.warning(f"Exit hotkeys were pressed. Terminating.")
        sys.exit()

    def hotkey_go(self):
        self.paused = False
        log.info(f"Resuming operations...")

    def run(self):
        while True:
            if not self.paused:
                try:
                    guardian_click()
                    buy_upgrades()
                    farm_gold()
                    map_missions()
                except FailSafeException:
                    log.info('Fail-safe triggered. Terminating.')
                    break
            else:
                time.sleep(1)

if __name__ == "__main__":
    bot = IdleBot()
    bot.run()
