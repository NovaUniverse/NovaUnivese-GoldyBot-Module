from __future__ import annotations
from typing import List
import datetime
import asyncio
import dateparser

import GoldyBot

MODULE_NAME = "TOURNAMENT"

client:GoldyBot.nextcord.Client = GoldyBot.cache.main_cache_dict["client"]

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
    """Represents a mcf tournament that can be crated in the database and many more things."""
    def __init__(self, mcf_database:GoldyBot.Database, mcf_date:str, mcf_time:str, max_players:str):
        self.mcf_database = mcf_database

        self.mcf_date = mcf_date
        self.mcf_time = mcf_time
        self.max_players_ = max_players

        self.mcf_was_created = False

    async def init(self):
        # Asyncronous way to run this shit.
        if not await self.tournament_exist:
            # Creates tournament in database if it's not there already.
            await self.create()

        self.tournament_data = await self.get_all_collections()
        super().__init__(self.tournament_data)

    async def create(self):
        """Creates the tournament in a database"""
        date = dateparser.parse(self.mcf_date + " " + self.mcf_time, 
            date_formats=["%d/%m/%Y %H:%M", "%Y/%m/%d %H:%M"])

        await self.mcf_database.create_collection(self.mcf_date, {"_id": 0, 
            "date": date.timestamp(),
            "max_players": int(self.max_players_)
        })

        self.mcf_was_created = True

        GoldyBot.log("info_4", f"[{MODULE_NAME}] MCF Tournament created for '{date.date()}'.")

    @property
    def was_created(self):
        return self.mcf_was_created

    @property
    async def tournament_exist(self):
        """Checks if the tournament exist in the database."""
        print("dfdfd")
        if self.mcf_date in await self.mcf_database.list_collection_names():
            return True
        else:
            return False

    @property
    async def free_team(self) -> str:
        """Finds a free team with no players that a player can be assigned to. If all teams have a player, a team with a player that has no teammate picked will be returned instead."""
        teams_list = []
        for team in range(1, self.max_players):
            team_data = await self.mcf_database.find(self.mcf_date, query={"team": f"{team}"}, key="team")
            teams_list.append(team_data)

            if team_data == []:
                # This team is empty.
                return f"{team}"

        # Find a team with a player that hasn't yet chosen a teammate.
        half_empty_teams_list = []
        team:list
        count = 0
        for team in teams_list:
            count += 1

            if len(team) == 1:
                half_empty_teams_list.append(team)

                if team[0]["teammate_discord_id"] == None:
                    return f"{count}"

            #TODO: #1 Finish free team propery.
        

    async def add_player(self, minecraft_ign:str, player_discord_id:int, player_teammate_discord_id:int | None):
        """Adds player to tournament."""
        await self.mcf_database.insert(self.mcf_date, {"_id"})

        pass

    async def get_all_collections(self):
        print("OwO!")
        return await self.mcf_database.find_all(self.mcf_date)