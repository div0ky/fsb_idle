import sqlite3
import os
from sys import platform
import uuid
from time import time
import functools
from .BotLog import log

def singleton(cls):
    # Only ONE instance allowed
    @functools.wraps(cls)
    def wrapper_singleton(*args, **kwargs):
        if not wrapper_singleton.instance:
            wrapper_singleton.instance = cls(*args, **kwargs)
        return wrapper_singleton.instance

    wrapper_singleton.instance = None
    return wrapper_singleton


@singleton
class DatabaseManager:
    def __init__(self):

        if platform == "linux" or platform == "linux2":
            log.debug("We're using Linux")
        elif platform == "darwin":
            log.debug("We're on MacOS")
            self.connection = sqlite3.connect(os.path.expanduser('~/Documents/Firestone Bot/memory.db'))
            self.ocr_image = os.path.expanduser('~/Documents/Firestone Bot/ss.png')
        elif platform == "win32":
            log.debug("We appear to be on a Windows OS")
            self.connection = sqlite3.connect(os.getenv('LOCALAPPDATA') + "\\Firestone Bot\\memory.db")
            self.ocr_image = os.getenv('LOCALAPPDATA') + "\\Firestone Bot\\OCR\\ss.png"

        # self.connection = sqlite3.connect("http://div0ky.com/repo/memory.db")
        self.c = self.connection.cursor()

        """
        declare system parameters
        """
        self.authenticated = False
        self.email = None
        self.license_key = ''
        self.public_id = ''

        """
        declare internal variales
        """
        self.active_missions = 0
        self.boss_failed = False
        self.fresh_start = False
        self.guild_mission_time_left = time() - 5
        self.map_troops = 0
        self.ocr_f_pct = 0
        self.ocr_fail_count = 0
        self.ocr_s_pct = 0
        self.ocr_succeed_count = 0
        self.prestige_check_time = time() - 5
        self.upgrades_lowered = False
        self.upgrade_status = "Milestone"

        """
        declare user configurable options
        """
        # declare update channel
        self.channel = 'Stable'

        # declare party variables
        self.heroes = None
        self.party_size = 5
        self.party_slot_1 = 'Boris'
        self.party_slot_2 = 'Solaine'
        self.party_slot_3 = 'Burt'
        self.party_slot_4 = 'Benedictus'
        self.party_slot_5 = 'Blaze'

        # declare bot function variables
        self.auto_prestige = True
        self.farm_gold = True
        self.farm_levels = 10
        self.guardian = 'Dragon'
        self.guild_missions = True
        self.in_guild = True
        self.prestige_level = 4

        """
        verify that the tables exist and initialize values
        """
        self._verify_tables()
        self._init_values()

    def _verify_tables(self):
        self.c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='config'")
        if self.c.fetchone()[0] == 1:
            log.debug("Config table exists in database")
        else:
            self.c.execute("CREATE TABLE config(setting UNIQUE, option TEXT)")
            log.debug("Config tables weren't found. Created necessary tables.")
            self.connection.commit()
            log.debug("Commited changes to database.")

    def save_option(self, setting, option):
        self.c.execute("INSERT OR REPLACE INTO config VALUES (?,?)", [setting, option])
        self.connection.commit()
        setattr(self, setting, option)
        log.debug(f"Saving '{setting}' to the database as '{option}'")
        return

    def read_option(self, setting):
        for row in self.c.execute("SELECT option FROM config WHERE setting=?", [setting]):
            variable = row[0]
            # setattr(self, setting, variable)
            break
        else:
            variable = False
        log.debug(f"Read '{setting}' from the database: '{variable}'")
        return variable

    def _init_values(self):
        # ocr_fail_count
        option = self.read_option('ocr_fail_count')
        if option:
            self.ocr_fail_count = int(option)
        else:
            self.save_option('ocr_fail_count', self.ocr_fail_count)

        # ocr_succeed_count
        option = self.read_option('ocr_succeed_count')
        if option:
            self.ocr_succeed_count = int(option)
        else:
            self.save_option('ocr_succeed_count', self.ocr_succeed_count)

        # ocr_f_pct
        option = self.read_option('ocr_f_pct')
        if option:
            self.ocr_f_pct = float(option)
        else:
            self.save_option('ocr_f_pct', self.ocr_f_pct)

        # public_id
        option = self.read_option('public_id')
        if option:
            self.public_id = str(option)
        else:
            self.save_option('public_id', str(uuid.uuid4()))

        # license_key
        option = self.read_option('license_key')
        if option:
            self.license_key = str(option)

        # ocr_s_pct
        option = self.read_option('ocr_s_pct')
        if option:
            self.ocr_s_pct = float(option)
        else:
            self.save_option('ocr_s_pct', self.ocr_s_pct)

        # guild_mission_time_left
        option = self.read_option('guild_mission_time_left')
        if option:
            self.guild_mission_time_left = float(option)
        else:
            self.save_option('guild_mission_time_left', self.guild_mission_time_left)

        # prestige_check_time
        option = self.read_option('prestige_check_time')
        if option:
            self.prestige_check_time = float(option)
        else:
            self.save_option('prestige_check_time', self.prestige_check_time)

        # upgrade_status
        option = self.read_option('upgrade_status')
        if option:
            self.upgrade_status = str(option)
        else:
            self.save_option('upgrade_status', self.upgrade_status)

        # fresh_start
        option = self.read_option('fresh_start')
        if option:
            self.fresh_start = bool(option)
        else:
            self.save_option('fresh_start', self.fresh_start)

        # boss_failed
        option = self.read_option('boss_failed')
        if option:
            self.boss_failed = bool(option)
        else:
            self.save_option('boss_failed', self.boss_failed)

        # ocr_image
        option = self.read_option('ocr_image')
        if option:
            self.ocr_image = str(option)
        else:
            self.save_option('ocr_image', self.ocr_image)

        # active_missions
        option = self.read_option('active_missions')
        if option:
            self.active_missions = int(option)
        else:
            self.save_option('active_missions', self.active_missions)

        # map_troops
        option = self.read_option('map_troops')
        if option:
            self.map_troops = int(option)
        else:
            self.save_option('map_troops', self.map_troops)

        # heroes
        option = self.read_option('heroes')
        if option:
            self.heroes = [x for x in self.read_option('heroes').split(',')]
        else:
            self.heroes = ['Talia', 'Boris', 'Asmondai', 'Burt', 'Muriel', 'Astrid', 'Ina', 'Fini', 'Solaine',
                           'Benedictus', 'Blaze', 'Luana', 'Valerius']

        # auto_prestige
        option = self.read_option('auto_prestige')
        if option:
            self.auto_prestige = bool(option)
        else:
            self.save_option('auto_prestige', self.auto_prestige)

        # prestige_level
        option = self.read_option('prestige_level')
        if option:
            self.prestige_level = int(option)
        else:
            self.save_option('prestige_level', self.prestige_level)

        # in_guild
        option = self.read_option('in_guild')
        if option:
            self.in_guild = bool(option)
        else:
            self.save_option('in_guild', self.in_guild)

        # guardian
        option = self.read_option('guardian')
        if option:
            self.guardian = str(option)
        else:
            self.save_option('guardian', self.guardian)

        # guild_missions
        option = self.read_option('guild_missions')
        if option:
            self.guild_missions = bool(option)
        else:
            self.save_option('guild_missions', self.guild_missions)

        # farm_gold
        option = self.read_option('farm_gold')
        if option:
            self.farm_gold = bool(option)
        else:
            self.save_option('farm_gold', self.farm_gold)

        # farm_levels
        option = self.read_option('farm_levels')
        if option:
            self.farm_levels = int(option)
        else:
            self.save_option('farm_levels', self.farm_levels)

        # update channel
        option = self.read_option('channel')
        if option:
            self.channel = str(option)
        else:
            self.save_option('channel', self.channel)

        # party_size
        option = self.read_option('party_size')
        if option:
            self.party_size = int(option)
        else:
            self.save_option('party_size', self.party_size)

        # party_slot_1
        option = self.read_option('party_slot_1')
        if option:
            self.party_slot_1 = str(option)
        else:
            self.save_option('party_slot_1', self.party_slot_1)

        # party_slot_2
        option = self.read_option('party_slot_2')
        if option:
            self.party_slot_2 = str(option)
        else:
            self.save_option('party_slot_2', self.party_slot_2)

        # party_slot_3
        option = self.read_option('party_slot_3')
        if option:
            self.party_slot_3 = str(option)
        else:
            self.save_option('party_slot_3', self.party_slot_3)

        # party_slot_4
        option = self.read_option('party_slot_4')
        if option:
            self.party_slot_4 = str(option)
        else:
            self.save_option('party_slot_4', self.party_slot_4)

        # party_slot_5
        option = self.read_option('party_slot_5')
        if option:
            self.party_slot_5 = str(option)
        else:
            self.save_option('party_slot_5', self.party_slot_5)


database = DatabaseManager()

if __name__ == "__main__":
    database = DatabaseManager()
