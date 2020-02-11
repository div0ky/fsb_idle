#! python3
"""

Firestone Idle RPG Bot

Alpha 2.1.0.5967

A bot to handle auto upgrading party members and such as it progresses.

"""

import logging
import os
import tkinter
import configparser
from logging.handlers import TimedRotatingFileHandler
from time import sleep as sleep
from time import time as now
from tkinter import messagebox
import threading
from Data.Includes import ConfigManager


import pyautogui
import pygetwindow as gw
import pytesseract
from PIL import Image
from pyautogui import click
from pyautogui import moveTo

"""
DEFINE VERSION INFO
"""

vMajor = 1  # Increments on a BREAKING change
vMinor = 1  # Increments on a FEATURE change
vPatch = 0  # Increments on a FIX
vRevision = 998  # Calculated by Ceil(HHmmss / 24)
vStage = "Alpha"
version = f"{vMajor}.{vMinor}.{vPatch}.{vRevision} {vStage}"  # Should be self explanatory

"""
SETUP OUR USER CONFIG
"""


class FirestoneBot():
    def __init__(self):
        os.system("cls")
        self.config = ConfigManager()
        self._setup_logging()

    def _check_thread_status(self):
        """ Check status of threads. If they're not running, start them.
        :return:
        """

        thread_names = ["configmonitor"]

        for thread in threading.enumerate():
            if thread.name.lower() in thread_names:
                thread_names.remove(thread.name.lower())

        for i in thread_names:

            if i == "configmonitor":
                msg = "Config Monitor Thread Crashed"
                self._output_error(msg)
                self.config = ConfigManager()
                continue

    def _setup_logging(self):
        if self.config.logging:
            # Create a custom logger
            self.log = logging.getLogger(__name__)
            self.log.setLevel(logging.INFO)

            # Create formatters
            file_format = logging.Formatter('%(asctime)s.%(msecs)03d | %(levelname)s | %(name)s | %(message)s',
                                            datefmt='%Y-%m-%d | %H:%M:%S')
            console_format = logging.Formatter('%(asctime)s.%(msecs)03d | %(levelname)s | %(name)s | %(message)s',
                                               datefmt='%Y-%m-%d | %H:%M:%S')

            # Create console handler
            c_handler = logging.StreamHandler()
            c_handler.setLevel(logging.DEBUG)
            c_handler.setFormatter(console_format)

            # Create debug handler
            f_handler = TimedRotatingFileHandler("debug.log", when="midnight", backupCount=7, interval=1)
            f_handler.setLevel(logging.DEBUG)
            f_handler.setFormatter(file_format)

            # Add handlers to the logger
            log.addHandler(c_handler)
            log.addHandler(f_handler)

    def _output_error(self, msg, output=True):
        """
        convenience method to log and/or print an error
        :param msg:
        :param output:
        :return:
        """

        if output:
            print(msg)
            if self.config.logging:
                self.log.info(msg)


"""
CLEAN UP TK'S WINDOWS
"""

root = tkinter.Tk()
root.withdraw()

"""
Setup all user configurable variables
"""

"""
Setup Logging
"""

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# Create formatters
file_format = logging.Formatter('%(asctime)s.%(msecs)03d | %(levelname)s | %(name)s | %(message)s',
                                datefmt='%Y-%m-%d | %H:%M:%S')
console_format = logging.Formatter('%(asctime)s.%(msecs)03d | %(levelname)s | %(name)s | %(message)s',
                                   datefmt='%Y-%m-%d | %H:%M:%S')

# Create console handler
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.DEBUG)
c_handler.setFormatter(console_format)

# Create debug handler
f_handler = TimedRotatingFileHandler("debug.log", when="midnight", backupCount=7, interval=1)
f_handler.setLevel(logging.DEBUG)
f_handler.setFormatter(file_format)

# Add handlers to the logger
log.addHandler(c_handler)
log.addHandler(f_handler)

"""
Define all the primary variables we'll be using for now
"""

# Various coordinates of objects in the game
GAME_REGION = ()  # left, top, width, height
FARM_TIME = 60
AUTO_PRESTIGE = False
GUILD_MISSION_TIME_LEFT = now() - 5
BOSS_FAILED = False
UPGRADE_LOWERED = True
FRESH_START = False
FARMING = False
LAST_BOSS_ATTEMPT = now() - FARM_TIME
LAST_PRESTIGE = now()
GUARDIAN_CLICK_COORDS = None
UPGRADE_COORDS = None
CLOSE_COORDS = None
PRIME_COORDS = None
GUARD_COORDS = None
PARTY1_COORDS = None
PARTY2_COORDS = None
PARTY3_COORDS = None
PARTY4_COORDS = None

