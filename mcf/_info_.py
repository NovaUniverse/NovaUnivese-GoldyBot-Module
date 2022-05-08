import GoldyBot
import datetime

class TournamentInfo():
    def __init__(self):
        self.database:GoldyBot.Database = GoldyBot.cache.main_cache_dict["database"]

    @property
    def start_date(self):
        """Returns the date the tournament is planned to start."""
        return datetime.datetime.fromtimestamp(1347517370)