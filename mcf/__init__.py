import nextcord
import GoldyBot

from . import _forms_, _info_, _tournament_, _player_

from GoldyBot.utility.datetime.user_input import *

from errors import TournamentDoesntExistError

class MCF(GoldyBot.Extenstion):
    def __init__(self, package_module=None):
        super().__init__(self, package_module_name=package_module)

    def loader(self):

        # mcf join command
        #======================
        @GoldyBot.command(help_des="An amazing command to sign up for the mcf minecraft tournament right from the confort of Discord.", slash_cmd_only=True, 
        slash_options={
            "teammate": nextcord.SlashOption("teammate", description="Mention the teammate you want to participate with here. Ignore this parameter for random teammates.", required=False)
        })
        async def join_mcf(self:MCF, ctx:GoldyBot.objects.slash.InteractionToCtx, teammate=None):
            # Check if a joinable mcf tournament exists.
            
            # Send member form.
            await ctx.send_modal(_forms_.JoinMCFForm())

        @GoldyBot.command(help_des="Admin command to open the mcf minecraft tournament forum.", slash_cmd_only=True, required_roles=["nova_staff"])
        async def mcf_open_form(self:MCF, ctx:GoldyBot.objects.slash.InteractionToCtx):
            await ctx.send_modal(_forms_.OpenMCFForm())

        @GoldyBot.command(help_des="Admin command for canceling an MCF tournament.", slash_cmd_only=True, required_roles=["nova_staff"],
        slash_options={
            "mcf_date":nextcord.SlashOption("mcf_date", "Date of the mcf your trying to cancel."),
            "mcf_time":nextcord.SlashOption("mcf_time", "Time of the mcf your trying to cancel.")
        })
        async def mcf_cancel(self:MCF, ctx:GoldyBot.objects.slash.InteractionToCtx, mcf_date):
            tournament_info = _info_.TournamentInfo()

            mcf = _tournament_.MCFTournament(tournament_info.mcf_database, mcf_date, None, None, 
                dont_create=True)

            try: 
                await mcf.init()
            except TournamentDoesntExistError:
                embed = GoldyBot.utility.goldy.embed.Embed(
                    title="❌ MCF doesn't exist!",
                    description=f"""
                    **❤ Can't find mcf for ``{mcf_date}``, it doesn't exist!** 
                    """,
                    colour=GoldyBot.utility.goldy.colours.RED)

                await ctx.send(embed=embed)
                return True
            
            if await mcf.delete():
                embed = GoldyBot.utility.goldy.embed.Embed(
                    title="⛔ MCF Cancelled!",
                    description=f"""
                    **❌ The MCF for ``{mcf_date}`` has been cancelled!** 
                    """,
                    colour=GoldyBot.utility.goldy.colours.AKI_RED)

                await ctx.send(embed=embed)
                return True

            return False