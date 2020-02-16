import configparser
import os
import sys
import time
from threading import Thread


class ConfigManager:
    def __init__(self):
        # self.config_file = os.path.dirname(__file__) + "/../../bot.ini"
        self.config_file = os.path.expanduser("~") + f"/Documents/Firestone Bot/bot.ini"
        # self.config_file = os.path.join(os.getcwd(), 'bot.ini')
        self.config_last_modified = round(os.path.getmtime(self.config_file))
        self.sentinel = False

        # General options - can be overriden from config
        self.auto_prestige = True
        self.in_guild = True
        self.guardian = "Dragon"
        self.guild_missions = True
        self.farm_gold = True
        self.farm_levels = 5
        self.logging = True

        # Party settings. Can be overriden via config
        self.party_size = 5
        self.party_leader = "Ranger"
        self.party_slot_2 = "Mage"
        self.party_slot_3 = "Warrior"
        self.party_slot_4 = "Tank"
        self.party_slot_5 = "Priest"

        # Load the config. If we can't find it, abort
        if os.path.isfile(self.config_file):
            config = configparser.ConfigParser()
            config.read(self.config_file)
            self._verify_ini(config_file=config)
        else:
            print("Unable to load config file. Ensure bot.ini is in the CWD")
            sys.exit(1)

        self._set_ini_options(config)

        Thread(target=self.reload_ini, name="ConfigMonitor", daemon=True).start()

    def reload_ini(self):
        """
        Check if the config has been updated. If it has, reload it.
        """

        while True:
            if round(os.path.getmtime(self.config_file)) > self.config_last_modified:
                print("Config changes detected. Reloading .ini file")
                config = configparser.ConfigParser()
                config.read(self.config_file)
                self._set_ini_options(config)
                self.config_last_modified = round(os.path.getmtime(self.config_file))
            if self.sentinel is True:
                return
            time.sleep(3)

    def _set_ini_options(self, config):
        """
        Set the optional values found in the ini
        """
        # Load options from config
        if "auto_prestige" in config['OPTIONS']:
            self.in_guild = config['OPTIONS'].getboolean("auto_prestige")
        if "prestige_level" in config['OPTIONS']:
            self.prestige_level = round(float(config['OPTIONS']['prestige_level']), 2)
        if "in_guild" in config['OPTIONS']:
            self.in_guild = config['OPTIONS'].getboolean("in_guild")
        if "guardian" in config['OPTIONS']:
            self.guardian = config['OPTIONS'].getint("guardian")
        if "guild_missions" in config['OPTIONS']:
            self.guild_missions = config['OPTIONS'].getboolean("guild_missions")
        if "farm_gold" in config['OPTIONS']:
            self.farm_gold = config['OPTIONS'].getboolean("farm_gold")
        if "farm_levels" in config['OPTIONS']:
            self.farm_levels = config['OPTIONS'].getint("farm_levels")

        if "party_size" in config['PARTY']:
            self.party_size = config['PARTY'].getint("party_size")
        if "party_leader" in config['PARTY']:
            self.party_leader = config['PARTY']['party_leader'].lower()
        if "party_slot_2" in config['PARTY']:
            self.party_slot_2 = config['PARTY']['party_slot_2'].lower()
        if "party_slot_3" in config['PARTY']:
            self.party_slot_3 = config['PARTY']['party_slot_3'].lower()
        if "party_slot_4" in config['PARTY']:
            self.party_slot_4 = config['PARTY']['party_slot_4'].lower()
        if "party_slot_5" in config['PARTY']:
            self.party_slot_5 = config['PARTY']['party_slot_5'].lower()

    def _verify_ini(self, config_file=None):
        """
        Make sure all required fields are in the config file. If they aren't, abort.
        """

        general_values = ["auto_prestige", "in_guild", "guardian", "guild_missions", "farm_gold", "farm_levels", "prestige_level"]
        party_values = ["party_size", "party_leader", "party_slot_2", "party_slot_3", "party_slot_4", "party_slot_5"]
        party_members = ["ranger", "tank", "mage", "warrior", "priest", "rogue"]
        incorrect_values = []
        missing_values = []

        if not config_file:
            print("No config file supplied. Aborting.")
            raise Exception("No config file supplied. Aborting.")

        for val in general_values:
            if val not in config_file["OPTIONS"]:
                missing_values.append("OPTIONS: " + val)

        for val in party_values:
            if val not in config_file["PARTY"]:
                missing_values.append("PARTY: " + val)

        for val in party_values[1:]:
            val = config_file['PARTY'][val]
            if val.lower() not in party_members:
                incorrect_values.append("PARTY: " + val)

        if missing_values:
            print("Config file is missing required values. \n Missing values:")
            for val in missing_values:
                print(val)
            raise Exception(f"Config file is missing required values: {missing_values}.")

        if incorrect_values:
            print("Config file has unusable values. \n Incorrect values:")
            for val in incorrect_values:
                print(val)
            raise Exception(f"Config file has unusable values: {incorrect_values}.")

        if config_file['OPTIONS'].getboolean("guild_missions"):
            if config_file['OPTIONS'].getboolean("in_guild") is False:
                raise Exception("Config file is set to do guild expeditions, but also says we're not in a guild.")

