#! python3
""" Firestone Idle RPG Bot
Divoky 20-01-18

Alpha 2.0.0.5967

A bot to handle auto upgrading party members and such as it progresses.
"""

import pyautogui, os, logging, tkinter
from tkinter import messagebox
import pygetwindow as gw
from time import time as now
from time import sleep as sleep
import cv2
from PIL import Image
import pytesseract
from pyautogui import click
from pyautogui import moveTo

version = "Alpha 1.0.0.7310"

"""
Setup logging handlers.
"""
logging.basicConfig(level=logging.INFO, format='%(asctime)s.%(msecs)03d - %(levelname)s: %(message)s', datefmt='%H:%M:%S', filename="debug.log")
root = tkinter.Tk()
root.withdraw()

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
    return os.path.join("images", filename)


def getGameRegion():
    """Obtains the region that the game is on the screen and assigns variables"""
    global GAME_REGION

    # identify the top-left corner
    logging.info("Finding game region...")
    game = gw.getWindowsWithTitle("Firestone")
    game[0].activate()
    sleep(1.5)
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
    GAME_REGION = (topLeftX, topLeftY, 1920, 1080)
    logging.info("Game region found: %s" % (GAME_REGION,))


def setupCoordinates():
    global UPGRADE_COORDS, CLICK_COORDS, CLOSE_COORDS
    UPGRADE_COORDS = (GAME_REGION[0] + 1835, GAME_REGION[1] + 660)
    CLICK_COORDS = (GAME_REGION[2] / 2, GAME_REGION[3] / 2)
    CLOSE_COORDS = (1875, 99)


def buyUpgrades():
    global CLICK_COORDS, UPGRADE_COORDS, CLOSE_COORDS
    # button = pyautogui.locateOnScreen(imPath("upgrades.png"), region=(1770, 605, 150, 130))
    pyautogui.click(UPGRADE_COORDS)
    pyautogui.moveTo(CLICK_COORDS)
    pause()
    logging.info("Buying any available upgrades.")
    while True:
        button = pyautogui.locateAllOnScreen(imPath("can_buy.png"), region=(1630, 140, 110, 800), confidence=0.96)
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
        click(1840, 258)
        pause()
        click(1510, 195)
        pause()
        click(175, 380)
        pause()

        pyautogui.screenshot(imPath("ss.png"), region=(600, 345, 195, 40))
        pause()
        result = ocr(imPath("ss.png"))
        if result != "Completed" and result != "":
            pause()
            try:
                result = result.partition(":")[0]
                time_left = int(result) + 1
                GUILD_MISSION_TIME_LEFT = now() + (time_left * 60)
                # logging.info(now())
                # logging.info(GUILD_MISSION_TIME_LEFT)
                logging.info(f"Current mission will complete in {time_left}min.")
                logging.info("Exiting Guild...")
                click(1820, 78, clicks=3, interval=0.5)
                return
            except Exception as e:
                logging.info(e)
                logging.warning("Not sure what the status is.")
                click(1335, 340)
                logging.info("Attempted to stat new expedition. Will check back later.")
                pause()
                logging.info("Exiting Guild...")
                click(1820, 78, clicks=3, interval=0.5)
                pause()
                return

        elif result == "Completed":
            logging.info("Mission completed.")
            moveTo(1335, 335, 0.5)
            click(1335, 335)
            sleep(1.5)
            moveTo(1180, 720, 0.5)
            click(1180, 720)
            logging.info("Claimed.")
            pause()
            
        pyautogui.screenshot(imPath("ss.png"), region=(620, 520, 680, 67))
        pause()
        result = ocr(imPath("ss.png"))
        if result != "There are no pending expeditions.":
            moveTo(1335, 340, 0.5)
            click(1335, 340)
            logging.info("Attempted to stat new expedition. Will check back later.")
            pause()
            logging.info("Exiting Guild...")
            click(1820, 78, clicks=3, interval=0.5)
        else:
            logging.info("No missions left.")
            pyautogui.screenshot(imPath("ss.png"), region=(1035, 140, 145, 43))
            pause()
            result = ocr(imPath("ss.png"))
            result = result.partition(":")[0]
            time_left = int(result) + 1
            GUILD_MISSION_TIME_LEFT = now() + (time_left * 60)
            logging.info(f"More missions available in {time_left}min.")
            logging.info("Exiting Guild...")
            click(1820, 78, clicks=3, interval=0.5)
    return


def farmGold(levels):

    global UPGRADE_LOWERED, UPGRADE_COORDS, CLOSE_COORDS

    pyautogui.click(693, 40, clicks=levels, interval=0.5)
    logging.info("Going back %s levels to farm." % levels)

    if UPGRADE_LOWERED is False:
        UPGRADE_LOWERED = True
        logging.info("Lowering upgrade progression to x1.")
        pyautogui.click(UPGRADE_COORDS)
        pause()
        pyautogui.click(1700, 1015, clicks=2, interval=0.5)
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
            pyautogui.click(1700, 1015, clicks=3, interval=0.5)
            pyautogui.click(CLOSE_COORDS)
    return


def freshSetup():
    global LAST_PRESTIGE, FRESH_START, UPGRADE_LOWERED, UPGRADE_COORDS, CLOSE_COORDS

    if FRESH_START is True:
        logging.info("Fresh start detected. Checking how long it's been.")
        if now() > (LAST_PRESTIGE + 120):
            logging.info("We should have enough gold to buy party now.")
            pyautogui.click(1842, 523)  # Open party menu
            pause()
            logging.info("Buying first party slot.")
            pyautogui.click(795, 860)  # Buy fist party slot
            pause()
            logging.info("Putting Ranger in first slot.")
            pyautogui.click(1660, 645)  # Put Ranger in first slot
            pause()
            logging.info("Buying second party slot.")
            pyautogui.click(765, 615)  # Buy second slot
            pause()
            logging.info("Putting Warrior in second slot.")
            pyautogui.click(1475, 635)  # Put warrior in first slot
            pause()
            logging.info("Buying third party slot.")
            pyautogui.click(565, 900)  # Buying third party slot
            pause()
            logging.info("Putting mage in third slot.")
            pyautogui.click(1660, 445)  # Putting mage in third slot
            pause()
            logging.info("Buying fourth party slot.")
            pyautogui.click(545, 520)  # Buying fourth party slot
            pause()
            logging.info("Putting tank in fourth party slot.")
            pyautogui.click(1480, 440)  # Put tank in fourth slot
            logging.info("Saving party changes.")
            pyautogui.click(1150, 95)  # Save changes
            pause()
            logging.info("Done configuring party.")
            pyautogui.click(1850, 65)  # Close party screen

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
