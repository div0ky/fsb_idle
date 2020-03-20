import functools
import os
import sqlite3
import uuid
from sys import platform
from time import time

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

# api_address = 'http://127.0.0.1:5000'
api_address = 'https://rest.div0ky.com'

@singleton
class DatabaseManager:
    def __init__(self):
        log.info(f'{__name__} has been initialized.')
        if platform == "linux" or platform == "linux2":
            log.debug("We're using Linux")
        elif platform == "darwin":
            log.debug("We're on MacOS")
            self.connection = sqlite3.connect(os.path.expanduser('~/Documents/Firestone Bot/memory.db'), check_same_thread=False)
            self.ocr_image = os.path.expanduser('~/Documents/Firestone Bot/ss.png')
        elif platform == "win32":
            log.debug("We appear to be on a Windows OS")
            self.connection = sqlite3.connect(os.getenv('LOCALAPPDATA') + "\\Firestone Bot\\memory.db", check_same_thread=False)
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
        self.activated = False
        self.token = None
        self.launch_progress = 0
        self.launch_running = True
        self.running = True
        self.paused = True
        self.launch_text = 'Authenticating...'
        self.launch_show_window = True
        self.updater_finished = False
        self.license_key_needed = False

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
        self.map_nodes = "(393, 350), (620, 425), (265, 635), (245, 960), (590, 772), (715, 735), (800, 975),(875, 875), (1000, 640), (1190, 640), (1270, 795), (1285, 485), (1578, 540), (1578, 365),(410, 725), (815, 775), (1040, 410), (1375, 350), (1570, 365), (1460, 800), (1300, 985),(760, 565), (830, 690), (875, 555), (1440, 645), (1440, 910), (1560, 980), (830, 395),(465, 445), (1550, 740), (1290, 688)"

        """
        declare user configurable options
        """
        # declare update channel
        self.channel = 'Stable'

        # declare party variables
        self.heroes = None
        self.guardians = None
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

        # declare stats
        self.total_chests_opened = 0
        self.total_clicks = 0
        self.total_daily_checkins = 0
        self.total_guardian_trainings = 0
        self.total_guild_expeditions = 0
        self.total_map_missions = 0
        self.total_prestiges = 0
        self.total_restarts = 0
        self.total_runtime = 0
        self.total_stages_farmed = 0
        self.total_tavern_cards = 0
        self.total_upgrades_purchased = 0

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
            log.debug("Created table 'config' in database")

        self.c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='stats'")
        if self.c.fetchone()[0] ==1:
            log.debug('Stats table exists in database')
        else:
            self.c.execute("CREATE TABLE stats(stat UNIQUE, value TEXT)")
            self.connection.commit()
            log.debug("Created table 'stats' in database")

    def save_option(self, setting, option):
        self.c.execute("INSERT OR REPLACE INTO config VALUES (?,?)", [setting, option])
        self.connection.commit()
        setattr(self, setting, option)
        if setting != 'token':
            log.debug(f"Saving '{setting}' to the database as '{option}'")
        return

    def read_option(self, setting):
        for row in self.c.execute("SELECT option FROM config WHERE setting=?", [setting]):
            variable = row[0]
            # setattr(self, setting, variable)
            break
        else:
            variable = False
        if setting != 'token':
            log.debug(f"Read '{setting}' from the database: '{variable}'")
        return variable

    def save_stat(self, stat, value):
        self.c.execute("INSERT OR REPLACE INTO stats VALUES (?,?)", [stat, value])
        self.connection.commit()
        setattr(self, stat, value)
        log.debug(f"Saving '{stat}' to the database as '{value}'")
        return

    def read_stat(self, stat):
        for row in self.c.execute("SELECT value FROM stats WHERE stat=?", [stat]):
            variable = row[0]
            # setattr(self, setting, variable)
            break
        else:
            variable = False
        log.debug(f"Read '{stat}' from the database: '{variable}'")
        return variable

    def _init_values(self):

        # email
        option = self.read_option('email')
        if option:
            self.email = str(option)

        # token
        option = self.read_option('token')
        if option:
            self.token = str(option)
        else:
            self.save_option('token', self.token)

        # map nodes
        option = self.read_option('map_nodes')
        if option:
            self.map_nodes = str(option)
        else:
            self.save_option('map_nodes', self.map_nodes)

        # activated
        option = self.read_option('activated')
        if option:
            self.activated = bool(option)
        else:
            self.save_option('activated', self.activated)

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
            self.heroes = sorted([x for x in str(option).split(',')])
        else:
            self.heroes = sorted(['Talia', 'Boris', 'Asmondai', 'Burt', 'Muriel', 'Astrid', 'Ina', 'Fini', 'Solaine','Benedictus', 'Blaze', 'Luana', 'Valerius'])

        # guardians
        option = self.read_option('guardians')
        if option:
            self.guardians = sorted([x for x in str(option).split(',')])
        else:
            self.guardians = sorted(['Fairy', 'Dragon'])

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

        """
        Handle initial stats entries
        """

        # total prestiges
        option = self.read_stat('total_prestiges')
        if option:
            self.total_prestiges = int(option)
        else:
            self.save_stat('total_prestiges', self.total_prestiges)

        # total map missions
        option = self.read_stat('total_map_missions')
        if option:
            self.total_map_missions = int(option)
        else:
            self.save_stat('total_map_missions', self.total_map_missions)

        # total guild expeditions
        option = self.read_stat('total_guild_expeditions')
        if option:
            self.total_guild_expeditions = int(option)
        else:
            self.save_stat('total_guild_expeditions', self.total_guild_expeditions)

        # total chests opened
        option = self.read_stat('total_chests_opened')
        if option:
            self.total_chests_opened = int(option)
        else:
            self.save_stat('total_chests_opened', self.total_chests_opened)

        # total guardian trainings
        option = self.read_stat('total_guardian_trainings')
        if option:
            self.total_guardian_trainings = int(option)
        else:
            self.save_stat('total_guardian_trainings', self.total_guardian_trainings)

        # total stages farmed
        option = self.read_stat('total_stages_farmed')
        if option:
            self.total_stages_farmed = int(option)
        else:
            self.save_stat('total_stages_farmed', self.total_stages_farmed)

        # total tavern cards
        option = self.read_stat('total_tavern_cards')
        if option:
            self.total_tavern_cards = int(option)
        else:
            self.save_stat('total_tavern_cards', self.total_tavern_cards)

        # total restarts
        stat = self.read_stat('total_restarts')
        if stat:
            self.total_restarts = int(stat)
        else:
            self.save_stat('total_restarts', self.total_restarts)

        # total daily checkins
        stat = self.read_stat('total_daily_checkins')
        if stat:
            self.total_daily_checkins = int(stat)
        else:
            self.save_stat('total_daily_checkins', self.total_daily_checkins)

        # total clicks
        stat = self.read_stat('total_clicks')
        if stat:
            self.total_clicks = int(stat)
        else:
            self.save_stat('total_clicks', self.total_clicks)

        # total upgrades purchased
        stat = self.read_stat('total_upgrades_purchased')
        if stat:
            self.total_upgrades_purchased = int(stat)
        else:
            self.save_stat('total_upgrades_purchased', self.total_upgrades_purchased)

        # total runtime
        stat = self.read_stat('total_runtime')
        if stat:
            self.total_runtime = float(stat)
        else:
            self.save_stat('total_runtime', self.total_runtime)


database = DatabaseManager()

if __name__ == "__main__":
    database = DatabaseManager()
