import pyautogui
from bot_internals.GameCoords import game_coords
from bot_internals.DatabaseManager import database
from bot_internals.BotLog import log
from bot_internals.SharedFunctions import image_path, change_upgrade_progression
import time

# Set pyautogui speed so we don't click so fast the game can't respond
pyautogui.PAUSE = 0.1

"""
Click the center of the screen to cause damage with your guardian
"""
def guardian_click(clicks=15, speed=1):
    ts = time.time()
    log.info('Resuming guardian duties.')
    if database.guardian == 'Dragon':
        clicks, speed = 15, 1.2
    else:
        clicks, speed = 100, 0.1
    log.debug(f'Will click {clicks} times with a {speed} second interval.')

    for x in range(clicks):
        pyautogui.click(game_coords.guardian_click_coords)
        log.debug(f"Clicked {x + 1} time/s")
        time.sleep(speed)
    log.debug(f"Spent {round(time.time() - ts, 2)} seconds on guardian duties.")

"""
Open the upgrades menu, check for any available (re: green) upgrades, and buy them.
Check starts from top of the list and works its way down.
"""
def buy_upgrades():
    log.info('Buying any and all upgrades that we can afford.')
    # TODO: possibly open drawer first time and then start looking for dot
    # if pyautogui.pixelMatchesColor(relCoords(1894), relCoords(619), (244, 0, 0), tolerance=5):  # Upgrades avail bubble
    pyautogui.click(game_coords.upgrade_button)  # Open the upgrade menu
    pyautogui.moveTo(game_coords.guardian_click_coords)

    upgrade_color = (43, 117, 41)
    tolerance = 5
    _slot_1_count = 0
    _slot_2_count = 0
    _slot_3_count = 0
    _slot_4_count = 0
    _slot_5_count = 0
    _slot_6_count = 0
    _slot_7_count = 0

    while True:

        if pyautogui.pixelMatchesColor(game_coords.relative_coords(1715), game_coords.relative_coords(175), upgrade_color,
                                       tolerance=tolerance):  # Party
            pyautogui.click(game_coords.relative_coords(1715, 175))
            _slot_1_count += 1
            pyautogui.moveTo(game_coords.guardian_click_coords)

        elif pyautogui.pixelMatchesColor(game_coords.relative_coords(1715), game_coords.relative_coords(295), upgrade_color,
                                         tolerance=tolerance):  # Guardian
            pyautogui.click(game_coords.relative_coords(1715, 295))
            _slot_2_count += 1
            pyautogui.moveTo(game_coords.guardian_click_coords)

        elif pyautogui.pixelMatchesColor(game_coords.relative_coords(1715), game_coords.relative_coords(415), upgrade_color,
                                         tolerance=tolerance):  # Party 1
            pyautogui.click(game_coords.relative_coords(1715, 415))
            _slot_3_count += 1
            pyautogui.moveTo(game_coords.guardian_click_coords)

        elif pyautogui.pixelMatchesColor(game_coords.relative_coords(1715), game_coords.relative_coords(540), upgrade_color,
                                         tolerance=tolerance):  # Party 2
            pyautogui.click(game_coords.relative_coords(1715, 540))
            _slot_4_count += 1
            pyautogui.moveTo(game_coords.guardian_click_coords)

        elif pyautogui.pixelMatchesColor(game_coords.relative_coords(1715), game_coords.relative_coords(655), upgrade_color,
                                         tolerance=tolerance):  # Party 3
            pyautogui.click(game_coords.relative_coords(1715, 655))
            _slot_5_count += 1
            pyautogui.moveTo(game_coords.guardian_click_coords)

        elif pyautogui.pixelMatchesColor(game_coords.relative_coords(1715), game_coords.relative_coords(775), upgrade_color,
                                         tolerance=tolerance):  # Party 4
            pyautogui.click(game_coords.relative_coords(1715, 775))
            _slot_6_count += 1
            pyautogui.moveTo(game_coords.guardian_click_coords)

        elif pyautogui.pixelMatchesColor(game_coords.relative_coords(1715), game_coords.relative_coords(895), upgrade_color,
                                         tolerance=tolerance):  # Party 5
            pyautogui.click(game_coords.relative_coords(1715, 895))
            _slot_7_count += 1
            pyautogui.moveTo(game_coords.guardian_click_coords)
        else:
            _total_count = _slot_1_count + _slot_2_count + _slot_3_count + _slot_4_count + _slot_5_count + _slot_6_count + _slot_7_count
            log.info(f"There were {_total_count} upgrades available.")
            break

    pyautogui.click(game_coords.small_close_coords)
    return

def farm_gold(levels=database.farm_levels):

    button = pyautogui.locateCenterOnScreen(image_path("boss.png"))
    if button is None:
        return
    else:
        log.info(f"It looks like we've failed to beat a boss.")
        count = levels
        log.info("Going back %s levels to farm." % levels)

        while count >= 0:
            pyautogui.click(game_coords.back_arrow_coords)
            time.sleep(0.5)
            count -= 1
        time.sleep(1.5)
        pyautogui.click(button)
    log.info("Lowering upgrade progression to x1.")
    change_upgrade_progression('x1')
