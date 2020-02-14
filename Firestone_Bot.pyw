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
vMinor = 1  # Increments on a FEATURE change
vPatch = 0  # Increments on a FIX / PATCH
vStage = "beta.0"
version = f"{vMajor}.{vMinor}.{vPatch}-{vStage}"  # Should be self explanatory

# Define where the tesseract engine is installed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'


def imPath(filename):
    # A shortcut for joining the 'images/' file path
    return os.path.join(r"C:\Program Files\Firestone Bot\Data\Images", filename)
    # return os.path.join(os.path.dirname(__file__), "/Data/Images/" + filename)


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
        self.PRESTIGE_CHECK_TIME = time() - 5
        self.PRESTIGE_TRIGGER = 3
        self.SMALL_CLOSE_COORDS = None
        self.BIG_CLOSE_COORDS = None
        self.GUILD_COORDS = None
        self.GUILD_EXPEDITIONS_COORDS = None
        self.TOWN_COORDS = None
        self.UPGRADES_LOWERED = True
        self.FRESH_START = False
        self.BOSS_FAILED = False
        self.BACK_ARROW_COORDS = None
        self.UPGRADES_BUTTON_COORDS = None
        self.TEMPLE_OF_ETERNALS_COORDS = None
        self.PRESTIGE_LEVEL = None
        self.OCR_IMAGE = os.path.expanduser("~") + "/Documents/Firestone Bot/ss.png"
        self.CLASS_COORDS = {}
        self.PARTY_COORDS = None

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
        self.TEMPLE_OF_ETERNALS_COORDS = (round(0.474 * self.GAME_REGION[2]), round(0.213 * self.GAME_REGION[3]))
        self.PARTY_COORDS = (round(0.9583 * self.GAME_REGION[2]), round(0.4815 * self.GAME_REGION[3]))

        self.CLASS_COORDS = {"ranger": (round(0.8672 * self.GAME_REGION[2]), round(0.5417 * self.GAME_REGION[3])),
                             "mage": (round(0.8698 * self.GAME_REGION[2]), round(0.3565 * self.GAME_REGION[3])),
                             "tank": (round(0.7708 * self.GAME_REGION[2]), round(0.3565 * self.GAME_REGION[3])),
                             "warrior": (round(0.7708 * self.GAME_REGION[2]), round(0.5444 * self.GAME_REGION[3])),
                             "priest": (round(0.7708 * self.GAME_REGION[2]), round(0.7269 * self.GAME_REGION[3])),
                             "rogue": (round(0.8698 * self.GAME_REGION[2]), round(0.7269 * self.GAME_REGION[3]))}

    def pause(self):
        sleep(self.PAUSE_LENGTH)

    def isNum(self, num, v=1):
        if v == 1:
            check = num.partition(":")[0]
            try:
                check = int(check)
            except ValueError:
                pass
            return isinstance(check, int)
        if v == 2:
            check = num[1:]
            try:
                check = round(float(check), 2)
            except ValueError:
                pass
            return isinstance(check, float)

    def ocr(self, file):
        # CONVERTS AN IMAGE INTO A STRING
        self.log.info("Reading...")
        im = Image.open(file).convert("LA")
        im.save(os.path.expanduser("~") + f"/Documents/Firestone Bot/ss.png")
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
            self.UPGRADES_LOWERED = True
            return
        elif way == 2:  # go up to milestone
            click(self.UPGRADE_COORDS)
            click(self.UPGRADES_BUTTON_COORDS, clicks=3, interval=0.5)
            click(self.SMALL_CLOSE_COORDS)
            self.UPGRADES_LOWERED = False
            return
        return

    def guardianClick(self, clicks, speed):
        self.log.info("Resuming Guardian duties. Clicking %s times." % clicks)
        click(self.GUARDIAN_CLICK_COORDS, clicks=clicks, interval=speed)

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

    def autoPrestige(self):
        if self.config.auto_prestige and time() >= self.PRESTIGE_CHECK_TIME:
            click(self.TOWN_COORDS)
            self.pause()
            click(self.TEMPLE_OF_ETERNALS_COORDS)
            self.pause()
            click(round(0.7031 * self.GAME_REGION[2]), round(0.5231 * self.GAME_REGION[3]))  # Open prestige menu

            pyautogui.screenshot(self.OCR_IMAGE, region=(round(0.5729 * self.GAME_REGION[2]), round(0.6926 * self.GAME_REGION[3]), round(0.0781 * self.GAME_REGION[2]), round(0.062 * self.GAME_REGION[3])))
            result = self.ocr(self.OCR_IMAGE)

            if self.isNum(result, 2):
                self.ocr_succeed_count += 1
                self.PRESTIGE_LEVEL = round(float(result[1:]), 2)

            else:
                self.ocr_fail_count += 1
                self.log.warning("Wasn't able to ascertain our current prestige level.")
                if self.ocr_f_pct > 50:
                    pyautogui.screenshot(os.path.expanduser("~") + f"/Documents/Firestone Bot/OCR/Fail_{self.ocr_fail_count}_{round(time(), 5)}.png")

            if self.PRESTIGE_LEVEL:
                progress = round((self.PRESTIGE_LEVEL / self.PRESTIGE_TRIGGER) * 100)
                self.log.info(f"Current earnings are at {self.PRESTIGE_LEVEL}x which is {progress}% of our goal.")

                snooze = ((progress - 100) / (0 - 100)) *  ((60 - 1) + 1) * 1000
                if snooze <= 1000:
                    snooze = 1000
                elif snooze >= 60000:
                    snooze = 60000

                self.PRESTIGE_CHECK_TIME = time() + snooze
                self.log.info(f"Will wait {(snooze / 1000)}min before checking Prestige progress again.")

                if self.PRESTIGE_LEVEL >= self.PRESTIGE_TRIGGER:
                    self.log.info("Firestone earnings are satisfactory. Prestiging...")
                    click(round(0.7031 * self.GAME_REGION[2]), round(0.5231 * self.GAME_REGION[3]))
                    self.pause()
                    click(round(0.6016 * self.GAME_REGION[2]), round(0.4769 * self.GAME_REGION[3]))

                    sleep(15)  # Wait for prestige to finish

                    click(self.GUARDIAN_CLICK_COORDS, clicks=20, interval=1.1)  # Let's get some gold to buy party with

                    self.setupParty()
                    if self.UPGRADES_LOWERED:
                        self.changeUpgradeProgression(2)

            self.log.info("Going back to home screen.")
            click(self.BIG_CLOSE_COORDS, clicks=3, interval=0.5)  # Go home because we're not prestiging

    def setupParty(self):
        self.log.info("Setting up the party.")
        self.pause()
        click(self.PARTY_COORDS)

        if self.config.party_size >= 1:
            self.pause()
            self.log.info("Buying first party slot.")
            click(round(0.4167 * self.GAME_REGION[2]), round(0.7315 * self.GAME_REGION[3]))  # Buy fist party slot
        if self.config.party_size >= 2:
            self.pause()
            self.log.info("Buying second party slot.")
            click(round(0.401 * self.GAME_REGION[2]), round(0.5139 * self.GAME_REGION[3]))  # Buy second slot
        if self.config.party_size >= 3:
            self.pause()
            self.log.info("Buying third party slot.")
            click(round(0.2995 * self.GAME_REGION[2]), round(0.7759 * self.GAME_REGION[3]))  # Buying third party slot
        if self.config.party_size >= 4:
            self.pause()
            self.log.info("Buying fourth party slot.")
            click(round(0.2995 * self.GAME_REGION[2]), round(0.4259 * self.GAME_REGION[3]))  # Buying fourth party slot
        if self.config.party_size >= 5:
            self.pause()
            self.log.info("Buying fifth party slot.")
            click(round(0.263 * self.GAME_REGION[2]), round(0.588 * self.GAME_REGION[3]))  # Buying fifth party slot

        if self.config.party_size >= 1:
            self.pause()
            click(self.CLASS_COORDS[self.config.party_leader])
        if self.config.party_size >= 2:
            self.pause()
            click(self.CLASS_COORDS[self.config.party_slot_2])
        if self.config.party_size >= 3:
            self.pause()
            click(self.CLASS_COORDS[self.config.party_slot_3])
        if self.config.party_size >= 4:
            self.pause()
            click(self.CLASS_COORDS[self.config.party_slot_4])
        if self.config.party_size >= 5:
            self.pause()
            click(self.CLASS_COORDS[self.config.party_slot_5])

        self.pause()
        click(round(0.599 * self.GAME_REGION[2]), round(0.088 * self.GAME_REGION[3]))  # Click to save changes
        self.pause()
        click(self.BIG_CLOSE_COORDS)
        self.pause()

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
            pyautogui.screenshot(self.OCR_IMAGE, region=(0.31 * self.GAME_REGION[2], 0.32 * self.GAME_REGION[3], 0.1 * self.GAME_REGION[2], 0.04 * self.GAME_REGION[3]))
            self.pause()
            # Attempt to read the time using OCR
            result = self.ocr(self.OCR_IMAGE)
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

            elif result == "":
                # If we can't tell, let's make sure it's not saying there are none.
                self.log.info("Checking to see if we're out of guild expeditions.")
                pyautogui.screenshot(self.OCR_IMAGE, region=(
                round(0.32 * self.GAME_REGION[2]), round(0.48 * self.GAME_REGION[3]), round(0.35 * self.GAME_REGION[2]),
                round(0.06 * self.GAME_REGION[3])))
                self.pause()  # Give it time to save the image
                result = self.ocr(self.OCR_IMAGE)  # attempt to read it

                if result == "There are no pending expeditions.":
                    self.ocr_succeed_count += 1
                    self.log.info("There are no more expeditions available right now.")
                    pyautogui.screenshot(self.OCR_IMAGE, region=(round(0.5365 * self.GAME_REGION[2]), round(0.1278 * self.GAME_REGION[3]), round(0.0708 * self.GAME_REGION[2]), round(0.0426 * self.GAME_REGION[3])))
                    self.pause()
                    result = self.ocr(self.OCR_IMAGE)

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
                            pyautogui.screenshot(os.path.expanduser("~") + f"/Documents/Firestone Bot/OCR/Fail_{self.ocr_fail_count}_{round(time(), 5)}.png")
                        self.log.warning("We weren't able to determine exepidtion renewal time. Returning home.")
                        click(self.BIG_CLOSE_COORDS, clicks=3, interval=0.5)  # Go back to main screen
                        return

            self.ocr_fail_count += 1
            if self.ocr_f_pct > 50:
                pyautogui.screenshot(
                    os.path.expanduser("~") + f"/Documents/Firestone Bot/OCR/Fail_{self.ocr_fail_count}_{round(time(), 5)}.png")
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
                            message=f"Click OK to start the bot.\n\nPress ESCAPE or move mouse to upper-left corner of screen to exit.")

        # TODO: Switch this timer back to something more than 1.5?
        sleep(1.5)
        while True:
            # os.system("cls")
            try:
                self.buyUpgrades()
                if self.config.guild_missions:
                    self.guildMissions()
                if self.config.farm_gold:
                    self.farmGold(self.config.farm_levels)
                if self.config.auto_prestige:
                    self.autoPrestige()
                if self.config.guardian == 1:
                    self.guardianClick(100, 0.15)
                if self.config.guardian == 2:
                    self.guardianClick(10, 1.2)
                self.ocr_check()
            except:
                self.log.exception("Something went wrong.")
                self.config.sentinel = True
                self.mouseLock.sentinel = True
                messagebox.showerror(title=f"Firestone Bot {version}", message="Oops! Bot must terminate.\n\nCheck the log for more info.")
                exit(1)

            cycles += 1
            self.log.info(f"Main loop has cycled {cycles} time(s).")

            self._check_thread_status()


def main():
    bot = FirestoneBot()
    bot.run()


if __name__ == "__main__":
    main()
