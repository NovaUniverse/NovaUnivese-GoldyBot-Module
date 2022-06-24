from __future__ import annotations
import GoldyBot
from . import _tournament_

class MCFPlayer(GoldyBot.Member):
    """Represents a member from the Nova Universe discord server that triggers an MCF command."""
    def __init__(self, ctx, mc_ign:str):
        self.ctx = ctx

        self.mc_ign_ = mc_ign

        super().__init__(ctx)

    @property
    def mc_ign(self):
        """Returns minecraft ign of player."""
        return self.mc_ign_