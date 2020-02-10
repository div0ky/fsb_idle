#! python3
"""

Firestone Idle RPG Bot

Alpha 2.1.0.5967

A bot to handle auto upgrading party members and such as it progresses.

"""


from time import sleep as sleep
from time import time as now
from tkinter import messagebox

import logging
import os
import pyautogui
from pyautogui import click
from pyautogui import moveTo
import pygetwindow as gw
import pytesseract
import tkinter
from PIL import Image


"""
DEFINE VERSION
"""
vMajor = 2  # Increments on a BREAKING change
vMinor = 0  # Increments on a FEATURE change
vPatch = 0  # Increments on a FIX
vRevision = 6906  # Calculated by HHmmss
vStage = "Alpha"
version = f"{vMajor}.{vMinor}.{vPatch}.{vRevision} {vStage}"  # Should be self explanatory

"""
Clean up Tk's window
"""

root = tkinter.Tk()
root.withdraw()

"""
Setup our various logger handlers.
"""

# Setup a logger filter
# class UserFilter(object):
#     def __init__(self, level):
#         self.__level = level
#
#     def filter(self, logRecord):
#         return logRecord.levelno <= self.__level


# Create a custom logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create formatters
file_format = logging.Formatter('%(asctime)s.%(msecs)03d | %(levelname)s | %(name)s | %(message)s', datefmt='%Y-%m-%d | %H:%M:%S')
# user_format = logging.Formatter('%(asctime)s: %(message)s', datefmt='%Y-%m-%d | %H:%M:%S')
console_format = logging.Formatter('%(asctime)s.%(msecs)03d | %(levelname)s | %(name)s | %(message)s', datefmt='%Y-%m-%d | %H:%M:%S')

# Create console handler
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.DEBUG)
c_handler.setFormatter(console_format)

# Create debug handler
d_handler = logging.FileHandler("debug.log")
d_handler.setLevel(logging.DEBUG)
d_handler.setFormatter(file_format)

# Create general handler
# g_handler = logging.FileHandler("game.log")
# g_handler.setLevel(logging.INFO)
# g_handler.setFormatter(user_format)
# g_handler.addFilter(UserFilter(logging.INFO))

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(d_handler)
# logger.addHandler(g_handler)

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
CLICK_COORDS = None
UPGRADE_COORDS = None
CLOSE_COORDS = None
PRIME_COORDS = None
GUARD_COORDS = None
PARTY1_COORDS = None
PARTY2_COORDS = None
PARTY3_COORDS = None
PARTY4_COORDS = None


def main():
    """Runs the entire program."""
    logging.info("Program started. Press Ctrl-C to abort at any time.")
    logging.info("To interrupt mouse movement, move mouse to upper left corner.")
    messagebox.showinfo(title=f"Firestone Bot {version}",
                        message=f"Click OK to start the bot.\nWithin 5sec after clicking OK, make sure the game is the main window on screen.\nMove mouse to upper-left corner of screen to stop.")
    getGameRegion()
    setupCoordinates()
    startPlaying()




def pause():
    sleep(0.5)


# Define where the tesseract engine is installed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'


def ocr(file):
    """
    This function will convert an image into a string.
    """
    logging.info(f"Opening {file} to read.")
    im = Image.open(file).convert("LA")
    im.save(imPath("ss.png"))
    text = pytesseract.image_to_string(Image.open(file))
    logging.info(f"I think it says: {text}")
    return text


def imPath(filename):
    """A shortcut for joining the 'images/' file path"""
    return os.path.join("Data\Images", filename)


def getGameRegion():
    """Obtains the region that the game is on the screen and assigns variables"""
    global GAME_REGION

    # identify the top-left corner
    logging.info("Finding game region...")
    game = gw.getWindowsWithTitle("Firestone")
    game[0].activate()
    sleep(6.5)
    if gw.getActiveWindowTitle() == "Firestone":
        pass
    else:
        logging.error("Could not find game. Is the game open?")
        messagebox.showerror(title=f"Firestone Bot {version}", message=f"Could not find game. Is the game open?")
        exit()
    region = pyautogui.locateOnScreen(imPath("top_left_corner.png"), confidence=0.9)
    if region is None:
        logging.warning("Not sure the game is on screen. Proceeding anyway.")
        region = (0, 0)  # manually set what it SHOULD be
        # raise Exception("Could not find game on screen. Is the game visible?")


    # calculate the region of the entire game
    topLeftX = region[0]
    topLeftY = region[1]  # top
    sWidth, sHeight = pyautogui.size()
    GAME_REGION = (topLeftX, topLeftY, sWidth, sHeight)
    logging.info("Game region found: %s" % (GAME_REGION,))


def setupCoordinates():
    UPGRADE_COORDS = (GAME_REGION[0] + (0.96 * GAME_REGION[2]), GAME_REGION[1] + (0.61 * GAME_REGION[3]))
    CLICK_COORDS = (GAME_REGION[2] / 2, GAME_REGION[3] / 2)
    CLOSE_COORDS = (0.98 * GAME_REGION[2], 0.09 * GAME_REGION[3])


