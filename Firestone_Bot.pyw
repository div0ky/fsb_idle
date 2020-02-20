#! python3
"""

Firestone Idle RPG Bot

A bot to handle auto upgrading party members and such as it progresses.

"""

import logging
import os
import pickle
import threading
import tkinter
from logging.handlers import TimedRotatingFileHandler
from time import sleep
from time import time
from tkinter import messagebox

import pyautogui
import pytesseract
import requests
from PIL import Image
from pyautogui import click
from pyautogui import moveTo

from Data.Includes.ConfigManager import ConfigManager
from Data.Includes.Lock import MouseLock

"""
DEFINE VERSION INFO
"""

vMajor = 3  # Increments on a BREAKING change
vMinor = 0  # Increments on a FEATURE change
vPatch = 0  # Increments on a FIX / PATCH
vStage = "alpha.0"
version = f"{vMajor}.{vMinor}.{vPatch}-{vStage}"  # Should be self explanatory

# Define where the tesseract engine is installed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'


def imPath(filename):
    # A shortcut for joining the 'images/' file path
    return os.path.join(r"C:\Program Files\Firestone Bot\Data\Images", filename)
    # return os.path.join(os.path.dirname(__file__), "/Data/Images/" + filename)


class FirestoneBot():
    def __init__(self):

        # INIT SOME ESSENTIAL STUFF UP FRONT
        os.system("cls")
        self.var = self.PersistantVariables()
        self._setup_logging()
        self.sentinel = False

        # INITIALIZE CONFIG FILE AND MOUSE LOCKDOWN
        self.config = ConfigManager()
        self.mouseLock = MouseLock()

        # INITIALIZE GUI OBJECTS
        self.root = tkinter.Tk()
        self.root.withdraw()

        # SETUP VOLATILE VARIABLES FOR COORDS
        self.GAME_REGION = None
        self.GUARDIAN_CLICK_COORDS = None
        self.UPGRADE_COORDS = None
        self.CLOSE_COORDS = None
        self.SMALL_CLOSE_COORDS = None
        self.BIG_CLOSE_COORDS = None
        self.GUILD_COORDS = None
        self.GUILD_EXPEDITIONS_COORDS = None
        self.TOWN_COORDS = None
        self.BACK_ARROW_COORDS = None
        self.UPGRADES_BUTTON_COORDS = None
        self.TEMPLE_OF_ETERNALS_COORDS = None
        self.CLASS_COORDS = {}
        self.PARTY_COORDS = None
        self.EXOTIC_MERCHANT_COORDS = None
        self.MAP_COORDS = None

        self.PRESTIGE_TRIGGER = self.config.prestige_level
        self.PRESTIGE_LEVEL = None
        self.PAUSE_LENGTH = 0.5

    class PersistantVariables:
        def __init__(self):

            # SETUP VARIABLES FOR DEBUGGING
            self.ocr_fail_count = 0
            self.ocr_succeed_count = 0
            self.ocr_f_pct = 0
            self.ocr_s_pct = 0

            # SETUP VARIABLES WE'LL NEED TO REMEMBER
            self.GUILD_MISSION_TIME_LEFT = time() - 5
            self.PRESTIGE_CHECK_TIME = time() - 5
            self.UPGRADES_LOWERED = False
            self.FRESH_START = False
            self.BOSS_FAILED = False
            self.OCR_IMAGE = os.path.expanduser("~") + "/Documents/Firestone Bot/OCR/ss.png"
            self.ACTIVE_MISSIONS = 1

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
        f_handler = TimedRotatingFileHandler(os.path.expanduser("~") + "/Documents/Firestone Bot/Logs/debug.log", when="midnight", backupCount=7, interval=1)
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
        self.UPGRADE_COORDS = (self.relCoords(1840, 660))
        self.GUARDIAN_CLICK_COORDS = (self.GAME_REGION[2] / 2, self.GAME_REGION[3] / 2)
        self.SMALL_CLOSE_COORDS = (self.relCoords(1875, 100))
        self.BIG_CLOSE_COORDS = (self.relCoords(1820, 75))
        self.GUILD_EXPEDITIONS_COORDS = (self.relCoords(175, 385))
        self.GUILD_COORDS = (self.relCoords(1520, 205))
        self.TOWN_COORDS = (self.relCoords(1845, 265))
        self.BACK_ARROW_COORDS = (self.relCoords(690, 40))
        self.UPGRADES_BUTTON_COORDS = (self.relCoords(1605, 1020))
        self.TEMPLE_OF_ETERNALS_COORDS = (self.relCoords(915, 250))
        self.PARTY_COORDS = (self.relCoords(1845, 520))
        self.EXOTIC_MERCHANT_COORDS = (self.relCoords(1445, 735))
        self.MAP_COORDS = (self.relCoords(1840, 395))

        self.CLASS_COORDS = {"ranger": (round(0.8672 * self.GAME_REGION[2]), round(0.5417 * self.GAME_REGION[3])),
                             "mage": (round(0.8698 * self.GAME_REGION[2]), round(0.3565 * self.GAME_REGION[3])),
                             "tank": (round(0.7708 * self.GAME_REGION[2]), round(0.3565 * self.GAME_REGION[3])),
                             "warrior": (round(0.7708 * self.GAME_REGION[2]), round(0.5444 * self.GAME_REGION[3])),
                             "priest": (round(0.7708 * self.GAME_REGION[2]), round(0.7269 * self.GAME_REGION[3])),
                             "rogue": (round(0.8698 * self.GAME_REGION[2]), round(0.7269 * self.GAME_REGION[3]))}

    def pause(self):
        sleep(self.PAUSE_LENGTH)

    def relCoords(self, x=None, y=None, w=None, h=None):
        if x:
            newX = round(x * self.GAME_REGION[2] / 1920)
            coords = newX
        if y:
            newY = round(y * self.GAME_REGION[3] / 1080)
            coords = (newX, newY)
        if w:
            newW = round(w * self.GAME_REGION[2] / 1920)
            coords = (newX, newY, newW)
        if h:
            newH = round(h * self.GAME_REGION[3] / 1080)
            coords = (newX, newY, newW, newH)
        return coords

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
        base = int(float(im.size[0] * 1.5))
        wpercent = (base / float(im.size[0]))
        hsize = int(float(im.size[1]) * float(wpercent))
        im = im.resize((base, hsize), Image.ANTIALIAS)
        im.save(self.var.OCR_IMAGE)
        text = pytesseract.image_to_string(file, lang="eng", config='--psm 7')
        self.log.info(f"I think it says: {text}")
        return text

    def ocr_check(self):
        ocr_total = self.var.ocr_fail_count + self.var.ocr_succeed_count
        self.var.ocr_f_pct = round(((self.var.ocr_fail_count / ocr_total) * 100), 2)
        self.var.ocr_s_pct = round(((self.var.ocr_succeed_count / ocr_total) * 100), 2)
        ocr_status = f"{self.var.ocr_f_pct}% Failure. {self.var.ocr_s_pct}% Success."
        if self.var.ocr_f_pct >= 20:
            self.log.warning(f"OCR currently has a {self.var.ocr_f_pct}% failure rate.")
        else:
            self.log.info(f"OCR currently has a {self.var.ocr_s_pct}% success rate.")
        return ocr_status

    def changeUpgradeProgression(self, way):
        if way == 1:  # go down to x1
            click(self.UPGRADE_COORDS)
            self.pause()
            click(self.UPGRADES_BUTTON_COORDS, clicks=2, interval=0.5)
            click(self.SMALL_CLOSE_COORDS)
            self.var.UPGRADES_LOWERED = True
            return
        elif way == 2:  # go up to milestone
            click(self.UPGRADE_COORDS)
            self.pause()
            click(self.UPGRADES_BUTTON_COORDS, clicks=3, interval=0.5)
            click(self.SMALL_CLOSE_COORDS)
            self.var.UPGRADES_LOWERED = False
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

        upgrade_color = (43, 117, 41)
        tolerance = 5

        while True:

            if pyautogui.pixelMatchesColor(self.relCoords(1715), self.relCoords(175), upgrade_color, tolerance=tolerance):  # Party
                click(self.relCoords(1715, 175))
                moveTo(self.GUARDIAN_CLICK_COORDS)

            elif pyautogui.pixelMatchesColor(self.relCoords(1715), self.relCoords(295), upgrade_color, tolerance=tolerance):  # Guardian
                click(self.relCoords(1715, 295))
                moveTo(self.GUARDIAN_CLICK_COORDS)

            elif pyautogui.pixelMatchesColor(self.relCoords(1715), self.relCoords(415), upgrade_color, tolerance=tolerance):  # Leader
                click(self.relCoords(1715, 415))
                moveTo(self.GUARDIAN_CLICK_COORDS)

            elif pyautogui.pixelMatchesColor(self.relCoords(1715), self.relCoords(540), upgrade_color, tolerance=tolerance):  # Party 1
                click(self.relCoords(1715, 540))
                moveTo(self.GUARDIAN_CLICK_COORDS)

            elif pyautogui.pixelMatchesColor(self.relCoords(1715), self.relCoords(655), upgrade_color, tolerance=tolerance):  # Party 2
                click(self.relCoords(1715, 655))
                moveTo(self.GUARDIAN_CLICK_COORDS)

            elif pyautogui.pixelMatchesColor(self.relCoords(1715), self.relCoords(775), upgrade_color, tolerance=tolerance):  # Party 3
                click(self.relCoords(1715, 775))
                moveTo(self.GUARDIAN_CLICK_COORDS)

            elif pyautogui.pixelMatchesColor(self.relCoords(1715), self.relCoords(895), upgrade_color, tolerance=tolerance):  # Party 4
                click(self.relCoords(1715, 895))
                moveTo(self.GUARDIAN_CLICK_COORDS)
            else:
                break

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
            sleep(1.5)
            click(button)
            if self.var.UPGRADES_LOWERED is False:
                self.var.UPGRADES_LOWERED = True
                self.log.info("Lowering upgrade progression to x1.")
                self.changeUpgradeProgression(1)

    def exoticMerchant(self):
        upgrade_color = (27, 102, 26)
        tolerance = 5

        self.pause()
        click(self.TOWN_COORDS)
        self.pause()
        click(self.EXOTIC_MERCHANT_COORDS)
        self.pause()

        # Scroll to top
        count = 2
        while count > 0:
            pyautogui.moveTo(x=self.relCoords(1460), y=self.relCoords(305))
            self.pause()
            pyautogui.drag(0, self.relCoords(705), 1, pyautogui.easeOutQuad)
            count -= 1

        while True:

            moveTo(5, 5)

            if pyautogui.pixelMatchesColor(self.relCoords(900), self.relCoords(570), upgrade_color, tolerance=tolerance):  # Scroll of Speed
                print("I should click.")
                click(self.relCoords(900, 570))
                moveTo(5, 5)

            elif pyautogui.pixelMatchesColor(self.relCoords(1220), self.relCoords(570), upgrade_color, tolerance=tolerance):  # Scroll of Damage
                click(self.relCoords(1300, 600))
                moveTo(5, 5)

            elif pyautogui.pixelMatchesColor(self.relCoords(1545), self.relCoords(570), upgrade_color, tolerance=tolerance):  # Scroll of Health
                click(self.relCoords(1545, 600))
                moveTo(5, 5)

            elif pyautogui.pixelMatchesColor(self.relCoords(900), self.relCoords(900), upgrade_color, tolerance=tolerance):  # Miads' Touch
                click(self.relCoords(900, 900))
                moveTo(5, 5)

            elif pyautogui.pixelMatchesColor(self.relCoords(1220), self.relCoords(900), upgrade_color, tolerance=tolerance):  # Pouch of Gold
                click(self.relCoords(1220, 900))
                moveTo(5, 5)

            elif pyautogui.pixelMatchesColor(self.relCoords(1540), self.relCoords(900), upgrade_color, tolerance=tolerance):  # Bucket of Gold
                click(self.relCoords(1540, 900))
                moveTo(5, 5)

            else:
                break

        pyautogui.moveTo(x=1460, y=1010)
        sleep(0.5)
        pyautogui.drag(0, -705, 1, pyautogui.easeOutQuad, pause=1)  # Scroll down to see more

        while True:

            moveTo(5, 5)

            if pyautogui.pixelMatchesColor(self.relCoords(900), self.relCoords(540), upgrade_color, tolerance=tolerance):  # Scroll of Speed
                click(self.relCoords(900, 540))
                moveTo(5, 5)

            elif pyautogui.pixelMatchesColor(self.relCoords(1220), self.relCoords(540), upgrade_color, tolerance=tolerance):  # Scroll of Damage
                click(self.relCoords(1300, 600))
                moveTo(5, 5)

            elif pyautogui.pixelMatchesColor(self.relCoords(1545), self.relCoords(540), upgrade_color, tolerance=tolerance):  # Scroll of Health
                click(self.relCoords(1545, 600))
                moveTo(5, 5)

            elif pyautogui.pixelMatchesColor(self.relCoords(900), self.relCoords(875), upgrade_color, tolerance=tolerance):  # Miads' Touch
                click(self.relCoords(900, 900))
                moveTo(5, 5)

            elif pyautogui.pixelMatchesColor(self.relCoords(1220), self.relCoords(875), upgrade_color, tolerance=tolerance):  # Pouch of Gold
                click(self.relCoords(1220, 900))
                moveTo(5, 5)

            elif pyautogui.pixelMatchesColor(self.relCoords(1540), self.relCoords(875), upgrade_color, tolerance=tolerance):  # Bucket of Gold
                click(self.relCoords(1540, 900))
                moveTo(5, 5)

            else:
                break

        click(self.BIG_CLOSE_COORDS, clicks=2, interval=0.5)

    def mapMissions(self):
        click(self.MAP_COORDS)  # Open the map
        sleep(1.5)

        # missions02 = pyautogui.locateAllOnScreen(imPath("map_missions_02.png"), confidence=0.8)
        # missions03 = pyautogui.locateAllOnScreen(imPath("map_missions_03.png"), confidence=0.8)

        while True:
            if pyautogui.pixelMatchesColor(self.relCoords(232), self.relCoords(315), (247, 163, 66), tolerance=10):
                self.log.info("Claiming a map mission.")
                click(self.relCoords(232, 315))
                self.pause()
                moveTo(self.GUARDIAN_CLICK_COORDS)
                pyautogui.press('esc')
                self.var.ACTIVE_MISSIONS -= 1
                self.pause()
            else:
                break

        if self.var.ACTIVE_MISSIONS < 3:
            self.log.info("Checking on map missions.")
            missions01 = pyautogui.locateAllOnScreen(imPath("map_missions_01.png"), confidence=0.745)
            missions01 = list(missions01)
            if len(missions01) > 0:
                self.log.info(f"We have {len(missions01)}")
                for x in missions01:
                    if self.var.ACTIVE_MISSIONS < 3:
                        click(x[0], x[1], duration=0.25)
                        self.pause()
                        # Check to see if the "Start Mission" popup occurred by checking for green button
                        if pyautogui.pixelMatchesColor(self.relCoords(830), self.relCoords(960), (11, 161, 8), tolerance=5):
                            click(self.relCoords(830, 960))
                            self.log.info("Started a mission.")
                            self.pause()
                            pyautogui.press('esc')
                            self.pause()
                            self.var.ACTIVE_MISSIONS += 1
                            continue
                        else:
                            pyautogui.press('esc')
                            self.pause()
                            continue
                    else:
                        pyautogui.press('esc', presses=1)
                        break

            missions02 = pyautogui.locateAllOnScreen(imPath("map_missions_02.png"), confidence=0.745)
            missions02 = list(missions02)
            if len(missions02) > 0:
                self.log.info(f"We have {len(missions02)}")
                for x in missions02:
                    if self.var.ACTIVE_MISSIONS < 3:
                        click(x[0], x[1], duration=0.25)
                        self.pause()
                        # Check to see if the "Start Mission" popup occurred by checking for green button
                        if pyautogui.pixelMatchesColor(self.relCoords(830), self.relCoords(960), (11, 161, 8),
                                                       tolerance=5):
                            click(self.relCoords(830, 960))
                            self.log.info("Started a mission.")
                            self.pause()
                            pyautogui.press('esc')
                            self.pause()
                            self.var.ACTIVE_MISSIONS += 1
                            continue
                        else:
                            pyautogui.press('esc')
                            self.pause()
                            continue
                    else:
                        pyautogui.press('esc', presses=1)
                        break

            missions03 = pyautogui.locateAllOnScreen(imPath("map_missions_03.png"), confidence=0.745)
            missions03 = list(missions03)
            if len(missions03) > 0:
                self.log.info(f"We have {len(missions03)}")
                for x in missions03:
                    if self.var.ACTIVE_MISSIONS < 3:
                        click(x[0], x[1], duration=0.25)
                        self.pause()
                        # Check to see if the "Start Mission" popup occurred by checking for green button
                        if pyautogui.pixelMatchesColor(self.relCoords(830), self.relCoords(960), (11, 161, 8),
                                                       tolerance=5):
                            click(self.relCoords(830, 960))
                            self.log.info("Started a mission.")
                            self.pause()
                            pyautogui.press('esc')
                            self.pause()
                            self.var.ACTIVE_MISSIONS += 1
                            continue
                        else:
                            pyautogui.press('esc')
                            self.pause()
                            continue
                    else:
                        pyautogui.press('esc', presses=1)
                        break
            else:
                self.log.info("Doesn't look like we have any missions to click.")
        self.log.info("Heading home.")
        pyautogui.press('esc')

    def autoPrestige(self):
        if self.config.auto_prestige and time() >= self.var.PRESTIGE_CHECK_TIME:
            self.pause()
            click(self.TOWN_COORDS)
            self.pause()
            click(self.TEMPLE_OF_ETERNALS_COORDS)
            self.pause()
            click(self.relCoords(1359, 560))  # Open prestige menu
            self.pause()

            pyautogui.screenshot(self.var.OCR_IMAGE, region=(self.relCoords(1070, 745, 160, 70)))
            result = self.ocr(self.var.OCR_IMAGE)

            # while not self.isNum(result, 2):
            #     pyautogui.screenshot(self.var.OCR_IMAGE, region=(self.relCoords(1070, 745, 160, 70)))
            #     result = self.ocr(self.var.OCR_IMAGE)

            if self.isNum(result, 2):
                self.var.ocr_succeed_count += 1
                self.PRESTIGE_LEVEL = round(float(result[1:]), 2)

            else:
                self.var.ocr_fail_count += 1
                self.log.warning("Wasn't able to ascertain our current prestige level.")
                if self.var.ocr_f_pct > 50:
                    pyautogui.screenshot(os.path.expanduser("~") + f"/Documents/Firestone Bot/OCR/Fail_{self.var.ocr_fail_count}_{round(time(), 5)}.png")

            if self.PRESTIGE_LEVEL:
                progress = round((self.PRESTIGE_LEVEL / self.PRESTIGE_TRIGGER) * 100)
                self.log.info(f"Current earnings are at {self.PRESTIGE_LEVEL}x which is {progress}% of our goal.")

                snooze = ((progress - 100) / (0 - 100)) * ((60 - 1) + 1) * 1000
                if snooze <= 1000:
                    snooze = 1000
                elif snooze >= 60000:
                    snooze = 60000

                self.var.PRESTIGE_CHECK_TIME = time() + snooze
                self.log.info(f"Will wait {round((snooze / 1000), 2)}min before checking Prestige progress again.")

                if self.PRESTIGE_LEVEL >= self.PRESTIGE_TRIGGER:
                    self.log.info("Firestone earnings are satisfactory. Prestiging...")
                    click(self.relCoords(1160, 525))  # Click on FREE prestige option
                    sleep(15)  # Wait for prestige to finish

                    click(self.GUARDIAN_CLICK_COORDS, clicks=20, interval=1.1)  # Let's get some gold to buy party with

                    self.setupParty()
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
            click(self.relCoords(802, 795))  # Buy fist party slot
        if self.config.party_size >= 2:
            self.pause()
            self.log.info("Buying second party slot.")
            click(self.relCoords(775, 540))  # Buy second slot
        if self.config.party_size >= 3:
            self.pause()
            self.log.info("Buying third party slot.")
            click(self.relCoords(575, 815))  # Buying third party slot
        if self.config.party_size >= 4:
            self.pause()
            self.log.info("Buying fourth party slot.")
            click(self.relCoords(550, 445))  # Buying fourth party slot
        if self.config.party_size >= 5:
            self.pause()
            self.log.info("Buying fifth party slot.")
            click(self.relCoords(510, 630))  # Buying fifth party slot

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
        click(self.relCoords(1160, 95))  # Click to save changes
        self.pause()
        click(self.BIG_CLOSE_COORDS)
        self.pause()

    def guildMissions(self):
        if time() > self.var.GUILD_MISSION_TIME_LEFT and self.config.guild_missions:
            self.log.info("Checking on Guild Expedition status.")
            self.pause()
            click(self.TOWN_COORDS)
            self.pause()
            click(self.GUILD_COORDS)
            self.pause()
            click(self.GUILD_EXPEDITIONS_COORDS)
            self.pause()
            # Take a screenshot of the mission timer
            pyautogui.screenshot(self.var.OCR_IMAGE, region=(self.relCoords(600, 345, 200, 40)))
            self.pause()
            # Attempt to read the time using OCR
            result = self.ocr(self.var.OCR_IMAGE)
            # If it doesn't say "Completed" but it's also not blank... it's probably a number?

            if result == "Completed":
                self.var.ocr_succeed_count += 1
                self.log.info("Current mission was completed.")
                # Click on the "Claim" button.
                click(self.relCoords(1345, 335))
                sleep(2)  # Wait for it to process
                click(self.relCoords(1185, 720))  # Click OK on the popup that occurs
                self.log.info("Claimed.")
                sleep(2)  # Wait for it to process.
                click(self.relCoords(1335, 335))  # Click to start new expedition
                self.pause()
                click(self.BIG_CLOSE_COORDS, clicks=3, interval=0.5)  # Go back to main screen
                return

            elif self.isNum(result):
                self.var.ocr_succeed_count += 1
                time_left = int(result.partition(":")[0]) + 1
                self.var.GUILD_MISSION_TIME_LEFT = time() + (time_left * 60)  # Add one minute to whatever minutes are left to be safe
                self.log.info(f"Current mission should complete in {time_left}min. Going Home.")
                click(self.BIG_CLOSE_COORDS, clicks=3, interval=0.5)  # Go back to main screen
                self.pause()
                return

            else:
                # If we can't tell, let's make sure it's not saying there are none.
                self.log.info("Checking to see if we're out of guild expeditions.")
                pyautogui.screenshot(self.var.OCR_IMAGE, region=(self.relCoords(625, 520, 690, 65)))
                self.pause()  # Give it time to save the image
                result = self.ocr(self.var.OCR_IMAGE)  # attempt to read it

                if result == "There are no pending expeditions.":
                    self.var.ocr_succeed_count += 1
                    self.log.info("There are no more expeditions available right now.")
                    pyautogui.screenshot(self.var.OCR_IMAGE, region=(self.relCoords(1030, 145, 145, 35)))
                    self.pause()
                    result = self.ocr(self.var.OCR_IMAGE)

                    if self.isNum(result):
                        self.var.ocr_succeed_count += 1
                        if len(result.partition(":")) > 1:

                            hours = int(result.partition(":")[0]) * 60 * 60
                            print(hours)
                            temp = result.partition(":")[2]
                            min = (int(temp.partition(":")[0]) + 1) * 60
                            print(min)

                            time_left = hours + min
                            print(time_left)
                        else:
                            time_left = int(result.partition(":")[0]) * 60

                        self.var.GUILD_MISSION_TIME_LEFT = time() + time_left  # Set timer
                        self.log.info(f"More missions available in {time_left / 60}min. Returning home.")
                        click(self.BIG_CLOSE_COORDS, clicks=3, interval=0.5)  # Go back to main screen
                        return
                    else:
                        self.var.ocr_fail_count += 1
                        if self.var.ocr_f_pct > 50:
                            pyautogui.screenshot(os.path.expanduser("~") + f"/Documents/Firestone Bot/OCR/Fail_{self.var.ocr_fail_count}_{round(time(), 5)}.png")
                        self.log.warning("We weren't able to determine exepidtion renewal time. Returning home.")
                        click(self.BIG_CLOSE_COORDS, clicks=3, interval=0.5)  # Go back to main screen
                        return

            self.var.ocr_fail_count += 1
            if self.var.ocr_f_pct > 50:
                pyautogui.screenshot(
                    os.path.expanduser("~") + f"/Documents/Firestone Bot/OCR/Fail_{self.var.ocr_fail_count}_{round(time(), 5)}.png")
            self.log.warning("Unable to ascertain the current mission status.")
            self.log.info("Trying to start a new expedition anyway.")
            click(self.relCoords(1335, 335))  # Click to start new expedition
            self.pause()
            self.log.info("Returning home.")
            click(self.BIG_CLOSE_COORDS, clicks=3, interval=0.5)  # Go back to main screen
            self.pause()
            return

    def run(self):
        cycles = 0

        # DEFINE SOME VOLATILE VARIABLES
        self.getGameRegion()
        self.setupCoordinates()

        messagebox.showinfo(title=f"Firestone Bot {version}",
                            message=f"Click OK to start the bot.\n\nPress SHIFT + ESCAPE or move mouse to upper-left corner of screen to exit.")

        # TODO: Switch this timer back to something more than 1.5?
        sleep(1.5)
        while True:
            # os.system("cls")
            self.buyUpgrades()
            if self.config.guild_missions:
                self.guildMissions()
            if self.config.farm_gold:
                self.farmGold(self.config.farm_levels)
            if self.config.auto_prestige:
                self.autoPrestige()

            self.mapMissions()

            if self.config.guardian == 1:
                self.guardianClick(100, 0.15)
            if self.config.guardian == 2:
                self.guardianClick(10, 1.2)

            self.ocr_check()

            cycles += 1
            self.log.info(f"Main loop has cycled {cycles} time(s).")

            self._check_thread_status()

            f = open(os.path.expanduser("~") + "/Documents/Firestone Bot/var.ini", 'wb')
            pickle.dump(self.var, f, 2)
            f.close()


