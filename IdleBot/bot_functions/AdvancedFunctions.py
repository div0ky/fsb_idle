import pyautogui
from bot_internals.GameCoords import game_coords
from bot_internals.DatabaseManager import database
from bot_internals.SharedFunctions import ocr, is_num, change_upgrade_progression
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


def auto_prestige():
    if database.auto_prestige and time.time() >= database.prestige_check_time:
        time.sleep(0.5)
        pyautogui.click(game_coords.town_coords)
        time.sleep(0.5)
        pyautogui.click(game_coords.temple_of_eternals_coords)
        time.sleep(0.5)
        pyautogui.click(game_coords.relative_coords(1359, 560))  # Open prestige menu
        time.sleep(0.5)

        pyautogui.screenshot(database.ocr_image, region=(game_coords.relative_coords(1070, 745, 160, 70)))
        result = ocr(database.ocr_image)

        # while not isNum(result, 2):
        #     pyautogui.screenshot(database.OCR_IMAGE, region=(relCoords(1070, 745, 160, 70)))
        #     result = ocr(database.OCR_IMAGE)

        if is_num(result, 2):
            database.save_option('ocr_succeed_count', int(database.read_option('ocr_succeed_count')) + 1)

            prestige_level = round(float(result[1:]), 2)

        else:
            database.save_option('ocr_fail_count', int(database.read_option('ocr_fail_count')) + 1)
            log.warning("Wasn't able to ascertain our current prestige level.")
            # TODO: Determine if this is still necessary. DISABLED for now.
            # if db.ocr_f_pct > 50:
            #     pyautogui.screenshot(os.path.expanduser("~") + f"/Documents/Firestone Bot/OCR/Fail_{db.ocr_fail_count}_{round(time(), 5)}.png")

        if prestige_level:
            progress = round((prestige_level / database.prestige_level) * 100)
            log.info(f"Current earnings are at {prestige_level}x which is {progress}% of our goal.")
            time.sleep(0.5)

            snooze = ((progress - 100) / (0 - 100)) * ((60 - 1) + 1) * 1000
            if snooze <= 1000:
                snooze = 1000
            elif snooze >= 60000:
                snooze = 60000
            database.save_option('prestige_check_time', time.time() + snooze)
            log.info(f"Will wait {round((snooze / 1000), 2)}min before checking Prestige progress again.")
            time.sleep(0.5)

            if prestige_level >= database.prestige_level:
                log.info("Firestone earnings are satisfactory. Prestiging...")
                pyautogui.click(game_coords.relative_coords(1160, 525))  # Click on FREE prestige option
                time.sleep(15)  # Wait for prestige to finish

                pyautogui.click(game_coords.guardian_click_coords, clicks=20, interval=1.1)  # Let's get some gold to buy party with

                setup_party()
                change_upgrade_progression('Milestone')

        log.info("Going back to home screen.")
        pyautogui.click(game_coords.big_close_coords, clicks=3, interval=0.5)  # Go home because we're not prestiging


def setup_party():
    log.info("Setting up the party.")
    time.sleep(0.5)
    pyautogui.click(game_coords.party_coords)

    if database.party_size >= 1:
        time.sleep(0.5)
        log.info("Buying first party slot.")
        pyautogui.click(game_coords.relative_coords(802, 795))  # Buy fist party slot
    if database.party_size >= 2:
        time.sleep(0.5)
        log.info("Buying second party slot.")
        pyautogui.click(game_coords.relative_coords(775, 540))  # Buy second slot
    if database.party_size >= 3:
        time.sleep(0.5)
        log.info("Buying third party slot.")
        pyautogui.click(game_coords.relative_coords(575, 815))  # Buying third party slot
    if database.party_size >= 4:
        time.sleep(0.5)
        log.info("Buying fourth party slot.")
        pyautogui.click(game_coords.relative_coords(550, 445))  # Buying fourth party slot
    if database.party_size >= 5:
        time.sleep(0.5)
        log.info("Buying fifth party slot.")
        pyautogui.click(game_coords.relative_coords(510, 630))  # Buying fifth party slot

    if database.party_size >= 1:
        time.sleep(0.5)
        pyautogui.click(game_coords.hero_coords[database.party_slot_1])
    if database.party_size >= 2:
        time.sleep(0.5)
        pyautogui.click(game_coords.hero_coords[database.party_slot_2])
    if database.party_size >= 3:
        time.sleep(0.5)
        pyautogui.click(game_coords.hero_coords[database.party_slot_3])
    if database.party_size >= 4:
        time.sleep(0.5)
        pyautogui.click(game_coords.hero_coords[database.party_slot_4])
    if database.party_size >= 5:
        time.sleep(0.5)
        pyautogui.click(game_coords.hero_coords[database.party_slot_5])

    time.sleep(0.5)
    pyautogui.click(game_coords.relative_coords(1160, 95))  # Click to save changes
    time.sleep(0.5)
    pyautogui.click(game_coords.big_close_coords)
    time.sleep(0.5)