#! python3
import os
import shelve
from time import time


class DatabaseManager:
    def __init__(self):

        self.database = shelve.open(os.getenv('LOCALAPPDATA') + "\\Firestone Bot\\data", flag='c', writeback=True)

        # SETUP VARIABLES FOR DEBUGGING
        self.ocr_fail_count = 0
        self.ocr_succeed_count = 0
        self.ocr_f_pct = 0
        self.ocr_s_pct = 0

        # SETUP VARIABLES WE'LL NEED TO REMEMBER
        self.GUILD_MISSION_TIME_LEFT = time() - 5
        self.PRESTIGE_CHECK_TIME = time() - 5
        self.UPGRADES_LOWERED = False
        self.FRESH_START = False
        self.BOSS_FAILED = False
        self.OCR_IMAGE = os.getenv('LOCALAPPDATA') + "/Firestone Bot/OCR/ss.png"
        self.ACTIVE_MISSIONS = 1
        self.MAP_TROOPS = 0

        self._define_values(self.database)

    def _define_values(self, database):
        if "ocr_fail_count" not in self.database.keys():
            self.database["ocr_fail_count"] = self.ocr_fail_count
        elif "ocr_fail_count" in self.database.keys():
            self.ocr_fail_count = self.database['ocr_fail_count']

        if "ocr_succeed_count" not in self.database.keys():
            self.database["ocr_succeed_count"] = self.ocr_succeed_count
        elif "ocr_succeed_count" in self.database.keys():
            self.ocr_succeed_count = self.database['ocr_succeed_count']

        if "ocr_f_pct" not in self.database.keys():
            self.database["ocr_f_pct"] = self.ocr_f_pct
        elif "ocr_f_pct" in self.database.keys():
            self.ocr_f_pct = self.database['ocr_f_pct']

        if "ocr_s_pct" not in self.database.keys():
            self.database["ocr_s_pct"] = self.ocr_s_pct
        elif "ocr_s_pct" in self.database.keys():
            self.ocr_s_pct = self.database['ocr_s_pct']

        if "GUILD_MISSION_TIME_LEFT" not in self.database.keys():
            self.database["GUILD_MISSION_TIME_LEFT"] = self.GUILD_MISSION_TIME_LEFT
        elif "GUILD_MISSION_TIME_LEFT" in self.database.keys():
            self.GUILD_MISSION_TIME_LEFT = self.database['GUILD_MISSION_TIME_LEFT']

        if "PRESTIGE_CHECK_TIME" not in self.database.keys():
            self.database["PRESTIGE_CHECK_TIME"] = self.PRESTIGE_CHECK_TIME
        elif "PRESTIGE_CHECK_TIME" in self.database.keys():
            self.PRESTIGE_CHECK_TIME = self.database['PRESTIGE_CHECK_TIME']

        if "UPGRADES_LOWERED" not in self.database.keys():
            self.database["UPGRADES_LOWERED"] = self.UPGRADES_LOWERED
        elif "UPGRADES_LOWERED" in self.database.keys():
            self.UPGRADES_LOWERED = self.database['UPGRADES_LOWERED']

        if "FRESH_START" not in self.database.keys():
            self.database["FRESH_START"] = self.FRESH_START
        elif "FRESH_START" in self.database.keys():
            self.FRESH_START = self.database['FRESH_START']

        if "BOSS_FAILED" not in self.database.keys():
            self.database["BOSS_FAILED"] = self.BOSS_FAILED
        elif "BOSS_FAILED" in self.database.keys():
            self.BOSS_FAILED = self.database['BOSS_FAILED']

        if "OCR_IMAGE" not in self.database.keys():
            self.database["OCR_IMAGE"] = self.OCR_IMAGE
        elif "OCR_IMAGE" in self.database.keys():
            self.OCR_IMAGE = self.database['OCR_IMAGE']

        if "ACTIVE_MISSIONS" not in self.database.keys():
            self.database["ACTIVE_MISSIONS"] = self.ACTIVE_MISSIONS
        elif "ACTIVE_MISSIONS" in self.database.keys():
            self.ACTIVE_MISSIONS = self.database['ACTIVE_MISSIONS']

        if "MAP_TROOPS" not in self.database.keys():
            self.database["MAP_TROOPS"] = self.MAP_TROOPS
        elif "MAP_TROOPS" in self.database.keys():
            self.MAP_TROOPS = self.database['MAP_TROOPS']

        self.database.sync()

    def change_value(self, key, value, diff="set"):
        if diff == "set":
            setattr(self, key, value)
            self.database[key] = value
            self.database.sync()
        if diff == "add":
            setattr(self, key, getattr(self, key) + value)
            self.database[key] = getattr(self, key)
            self.database.sync()
        if diff == "sub":
            setattr(self, key, getattr(self, key) - value)
            self.database[key] = getattr(self, key)
            self.database.sync()
