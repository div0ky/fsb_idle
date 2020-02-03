#! python3
""" Firestone Idle RPG Bot
Divoky 20-01-18

BUILD 46.4769

A bot to handle auto upgrading party members and such as it progresses.
"""

import pyautogui, time, os, logging, sys, random, copy

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s.%(msecs)03d: %(message)s', datefmt='%H:%M:%S')

# Various coordinates of objects in the game
GAME_REGION = ()  # left, top, width, height
FARM_TIME = 60
AUTO_PRESTIGE = False
BOSS_FAILED = False
UPGRADE_LOWERED = True
FRESH_START = False
FARMING = False
LAST_BOSS_ATTEMPT = time.time() - FARM_TIME
LAST_PRESTIGE = time.time()
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
    logging.debug("Program started. Press Ctrl-C to abort at any time.")
    logging.debug("To interrupt mouse movement, move mouse to upper left corner.")
    getGameRegion()
    setupCoordinates()
    startPlaying()


def imPath(filename):
    """A shortcut for joining the 'images/' file path"""
    return os.path.join("images", filename)


def getGameRegion():
    """Obtains the region that the game is on the screen and assigns variables"""
    global GAME_REGION

    # identify the top-left corner
    logging.debug("Finding game region...")
    region = pyautogui.locateOnScreen(imPath("top_left_corner.png"), confidence=0.9)
    if region is None:
        logging.debug("Not sure the game is on screen. Proceeding anyway.")
        region = (0, 0)  # manually set what it SHOULD be
        # raise Exception("Could not find game on screen. Is the game visible?")


    # calculate the region of the entire game
    topLeftX = region[0]
    topLeftY = region[1]  # top
    GAME_REGION = (topLeftX, topLeftY, 1920, 1080)
    logging.debug("Game region found: %s" % (GAME_REGION,))


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
    time.sleep(0.5)
    logging.debug("Buying any available upgrades.")
    while True:
        button = pyautogui.locateAllOnScreen(imPath("can_buy.png"), region=(1630, 140, 110, 800), confidence=0.96)
        button = list(button)
        if len(button) == 0:
            logging.debug("No more upgrades available.")
            break
        else:
            # logging.debug("At least %s upgrade(s) available." % len(button))
            for i in button:
                pyautogui.click(x=i[0] + i[2]/2, y=i[1] + i[3]/2, interval=0.01)
            pyautogui.moveTo(CLICK_COORDS)
    pyautogui.click(CLOSE_COORDS)
    return

def farmGold(levels):

    global UPGRADE_LOWERED, UPGRADE_COORDS, CLOSE_COORDS

    button = pyautogui.locateCenterOnScreen(imPath("go_back.png"), grayscale=True, confidence=0.9)

    if button is None:
        raise Exception("Couldn't find arrow to bo back!")
    pyautogui.click(button[0], button[1], clicks=levels, interval=0.5)
    logging.debug("Going back %s levels to farm." % levels)

    if UPGRADE_LOWERED is False:
        UPGRADE_LOWERED = True
        logging.debug("Lowering upgrade progression to x1.")
        pyautogui.click(UPGRADE_COORDS)
        time.sleep(0.5)
        pyautogui.click(1700, 1015, clicks=2, interval=0.5)
        pyautogui.click(CLOSE_COORDS)
    return


def fightBoss():
    global LAST_BOSS_ATTEMPT, BOSS_FAILED, FARMING, FARM_TIME

    if time.time() > (LAST_BOSS_ATTEMPT + FARM_TIME):
        FARMING = False

        button = pyautogui.locateCenterOnScreen(imPath("boss.png"))
        if button is None:
            return
        else:
            # logging.debug("Attempting to fight boss.")
            LAST_BOSS_ATTEMPT = time.time()
            BOSS_FAILED = True
            FARMING = True
            farmGold(20)
            time.sleep(1)
            pyautogui.click(button)
    return


def guardianClick(clicks):
    global CLICK_COORDS

    logging.debug("Clicking %s times." % clicks)
    pyautogui.click(x=CLICK_COORDS[0], y=CLICK_COORDS[1], clicks=clicks, interval=1.0)


def prestige():
    global AUTO_PRESTIGE, LAST_PRESTIGE, FRESH_START, UPGRADE_LOWERED, CLOSE_COORDS

    if AUTO_PRESTIGE is True:
        button = pyautogui.locateCenterOnScreen(imPath("prestige.png"), confidence=0.9)
        if button is None:
            return
        logging.debug("READY TO PRESTIGE! Doing so now.")
        pyautogui.click(button)
        time.sleep(1)
        button = pyautogui.locateCenterOnScreen(imPath("choose_prestige.png"))
        pyautogui.click(button)
        time.sleep(1)
        logging.debug("Choosing the FREE prestige option.")
        button = pyautogui.locateCenterOnScreen(imPath("free_prestige.png"))
        pyautogui.click(button)
        LAST_PRESTIGE = time.time()
        FRESH_START = True
        time.sleep(20)

        if UPGRADE_LOWERED is True:
            UPGRADE_LOWERED = False
            logging.debug("Raise upgrade progression to 'Next Milestone.'")
            pyautogui.click(UPGRADE_COORDS)
            time.sleep(0.5)
            pyautogui.click(1700, 1015, clicks=3, interval=0.5)
            pyautogui.click(CLOSE_COORDS)
    return


def freshSetup():
    global LAST_PRESTIGE, FRESH_START, UPGRADE_LOWERED, UPGRADE_COORDS, CLOSE_COORDS

    if FRESH_START is True:
        logging.debug("Fresh start detected. Checking how long it's been.")
        if time.time() > (LAST_PRESTIGE + 120):
            logging.debug("We should have enough gold to buy party now.")
            pyautogui.click(1842, 523)  # Open party menu
            time.sleep(0.5)
            logging.debug("Buying first party slot.")
            pyautogui.click(795, 860)  # Buy fist party slot
            time.sleep(0.5)
            logging.debug("Putting Ranger in first slot.")
            pyautogui.click(1660, 645)  # Put Ranger in first slot
            time.sleep(0.5)
            logging.debug("Buying second party slot.")
            pyautogui.click(765, 615)  # Buy second slot
            time.sleep(0.5)
            logging.debug("Putting Warrior in second slot.")
            pyautogui.click(1475, 635)  # Put warrior in first slot
            time.sleep(0.5)
            logging.debug("Buying third party slot.")
            pyautogui.click(565, 900)  # Buying third party slot
            time.sleep(0.5)
            logging.debug("Putting mage in third slot.")
            pyautogui.click(1660, 445)  # Putting mage in third slot
            time.sleep(0.5)
            logging.debug("Buying fourth party slot.")
            pyautogui.click(545, 520)  # Buying fourth party slot
            time.sleep(0.5)
            logging.debug("Putting tank in fourth party slot.")
            pyautogui.click(1480, 440)  # Put tank in fourth slot
            logging.debug("Saving party changes.")
            pyautogui.click(1150, 95)  # Save changes
            time.sleep(0.5)
            logging.debug("Done configuring party.")
            pyautogui.click(1850, 65)  # Close party screen

            logging.debug("Fresh setup complete. Fresh start status removed.")
            FRESH_START = False

    return


def startPlaying():
    global UPGRADE_COORDS, CLICK_COORDS
    while True:
        guardianClick(15)
        freshSetup()
        buyUpgrades()
        fightBoss()
        prestige()


if __name__ == '__main__':
    main()
