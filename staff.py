import datetime
import dateparser
import nextcord

import GoldyBot
from GoldyBot.utility.commands import *

class NovaStaffUtils(GoldyBot.Extenstion):
    def __init__(self, package_module_name=None):
        super().__init__(self, package_module_name)

    def loader(self):
        @GoldyBot.command(help_des="A command used by staff for logging activity in #🔒staff-activity-log.", 
            required_roles=["nova_staff"], slash_cmd_only=True, slash_options= {
            "action" : nextcord.SlashOption("action", "What action did you perform?", required=True),
            "type" : nextcord.SlashOption("type", "What type?", required=True),
            "date" : nextcord.SlashOption("date", "When did you take action?", required=True),
            "user" : nextcord.SlashOption("user", "Who did you take the action on?", required=True),
            "reason" : nextcord.SlashOption("reason", "Why did you take action?", required=True)
        })
        async def staff_log(self:NovaStaffUtils, ctx, action:str, type, date:str, user:GoldyBot.Member, reason:str):
            user = GoldyBot.Member(ctx, mention_str=user)

            # Parsing Date
            if not date.lower() in ["today", "", "none", "null"]:
                actual_date = dateparser.parse(date, date_formats=["%d/%m/%Y", "%Y/%m/%d", "%d.%m.%Y"]).strftime("%d/%m/%Y")
            else:
                actual_date = datetime.datetime.now().strftime("%d/%m/%Y")

            embed = GoldyBot.utility.goldy.embed.Embed(title=Embed.title, colour=Embed.colour)
            embed.set_thumbnail(url=await get_member_pfp(ctx.author))
            embed.description = Embed.des.format(action, type, actual_date, mention(user), reason)

            await ctx.send(embed=embed)

class Embed:
    title = "📰 Activity Report"
    des = """
    **Action: ** *{}*
    **Type: ** ``{}``
    **Date: ** ``{}``
    **User: ** {}
    **Reason: ** *{}*
    """
    colour = GoldyBot.utility.goldy.colours.GREY