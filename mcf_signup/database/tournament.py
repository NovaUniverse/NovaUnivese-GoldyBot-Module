from __future__ import annotations

import GoldyBot
from . import TOURNAMENTS_COLLECTION
from .. import objects

from datetime import datetime

class McfDataUtils():
    """Class containing utils to help find tournaments and a lot more in the database."""
    def __init__(self, database:GoldyBot.Database):
        self.database = database


class Tournament():
    """Creates tournament database interface with ctx to allow for easy grabbing of tournament data."""
    def __init__(self, ctx, tournament_data:objects.TournamentData) -> None:
        self.ctx = ctx
        self.tournament_data = tournament_data

        self.database = tournament_data.database

    async def add_player(self, player_data:objects.PlayerData):
        """Adds player to tournament."""
        if not await self.player_in_tournament():

            await self.database.edit(
                TOURNAMENTS_COLLECTION, 
                query = {"_id":int(self.tournament_data.time_and_date.timestamp())},

                data = {
                    "players": [
                        {
                            "discord_id" : str(player_data.member.member_id),
                            "mc_ign" : str(player_data.mc_ign),
                            "mc_uuid" : str(player_data.mc_uuid),
                            "team" : str(player_data.team),
                            "pending_teammate": str(player_data.pending_teammate.member_id)
                        }
                    ]
                }
            )

            return True

        return False

    async def player_in_tournament(self, member:GoldyBot.Member) -> bool:
        """Checks if player is in tournament."""
        for player in await self.get_tournament_data()["players"]:
            if player["id"] == member.member_id:
                return True

        return False

    async def get_tournament_data(self) -> dict|None:
        """Returns tournament's database collection."""
        # Generate document if tournament doesn't exists in collection.
        await self.setup()

        # Return tournament data.
        return await self.database.find_one(TOURNAMENTS_COLLECTION, {"_id":int(self.tournament_data.time_and_date.timestamp())})


    async def remove(self):
        """Removes this tournament from the 'mcf_signup' database collection."""

        # Check if tournament exists in 'tournaments' collection.
        if not await self.database.find_one(TOURNAMENTS_COLLECTION, {"_id":int(self.tournament_data.time_and_date.timestamp())}) == None:
            await self.database.remove(TOURNAMENTS_COLLECTION, data={
                "_id" : int(self.tournament_data.time_and_date.timestamp()),
                "created_at" : int(datetime.now().timestamp()),
                "event_start_at" : int(self.tournament_data.time_and_date.timestamp()),
                "max_players" : self.tournament_data.max_players,
                "created_by" : str(self.ctx.author.id),

                "players" : []
            })

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

                "players" : []
            })

            return True
            
        return False