"""
Begin defining functions
"""


# RUNS EVERYTHING
def main():
    log.info("\n\n###############  PROGRAM STARTED  ###############")
    messagebox.showinfo(title=f"Firestone Bot {version}",
                        message=f"Click OK to start the bot.\nWithin 5sec after clicking OK, make sure the game is the main window on screen.\nMove mouse to upper-left corner of screen to stop.")

    getGameRegion()
    setupCoordinates()
    startPlaying()


# FOR CODE READABILITY
def pause():
    sleep(0.5)


# Define where the tesseract engine is installed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'


def ocr(file):
    # CONVERTS AN IMAGE INTO A STRING
    log.info("Reading...")
    im = Image.open(file).convert("LA")
    im.save(imPath("ss.png"))
    text = pytesseract.image_to_string(Image.open(file))
    log.info(f"I think it says: {text}")
    return text


def imPath(filename):
    # A shortcut for joining the 'images/' file path
    return os.path.join(r"Data\Images", filename)


def getGameRegion():
    # Obtains the region that the game is on the screen and assigns variables
    global GAME_REGION

    # Attempt to find the games window so we can switch to it, and make sure it's up before starting.
    game = gw.getWindowsWithTitle("Firestone")

    # Attempt to bring the game into focus
    # TODO: This seems to be buggy. Need to find a better solution.
    game[0].activate()
    sleep(3.5)  # Pause a moment so the user can activate the game window

    # Check to see if the game window is active.
    if gw.getActiveWindowTitle() == "Firestone":
        pass
    else:
        log.error("Could not find game. Is the game open?")
        # Let the user know we have a problem.
        messagebox.showerror(title=f"Firestone Bot {version}", message=f"Could not find game. Is the game open?")
        exit()

    # Calculate the game region based on screen resolution.
    sWidth, sHeight = pyautogui.size()
    GAME_REGION = (0, 0, sWidth, sHeight)
    log.info(f"Screen resolution detected as: {sWidth}x{sHeight}")


def setupCoordinates():
    global UPGRADE_COORDS, GUARDIAN_CLICK_COORDS, CLOSE_COORDS

    # TODO: This is going to need considerable expansion if all clicks are to be dynamic
    UPGRADE_COORDS = (GAME_REGION[0] + (0.96 * GAME_REGION[2]), GAME_REGION[1] + (0.61 * GAME_REGION[3]))
    GUARDIAN_CLICK_COORDS = (GAME_REGION[2] / 2, GAME_REGION[3] / 2)
    CLOSE_COORDS = (0.98 * GAME_REGION[2], 99)


def buyUpgrades():
    global GAME_REGION, GUARDIAN_CLICK_COORDS, UPGRADE_COORDS, CLOSE_COORDS

    pyautogui.click(UPGRADE_COORDS)  # Open the upgrade menu
    pyautogui.moveTo(GUARDIAN_CLICK_COORDS)
    pause()
    log.info("Buying any available upgrades.")
    while True:
        button = pyautogui.locateAllOnScreen(imPath("can_buy.png"), region=(
        round(0.85 * GAME_REGION[2]), round(0.13 * GAME_REGION[3]), round(0.06 * GAME_REGION[2]),
        round(0.74 * GAME_REGION[3])), confidence=0.96)
        button = list(button)
        if len(button) == 0:
            log.info("No more upgrades available.")
            break
        else:
            # log.info("At least %s upgrade(s) available." % len(button))
            for i in button:
                pyautogui.click(x=i[0] + i[2] / 2, y=i[1] + i[3] / 2, interval=0.01)
            pyautogui.moveTo(GUARDIAN_CLICK_COORDS)
    pyautogui.click(CLOSE_COORDS)
    return


