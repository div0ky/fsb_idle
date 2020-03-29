import pyautogui
from datetime import datetime, timedelta
from bot_internals.GameCoords import game_coords
from bot_internals.DatabaseManager import database
from bot_internals.SharedFunctions import ocr, is_num, change_upgrade_progression, image_path
from bot_internals.BotLog import log
import re, ast
import time

last_check = datetime.utcnow() - timedelta(minutes=5)

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
