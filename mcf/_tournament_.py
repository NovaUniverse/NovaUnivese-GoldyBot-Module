from typing import List
import datetime
import asyncio

import GoldyBot

loop = asyncio.get_event_loop()

class BasicMCFTournament():
    """Represents an mcf tournament that is already created and also the base class."""

    def __init__(self, tournament_data:List[dict]):
        self.info = tournament_data[0]
        self.players = tournament_data[1:]

    @property
    def date(self):
        """Returns the date the mcf tournament will be hosted."""
        return datetime.datetime.fromtimestamp(self.info["date"])

    @property
    def max_players(self) -> int:
        """Returns the max amount of players allowed in this tournament."""
        return self.info["max_players"]

class MCFTournament(BasicMCFTournament):
    def __init__(self, mcf_database:GoldyBot.Database, collection_name:str):
        tournament_data = loop.run_until_complete(mcf_database.find_all(collection_name))
        super().__init__(tournament_data)