#! python3
"""

Firestone Idle RPG Bot

A bot to handle auto upgrading party members and such as it progresses.

"""
from bot_internals.BotLog import log
from bot_internals.GameCoords import game_coords


class IdleBot:
    def __init__(self):
        log.info(f'{__name__} has been initialized.')


if __name__ == "__main__":
    bot = IdleBot()
