import GoldyBot

class TournamentDoesntExistError(GoldyBot.errors.GoldyBotError):
    def __init__(self, error):
        super().__init__(error)