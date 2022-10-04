import GoldyBot
from  GoldyBot.utility.commands import send as send_msg, mention

class WoltryBucks(GoldyBot.Currency):
    """Don't question this, it had to be done."""
    def __init__(self):
        super().__init__("woltry_bucks", "Woltry Bucks", "💷", 0)

class WoltryBucksExtension(GoldyBot.Extension):
    def __init__(self, package_module=None):
        self.currency = WoltryBucks()

        self.sent_money_embed = GoldyBot.Embed(
            title=f"💚 {self.currency.display_emoji}{self.currency.display_name} Sent!",
            colour=GoldyBot.colours.GREEN
        )

        self.took_money_embed = GoldyBot.Embed(
            title=f"💛 {self.currency.display_emoji}{self.currency.display_name} Taken!",
            colour=GoldyBot.colours.YELLOW
        )

        self.money_not_processed_embed = GoldyBot.Embed(
            title=f"❤ Not Processed!",
            description="The ``{}`` failed to process for some reason. Contact {}.",
            colour=GoldyBot.colours.RED
        )

        super().__init__(self, package_module_name=package_module)

    def loader(self):

        @GoldyBot.command(slash_cmd_only=True)
        async def woltry_bucks(self:WoltryBucksExtension, ctx):
            pass

        @woltry_bucks.sub_command(required_roles=["woltry_bucks_seller"], also_run_parent_CMD=False, slash_options={
            "member":GoldyBot.nextcord.SlashOption(description="Mention of member you would like to send woltry bucks to.", required=True)
        })
        async def send(self:WoltryBucksExtension, ctx, member:str, amount:str):
            target_member = GoldyBot.Member(ctx, mention_str=member)

            result = await target_member.give_money(self.currency, str(amount))

            if result:
                embed = self.sent_money_embed.copy()
                embed.description = f"**{self.currency.display_emoji}``{amount}``** of **{self.currency.display_emoji} {self.currency.display_name}** has been sent to {mention(target_member)}"
                
                await send_msg(ctx, embed=embed)

            else:
                embed = self.money_not_processed_embed.copy()
                embed.description = embed.description.format(self.currency.display_name, mention(GoldyBot.Member(ctx, member_id=332592361307897856)))

                await send_msg(ctx, embed=embed)

                

        @woltry_bucks.sub_command(required_roles=["woltry_bucks_seller"], also_run_parent_CMD=False, slash_options={
            "member":GoldyBot.nextcord.SlashOption(description="Mention of member you would like to take woltry bucks from.", required=True)
        })
        async def take(self:WoltryBucksExtension, ctx, member:str, amount:str):
            target_member = GoldyBot.Member(ctx, mention_str=member)

            result = await target_member.take_money(self.currency, str(amount))

            if result:
                embed = self.took_money_embed.copy()
                embed.description = f"**{self.currency.display_emoji}``{amount}``** of **{self.currency.display_emoji} {self.currency.display_name}** has been taken from {mention(target_member)}"
                
                await send_msg(ctx, embed=embed)

            else:
                embed = self.money_not_processed_embed.copy()
                embed.description = embed.description.format(self.currency.display_name, mention(GoldyBot.Member(ctx, member_id=332592361307897856)))

                await send_msg(ctx, embed=embed)