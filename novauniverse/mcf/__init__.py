import nextcord
import GoldyBot

from . import _forms_

class MCF(GoldyBot.Extenstion):
    def __init__(self, package_module=None):
        super().__init__(self, package_module_name=package_module)

    def loader(self):

        @GoldyBot.command(help_des="An amazing command to join the mcf minecraft tournament.", slash_cmd_only=True, slash_options={
            "teammate": nextcord.SlashOption("teammate", 
            description="Mention the teammate you want to participate with here. Pick No Teammate for random teammate.", required=True, 
            choices={"No Teammate": "none"})
        })
        async def join_mcf(self:MCF, ctx:GoldyBot.objects.slash.InteractionToCtx, teammate:GoldyBot.nextcord.Member=None):
            if isinstance(teammate, GoldyBot.nextcord.Member):
                await ctx.send_modal(_forms_.JoinMCFForm(teammate))
            else:
                await ctx.send_modal(_forms_.JoinMCFForm())

        @GoldyBot.command(help_des="Admin command to open the mcf minecraft tournament forum.", slash_cmd_only=True, required_roles=["nova_staff"])
        async def open_mcf_form(self:MCF, ctx:GoldyBot.objects.slash.InteractionToCtx):
            await ctx.send_modal(_forms_.OpenMCFForm())