#! python3
"""

Firestone Idle RPG Bot

A bot to handle auto upgrading party members and such as it progresses.

"""
from bot_internals.BotLog import log

class IdleBot:
    def __init__(self):
        log.info('Test')
        log.debug('Test')

if __name__ == "__main__":
    bot = IdleBot()
