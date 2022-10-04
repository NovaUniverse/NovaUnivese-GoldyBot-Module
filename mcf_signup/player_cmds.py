import GoldyBot

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
            pass