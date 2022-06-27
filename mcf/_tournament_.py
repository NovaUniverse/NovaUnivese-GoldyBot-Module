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

class Tournament():
    """Represents a mcf tournament that can be crated in the database and many more things."""
    def __init__(self, database:GoldyBot.Database, date:str=None, time:str=None, max_players:int=24, tournament_data=[], dont_create:bool=False):
        self.tournament_database = database
        self.tournament_data = tournament_data

        self.date_ = date
        self.time_ = time
        self.max_players_ = max_players
        
        self.dont_create_ = dont_create

        self.was_created_ = False

    async def init(self):
        """Asyncronous way to run this shit."""
        if not await self.tournament_exist:
            if self.dont_create_ == False:
                # Creates tournament in database if it's not there already.
                await self.create()

        if self.tournament_data == []:
            self.tournament_data = await self.get_all_docs()
            super().__init__(self.tournament_data)

    async def create(self):
        """Creates the tournament in a database"""
        date = self.date

        await self.tournament_database.create_collection(date.date(), {"_id": 0, 
            "date": date.timestamp(),
            "max_players": int(self.max_players)
        })

        self.mcf_was_created = True

        GoldyBot.log("info_4", f"[{MODULE_NAME}] MCF Tournament created for '{date.date()}'.")

    async def delete(self):
        """Deletes the tournament in the database"""
        await self.tournament_database.delete_collection(self.date.date())

        GoldyBot.log("info_4", f"[{MODULE_NAME}] The MCF Tournament for '{self.date.date()}' was deleted!")

        return True

    @property
    def date(self):
        """Returns the date the mcf tournament will be hosted."""
        if not self.date_ == None:
            if not self.time_ == None:
                return GoldyBot.utility.datetime.user_input.get_time_and_date(f"{self.date_} {self.time_}")

        try: 
            return datetime.datetime.fromtimestamp(self.tournament_data[0]["date"])
        except: 
            raise GoldyBot.errors.GoldyBotError("Tournament class must include either params ``date`` and ``time`` or ``tournament_data``!")

    @property
    def max_players(self) -> int:
        """Returns the max amount of players allowed in this tournament."""
        try:
            return self.tournament_data[0]["max_players"]
        except KeyError:
            return self.max_players_

    @property
    def was_created(self):
        """Returns true or false if the tournament was just created."""
        return self.was_created_

    @property
    async def tournament_exist(self):
        """Checks if the tournament exist in the database."""
        if self.tournament_data == []:
            if self.date.date() in await self.tournament_database.list_collection_names():
                return True
            else:
                return False
        else:
            return True

    async def get_all_docs(self):
        return await self.tournament_database.find_all(self.date.date())

class MCFTournament(Tournament):
    def __init__(self, mcf_database: GoldyBot.Database, mcf_date: str=None, mcf_time: str=None, max_players: str=24, tournament_data=[], dont_create: bool = False):
        super().__init__(mcf_database, mcf_date, mcf_time, max_players, tournament_data, dont_create)

    @property
    async def free_team(self, teammate=None) -> str:
        """Finds a free team with no players that a player can be assigned to. If all teams have a player, a team with a player that has no teammate picked will be returned instead."""
        teams_list = []
        for team in range(1, self.max_players):
            team_data = await self.tournament_database.find(self.date.date(), query={"team": f"{team}"}, key="team")
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
        """Adds player to the mcf tournament."""
        await self.tournament_database.insert(self.date.date(), 
            {
                "_id": player.member_id,
                "mc_ign": player.mc_ign
            })

    async def remove_player(self, player:MCFPlayer):
        """Removes player from the mcf tournament."""
        await self.tournament_database.remove(self.date.date(), 
            {
                "_id": player.member_id,
                "mc_ign": player.mc_ign
            })