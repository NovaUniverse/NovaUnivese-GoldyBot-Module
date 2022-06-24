from __future__ import annotations
from typing import List
import datetime
import asyncio
import dateparser

import GoldyBot
from mcf._player_ import MCFPlayer

import errors

MODULE_NAME = "TOURNAMENT"

client:GoldyBot.nextcord.Client = GoldyBot.cache.main_cache_dict["client"]

class BasicMCFTournament():
    """Represents an mcf tournament that is already created and also the base class."""

    def __init__(self, tournament_data:List[dict]):
        try:
            self.info = tournament_data[0]
            self.players = tournament_data[1:]
        except IndexError:
            raise errors.TournamentDoesntExistError("Tournament doesn't exist. You'll need to create it first.")

    @property
    def date(self):
        """Returns the date the mcf tournament will be hosted."""
        return datetime.datetime.fromtimestamp(self.info["date"])

    @property
    def max_players(self) -> int:
        """Returns the max amount of players allowed in this tournament."""
        return self.info["max_players"]

    def convert_to_full_class(self):
        # Where I left off
        pass

class MCFTournament(BasicMCFTournament):
    """Represents a mcf tournament that can be crated in the database and many more things."""
    def __init__(self, mcf_database:GoldyBot.Database, mcf_date:str, mcf_time:str, max_players:str, dont_create:bool=False):
        self.mcf_database = mcf_database

        self.mcf_date = mcf_date
        self.mcf_time = mcf_time
        self.max_players_ = max_players
        
        self.dont_create_ = dont_create

        self.mcf_was_created = False

    async def init(self):
        """Asyncronous way to run this shit."""
        if not await self.tournament_exist:
            if self.dont_create_ == False:
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

    async def delete(self):
        """Deletes the tournament in the database"""
        await self.mcf_database.delete_collection(self.mcf_date)

        GoldyBot.log("info_4", f"[{MODULE_NAME}] The MCF Tournament for '{self.mcf_date}' was deleted!")

        return True

    @property
    def was_created(self):
        return self.mcf_was_created

    @property
    async def tournament_exist(self):
        """Checks if the tournament exist in the database."""
        if self.mcf_date in await self.mcf_database.list_collection_names():
            return True
        else:
            return False

    @property
    async def free_team(self, teammate=None) -> str:
        """Finds a free team with no players that a player can be assigned to. If all teams have a player, a team with a player that has no teammate picked will be returned instead."""
        teams_list = []
        for team in range(1, self.max_players):
            team_data = await self.mcf_database.find(self.mcf_date, query={"team": f"{team}"}, key="team")
            teams_list.append(team_data)

            if team_data == []:
                # This team is empty.
                return f"{team}"

        # Find a team with a player that hasn't yet chosen a teammate.
        if teammate == None:
            half_empty_teams_list = []
            team:list
            count = 0

            for team in teams_list:
                count += 1

                if len(team) == 1:
                    half_empty_teams_list.append(team)

                    if team[0]["teammate_discord_id"] == None:
                        return f"{count}"

            # No free teams.
            return None

        else:
            # Not enough space. There's no free team
            return None
        
    async def add_player(self, player:MCFPlayer):
        """Adds player to tournament."""
        await self.mcf_database.insert(self.mcf_date, 
            {
                "_id": player.member_id,
                "mc_ign": player.mc_ign
            })

    async def remove_player(self, player:MCFPlayer):
        """Removes player from tournament."""
        await self.mcf_database.remove(self.mcf_date, 
            {
                "_id": player.member_id,
                "mc_ign": player.mc_ign
            })

    async def get_all_collections(self):
        return await self.mcf_database.find_all(self.mcf_date)