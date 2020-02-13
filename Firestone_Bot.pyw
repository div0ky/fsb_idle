#! python3
"""

Firestone Idle RPG Bot

A bot to handle auto upgrading party members and such as it progresses.

"""

import logging
import os
import threading
import tkinter
from logging.handlers import TimedRotatingFileHandler
from time import sleep
from time import time
from tkinter import messagebox

import pyautogui
import pytesseract
from PIL import Image
from pyautogui import click
from pyautogui import moveTo

from Data.Includes.ConfigManager import ConfigManager
from Data.Includes.Lock import MouseLock

"""
DEFINE VERSION INFO
"""

vMajor = 2  # Increments on a BREAKING change
vMinor = 0  # Increments on a FEATURE change
vPatch = 4  # Increments on a FIX
vBuild = 1010  # Incremented on any changes
vStage = "Alpha"
version = f"{vMajor}.{vMinor}.{vPatch}.{vBuild} {vStage}"  # Should be self explanatory

# Define where the tesseract engine is installed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'


def imPath(filename):
    # A shortcut for joining the 'images/' file path
    return os.path.join(r"Data\Images", filename)


class FirestoneBot():
    def __init__(self):
        os.system("cls")

        self._setup_logging()
        self.sentinel = False

        # Init config and logging
        self.config = ConfigManager()
        self.mouseLock = MouseLock()

        self.root = tkinter.Tk()
        self.root.withdraw()

        # Setup some check variables
        self.ocr_fail_count = 0
        self.ocr_succeed_count = 0
        self.ocr_f_pct = 0
        self.ocr_s_pct = 0

        # Setup some common variables
        self.GAME_REGION = None
        self.GUARDIAN_CLICK_COORDS = None
        self.UPGRADE_COORDS = None
        self.CLOSE_COORDS = None
        self.PAUSE_LENGTH = 0.5
        self.GUILD_MISSION_TIME_LEFT = time() - 5
        self.SMALL_CLOSE_COORDS = None
        self.BIG_CLOSE_COORDS = None
        self.GUILD_COORDS = None
        self.GUILD_EXPEDITIONS_COORDS = None
        self.TOWN_COORDS = None
        self.UPGRADES_LOWERED = False
        self.FRESH_START = False
        self.BOSS_FAILED = False
        self.BACK_ARROW_COORDS = None
        self.UPGRADES_BUTTON_COORDS = None

    def _check_thread_status(self):
        """ Check status of threads. If they're not running, start them.
        :return:
        """

        thread_names = ["configmonitor", "mouselock"]

        for thread in threading.enumerate():
            if thread.name.lower() in thread_names:
                thread_names.remove(thread.name.lower())

        for i in thread_names:

            if i == "configmonitor":
                self.log.warning("Config Monitor Thread Crashed")
                self.config = ConfigManager()
                continue
            if i == "mouselock":
                self.log.warning("Mouse Lockdown Thread Chrashed")
                self.mouseLock = MouseLock()
                continue

    def _setup_logging(self):
        # Create a custom logger
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.INFO)

        # Create formatters
        file_format = logging.Formatter(f'%(asctime)s.%(msecs)03d  |  %(levelname)s     |  %(name)s  |  {version}  |  %(message)s',
                                           datefmt='%Y-%m-%d | %H:%M:%S')
        console_format = logging.Formatter(f'%(asctime)s.%(msecs)03d  |  %(levelname)s     |  %(name)s  |  {version}  |  %(message)s',
                                           datefmt='%Y-%m-%d | %H:%M:%S')

        # Create console handler
        c_handler = logging.StreamHandler()
        c_handler.setLevel(logging.DEBUG)
        c_handler.setFormatter(console_format)

        # Create debug handler
        f_handler = TimedRotatingFileHandler(os.path.expanduser("~") + "/Documents/Firestone Bot/debug.log", when="midnight", backupCount=7, interval=1)
        f_handler.setLevel(logging.DEBUG)
        f_handler.setFormatter(file_format)

        # Add handlers to the logger
        self.log.addHandler(c_handler)
        self.log.addHandler(f_handler)

    def getGameRegion(self):
        # Calculate the game region based on screen resolution.
        sWidth, sHeight = pyautogui.size()
        self.GAME_REGION = (0, 0, sWidth, sHeight)
        self.log.info("##########  PROGRAM STARTED  ##########\n\n")
        self.log.info(f"Screen resolution detected as: {sWidth}x{sHeight}")

    def setupCoordinates(self):
        # TODO: This is going to need considerable expansion if all clicks are to be dynamic
        self.UPGRADE_COORDS = (self.GAME_REGION[0] + (round(0.96 * self.GAME_REGION[2])), self.GAME_REGION[1] + (round(0.61 * self.GAME_REGION[3])))
        self.GUARDIAN_CLICK_COORDS = (self.GAME_REGION[2] / 2, self.GAME_REGION[3] / 2)
        self.SMALL_CLOSE_COORDS = (round(0.98 * self.GAME_REGION[2]), 99)
        self.BIG_CLOSE_COORDS = round(0.95 * self.GAME_REGION[2]), round(0.07 * self.GAME_REGION[3])
        self.GUILD_EXPEDITIONS_COORDS = (round(0.09 * self.GAME_REGION[2]), round(0.35 * self.GAME_REGION[3]))
        self.GUILD_COORDS = (round(0.79 * self.GAME_REGION[2]), round(0.18 * self.GAME_REGION[3]))
        self.TOWN_COORDS = (round(0.96 * self.GAME_REGION[2]), round(0.24 * self.GAME_REGION[3]))
        self.BACK_ARROW_COORDS = (round(0.36 * self.GAME_REGION[2]), round(0.04 * self.GAME_REGION[3]))
        self.UPGRADES_BUTTON_COORDS = (round(0.89 * self.GAME_REGION[2]), round(0.94 * self.GAME_REGION[3]))

    def pause(self):
        sleep(self.PAUSE_LENGTH)

    def isNum(self, num):
        check = num.partition(":")[0]
        try:
            check = int(check)
        except ValueError:
            pass
        return isinstance(check, int)

    def ocr(self, file):
        # CONVERTS AN IMAGE INTO A STRING
        self.log.info("Reading...")
        im = Image.open(file).convert("LA")
        im.save(os.path.expanduser("~") + "/Documents/Firestone Bot/ss.png")
        text = pytesseract.image_to_string(Image.open(file), lang="eng")
        self.log.info(f"I think it says: {text}")
        return text

    def ocr_check(self):
        ocr_total = self.ocr_fail_count + self.ocr_succeed_count
        self.ocr_f_pct = round(((self.ocr_fail_count / ocr_total) * 100), 2)
        self.ocr_s_pct = round(((self.ocr_succeed_count / ocr_total) * 100), 2)
        ocr_status = f"{self.ocr_f_pct}% Failure. {self.ocr_s_pct}% Success."
        if self.ocr_f_pct >= 20:
            self.log.warning(f"OCR currently has a {self.ocr_f_pct}% failure rate.")
        else:
            self.log.info(f"OCR currently has a {self.ocr_s_pct}% success rate.")
        return ocr_status

    def changeUpgradeProgression(self, way):
        if way == 1:  # go down to x1
            click(self.UPGRADE_COORDS)
            click(self.UPGRADES_BUTTON_COORDS, clicks=2, interval=0.5)
            click(self.SMALL_CLOSE_COORDS)
            return
        elif way == 2:  # go up to milestone
            click(self.UPGRADE_COORDS)
            click(self.UPGRADES_BUTTON_COORDS, clicks=3, interval=0.5)
            click(self.SMALL_CLOSE_COORDS)
            return
        return

    def guardianClick(self, clicks):
        self.log.info("Resuming Guardian duties. Clicking %s times." % clicks)
        click(self.GUARDIAN_CLICK_COORDS, clicks=clicks, interval=1.0)

    def buyUpgrades(self):
        click(self.UPGRADE_COORDS)  # Open the upgrade menu
        moveTo(self.GUARDIAN_CLICK_COORDS)
        self.log.info("Buying any available upgrades.")
        self.pause()
        while True:
            button = pyautogui.locateAllOnScreen(imPath("can_buy.png"), region=(round(0.85 * self.GAME_REGION[2]), round(0.13 * self.GAME_REGION[3]), round(0.06 * self.GAME_REGION[2]), round(0.74 * self.GAME_REGION[3])), confidence=0.96)
            button = list(button)
            if len(button) == 0:
                self.log.info("No (more) upgrades available.")
                break
            else:
                # log.info("At least %s upgrade(s) available." % len(button))
                for i in button:
                    pyautogui.click(x=i[0] + i[2] / 2, y=i[1] + i[3] / 2, interval=0.01)
                pyautogui.moveTo(self.GUARDIAN_CLICK_COORDS)
        pyautogui.click(self.SMALL_CLOSE_COORDS)
        return

    def farmGold(self, levels):
        button = pyautogui.locateCenterOnScreen(imPath("boss.png"))
        if button is None:
            return
        else:
            self.log.info("We seem to have hit a wall.")
            count = levels
            self.log.info("Going back %s levels to farm." % levels)
            while count >= 0:
                click(self.BACK_ARROW_COORDS)
                sleep(0.5)
                count -= 1
            click(button)
            if self.UPGRADES_LOWERED is False:
                self.UPGRADES_LOWERED = True
                self.log.info("Lowering upgrade progression to x1.")
                self.changeUpgradeProgression(1)

    def guildMissions(self):
        if time() > self.GUILD_MISSION_TIME_LEFT and self.config.guild_missions:
            self.log.info("Checking on Guild Expedition status.")
            self.pause()
            click(self.TOWN_COORDS)
            self.pause()
            click(self.GUILD_COORDS)
            self.pause()
            click(self.GUILD_EXPEDITIONS_COORDS)
            self.pause()
            # Take a screenshot of the mission timer
            pyautogui.screenshot(os.path.expanduser("~") + "/Documents/Firestone Bot/ss.png", region=(0.31 * self.GAME_REGION[2], 0.32 * self.GAME_REGION[3], 0.1 * self.GAME_REGION[2], 0.04 * self.GAME_REGION[3]))
            self.pause()
            # Attempt to read the time using OCR
            result = self.ocr(os.path.expanduser("~") + "/Documents/Firestone Bot/ss.png")
            # If it doesn't say "Completed" but it's also not blank... it's probably a number?

            if result == "Completed":
                self.ocr_succeed_count += 1
                self.log.info("Current mission was completed.")
                # Click on the "Claim" button.
                click(round(0.7 * self.GAME_REGION[2]), round(0.31 * self.GAME_REGION[3]))
                sleep(2)  # Wait for it to process
                click(round(0.61 * self.GAME_REGION[2]), round(0.67 * self.GAME_REGION[3]))  # Click OK on the popup that occurs
                self.log.info("Claimed.")
                sleep(2)  # Wait for it to process.
                click(round(0.7 * self.GAME_REGION[2]), round(0.32 * self.GAME_REGION[3]))  # Click to start new expedition
                self.pause()
                click(self.BIG_CLOSE_COORDS, clicks=3, interval=0.5)  # Go back to main screen
                return

            elif self.isNum(result):
                self.ocr_succeed_count += 1
                time_left = int(result.partition(":")[0]) + 1
                self.GUILD_MISSION_TIME_LEFT = time() + (time_left * 60)  # Add one minute to whatever minutes are left to be safe
                self.log.info(f"Current mission should complete in {time_left}min. Going Home.")
                click(self.BIG_CLOSE_COORDS, clicks=3, interval=0.5)  # Go back to main screen
                self.pause()
                return

            elif result != "":
                # If we can't tell, let's make sure it's not saying there are none.
                self.log.info("Checking to see if we're out of guild expeditions.")
                pyautogui.screenshot(os.path.expanduser("~") + "/Documents/Firestone Bot/ss.png", region=(
                round(0.32 * self.GAME_REGION[2]), round(0.48 * self.GAME_REGION[3]), round(0.35 * self.GAME_REGION[2]),
                round(0.06 * self.GAME_REGION[3])))
                self.pause()  # Give it time to save the image
                result = self.ocr(os.path.expanduser("~") + "/Documents/Firestone Bot/ss.png")  # attempt to read it

                if result == "There are no pending expeditions.":
                    self.ocr_succeed_count += 1
                    self.log.info("There are no more expeditions available right now.")
                    pyautogui.screenshot(os.path.expanduser("~") + "/Documents/Firestone Bot/ss.png", region=(
                    round(0.54 * self.GAME_REGION[2]), round(0.13 * self.GAME_REGION[3]),
                    round(0.08 * self.GAME_REGION[2]), round(0.04 * self.GAME_REGION[3])))
                    self.pause()
                    result = self.ocr(os.path.expanduser("~") + "/Documents/Firestone Bot/ss.png")

                    if self.isNum(result):
                        self.ocr_succeed_count += 1
                        time_left = int(result.partition(":")[0]) + 1
                        self.GUILD_MISSION_TIME_LEFT = time() + (time_left * 60)  # Add one minute to whatever minutes are left to be safe
                        self.log.info(f"More missions available in {time_left}min. Returning home.")
                        click(self.BIG_CLOSE_COORDS, clicks=3, interval=0.5)  # Go back to main screen
                        return
                    else:
                        self.ocr_fail_count += 1
                        if self.ocr_f_pct > 50:
                            pyautogui.screenshot(os.path.expanduser("~") + f"/Documents/Firestone Bot/OCR/Fail_{self.ocr_fail_count}.png")
                        self.log.warning("We weren't able to determine exepidtion renewal time. Returning home.")
                        click(self.BIG_CLOSE_COORDS, clicks=3, interval=0.5)  # Go back to main screen
                        return

            self.ocr_fail_count += 1
            if self.ocr_f_pct > 50:
                pyautogui.screenshot(
                    os.path.expanduser("~") + f"/Documents/Firestone Bot/OCR/Fail_{self.ocr_fail_count}.png")
            self.log.warning("Unable to ascertain the current mission status.")
            self.log.info("Trying to start a new expedition anyway.")
            click(round(0.7 * self.GAME_REGION[2]), round(0.32 * self.GAME_REGION[3]))  # Click to start new expedition
            self.pause()
            self.log.info("Returning home.")
            click(self.BIG_CLOSE_COORDS, clicks=3, interval=0.5)  # Go back to main screen
            self.pause()
            return

    def run(self):
        cycles = 0

        self.getGameRegion()
        self.setupCoordinates()

        messagebox.showinfo(title=f"Firestone Bot {version}",
                            message=f"Click OK to start the bot.\n\nWithin 5sec after clicking OK, make sure the game is the main window on screen.\n\nMove mouse to upper-left corner of screen to stop.")

        sleep(5)
        while True:
            # os.system("cls")
            try:
                self.buyUpgrades()
                self.guildMissions()
                self.farmGold(5)
                self.guardianClick(10)
                self.ocr_check()
            except:
                self.log.exception("Something went wrong.")
                self.config.sentinel = True
                self.mouseLock.sentinel = True
                messagebox.showerror(title=f"Firestone Bot {version}", message="Oops! Bot must terminate.\n\nCheck log for more.")
                exit(1)

            cycles += 1
            self.log.info(f"Main loop has cycled {cycles} time(s).")

            self._check_thread_status()


def main():
    bot = FirestoneBot()
    bot.run()


if __name__ == "__main__":
    main()
