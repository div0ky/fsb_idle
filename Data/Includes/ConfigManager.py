import os
import sys
import configparser
import time
import threading


class ConfigManager:
    def __init__(self):
        self.config_file = os.path.join(os.getcwd(), 'bot.ini')
        self.config_last_modified = round(os.path.getmtime(self.config_file))

        # General options - can be overriden from config
        self.auto_prestige = True
        self.in_guild = True
        self.guardian = "Dragon"

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

        threading.Thread(target=self.reload_ini, name="ConfigMonitor").start()

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
            time.sleep(3)

    def _set_ini_options(self, config):
        """
        Set the optional values found in the ini
        """
        # Load options from config
        if "in_guild" in config['OPTIONS']:
            self.in_guild = config['OPTIONS'].getboolean("in_guild")

    def _verify_ini(self, config_file=None):
        """
        Make sure all required fields are in the config file. If they aren't, abort.
        """

        general_values = ["auto_prestige", "in_guild", "guardian"]
        party_values = ["party_size", "party_leader", "party_slot_2", "party_slot_3", "party_slot_4", "party_slot_5"]
        missing_values = []

        if not config_file:
            print("No config file supplied. Aborting.")
            sys.exit(1)

        for val in general_values:
            if val not in config_file["OPTIONS"]:
                missing_values.append("OPTIONS: " + val)

        for val in party_values:
            if val not in config_file["PARTY"]:
                missing_values.append("PARTY: " + val)

        if missing_values:
            print("Config file is missing required values. \n Missing values:")
            for val in missing_values:
                print(val)
            sys.exit(1)
