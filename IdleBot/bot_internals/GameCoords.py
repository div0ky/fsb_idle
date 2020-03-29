from .BotLog import log
from .DatabaseManager import database


class GameCoords:
    def __init__(self):
        log.info('Figuring out screen coordinates')
        # SETUP VOLATILE VARIABLES FOR COORDS
        self.game_region = None
        self.guardian_click_coords = None
        self.upgrade_button = None
        self.close_coords = None
        self.small_close_coords = None
        self.big_close_coords = None
        self.guild_coords = None
        self.guild_expeditions_coords = None
        self.town_coords = None
        self.back_arrow_coords = None
        self.upgrade_progression_button = None
        self.temple_of_eternals_coords = None
        self.inventory = None
        self.chests_tab = None
        self.magic_quarter = None
        self.big_chest = None
        self.open_chest = None
        self.hero_coords = {}
        self.party_coords = None
        self.exotic_merchant_coords = None
        self.map_coords = None
        self.pause_length = 0.5

        self.get_game_region()
        self.setup_coordinates()

    """
    After much debate, the game is hard-coded for 1920x1080 resolution for now.
    I have no current plans to support other resolutions.
    """
    def get_game_region(self):  # Calculate the game region based on screen resolution.
        screen_width, screen_height = (1920, 1080)
        self.game_region = (0, 0, screen_width, screen_height)
        # log.info(f"Screen resolution detected as: {screen_width}x{screen_height}")

    def relative_coords(self, x=None, y=None, w=None, h=None):
        if x:
            new_x = round(x * self.game_region[2] / 1920)
            coords = new_x
        if y:
            new_y = round(y * self.game_region[3] / 1080)
            coords = (new_x, new_y)
        if w:
            new_width = round(w * self.game_region[2] / 1920)
            coords = (new_x, new_y, new_width)
        if h:
            new_height = round(h * self.game_region[3] / 1080)
            coords = (new_x, new_y, new_width, new_height)
        return coords

    def setup_coordinates(self):
        self.upgrade_button = (self.relative_coords(1840, 660))
        self.guardian_click_coords = (self.game_region[2] / 2, self.game_region[3] / 2)
        self.small_close_coords = (self.relative_coords(1875, 100))
        self.big_close_coords = (self.relative_coords(1820, 75))
        self.guild_expeditions_coords = (self.relative_coords(175, 385))
        self.guild_coords = (self.relative_coords(1520, 205))
        self.town_coords = (self.relative_coords(1845, 265))
        self.back_arrow_coords = (self.relative_coords(690, 40))
        self.upgrade_progression_button = (self.relative_coords(1605, 1020))
        self.temple_of_eternals_coords = (self.relative_coords(915, 250))
        self.magic_quarter = (600, 250)
        self.inventory = (1840, 800)
        self.chests_tab = (1785, 200)
        self.big_chest = (500, 325)
        self.open_chest = (500, 540)
        self.party_coords = (self.relative_coords(1845, 520))
        self.exotic_merchant_coords = (self.relative_coords(1445, 735))
        self.map_coords = (self.relative_coords(1840, 395))

        for hero in database.heroes:
            setattr(self, f"hero_{hero}", None)


game_coords = GameCoords()
