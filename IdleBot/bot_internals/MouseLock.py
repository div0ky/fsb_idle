import threading
from time import sleep

import pyautogui


class MouseLock:
    def __init__(self):
        self.sentinel = False
        self.sWidth, self.sHeight = pyautogui.size()
        self.GAME_REGION = (0, 0, self.sWidth, self.sHeight)
        self.RETURN_COORDS = (self.GAME_REGION[2] / 2, self.GAME_REGION[3] / 2)

        threading.Thread(target=self.lockMouse, name="MouseLock", daemon=True).start()

    def lockMouse(self):
        print("Locking...")
        while True:
            # print("Doing stuff.")
            pos = pyautogui.position()
            if pos[0] < self.GAME_REGION[0] or pos[1] < self.GAME_REGION[1] or pos[0] > self.GAME_REGION[2] or pos[1] > \
                    self.GAME_REGION[3]:
                pyautogui.moveTo(self.RETURN_COORDS)
                print("Mouse was out of bounds and was rebounded.")
            if self.sentinel is True:
                return
            sleep(0.1)
