from __future__ import annotations
import GoldyBot
from . import _tournament_

class MCFPlayer(GoldyBot.Member):
    """Represents a member from the Nova Universe discord server that triggers an MCF command."""
    def __init__(self, ctx, mcf:_tournament_.MCFTournament):
        self.ctx = ctx
        self.mcf = mcf

        super().__init__(ctx)

    @property
    def is_signed_up(self):
        """Checks if the player is signed up for mcf already."""
        pass

    def signup(self, minecraft_ign:str, teammate:GoldyBot.Member | None):
        """Signs player up for MCF and sends invite to their teammate."""

        self.mcf

        pass