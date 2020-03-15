import sqlite3
import os
from sys import platform
import uuid
from time import time
import functools

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
            print("We're using Linux")
        elif platform == "darwin":
            print("We're on MacOS")
            self.connection = sqlite3.connect(os.path.expanduser('~/Documents/Firestone Bot/memory.db'))
            self.ocr_image = os.path.expanduser('~/Documents/Firestone Bot/ss.png')
        elif platform == "win32":
            print("We're on Windows")
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
        self.farm_levels = 5
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
            print("Table exists.")
        else:
            self.c.execute("CREATE TABLE config(setting UNIQUE, option TEXT)")
            print("Created tables.")
            self.connection.commit()
            print("Commited changes to database.")

    def save_option(self, setting, option):
        self.c.execute("INSERT OR REPLACE INTO config VALUES (?,?)", [setting, option])
        self.connection.commit()
        setattr(self, setting, option)

    def read_option(self, setting):
        for row in self.c.execute("SELECT option FROM config WHERE setting=?", [setting]):
            variable = row[0]
            # setattr(self, setting, variable)
            break
        else:
            variable = False
        return variable

    def _init_values(self):
        # ocr_fail_count
        if self.read_option('ocr_fail_count'):
            self.ocr_fail_count = int(self.read_option('ocr_fail_count'))
        else:
            self.save_option('ocr_fail_count', self.ocr_fail_count)

        # ocr_succeed_count
        if self.read_option('ocr_succeed_count'):
            self.ocr_succeed_count = int(self.read_option('ocr_succeed_count'))
        else:
            self.save_option('ocr_succeed_count', self.ocr_succeed_count)

        # ocr_f_pct
        if self.read_option('ocr_f_pct'):
            self.ocr_f_pct = float(self.read_option('ocr_f_pct'))
        else:
            self.save_option('ocr_f_pct', self.ocr_f_pct)

        # public_id
        if self.read_option('public_id'):
            self.public_id = str(self.read_option('public_id'))
        else:
            self.save_option('public_id', str(uuid.uuid4()))

        # license_key
        if self.read_option('license_key'):
            self.license_key = str(self.read_option('license_key'))

        # ocr_s_pct
        if self.read_option('ocr_s_pct'):
            self.ocr_s_pct = float(self.read_option('ocr_s_pct'))
        else:
            self.save_option('ocr_s_pct', self.ocr_s_pct)

        # guild_mission_time_left
        if self.read_option('guild_mission_time_left'):
            self.guild_mission_time_left = float(self.read_option('guild_mission_time_left'))
        else:
            self.save_option('guild_mission_time_left', self.guild_mission_time_left)

        # prestige_check_time
        if self.read_option('prestige_check_time'):
            self.prestige_check_time = float(self.read_option('prestige_check_time'))
        else:
            self.save_option('prestige_check_time', self.prestige_check_time)

        # upgrade_status
        if self.read_option('upgrade_status'):
            self.upgrade_status = self.read_option('upgrade_status')
        else:
            self.save_option('upgrade_status', self.upgrade_status)

        # fresh_start
        if self.read_option('fresh_start'):
            self.fresh_start = bool(self.read_option('fresh_start'))
        else:
            self.save_option('fresh_start', self.fresh_start)

        # boss_failed
        if self.read_option('boss_failed'):
            self.boss_failed = bool(self.read_option('boss_failed'))
        else:
            self.save_option('boss_failed', self.boss_failed)

        # ocr_image
        if self.read_option('ocr_image'):
            self.ocr_image = self.read_option('ocr_image')
        else:
            self.save_option('ocr_image', self.ocr_image)

        # active_missions
        if self.read_option('active_missions'):
            self.active_missions = int(self.read_option('active_missions'))
        else:
            self.save_option('active_missions', self.active_missions)

        # map_troops
        if self.read_option('map_troops'):
            self.map_troops = int(self.read_option('map_troops'))
        else:
            self.save_option('map_troops', self.map_troops)

        # heroes
        if self.read_option('heroes'):
            self.heroes = [x for x in self.read_option('heroes').split(',')]
        else:
            self.heroes = ['Talia','Boris','Asmondai','Burt','Muriel','Astrid','Ina','Fini','Solaine','Benedictus','Blaze','Luana','Valerius']

        # auto_prestige
        if self.read_option('auto_prestige'):
            self.auto_prestige = self.read_option('auto_prestige')
        else:
            self.save_option('auto_prestige', self.auto_prestige)

        # prestige_level
        if self.read_option('prestige_level'):
            self.prestige_level = self.read_option('prestige_level')
        else:
            self.save_option('prestige_level', self.prestige_level)

        # in_guild
        if self.read_option('in_guild'):
            self.in_guild = self.read_option('in_guild')
        else:
            self.save_option('in_guild', self.in_guild)

        # guardian
        if self.read_option('guardian'):
            self.guardian = self.read_option('guardian')
        else:
            self.save_option('guardian', self.guardian)

        # guild_missions
        if self.read_option('guild_missions'):
            self.guild_missions = self.read_option('guild_missions')
        else:
            self.save_option('guild_missions', self.guild_missions)

        # farm_gold
        if self.read_option('farm_gold'):
            self.farm_gold = self.read_option('farm_gold')
        else:
            self.save_option('farm_gold', self.farm_gold)

        # farm_levels
        if self.read_option('farm_levels'):
            self.farm_levels = self.read_option('farm_levels')
        else:
            self.save_option('farm_levels', self.farm_levels)

        # update channel
        if self.read_option('channel'):
            self.channel = self.read_option('channel')
        else:
            self.save_option('channel', self.channel)

        # party_size
        if self.read_option('party_size'):
            self.party_size = self.read_option('party_size')
        else:
            self.save_option('party_size', self.party_size)

        # party_slot_1
        if self.read_option('party_slot_1'):
            self.party_slot_1 = self.read_option('party_slot_1')
        else:
            self.save_option('party_slot_1', self.party_slot_1)

        # party_slot_2
        if self.read_option('party_slot_2'):
            self.party_slot_2 = self.read_option('party_slot_2')
        else:
            self.save_option('party_slot_2', self.party_slot_2)

        # party_slot_3
        if self.read_option('party_slot_3'):
            self.party_slot_3 = self.read_option('party_slot_3')
        else:
            self.save_option('party_slot_3', self.party_slot_3)

        # party_slot_4
        if self.read_option('party_slot_4'):
            self.party_slot_4 = self.read_option('party_slot_4')
        else:
            self.save_option('party_slot_4', self.party_slot_4)

        # party_slot_5
        if self.read_option('party_slot_5'):
            self.party_slot_5 = self.read_option('party_slot_5')
        else:
            self.save_option('party_slot_5', self.party_slot_5)

database = DatabaseManager()

if __name__ == "__main__":
    database = DatabaseManager()