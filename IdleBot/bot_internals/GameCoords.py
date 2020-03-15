from win32api import GetSystemMetrics
from bot_internals.BotLog import log
from bot_internals.DatabaseManager import database

class GameCoords:
    def __init__(self):
        # SETUP VOLATILE VARIABLES FOR COORDS
        self.game_region = None
        self.guardian_click_coords = None
        self.upgrade_coords = None
        self.close_coords = None
        self.small_close_coords = None
        self.big_close_coords = None
        self.guild_coords = None
        self.guild_expeditions_coords = None
        self.town_coords = None
        self.back_arrow_coords = None
        self.upgrades_button_coords = None
        self.temple_of_eternals_coords = None
        self.class_coords = {}
        self.party_coords = None
        self.exotic_merchant_coords = None
        self.map_coords = None
        self.pause_length = 0.5

        self.getGameRegion()
        self.setupCoordinates()

    def getGameRegion(self):
        # Calculate the game region based on screen resolution.
        sWidth, sHeight = GetSystemMetrics(0), GetSystemMetrics(1)
        self.game_region = (0, 0, sWidth, sHeight)
        log.info("Program Start\n\n")
        log.info(f"Screen resolution detected as: {sWidth}x{sHeight}")

    def relative_coords(self, x=None, y=None, w=None, h=None):
        if x:
            newX = round(x * self.game_region[2] / 1920)
            coords = newX
        if y:
            newY = round(y * self.game_region[3] / 1080)
            coords = (newX, newY)
        if w:
            newW = round(w * self.game_region[2] / 1920)
            coords = (newX, newY, newW)
        if h:
            newH = round(h * self.game_region[3] / 1080)
            coords = (newX, newY, newW, newH)
        return coords

    def setupCoordinates(self):
        self.upgrade_coords = (self.relative_coords(1840, 660))
        self.guardian_click_coords = (self.game_region[2] / 2, self.game_region[3] / 2)
        self.small_close_coords = (self.relative_coords(1875, 100))
        self.big_close_coords = (self.relative_coords(1820, 75))
        self.guild_expeditions_coords = (self.relative_coords(175, 385))
        self.guild_coords = (self.relative_coords(1520, 205))
        self.town_coords = (self.relative_coords(1845, 265))
        self.back_arrow_coords = (self.relative_coords(690, 40))
        self.upgrades_button_coords = (self.relative_coords(1605, 1020))
        self.temple_of_eternals_coords = (self.relative_coords(915, 250))
        self.party_coords = (self.relative_coords(1845, 520))
        self.exotic_merchant_coords = (self.relative_coords(1445, 735))
        self.map_coords = (self.relative_coords(1840, 395))

        self.class_coords = {"ranger": (round(0.8672 * self.game_region[2]), round(0.5417 * self.game_region[3])),
                             "mage": (round(0.8698 * self.game_region[2]), round(0.3565 * self.game_region[3])),
                             "tank": (round(0.7708 * self.game_region[2]), round(0.3565 * self.game_region[3])),
                             "warrior": (round(0.7708 * self.game_region[2]), round(0.5444 * self.game_region[3])),
                             "priest": (round(0.7708 * self.game_region[2]), round(0.7269 * self.game_region[3])),
                             "rogue": (round(0.8698 * self.game_region[2]), round(0.7269 * self.game_region[3]))}


