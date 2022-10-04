from __future__ import annotations

import GoldyBot
from datetime import datetime

class TournamentData():
    """Class containing all info to create a tournament."""
    def __init__(self, database:GoldyBot.Database, time_and_date:datetime, max_players:int):
        self.database_ = database

        self.time_and_date_ = time_and_date
        self.max_players_ = max_players

    @property
    def database(self):
        return self.database_

    @property
    def time_and_date(self):
        return self.time_and_date_

    @property
    def max_players(self):
        return self.max_players_