def guildMission():
    global GUILD_MISSION_TIME_LEFT

    if now() > GUILD_MISSION_TIME_LEFT:
        log.info("Checking on Guild Expedition status.")
        pause()
        click(0.96 * GAME_REGION[2], 0.24 * GAME_REGION[3])
        pause()
        click(0.79 * GAME_REGION[2], 0.18 * GAME_REGION[3])
        pause()
        click(0.09 * GAME_REGION[2], 0.35 * GAME_REGION[3])
        pause()

        pyautogui.screenshot(imPath("ss.png"), region=(
        0.31 * GAME_REGION[2], 0.32 * GAME_REGION[3], 0.1 * GAME_REGION[2], 0.04 * GAME_REGION[3]))
        pause()
        result = ocr(imPath("ss.png"))
        if result != "Completed" and result != "":
            pause()
            try:
                result = result.partition(":")[0]
                time_left = int(result) + 1
                GUILD_MISSION_TIME_LEFT = now() + (time_left * 60)
                # log.info(now())
                # log.info(GUILD_MISSION_TIME_LEFT)
                log.info(f"Current mission will complete in {time_left}min.")
                log.info("Exiting Guild...")
                click(0.95 * GAME_REGION[2], 0.07 * GAME_REGION[3], clicks=3, interval=0.5)
                return
            except Exception as e:
                log.exception("Not sure what the status is.")
                click(0.7 * GAME_REGION[2], 0.31 * GAME_REGION[3])
                log.info("Attempted to start new expedition. Will check back later.")
                pause()
                log.info("Exiting Guild...")
                click(0.95 * GAME_REGION[2], 0.07 * GAME_REGION[3], clicks=3, interval=0.5)
                pause()
                return

        elif result == "Completed":
            log.info("Mission completed.")
            moveTo(0.7 * GAME_REGION[2], 0.31 * GAME_REGION[3], 0.5)
            click(0.7 * GAME_REGION[2], 0.31 * GAME_REGION[3])
            sleep(1.5)
            moveTo(0.61 * GAME_REGION[2], 0.67 * GAME_REGION[3], 0.5)
            click(0.61 * GAME_REGION[2], 0.67 * GAME_REGION[3])
            log.info("Claimed.")
            pause()

        pyautogui.screenshot(imPath("ss.png"), region=(
        0.32 * GAME_REGION[2], 0.48 * GAME_REGION[3], 0.35 * GAME_REGION[2], 0.06 * GAME_REGION[3]))
        pause()
        result = ocr(imPath("ss.png"))
        if result != "There are no pending expeditions.":
            moveTo(0.7 * GAME_REGION[2], 0.31 * GAME_REGION[3], 0.5)
            click(0.7 * GAME_REGION[2], 0.31 * GAME_REGION[3])
            log.info("Attempted to stat new expedition. Will check back later.")
            pause()
            log.info("Exiting Guild...")
            click(0.95 * GAME_REGION[2], 0.07 * GAME_REGION[3], clicks=3, interval=0.5)
        else:
            log.info("No missions left.")
            pyautogui.screenshot(imPath("ss.png"), region=(
            0.54 * GAME_REGION[2], 0.13 * GAME_REGION[3], 0.08 * GAME_REGION[2], 0.04 * GAME_REGION[3]))
            pause()
            result = ocr(imPath("ss.png"))
            result = result.partition(":")[0]
            time_left = int(result) + 1
            GUILD_MISSION_TIME_LEFT = now() + (time_left * 60)
            log.info(f"More missions available in {time_left}min.")
            log.info("Exiting Guild...")
            click(0.95 * GAME_REGION[2], 0.07 * GAME_REGION[3], clicks=3, interval=0.5)
    return


def farmGold(levels):
    global UPGRADE_LOWERED, UPGRADE_COORDS, CLOSE_COORDS

    pyautogui.click(0.36 * GAME_REGION[2], 0.04 * GAME_REGION[3], clicks=levels, interval=0.5)
    log.info("Going back %s levels to farm." % levels)

    if UPGRADE_LOWERED is False:
        UPGRADE_LOWERED = True
        log.info("Lowering upgrade progression to x1.")
        pyautogui.click(UPGRADE_COORDS)
        pause()
        pyautogui.click(0.89 * GAME_REGION[2], 0.94 * GAME_REGION[3], clicks=2, interval=0.5)
        pyautogui.click(CLOSE_COORDS)
    return


def fightBoss():
    global LAST_BOSS_ATTEMPT, BOSS_FAILED, FARMING, FARM_TIME

    if now() > (LAST_BOSS_ATTEMPT + FARM_TIME):
        FARMING = False

        button = pyautogui.locateCenterOnScreen(imPath("boss.png"))
        if button is None:
            return
        else:
            # log.info("Attempting to fight boss.")
            LAST_BOSS_ATTEMPT = now()
            BOSS_FAILED = True
            FARMING = True
            farmGold(20)
            sleep(1)
            pyautogui.click(button)
    return