def buyUpgrades():
    global CLICK_COORDS, UPGRADE_COORDS, CLOSE_COORDS
    # button = pyautogui.locateOnScreen(imPath("upgrades.png"), region=(0.92 * GAME_REGION[2], 0.56 * GAME_REGION[3]), 0.08 * GAME_REGION[2], 0.12 * GAME_REGION[3]))
    pyautogui.click(UPGRADE_COORDS)
    pyautogui.moveTo(CLICK_COORDS)
    pause()
    logging.info("Buying any available upgrades.")
    while True:
        button = pyautogui.locateAllOnScreen(imPath("can_buy.png"), region=(0.85 * GAME_REGION[2], 0.13 * GAME_REGION[3], 0.06 * GAME_REGION[2], 0.74 * GAME_REGION[3]), confidence=0.96)
        button = list(button)
        if len(button) == 0:
            logging.info("No more upgrades available.")
            break
        else:
            # logging.info("At least %s upgrade(s) available." % len(button))
            for i in button:
                pyautogui.click(x=i[0] + i[2]/2, y=i[1] + i[3]/2, interval=0.01)
            pyautogui.moveTo(CLICK_COORDS)
    pyautogui.click(CLOSE_COORDS)
    return


def guildMission():
    global GUILD_MISSION_TIME_LEFT

    if now() > GUILD_MISSION_TIME_LEFT:
        pause()
        click(0.96 * GAME_REGION[2], 0.24 * GAME_REGION[3])
        pause()
        click(0.79 * GAME_REGION[2], 0.18 * GAME_REGION[3])
        pause()
        click(0.09 * GAME_REGION[2], 0.35 * GAME_REGION[3])
        pause()

        pyautogui.screenshot(imPath("ss.png"), region=(0.31 * GAME_REGION[2], 0.32 * GAME_REGION[3], 0.1 * GAME_REGION[2], 0.04 * GAME_REGION[3]))
        pause()
        result = ocr(imPath("ss.png"))
        if result != "Completed" and result != "":
            pause()
            try:
                result = result.partition(":")[0]
                time_left = int(result) + 1
                # TODO: Set back to 60min
                GUILD_MISSION_TIME_LEFT = now() + (time_left * 60)
                # logging.info(now())
                # logging.info(GUILD_MISSION_TIME_LEFT)
                logging.info(f"Current mission will complete in {time_left}min.")
                logging.info("Exiting Guild...")
                click(0.95 * GAME_REGION[2], 0.07 * GAME_REGION[3], clicks=3, interval=0.5)
                return
            except Exception as e:
                logging.info(e)
                logging.warning("Not sure what the status is.")
                click(0.7 * GAME_REGION[2], 0.31 * GAME_REGION[3])
                logging.info("Attempted to stat new expedition. Will check back later.")
                pause()
                logging.info("Exiting Guild...")
                click(0.95 * GAME_REGION[2], 0.07 * GAME_REGION[3], clicks=3, interval=0.5)
                pause()
                return

        elif result == "Completed":
            logging.info("Mission completed.")
            moveTo(0.7 * GAME_REGION[2], 0.31 * GAME_REGION[3], 0.5)
            click(0.7 * GAME_REGION[2], 0.31 * GAME_REGION[3])
            sleep(1.5)
            moveTo(0.61 * GAME_REGION[2], 0.67 * GAME_REGION[3], 0.5)
            click(0.61 * GAME_REGION[2], 0.67 * GAME_REGION[3])
            logging.info("Claimed.")
            pause()
            
        pyautogui.screenshot(imPath("ss.png"), region=(0.32 * GAME_REGION[2], 0.48 * GAME_REGION[3], 0.35 * GAME_REGION[2], 0.06 * GAME_REGION[3]))
        pause()
        result = ocr(imPath("ss.png"))
        if result != "There are no pending expeditions.":
            moveTo(0.7 * GAME_REGION[2], 0.31 * GAME_REGION[3], 0.5)
            click(0.7 * GAME_REGION[2], 0.31 * GAME_REGION[3])
            logging.info("Attempted to stat new expedition. Will check back later.")
            pause()
            logging.info("Exiting Guild...")
            click(0.95 * GAME_REGION[2], 0.07 * GAME_REGION[3], clicks=3, interval=0.5)
        else:
            logging.info("No missions left.")
            pyautogui.screenshot(imPath("ss.png"), region=(0.54 * GAME_REGION[2], 0.13 * GAME_REGION[3], 0.08 * GAME_REGION[2], 0.04 * GAME_REGION[3]))
            pause()
            result = ocr(imPath("ss.png"))
            result = result.partition(":")[0]
            time_left = int(result) + 1
            # TODO: Set this back to "* 60"
            GUILD_MISSION_TIME_LEFT = now() + (time_left * 60)
            logging.info(f"More missions available in {time_left}min.")
            logging.info("Exiting Guild...")
            click(0.95 * GAME_REGION[2], 0.07 * GAME_REGION[3], clicks=3, interval=0.5)
    return


