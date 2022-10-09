from __future__ import annotations
from typing import Dict, List

import GoldyBot
from . import TOURNAMENTS_COLLECTION, DELETED_TOURNAMENTS_COLLECTION
from .. import objects

from datetime import datetime

MODULE_NAME = "TOURNAMENT"

class McfDataUtils():
    """Class containing utils to help find tournaments and a lot more in the database."""
    def __init__(self, ctx, database:GoldyBot.Database):
        self.ctx = ctx
        self.database = database

    async def get_latest_tournament(self) -> objects.TournamentData | None:
        """Returns the latest tournament that has not started. Returns 'None' if there are none or all tournaments have passed their start date."""

        all_tournaments = await self.get_all_tournaments()

        try:
            if not datetime.now().timestamp() > all_tournaments[0].time_and_date.timestamp():
                return all_tournaments[0]

            else:
                return None

        except IndexError:
            GoldyBot.log("info", f"[{MODULE_NAME}] There's no tournaments so I'm returning 'None'.")
            return None


    async def get_all_tournaments(self) -> List[objects.TournamentData]:
        """Returns information of every tournament in the 'tournaments' collection."""
        all_tournaments = await self.database.find_all(TOURNAMENTS_COLLECTION)
        all_tournaments.sort(key=(lambda x: x["event_start_at"]))
        all_tournaments.reverse()

        tourny_list:List[objects.TournamentData] = []

        for tournament in all_tournaments:
            tourny_list.append(
                objects.TournamentData(
                    self.database,
                    time_and_date=datetime.fromtimestamp(tournament["event_start_at"]),
                    max_players=tournament["max_players"],
                    creator=GoldyBot.Member(self.ctx, member_id=tournament["created_by"])
                )
            )

        return tourny_list


class Tournament():
    """Creates tournament database interface with ctx to allow for easy grabbing of tournament data."""
    def __init__(self, ctx, tournament_data:objects.TournamentData) -> None:
        self.ctx = ctx
        self.tournament_data = tournament_data

        self.database = tournament_data.database


    def free_team(self, tournament_data:dict) -> str:
        """Returns a free team."""

        players:Dict[str, dict] = tournament_data["players"]

        all_used_team_nums:List[int] = []

        # Getting all used teams.
        for player in players:
            team = players[player]["team"]
            if not team == None:
                all_used_team_nums.append(team)

        if len(all_used_team_nums) > 0:
            # Find last used team number and return the number after that as a free team.
            all_used_team_nums.sort()
            return str(int(all_used_team_nums[-1]) + 1)
        else:
            return "1"


    async def add_player(self, player_data:objects.PlayerData):
        """Adds player to tournament."""
        # Get tournament current data.
        tournament_data = await self.get_tournament_data()

        if not await self.player_in_tournament(player_data.member, tournament_data):

            tournament_data["players"][player_data.member.member_id] = {

                "discord_id" : str(player_data.member.member_id),
                "mc_ign" : str(player_data.mc_ign),
                "mc_uuid" : str(player_data.mc_uuid),
                "team" : str(player_data.team),
                # Returns 'None' if pending_teammate is none but returns 'pending_teammate.discord_id' if not None.
                "pending_teammate": (lambda teammate: None if (teammate == None) else teammate.member_id)(player_data.pending_teammate) 
            
            }

            await self.database.edit(
                TOURNAMENTS_COLLECTION, 
                query = {"_id":int(self.tournament_data.time_and_date.timestamp())},
                data=tournament_data
            )

            return True

        return False


    async def remove_player(self, player_data:objects.PlayerData):
        """Adds player to tournament."""
        # Get tournament current data.
        tournament_data = await self.get_tournament_data()

        if await self.player_in_tournament(player_data.member, tournament_data):

            # Removing player from dict.
            del tournament_data["players"][player_data.member.member_id]
            
            # Update database with removed player.
            await self.database.edit(
                TOURNAMENTS_COLLECTION, 
                query={"_id":int(self.tournament_data.time_and_date.timestamp())},
                data=tournament_data
            )

            return True

        return False


    async def team_player(self, member:GoldyBot.Member, teammate:GoldyBot.Member):
        """Sets the pending teammate of the first player to the 2nd player. Repeating this for the 2nd player will make these two players officially teamed."""
        # Get tournament current data.
        tournament_database_data = await self.get_tournament_data()

        if await self.player_in_tournament(member, tournament_database_data):

            # Editing player pending teammate in dict.
            tournament_database_data["players"][member.member_id]["pending_teammate"] = teammate.member_id
            
            # Update database with edited player pending teammate.
            await self.database.edit(
                TOURNAMENTS_COLLECTION, 
                query={"_id":int(self.tournament_data.time_and_date.timestamp())},
                data=tournament_database_data
            )

            return True

        return False


    async def player_in_tournament(self, member:GoldyBot.Member, tournament_database_data:dict) -> bool:
        """Checks if player is in tournament."""

        if not tournament_database_data["players"].get(member.member_id) == None:
            return True

        return False


    async def remove(self):
        """Removes this tournament from the 'mcf_signup' database collection."""

        # Check if tournament exists in 'tournaments' collection.
        document = await self.get_tournament_data()
        
        if not document == None: # Delete if exists.
            # Remove from 'tournaments' collection.
            await self.database.remove(TOURNAMENTS_COLLECTION, data=document)

            # Move to 'deleted_tournaments' collection.
            await self.database.insert(DELETED_TOURNAMENTS_COLLECTION, data=document)

            return True
            
        return False


    async def setup(self):
        """Makes sure this tournament is setup in the 'mcf_signup' database collection."""

        # Check if tournament does not exist in 'tournaments' collection.
        if await self.database.find_one(TOURNAMENTS_COLLECTION, {"_id":int(self.tournament_data.time_and_date.timestamp())}) == None:
            await self.database.insert(TOURNAMENTS_COLLECTION, data={
                "_id" : int(self.tournament_data.time_and_date.timestamp()),
                "created_at" : int(datetime.now().timestamp()),
                "event_start_at" : int(self.tournament_data.time_and_date.timestamp()),
                "max_players" : self.tournament_data.max_players,
                "created_by" : str(self.ctx.author.id),

                "players" : {}
            })

            return True
            
        return False
    
    create = setup
    """Creates this tournament."""


    async def get_tournament_data(self) -> dict|None:
        """Returns tournament's database data."""
        # Generate document if tournament doesn't exists in collection.
        await self.setup()

        # Return tournament data.
        return await self.database.find_one(TOURNAMENTS_COLLECTION, {"_id":int(self.tournament_data.time_and_date.timestamp())})