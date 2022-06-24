from typing import List
import GoldyBot
import datetime

from . import _tournament_

class TournamentInfo():
    def __init__(self):
        database:GoldyBot.Database = GoldyBot.cache.main_cache_dict["database"]
        self.mcf_database = database.new_instance("mcf_data")

    async def get_all_mcfs(self) -> List[_tournament_.BasicMCFTournament]:
        """Get's and returns every mcf tournament in the database."""
        
        mcf_tournament_list = []
        list_of_mcfs = await self.mcf_database.list_collection_names()

        for mcf in list_of_mcfs:
            mcf_data = await self.mcf_database.find_all(mcf)

            mcf_tournament_list.append(_tournament_.BasicMCFTournament(tournament_data=mcf_data))

        return mcf_tournament_list