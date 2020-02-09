try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import pyautogui
import time, string, logging
from pyautogui import click
from pyautogui import moveTo
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s.%(msecs)03d: %(message)s', datefmt='%H:%M:%S')
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

global result


def pause():
    time.sleep(0.5)

def ocr(file):
    """
    This function will convert an image into a string.
    """
    text = pytesseract.image_to_string(file)
    return text


def guildMission():
    global GUILD_MISSION_TIME_LEFT, result
    click(1840, 258)
    pause()
    click(1510, 195)
    pause()
    click(175, 380)
    pause()

    im = pyautogui.screenshot("ss.png", region=(600, 345, 195, 40))
    pause()
    result = ocr(im)
    logging.debug(f"I think it says: {result}")
    if result != "Completed":
        pause()
        try:
            result = result[0:2]
            time_left = int(result) + 1
            GUILD_MISSION_TIME_LEFT = time.time() + time_left
            logging.debug(time.time())
            logging.debug(GUILD_MISSION_TIME_LEFT)
            logging.debug(f"Current mission will complete in {time_left}min.")
            logging.debug("Exiting Guild...")
            click(1820, 78, clicks=3, interval=0.5)
        except Exception as e:
            logging.debug(e)
            logging.debug("Not sure what the status is.")
            click(1335, 340)
            logging.debug("Attempted to stat new expedition. Will check back later.")
            logging.debug("Exiting Guild...")
            click(1820, 78, clicks=3, interval=0.5)
            pause()

    else:
        logging.debug("Mission completed.")
        # moveTo(1335, 335, 1)
        click(1335, 335)
        pause()
        logging.debug("Claimed.")
        # moveTo(1335, 540, 1)
        click(1335, 540)
        pause()
        logging.debug("Started new mission.")
        pause()
        logging.debug("Exiting Guild...")
        click(1820, 78, clicks=3, interval=0.5)
        


# im = pyautogui.screenshot(region=(650, 345, 100, 40))
# time_left = int(ocr(im)[0:2]) + 1
# logging.debug(f"Sleeping for {time_left}min.")
# logging.debug(ocr(im))
