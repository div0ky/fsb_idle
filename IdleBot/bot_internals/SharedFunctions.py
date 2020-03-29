import http.client
import os
import urllib
from time import sleep

import pytesseract
import pyautogui
import requests
from PIL import Image

from .BotLog import log
from .DatabaseManager import database
from .GameCoords import game_coords
import time

# Define where the tesseract engine is installed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

pyautogui.PAUSE = 0.5  # set the fail-safe delay between operations in seconds

def is_num(num, v=1):
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
    if v == 3:
        print(len(num))
        check1 = num[0]

        try:
            check1 = round(int(check1))
        except ValueError:
            pass

        if isinstance(check1, int):
            return True
        else:
            return False


def ocr(file):
    # CONVERTS AN IMAGE INTO A STRING
    log.info("Reading...")
    im = Image.open(file).convert("LA")
    base = int(float(im.size[0] * 1.5))
    wpercent = (base / float(im.size[0]))
    hsize = int(float(im.size[1]) * float(wpercent))
    im = im.resize((base, hsize), Image.ANTIALIAS)
    im.save(database.ocr_image)
    text = pytesseract.image_to_string(file, lang="eng", config='--psm 7')
    log.debug(f"I think it says: {text}")
    return text


def push(msg):
    ip = requests.get('https://api.ipify.org').text
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
                 urllib.parse.urlencode({
                     "token": "anj13d6adu8s3hm66pfmiwacjxwt36",
                     "user": "uGUQThApDAJfvscP5Levk419xn7yyx",
                     "message": f"{ip} - {msg}",
                 }), {"Content-type": "application/x-www-form-urlencoded"})
    conn.getresponse()

def image_path(filename):
    # A shortcut for joining the 'images/' file path
    return os.path.join(r"C:\Program Files\Firestone Idle Bot\Data\Images", filename)

def change_upgrade_progression(option):
    current_progression = database.upgrade_status
    valid_options = ['x1', 'x10', 'x100', 'Milestone', 'Max']
    progressions = {'x1': {'x10': 1, 'x100': 2, 'Milestone': 3, 'Max': 4},
                    'x10': {'x100': 1, 'Milestone': 2, 'Max': 3, 'x1': 4},
                    'x100': {'Milestone': 1, 'Max': 2, 'x1': 3, 'x10': 4},
                    'Milestone': {'Max': 1, 'x1': 2, 'x10': 3, 'x100': 4},
                    'Max': {'x1': 1, 'x10': 2, 'x100': 3, 'Milestone': 4}}
    log.debug(f"Received request to change progression to {option}.")

    if option in valid_options:
        if option == current_progression:
            log.warning(f"We're already at {option} progression!")
        else:
            clicks = int(progressions[current_progression][option])
            pyautogui.click(game_coords.upgrade_button)
            time.sleep(0.5)
            log.debug(f"We need to click {clicks} times to get to {option}")
            pyautogui.click(game_coords.upgrade_progression_button, clicks=clicks, interval=0.5)
            pyautogui.click(game_coords.small_close_coords)
            log.info(f"Changed progression to {option}")
            database.save_option('upgrade_status', option)
    else:
        log.warning(f"We did not receive a valid upgrade progression option!")
