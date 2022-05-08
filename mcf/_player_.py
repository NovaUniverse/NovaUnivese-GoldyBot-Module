import GoldyBot

class MCFPlayer(GoldyBot.Member):
    """Represents a member on the Nova Universe discord server that triggers an MCF command."""
    def __init__(self, ctx):
        self.ctx = ctx
        super().__init__(ctx)

    @property
    def is_signed_up(self):
        """Checks if the player is signed up for mcf already."""
        pass

    def signup(self, minecraft_ign:str, teammate:GoldyBot.Member):
        """Signs player up for MCF."""
        pass