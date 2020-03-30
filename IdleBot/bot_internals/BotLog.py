from logging.handlers import RotatingFileHandler
import logging
import os
import functools
from .version_info import *


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
class BotLog:
    def __init__(self):
        self.log = logging.getLogger('Firestone Idle Bot')
        self.log.setLevel(logging.DEBUG)

        # Create formatters
        file_format = logging.Formatter(
            f'%(asctime)s.%(msecs)03d  |  %(levelname)s  |  %(module)s  |  {full_version}  |  %(message)s',
            datefmt='%Y-%m-%d | %H:%M:%S')
        console_format = logging.Formatter(
            f'%(asctime)s.%(msecs)03d  |  %(levelname)s  |  %(module)s  |  {full_version}  |  %(message)s',
            datefmt='%Y-%m-%d | %H:%M:%S')
        # Create console handler
        c_handler = logging.StreamHandler()
        c_handler.setLevel(logging.DEBUG)
        c_handler.setFormatter(console_format)
        # Create debug handler
        f_handler = RotatingFileHandler(os.path.expanduser("~") + "/Documents/Firestone Idle Bot/Logs/debug.log", maxBytes=10240, backupCount=10)
        f_handler.setLevel(logging.DEBUG)
        f_handler.setFormatter(file_format)
        # Add handlers to the logger
        self.log.addHandler(c_handler)
        self.log.addHandler(f_handler)


log = BotLog().log