def checkVersion():
    response = requests.get("http://div0ky.com/repo/latest.txt")
    latest = response.text
    latest = str(latest)
    if latest > version:
        messagebox.showwarning(title=f"Firestone Bot {version}", message=f"A new version is availble. Downloading v{latest}.")
        update = requests.get(f"http://div0ky.com/repo/Firestone Bot_v{latest}.exe")
        open(os.path.expanduser("~") + f"/Documents/Firestone Bot/Firestone Bot_v{latest}.exe", 'wb').write(update.content)
        os.startfile(os.path.expanduser("~") + f"/Documents/Firestone Bot/Firestone Bot_v{latest}.exe")


def main():
    try:
        bot.run()
    except:
        pickle.dump(bot.var, open(os.path.expanduser("~") + "/Documents/Firestone Bot/var.ini", 'wb'))
        bot.log.info("Variables saved to file.")

        bot.config.sentinel = True
        bot.mouseLock.sentinel = True

        bot.log.exception("Something went wrong.")
        messagebox.showerror(title=f"Firestone Bot {version}",
                             message="Oops! Bot must terminate.\n\nCheck the log for more info.")
        exit(1)


if __name__ == "__main__":
    checkVersion()
    bot = FirestoneBot()
    try:
        bot.var = pickle.load(open(os.path.expanduser("~") + "/Documents/Firestone Bot/var.ini", 'rb'))
        bot.log.info("Variables loaded to file.")
    except:
        pass
    main()
