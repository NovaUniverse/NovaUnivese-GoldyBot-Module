from __future__ import annotations
import GoldyBot
import novauniverse
from . import _tournament_

class MCFPlayer(GoldyBot.Member):
    """Represents a member from the Nova Universe discord server that triggers an MCF command."""
    def __init__(self, ctx, mc_ign:str=None):
        self.ctx = ctx

        self.mc_ign_ = mc_ign

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
    def discord_id(self):
        """Returns the discord id of the player."""
        return self.member_id