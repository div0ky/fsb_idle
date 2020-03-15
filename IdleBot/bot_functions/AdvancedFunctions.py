import pyautogui
from bot_internals.GameCoords import game_coords
from bot_internals.DatabaseManager import database
from bot_internals.SharedFunctions import ocr, is_num
from bot_internals.BotLog import log
import time

def map_missions():
        spawn_points = [(393, 350), (620, 425), (265, 635), (245, 960), (590, 772), (715, 735), (800, 975), (875, 875),
                        (1000, 640), (1190, 640), (1270, 795), (1285, 485), (1578, 540), (1578, 365), (410, 725),
                        (815, 775), (1040, 410), (1375, 350), (1570, 365), (1460, 800), (1300, 985), (760, 565),
                        (830, 690), (875, 555), (1440, 645), (1440, 910), (1560, 980), (830, 395), (465, 445),
                        (1550, 740), (1290, 688)]

        pyautogui.click(game_coords.map_coords)  # Open the map
        time.sleep(1.5)

        pyautogui.screenshot(database.ocr_image, region=(game_coords.relative_coords(825, 30, 100, 38)))
        result = ocr(database.ocr_image)

        if is_num(result):
            database.save_option('map_troops', int(result[0]))
            log.info(f"We appear to have {database.map_troops} troops available.")

        while True:
            if pyautogui.pixelMatchesColor(game_coords.relative_coords(232), game_coords.relative_coords(315), (247, 163, 66), tolerance=10):
                log.info("Claiming a map mission.")
                pyautogui.click(game_coords.relative_coords(232, 315))
                time.sleep(0.5)
                pyautogui.moveTo(game_coords.guardian_click_coords)
                pyautogui.press('esc')
                time.sleep(0.5)
            else:
                break

        if database.map_troops > 0:
            log.info("Entered map missions loop")
            for x in spawn_points:
                if database.map_troops > 0:
                    log.debug(f"Clicking @ {x[0], x[1]}")
                    pyautogui.click(x)  # Click known spawn points
                    time.sleep(0.5)
                    if pyautogui.pixelMatchesColor(game_coords.relative_coords(830), game_coords.relative_coords(960), (11, 161, 8), tolerance=5):
                        pyautogui.click(game_coords.relative_coords(830, 960))
                        log.info("Started a mission.")
                        time.sleep(0.5)
                        pyautogui.press('esc')
                        time.sleep(0.5)
                        database.save_option('map_troops', database.map_troops -1)
                        continue
                    elif pyautogui.pixelMatchesColor(game_coords.relative_coords(743), game_coords.relative_coords(934), (231, 77, 66),
                                                     tolerance=5):
                        pyautogui.press('esc')
                    else:
                        # pyautogui.press('esc')
                        # time.sleep(0.5)
                        continue
                else:
                    break
        else:
            log.info("Going home.")

        pyautogui.press('esc')