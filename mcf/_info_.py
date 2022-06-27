from __future__ import annotations
from typing import List
import GoldyBot
import datetime

from . import _tournament_

class TournamentInfo():
    def __init__(self):
        database:GoldyBot.Database = GoldyBot.cache.main_cache_dict["database"]
        self.mcf_database = database.new_instance("mcf_data")

    async def get_all_mcfs(self) -> List[_tournament_.MCFTournament]:
        """Get's and returns every mcf tournament in the database."""
        
        mcf_tournament_list = []
        list_of_mcfs = await self.mcf_database.list_collection_names()

        for mcf in list_of_mcfs:
            mcf_data = await self.mcf_database.find_all(mcf)

            mcf_tournament_list.append(_tournament_.MCFTournament(self.mcf_database, tournament_data=mcf_data))

        return mcf_tournament_list

    async def get_latest_mcf(self) -> _tournament_.MCFTournament | None:
        """Returns the lastest available mcf tournament to join, returns none if all mcfs have finished."""
        mcf_date_dict = {}
        for mcf in await self.get_all_mcfs():
            if mcf.date.timestamp() > datetime.datetime.now().timestamp():
                mcf_date_dict[mcf.date.timestamp()] = mcf

        try:
            return list(reversed(sorted(mcf_date_dict.items())))[0][1]
        except IndexError:
            return None # There are no mcfs available to join.

        