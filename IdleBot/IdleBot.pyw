#! python3
"""

Firestone Idle RPG Bot

A bot to handle auto upgrading party members and such as it progresses.

"""
import os
import sys

import keyboard
from pyautogui import FailSafeException
from threading import Thread

from bot_functions.AdvancedFunctions import *
from bot_functions.LiteFunctions import *
from bot_internals.GUI import Interface
from bot_internals.Launcher import Setup
from bot_internals.MouseLock import MouseLock
from bot_functions.GuildFunctions import guild_expeditions


class IdleBot:
    def __init__(self):
        os.system('cls')  # clear the console for debug
        log.info(f'{__name__} has been initialized.')
        self.start_time = 0
        keyboard.add_hotkey('ctrl+p', callback=self.hotkey_pause, suppress=True, trigger_on_release=True)
        keyboard.add_hotkey('shift+esc', callback=self.hotkey_quit, suppress=True, trigger_on_release=True)
        keyboard.add_hotkey('ctrl+g', callback=self.hotkey_go, suppress=True, trigger_on_release=True)

        """
        Let's start some instances from other modules and configure some things.
        """
        # self.mouse_lock = MouseLock()  # Locks the mouse down to the primary screen
        self.setup = Setup()
        while not database.updater_finished:
            time.sleep(0.5)
        self.interface = Thread(target=Interface, daemon=True, name='Interface') # All GUI instances we should need
        self.interface.start()
        self.interface.join()
        # self.interface = Interface()

        """
        Get a Tk instance going so we can use message boxes.
        """
        # TODO: How to handle message boxes. Likely create function in the Interface module?

    def hotkey_pause(self):
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
        log.info(f'Bot ran for {runtime}')
        return

    def run(self):
        self.start_time = time.time()
        while True:
            if database.running:
                if not database.paused:
                    try:
                        guardian_click()
                        buy_upgrades()
                        farm_gold()
                        map_missions()
                        guild_expeditions()
                        auto_prestige()
                        self.save_runtime()
                    except FailSafeException:
                        log.info('Fail-safe triggered. Terminating.')
                        break
                else:
                    time.sleep(1)
            else:
                self.save_runtime()
                sys.exit()

if __name__ == "__main__":
    bot = IdleBot()
    bot.run()
    sys.exit()
