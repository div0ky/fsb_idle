import threading
from time import sleep
from bot_internals.BotLog import log

import pyautogui


class MouseLock:
    def __init__(self):
        log.info(f'{__name__} has been initialized.')
        self.sentinel = False
        self.sWidth, self.sHeight = pyautogui.size()
        self.GAME_REGION = (0, 0, self.sWidth, self.sHeight)
        self.RETURN_COORDS = (self.GAME_REGION[2] / 2, self.GAME_REGION[3] / 2)

        threading.Thread(target=self.lockMouse, name="MouseLock", daemon=True).start()

    def lockMouse(self):
        log.info("Mouse has been locked down.")
        while True:
            # print("Doing stuff.")
            pos = pyautogui.position()
            if pos[0] < self.GAME_REGION[0] or pos[1] < self.GAME_REGION[1] or pos[0] > self.GAME_REGION[2] or pos[1] > \
                    self.GAME_REGION[3]:
                pyautogui.moveTo(self.RETURN_COORDS)
                log.warning("Mouse was out of bounds and was rebounded.")
            if self.sentinel is True:
                return
            sleep(0.1)
