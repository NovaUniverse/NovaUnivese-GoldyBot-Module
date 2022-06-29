import asyncio
import nextcord
import GoldyBot

from . import _forms_, _info_, _tournament_, _player_

from GoldyBot.utility.datetime.user_input import *
from GoldyBot.utility.commands import *

from errors import TournamentDoesntExistError

class MCF(GoldyBot.Extenstion):
    def __init__(self, package_module=None):
        super().__init__(self, package_module_name=package_module)

    def loader(self):

        # mcf join command
        #======================
        @GoldyBot.command(help_des="An amazing command to sign up for the mcf minecraft tournament right from the confort of Discord.", slash_cmd_only=True)
        async def join_mcf(self:MCF, ctx:GoldyBot.objects.slash.InteractionToCtx):
            # Check if a joinable mcf tournament exists.
            tournament = await _info_.TournamentInfo().get_latest_mcf()

            if not tournament == None:
                # Send member form.
                await ctx.send_modal(_forms_.JoinMCFForm(tournament))
            else:
                # No mcf available.
                message = await send(ctx, embed=GoldyBot.utility.goldy.embed.Embed(
                    title="⛔ SignUps not open yet!",
                    description=f"""
                    ❌ *Sorry we haven't open signups for the next mcf yet.*
                    """,
                    colour=GoldyBot.utility.goldy.colours.AKI_RED
                ))

                await asyncio.sleep(6)

                await message.delete()

        @GoldyBot.command(help_des="Admin command to open the mcf minecraft tournament forum.", slash_cmd_only=True, required_roles=["nova_staff"])
        async def mcf_open_form(self:MCF, ctx:GoldyBot.objects.slash.InteractionToCtx):
            await ctx.send_modal(_forms_.OpenMCFForm())

        @GoldyBot.command(help_des="Admin command for canceling an MCF tournament.", slash_cmd_only=True, required_roles=["nova_staff"],
        slash_options={
            "mcf_date":nextcord.SlashOption("mcf_date", "Date of the mcf your trying to cancel."),
            "mcf_time":nextcord.SlashOption("mcf_time", "Time of the mcf your trying to cancel.")
        })
        async def mcf_cancel(self:MCF, ctx:GoldyBot.objects.slash.InteractionToCtx):
            tournament_info = _info_.TournamentInfo()
            
            view = _forms_.MCFCancelDropdownView(GoldyBot.Member(ctx), await tournament_info.get_all_mcfs())

            await ctx.send(embed=GoldyBot.utility.goldy.embed.Embed(
                title="🛑 Which MCF?",
                description="**⏱ Pick the mcf you would like to cancel.**",
                colour=GoldyBot.utility.goldy.colours.WHITE
            ), view=view)