def farmGold(levels):

    global UPGRADE_LOWERED, UPGRADE_COORDS, CLOSE_COORDS

    pyautogui.click(0.36 * GAME_REGION[2], 0.04 * GAME_REGION[3], clicks=levels, interval=0.5)
    logging.info("Going back %s levels to farm." % levels)

    if UPGRADE_LOWERED is False:
        UPGRADE_LOWERED = True
        logging.info("Lowering upgrade progression to x1.")
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
            # logging.info("Attempting to fight boss.")
            LAST_BOSS_ATTEMPT = now()
            BOSS_FAILED = True
            FARMING = True
            farmGold(20)
            sleep(1)
            pyautogui.click(button)
    return


def guardianClick(clicks):
    global CLICK_COORDS

    logging.info("Clicking %s times." % clicks)
    pyautogui.click(x=CLICK_COORDS[0], y=CLICK_COORDS[1], clicks=clicks, interval=1.0)


def prestige():
    global AUTO_PRESTIGE, LAST_PRESTIGE, FRESH_START, UPGRADE_LOWERED, CLOSE_COORDS

    if AUTO_PRESTIGE is True:
        button = pyautogui.locateCenterOnScreen(imPath("prestige.png"), confidence=0.9)
        if button is None:
            return
        logging.info("READY TO PRESTIGE! Doing so now.")
        pyautogui.click(button)
        sleep(1)
        button = pyautogui.locateCenterOnScreen(imPath("choose_prestige.png"))
        pyautogui.click(button)
        sleep(1)
        logging.info("Choosing the FREE prestige option.")
        button = pyautogui.locateCenterOnScreen(imPath("free_prestige.png"))
        pyautogui.click(button)
        LAST_PRESTIGE = now()
        FRESH_START = True
        sleep(20)

        if UPGRADE_LOWERED is True:
            UPGRADE_LOWERED = False
            logging.info("Raise upgrade progression to 'Next Milestone.'")
            pyautogui.click(UPGRADE_COORDS)
            pause()
            pyautogui.click(0.89 * GAME_REGION[2], 0.94 * GAME_REGION[3], clicks=3, interval=0.5)
            pyautogui.click(CLOSE_COORDS)
    return


def freshSetup():
    global LAST_PRESTIGE, FRESH_START, UPGRADE_LOWERED, UPGRADE_COORDS, CLOSE_COORDS

    if FRESH_START is True:
        logging.info("Fresh start detected. Checking how long it's been.")
        if now() > (LAST_PRESTIGE + 120):
            logging.info("We should have enough gold to buy party now.")
            pyautogui.click(0.96 * GAME_REGION[2], 0.48 * GAME_REGION[3])  # Open party menu
            pause()
            logging.info("Buying first party slot.")
            pyautogui.click(0.41 * GAME_REGION[2], 0.8 * GAME_REGION[3])  # Buy fist party slot
            pause()
            logging.info("Putting Ranger in first slot.")
            pyautogui.click(0.86 * GAME_REGION[2], 0.6 * GAME_REGION[3])  # Put Ranger in first slot
            pause()
            logging.info("Buying second party slot.")
            pyautogui.click(0.4 * GAME_REGION[2], 0.57 * GAME_REGION[3])  # Buy second slot
            pause()
            logging.info("Putting Warrior in second slot.")
            pyautogui.click(0.77 * GAME_REGION[2], 0.59 * GAME_REGION[3])  # Put warrior in first slot
            pause()
            logging.info("Buying third party slot.")
            pyautogui.click(0.29 * GAME_REGION[2], 0.83 * GAME_REGION[3])  # Buying third party slot
            pause()
            logging.info("Putting mage in third slot.")
            pyautogui.click(0.86 * GAME_REGION[2], 0.41 * GAME_REGION[3])  # Putting mage in third slot
            pause()
            logging.info("Buying fourth party slot.")
            pyautogui.click(0.28 * GAME_REGION[2], 0.48 * GAME_REGION[3])  # Buying fourth party slot
            pause()
            logging.info("Putting tank in fourth party slot.")
            pyautogui.click(0.77 * GAME_REGION[2], 0.41 * GAME_REGION[3])  # Put tank in fourth slot
            logging.info("Saving party changes.")
            pyautogui.click(0.6 * GAME_REGION[2], 0.09 * GAME_REGION[3])  # Save changes
            pause()
            logging.info("Done configuring party.")
            pyautogui.click(0.96 * GAME_REGION[2], 0.06 * GAME_REGION[3])  # Close party screen

            logging.info("Fresh setup complete. Fresh start status removed.")
            FRESH_START = False

    return


def startPlaying():
    global UPGRADE_COORDS, CLICK_COORDS
    while True:
        try:
            buyUpgrades()
            guildMission()
            guardianClick(15)
            freshSetup()
            fightBoss()
            prestige()
        except pyautogui.FailSafeException:
            logging.error("Fail safe detected! Terminating.")
            messagebox.showerror(title=f"Firestone Bot {version}", message="Fail safe detected! Exiting.")
            exit()


if __name__ == '__main__':
    main()