def guardianClick(clicks):
    global GUARDIAN_CLICK_COORDS

    log.info("Clicking %s times." % clicks)
    pyautogui.click(x=GUARDIAN_CLICK_COORDS[0], y=GUARDIAN_CLICK_COORDS[1], clicks=clicks, interval=1.0)


def prestige():
    global AUTO_PRESTIGE, LAST_PRESTIGE, FRESH_START, UPGRADE_LOWERED, CLOSE_COORDS

    if AUTO_PRESTIGE is True:
        button = pyautogui.locateCenterOnScreen(imPath("prestige.png"), confidence=0.9)
        if button is None:
            return
        log.info("READY TO PRESTIGE! Doing so now.")
        pyautogui.click(button)
        sleep(1)
        button = pyautogui.locateCenterOnScreen(imPath("choose_prestige.png"))
        pyautogui.click(button)
        sleep(1)
        log.info("Choosing the FREE prestige option.")
        button = pyautogui.locateCenterOnScreen(imPath("free_prestige.png"))
        pyautogui.click(button)
        LAST_PRESTIGE = now()
        FRESH_START = True
        sleep(20)

        if UPGRADE_LOWERED is True:
            UPGRADE_LOWERED = False
            log.info("Raise upgrade progression to 'Next Milestone.'")
            pyautogui.click(UPGRADE_COORDS)
            pause()
            pyautogui.click(0.89 * GAME_REGION[2], 0.94 * GAME_REGION[3], clicks=3, interval=0.5)
            pyautogui.click(CLOSE_COORDS)
    return


def freshSetup():
    global LAST_PRESTIGE, FRESH_START, UPGRADE_LOWERED, UPGRADE_COORDS, CLOSE_COORDS

    if FRESH_START is True:
        log.info("Fresh start detected. Checking how long it's been.")
        if now() > (LAST_PRESTIGE + 120):
            log.info("We should have enough gold to buy party now.")
            pyautogui.click(0.96 * GAME_REGION[2], 0.48 * GAME_REGION[3])  # Open party menu
            pause()
            log.info("Buying first party slot.")
            pyautogui.click(0.41 * GAME_REGION[2], 0.8 * GAME_REGION[3])  # Buy fist party slot
            pause()
            log.info("Putting Ranger in first slot.")
            pyautogui.click(0.86 * GAME_REGION[2], 0.6 * GAME_REGION[3])  # Put Ranger in first slot
            pause()
            log.info("Buying second party slot.")
            pyautogui.click(0.4 * GAME_REGION[2], 0.57 * GAME_REGION[3])  # Buy second slot
            pause()
            log.info("Putting Warrior in second slot.")
            pyautogui.click(0.77 * GAME_REGION[2], 0.59 * GAME_REGION[3])  # Put warrior in first slot
            pause()
            log.info("Buying third party slot.")
            pyautogui.click(0.29 * GAME_REGION[2], 0.83 * GAME_REGION[3])  # Buying third party slot
            pause()
            log.info("Putting mage in third slot.")
            pyautogui.click(0.86 * GAME_REGION[2], 0.41 * GAME_REGION[3])  # Putting mage in third slot
            pause()
            log.info("Buying fourth party slot.")
            pyautogui.click(0.28 * GAME_REGION[2], 0.48 * GAME_REGION[3])  # Buying fourth party slot
            pause()
            log.info("Putting tank in fourth party slot.")
            pyautogui.click(0.77 * GAME_REGION[2], 0.41 * GAME_REGION[3])  # Put tank in fourth slot
            log.info("Saving party changes.")
            pyautogui.click(0.6 * GAME_REGION[2], 0.09 * GAME_REGION[3])  # Save changes
            pause()
            log.info("Done configuring party.")
            pyautogui.click(0.96 * GAME_REGION[2], 0.06 * GAME_REGION[3])  # Close party screen

            log.info("Fresh setup complete. Fresh start status removed.")
            FRESH_START = False

    return


def startPlaying():
    global UPGRADE_COORDS, GUARDIAN_CLICK_COORDS
    while True:
        try:
            buyUpgrades()
            guildMission()
            guardianClick(15)
            freshSetup()
            fightBoss()
            prestige()
        except pyautogui.FailSafeException:
            log.exception("Fail safe detected! Terminating.")
            messagebox.showerror(title=f"Firestone Bot {version}", message="Fail safe detected! Exiting.")
            exit()


if __name__ == '__main__':
    main()
