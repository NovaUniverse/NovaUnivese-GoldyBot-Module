from datetime import datetime
import GoldyBot

from . import objects
from . import database

mcf_database = GoldyBot.cache.database().new_instance("mcf_data")

class MCFSignup(GoldyBot.Extension):
    def __init__(self, package_module=None):
        super().__init__(self, package_module_name=package_module)

        # Embeds
        #==========
        self.form_closed = GoldyBot.utility.goldy.embed.Embed(
            title="🔒 The form is now closed!",
            description=f"""
            ❌ *You can no longer join or leave the tournament. If you would like to do any of those please contact staff.*
            """,
            colour=GoldyBot.utility.goldy.colours.AKI_ORANGE
        )

        self.no_mcf_embed = GoldyBot.utility.goldy.embed.Embed(
            title="⛔ SignUps not open yet!",
            description=f"""
            ❌ *Sorry we haven't open signups for the next mcf yet.*
            """,
            colour=GoldyBot.utility.goldy.colours.AKI_RED
        )

        self.youve_been_removed_embed = GoldyBot.utility.goldy.embed.Embed(
            title="🧳 You've been removed!",
            description=f"""
            🚚 You've been removed from this week's mcf.
            """,
            colour=GoldyBot.utility.goldy.colours.WHITE
        )

        self.your_already_registered_embed = GoldyBot.utility.goldy.embed.Embed(
            title="💚 Your already in! 😊",
            description=f"""
            ✔ You're already registered for this week's mcf.
            """,
            colour=GoldyBot.utility.goldy.colours.GREEN,
        )
        self.your_already_registered_embed.footer.text = "(Notice: Just a reminder that this doesn't mean your actually confirmed to be playing.)"

        self.your_not_in_this_weeks_mcf_embed = GoldyBot.utility.goldy.embed.Embed(
            title="❤ Your not in this weeks mcf!",
            description=f"""
            ⚠ You're not registered for this week's mcf.
            """,
            colour=GoldyBot.utility.goldy.colours.RED
        )

    def loader(self):

        @GoldyBot.command(help_des="A command for players to sign up for the MCF tournament.", slash_cmd_only=True)
        async def mcf(self:MCFSignup, ctx):
            pass

        @mcf.sub_command()
        async def join(self:MCFSignup, ctx):

            # TEMPORARY
            tournament_data = objects.TournamentData(
                mcf_database,
                datetime(2000, 12, 14, 7, 15, 29, 24, tzinfo=None),
                max_players=69
            )

            player_data = objects.PlayerData(GoldyBot.Member(ctx), "THEGOLDENPRO", "1", pending_teammate=None)
            
            await database.Tournament(ctx, tournament_data).add_player(player_data)

        @mcf.sub_command()
        async def leave(self:MCFSignup, ctx):

            # TEMPORARY
            tournament_data = objects.TournamentData(
                mcf_database,
                datetime(2000, 12, 14, 7, 15, 29, 24, tzinfo=None),
                max_players=69
            )

            player_data = objects.PlayerData(GoldyBot.Member(ctx), "THEGOLDENPRO", "1", pending_teammate=None)
            
            await database.Tournament(ctx, tournament_data).remove_player(player_data)