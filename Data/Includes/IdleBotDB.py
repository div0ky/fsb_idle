import sqlite3
import os
from sys import platform
from time import time

class IdleBotDB:
    def __init__(self):

        if platform == "linux" or platform == "linux2":
            print("We're using Linux")
        elif platform == "darwin":
            print("We're on MacOS")
            self.connection = sqlite3.connect(os.path.expanduser('~/Documents/Firestone Bot/memory.db'))
            self.OCR_IMAGE = os.path.expanduser('~/Documents/Firestone Bot/ss.png')
        elif platform == "win32":
            print("We're on Windows")
            self.connection = sqlite3.connect(os.getenv('LOCALAPPDATA') + "\\Firestone Bot\\memory.db")
            self.OCR_IMAGE = os.getenv('LOCALAPPDATA') + "\\Firestone Bot\\OCR\\ss.png"

        # self.connection = sqlite3.connect("http://div0ky.com/repo/memory.db")
        self.c = self.connection.cursor()

        # SETUP VARIABLES FOR DEBUGGING
        self.ocr_fail_count = 0
        self.ocr_succeed_count = 0
        self.ocr_f_pct = 0
        self.ocr_s_pct = 0

        # SETUP VARIABLES WE'LL NEED TO REMEMBER
        self.GUILD_MISSION_TIME_LEFT = time() - 5
        self.PRESTIGE_CHECK_TIME = time() - 5
        self.UPGRADES_LOWERED = False
        self.UPGRADES_STATUS = "Milestone"
        self.FRESH_START = False
        self.BOSS_FAILED = False
        self.ACTIVE_MISSIONS = 0
        self.MAP_TROOPS = 0

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
        if self.read_option('ocr_fail_count'):
            self.ocr_fail_count = int(self.read_option('ocr_fail_count'))
        else:
            self.save_option('ocr_fail_count', self.ocr_fail_count)

        if self.read_option('ocr_succeed_count'):
            self.ocr_succeed_count = int(self.read_option('ocr_succeed_count'))
        else:
            self.save_option('ocr_succeed_count', self.ocr_succeed_count)

        if self.read_option('ocr_f_pct'):
            self.ocr_f_pct = float(self.read_option('ocr_f_pct'))
        else:
            self.save_option('ocr_f_pct', self.ocr_f_pct)


        if self.read_option('ocr_s_pct'):
            self.ocr_s_pct = float(self.read_option('ocr_s_pct'))
        else:
            self.save_option('ocr_s_pct', self.ocr_s_pct)


        if self.read_option('GUILD_MISSION_TIME_LEFT'):
            self.GUILD_MISSION_TIME_LEFT = float(self.read_option('GUILD_MISSION_TIME_LEFT'))
        else:
            self.save_option('GUILD_MISSION_TIME_LEFT', self.GUILD_MISSION_TIME_LEFT)

        # PRESTIGE CHECK TIME
        if self.read_option('PRESTIGE_CHECK_TIME'):
            self.PRESTIGE_CHECK_TIME = float(self.read_option('PRESTIGE_CHECK_TIME'))
        else:
            self.save_option('PRESTIGE_CHECK_TIME', self.PRESTIGE_CHECK_TIME)


        if self.read_option('UPGRADES_STATUS'):
            self.UPGRADES_STATUS = self.read_option('UPGRADES_STATUS')
        else:
            self.save_option('UPGRADES_STATUS', self.UPGRADES_STATUS)


        if self.read_option('FRESH_START'):
            self.FRESH_START = bool(self.read_option('FRESH_START'))
        else:
            self.save_option('FRESH_START', self.FRESH_START)


        if self.read_option('BOSS_FAILED'):
            self.BOSS_FAILED = bool(self.read_option('BOSS_FAILED'))
        else:
            self.save_option('BOSS_FAILED', self.BOSS_FAILED)


        if self.read_option('OCR_IMAGE'):
            self.OCR_IMAGE = self.read_option('OCR_IMAGE')
        else:
            self.save_option('OCR_IMAGE', self.OCR_IMAGE)


        if self.read_option('ACTIVE_MISSIONS'):
            self.ACTIVE_MISSIONS = int(self.read_option('ACTIVE_MISSIONS'))
        else:
            self.save_option('ACTIVE_MISSIONS', self.ACTIVE_MISSIONS)


        if self.read_option('MAP_TROOPS'):
            self.MAP_TROOPS = int(self.read_option('MAP_TROOPS'))
        else:
            self.save_option('MAP_TROOPS', self.MAP_TROOPS)


if __name__ == "__main__":
    database = IdleBotDB()