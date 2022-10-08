from typing import List
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

        self.no_tournaments_exist = GoldyBot.Embed(
            title="🌵🕸 No tournaments exist.",
            description="There's no tournaments currently in the list, you can create one with {}.",
            colour=GoldyBot.Colours.LIME_GREEN
        )


        # Views

        self.which_mcf = GoldyBot.Embed(
            title="🛑 Which MCF?",
            description="**⏱ Pick the mcf you would like to cancel.**",
            colour=GoldyBot.utility.goldy.colours.WHITE
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
                max_players=69,
                creator=GoldyBot.Member(ctx)
            ) #TODO: Change to form input.

            # Send Form
            await send_modal(ctx, 
                await GoldyBot.utility.views.forms.normal_form(
                    title="🏆 Create Tournament",
                    items=[

                    ]
                )
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
            all_mcf_tournaments = await database.McfDataUtils(ctx, mcf_database).get_all_tournaments()

            options:List[GoldyBot.nextcord.SelectOption] = []

            id = 0
            for tournament in all_mcf_tournaments:
                options.append(
                    GoldyBot.nextcord.SelectOption(
                        label=f"🔥 MCF - {GoldyBot.utility.datetime.user_output.make_date_human(tournament.time_and_date, date_format='(%a, %d %b)')}",
                        description=f"{GoldyBot.utility.datetime.user_output.make_date_human(tournament.time_and_date, date_format='%Y')} • Created By '{tournament.creator.name}'",
                        value=id
                    )
                )

                id += 1

            if not options == []: # If not empty.
                async def delete_tournaments(ids): 
                    for id in ids: 
                        await database.Tournament(ctx, all_mcf_tournaments[int(id)]).remove()

                view = await GoldyBot.utility.views.dropdown.dropdown(ctx, options, min_max_value=(1, 5), callback=delete_tournaments)
                await send(ctx, embed=self.which_mcf, view=view)
            
            else:
                embed = self.no_tournaments_exist.copy()
                embed.description = self.no_tournaments_exist.description.format(create.mention())
                message = await send(ctx, embed=embed)
                await message.delete(delay=6)


            # TEMPORARY CODE
            """
            tournament_data = objects.TournamentData(
                mcf_database,
                datetime(2000, 12, 14, 7, 15, 29, 24, tzinfo=None),
                max_players=69
            ) #TODO: Change to form input.

            await database.Tournament(ctx, tournament_data).remove()   
            """

        #  Form commands.
        #====================

        @mcf_admin.sub_command()
        async def open_form(self:MCFSignupStaff, ctx):
            pass

        @mcf_admin.sub_command()
        async def close_form(self:MCFSignupStaff, ctx):
            pass