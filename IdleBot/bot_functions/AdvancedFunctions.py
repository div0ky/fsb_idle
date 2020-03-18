import pyautogui
from bot_internals.GameCoords import game_coords
from bot_internals.DatabaseManager import database
from bot_internals.SharedFunctions import ocr, is_num
from bot_internals.BotLog import log
import re, ast
import time

def map_missions():
        spawn_points = [ast.literal_eval(i) for i in re.split('(?<=\)),(?=\()', str(database.map_nodes))]

        pyautogui.click(game_coords.map_coords)  # Open the map
        time.sleep(1.5)

        pyautogui.screenshot(database.ocr_image, region=(game_coords.relative_coords(825, 30, 100, 38)))
        result = ocr(database.ocr_image)

        if is_num(result, 3):
            database.save_option('map_troops', int(result[0]))
            log.info(f"We appear to have {database.map_troops} troops available.")

        # claim any completed map missions
        _map_mission_count = 0
        while True:
            if pyautogui.pixelMatchesColor(game_coords.relative_coords(232), game_coords.relative_coords(315), (247, 163, 66), tolerance=10):
                log.info("Claiming a map mission.")
                pyautogui.click(game_coords.relative_coords(232, 315))
                _map_mission_count += 1
                time.sleep(0.5)
                pyautogui.moveTo(game_coords.guardian_click_coords)
                pyautogui.press('esc')
                time.sleep(0.5)
            else:
                if _map_mission_count > 0:
                    database.save_stat('total_map_missions', database.total_map_missions + _map_mission_count)
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