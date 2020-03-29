import time
from datetime import datetime, timedelta

import pyautogui

from bot_internals.BotLog import log
from bot_internals.GameCoords import game_coords
from bot_internals.SharedFunctions import image_path

last_check = datetime.utcnow() - timedelta(minutes=5)
chests_timestamp = datetime.utcnow() - timedelta(hours=2)

def guardian_training():
    global last_check
    snooze = timedelta(minutes=5)
    if last_check + snooze <= datetime.utcnow():
        last_check = datetime.utcnow()
        log.info("Checking on Guardian Training")
        upgrade_color = (27, 102, 26)
        tolerance = 5
        time.sleep(0.75)
        pyautogui.click(game_coords.town_coords)
        time.sleep(0.5)
        pyautogui.click(game_coords.magic_quarter)
        time.sleep(0.5)
        if pyautogui.pixelMatchesColor(1030, 790, upgrade_color, tolerance=tolerance):
            pyautogui.click(1030, 790)
            time.sleep(0.5)
            pyautogui.click(game_coords.big_close_coords, clicks=2, interval=0.5)
            log.info('Guardian training started. Going home.')
        else:
            log.info("Guardian training isn't ready yet. Going home.")
            pyautogui.click(game_coords.big_close_coords, clicks=2, interval=0.5)
    else:
        log.info("Waiting to check on Guardian Training")

def open_chests():
    global chests_timestamp
    if chests_timestamp + timedelta(hours=2) <= datetime.utcnow():
        chests_timestamp = datetime.utcnow()
        log.info('Opening any available chests.')
        time.sleep(0.5)
        pyautogui.click(game_coords.inventory)
        time.sleep(0.5)
        pyautogui.click(game_coords.chests_tab)
        time.sleep(0.5)
        chests = ['inv_common_chest.png', 'inv_uncommon_chest.png', 'inv_rare_chest.png', 'inv_epic_chest.png']
        found = []
        for chest in chests:
            img = pyautogui.locateCenterOnScreen(image_path(chest), region=(1530, 315, 390, 665))
            if img is not None:
                found.append(img)
        if found:
            log.info('Looks like we have at least one chest. Opening it and any others.')
            pyautogui.click(found[0])
        time.sleep(0.5)
        while True:
            img = pyautogui.locateCenterOnScreen(image_path(chests[0]), region=(1060, 915, 565, 140))
            if img is not None:
                pyautogui.click(img)
                time.sleep(0.5)
                pyautogui.click(game_coords.big_chest)
                time.sleep(0.5)
                pyautogui.click(game_coords.open_chest, clicks=3, interval=1)
                log.info('Opened a common chest.')
            else:
                log.info('All common chests are opened.')
                break

        while True:
            img = pyautogui.locateCenterOnScreen(image_path(chests[1]), region=(1060, 915, 565, 140))
            if img is not None:
                pyautogui.click(img)
                time.sleep(0.5)
                pyautogui.click(game_coords.big_chest)
                time.sleep(0.5)
                pyautogui.click(game_coords.open_chest, clicks=5, interval=1)
                log.info('Opened an uncommon chest.')
            else:
                log.info('All uncommon chests are opened.')
                break

        while True:
            img = pyautogui.locateCenterOnScreen(image_path(chests[2]), region=(1060, 915, 565, 140))
            if img is not None:
                pyautogui.click(img)
                time.sleep(0.5)
                pyautogui.click(game_coords.big_chest)
                time.sleep(0.5)
                pyautogui.click(game_coords.open_chest, clicks=7, interval=1)
                log.info('Opened a rare chest.')
            else:
                log.info('All rare chests are opened.')
                break

        while True:
            img = pyautogui.locateCenterOnScreen(image_path(chests[3]), region=(1060, 915, 565, 140))
            if img is not None:
                pyautogui.click(img)
                time.sleep(0.5)
                pyautogui.click(game_coords.big_chest)
                time.sleep(0.5)
                pyautogui.click(game_coords.open_chest, clicks=9, interval=1)
                log.info('Opened an epic chest.')
            else:
                log.info('All epic chests are opened.')
                break
    else:
        log.info("It isn't time to check the chests again yet.")


