import GoldyBot
from GoldyBot.utility.commands import *

from . import objects
from . import database

from datetime import datetime

mcf_database = GoldyBot.cache.database().new_instance("mcf_data")

class MCFSignupStaff(GoldyBot.Extension):
    def __init__(self, package_module=None):
        super().__init__(self, package_module_name=package_module)

        # Embeds
        #==========
        self.tournament_created = GoldyBot.utility.goldy.embed.Embed(
            title="🔥 Tournament has been created!",
            description="""
            ✅ Tournament has been created for **<t:{}:{}>**.

            {} *- To open the form now.*
            """,
            colour=GoldyBot.utility.goldy.colours.AKI_ORANGE
        )


        self.tournament_already_exist = GoldyBot.utility.goldy.embed.Embed(
            title="🛑 Tournament already exist!",
            description="""
            ❌ There is already a tournament for **<t:{}:{}>**.

            {} *- To cancel it.*
            """,
            colour=GoldyBot.utility.goldy.colours.RED
        )

    def loader(self):

        @GoldyBot.command(help_des="Allows admins to create, edit and cancel an mcf tournament.", slash_cmd_only=True, required_roles=["nova_admin", "nova_tournament_host"])
        async def mcf_admin(self:MCFSignupStaff, ctx):
            pass

        # Creation commands
        #===========================

        @mcf_admin.sub_command()
        async def create(self:MCFSignupStaff, ctx):
            # Create tournament data object.
            tournament_data = objects.TournamentData(
                mcf_database,
                datetime(2000, 12, 14, 7, 15, 29, 24, tzinfo=None),
                max_players=69
            )

            # Add tournament to database and send embed if added.
            if await database.Tournament(ctx, tournament_data).setup():
                # Tournament Created.
                embed = self.tournament_created.copy()
                embed.description = self.tournament_created.description.format(
                    int(tournament_data.time_and_date.timestamp()),
                    "F",
                    open_form.mention()
                )
                
                await send(ctx, embed=embed)

            else:
                # Tournament already exist with this date.
                embed = self.tournament_already_exist.copy()
                embed.description = self.tournament_already_exist.description.format(
                    int(tournament_data.time_and_date.timestamp()),
                    "F",
                    cancel.mention()
                )
                
                await send(ctx, embed=embed)

        @mcf_admin.sub_command()
        async def cancel(self:MCFSignupStaff, ctx):

            # TEMPORARY CODE

            tournament_data = objects.TournamentData(
                mcf_database,
                datetime(2000, 12, 14, 7, 15, 29, 24, tzinfo=None),
                max_players=69
            )

            await database.Tournament(ctx, tournament_data).remove()
                    


        #  Form commands.
        #====================

        @mcf_admin.sub_command()
        async def open_form(self:MCFSignupStaff, ctx):
            pass

        @mcf_admin.sub_command()
        async def close_form(self:MCFSignupStaff, ctx):
            pass