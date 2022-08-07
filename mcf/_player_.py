from __future__ import annotations
import GoldyBot
import novauniverse

from GoldyBot.utility.datetime import user_output
from . import _tournament_, _info_

MODULE_NAME = "PLAYER"

class MCFPlayer(GoldyBot.Member):
    """Represents a member from the Nova Universe discord server that triggers an MCF command."""
    def __init__(self, ctx, mc_ign:str=None, team:str=None, pending_teammate_:str=None):
        self.ctx = ctx

        self.mc_ign_ = mc_ign
        self.team_ = team
        self.pending_teammate_ = pending_teammate_

        super().__init__(ctx)

    @property
    def mc_ign(self):
        """Returns minecraft ign of player."""
        return self.mc_ign_

    @property
    def uuid(self):
        """Returns minecraft uuid of player."""
        return novauniverse.Player(self.mc_ign).uuid

    @property
    def team(self) -> str|None:
        """Returns team number."""
        return self.team_

    @property
    def pending_teammate(self) -> str|None:
        """Returns the pending teammate of the player."""
        return self.pending_teammate_

    async def set_teammate(self, mcf_player:MCFPlayer):
        """Sets teammate of player, the teammate has to also have their teammate set to this player for them to officially become teammates. (Complicated I know)"""
        mcf = await _info_.TournamentInfo().get_latest_mcf()

        if not mcf_player.pending_teammate == None:
            if mcf_player.pending_teammate == self.discord_id:
                # Assign them into a team.
                free_team = await mcf.free_team(mcf_player)

                # Assign team to this player.
                mcf.tournament_database.edit(user_output.make_date_human(mcf.date), {
                    "_id": self.discord_id
                },
                {
                    "team": free_team
                })

                # Assign team to teammate.
                mcf.tournament_database.edit(user_output.make_date_human(mcf.date), {
                    "_id": mcf_player.discord_id
                },
                {
                    "team": free_team
                }) #TODO: Where I left off, add print statements. Also else don't assign them.
        else:
            # Don't assign them into a team yet, give this player a pending teammate id.
            mcf.tournament_database.edit(user_output.make_date_human(mcf.date), {
                    "_id": self.discord_id
                },
                {
                    "pending_teammate": mcf_player.discord_id
                })

            GoldyBot.log(f"[{MODULE_NAME}] I didn't assign '{self.name}' a teammate right away because I'm waiting on the teammate ({mcf_player.name}) to also team with them.")


    @property
    def discord_id(self):
        """Returns the discord id of the player."""
        return self.member_id


    @property
    def head_url(self):
        """Returns url to png image of player's head."""
        return f"https://crafatar.com/avatars/{self.uuid}.png"