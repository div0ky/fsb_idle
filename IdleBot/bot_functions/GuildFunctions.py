from bot_internals.DatabaseManager import database
from bot_internals.BotLog import log
from bot_internals.GameCoords import game_coords
from bot_internals.SharedFunctions import ocr, is_num
import pyautogui
from datetime import datetime, timedelta
from time import sleep as sleep

def guild_expeditions():
    if datetime.now() > database.guild_mission_time_left and database.guild_missions:
        log.info("Checking on Guild Expedition status.")
        sleep(0.5)
        pyautogui.click(game_coords.town_coords)
        sleep(0.5)
        pyautogui.click(game_coords.guild_coords)
        sleep(0.5)
        pyautogui.click(game_coords.guild_expeditions_coords)
        sleep(0.5)
        # Take a screenshot of the mission timer
        pyautogui.screenshot(database.ocr_image, region=(game_coords.relative_coords(600, 345, 200, 40)))
        sleep(0.5)
        # Attempt to read the time using OCR
        result = ocr(database.ocr_image)
        # If it doesn't say "Completed" but it's also not blank... it's probably a number?

        if result == "Completed":
            database.save_option('ocr_succeed_count', int(database.read_option('ocr_succeed_count')) + 1)
            log.info("Current mission was completed.")
            # Click on the "Claim" button.
            pyautogui.click(game_coords.relative_coords(1345, 335))
            sleep(2)  # Wait for it to process
            pyautogui.click(game_coords.relative_coords(1185, 720))  # Click OK on the popup that occurs
            log.info("Claimed.")
            sleep(2)  # Wait for it to process.
            pyautogui.click(game_coords.relative_coords(1335, 335))  # Click to start new expedition
            sleep(0.5)
            pyautogui.click(game_coords.big_close_coords, clicks=3, interval=0.5)  # Go back to main screen
            return

        elif is_num(result):
            database.save_option('ocr_succeed_count', int(database.read_option('ocr_succeed_count')) + 1)
            time_left = int(result.partition(":")[0]) + 1  # Add one minute to whatever minutes are left to be safe
            snooze = datetime.now() + timedelta(minutes=time_left)
            database.save_option('guild_mission_time_left', snooze)
            log.info(f"Current mission should complete in {time_left}min. Going Home.")
            pyautogui.click(game_coords.big_close_coords, clicks=3, interval=0.5)  # Go back to main screen
            sleep(0.5)
            return

        else:
            # If we can't tell, let's make sure it's not saying there are none.
            log.info("Checking to see if we're out of guild expeditions.")
            pyautogui.screenshot(database.ocr_image, region=(game_coords.relative_coords(625, 520, 690, 65)))
            sleep(0.5)  # Give it time to save the image
            result = ocr(database.ocr_image)  # attempt to read it

            if result == "There are no pending expeditions.":
                database.save_option('ocr_succeed_count', int(database.read_option('ocr_succeed_count')) + 1)
                log.info("There are no more expeditions available right now.")
                pyautogui.screenshot(database.ocr_image, region=(game_coords.relative_coords(1030, 145, 145, 35)))
                sleep(0.5)
                result = ocr(database.ocr_image)

                if is_num(result):
                    database.save_option('ocr_succeed_count',
                                              int(database.read_option('ocr_succeed_count')) + 1)
                    if len(result.partition(":")) > 1:
                        # TODO: This math is off, it needs to consider 3 part timecodes and not just 2 re: partition
                        hours = int(result.partition(":")[0]) * 60
                        print(hours)
                        temp = result.partition(":")[2]
                        min = (int(temp.partition(":")[0]) + 1) * 60
                        print(min)

                        time_left = hours + min
                        print(time_left)
                    else:
                        time_left = int(result.partition(":")[0]) * 60

                    snooze = datetime.now() + timedelta(minutes=time_left)
                    database.save_option('guild_mission_time_left', snooze)  # Set timer
                    log.info(f"More missions available in {time_left / 60}min. Returning home.")
                    pyautogui.click(game_coords.big_close_coords, clicks=3, interval=0.5)  # Go back to main screen
                    return
                else:
                    database.save_option('ocr_fail_count', int(database.read_option('ocr_fail_count')) + 1)
                    # TODO: Determine if this is still necessary. DISABLED for now.
                    # if db.ocr_f_pct > 50:
                    #     pyautogui.screenshot(os.path.expanduser("~") + f"/Documents/Firestone Bot/OCR/Fail_{db.ocr_fail_count}_{round(time(), 5)}.png")
                    log.warning("I wasn't able to determine expedition renewal time. Returning home.")
                    pyautogui.click(game_coords.big_close_coords, clicks=3, interval=0.5)  # Go back to main screen
                    return

        database.save_option('ocr_fail_count', int(database.read_option('ocr_fail_count')) + 1)
        # TODO: Determine if this is still necessary. DISABLED for now.
        # if db.ocr_f_pct > 50:
        #     pyautogui.screenshot(
        #         os.path.expanduser("~") + f"/Documents/Firestone Bot/OCR/Fail_{db.ocr_fail_count}_{round(time(), 5)}.png")
        log.warning("Unable to ascertain the current mission status.")
        log.info("Trying to start a new expedition anyway.\nReturning home.")
        pyautogui.click(game_coords.relative_coords(1335, 335))  # Click to start new expedition
        sleep(0.5)
        pyautogui.click(game_coords.big_close_coords, clicks=3, interval=0.5)  # Go back to main screen
        sleep(0.5)
        return