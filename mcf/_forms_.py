import GoldyBot
import datetime
import dateparser

from . import _tournament_, _player_, _info_

database:GoldyBot.Database = GoldyBot.cache.main_cache_dict["database"]
mcf_database = database.new_instance("mcf_data")

class JoinMCFForm(GoldyBot.nextcord.ui.Modal):
    def __init__(self, tournament:_tournament_.MCFTournament):
        super().__init__(
            "Join 🔥 MCF Tournament",
        )

        self.tournament = tournament

        self.time_agree = GoldyBot.nextcord.ui.TextInput(
            label="Will you be on time? (Saturday 18:00 GMT+1)",
            style=GoldyBot.nextcord.TextInputStyle.short,
            placeholder="Yes",
            default_value="No",
            required=True,
            min_length=2,
            max_length=3
        )
        self.add_item(self.time_agree)

        self.mc_username = GoldyBot.nextcord.ui.TextInput(
            label="Enter Minecraft IGN",
            placeholder="Minecraft IGN...",
            required=True
        )
        self.add_item(self.mc_username)

    async def callback(self, interaction: GoldyBot.nextcord.Interaction) -> None:
        mcf_player = _player_.MCFPlayer(interaction, 
            self.mc_username.value)

        await self.tournament.add_player(mcf_player)

        embed = GoldyBot.utility.goldy.embed.Embed(
            title="✅ Join Request Sent!",
            colour=GoldyBot.utility.goldy.colours.GREEN,
            description=f"""
            **Your form has been sent. You've been added to the tournament player list. Closer to tournament date, you'll be pinged in <#7188671160430632> when your in!**

            **[How to Team with Friends?]()**
            """)

        # Move this message to a discord server help channel.
        """💌 To team with a friend they must also do ``/join_mcf`` and then your able to send eachother team requests via ``/mcf_team``. 😊"""

        await interaction.send(embed=embed)

class OpenMCFForm(GoldyBot.nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            "🔓 Open 🔥 MCF Tournament",
        )

        self.tournament_date = GoldyBot.nextcord.ui.TextInput(
            label="Tournament Date",
            style=GoldyBot.nextcord.TextInputStyle.short,
            placeholder="The damn date you idiot! Like --> 13/05/2022",
            default_value=f"{datetime.date.today().strftime('%d/%m/%Y')}",
            required=True,
            min_length=6,
        )
        self.add_item(self.tournament_date)

        self.tournament_time = GoldyBot.nextcord.ui.TextInput(
            label="Tournament Time",
            style=GoldyBot.nextcord.TextInputStyle.short,
            placeholder="The damn time you idiot! Like --> 18:00",
            default_value=f"{datetime.date.today().strftime('%H:%M')}",
            required=True,
            min_length=5,
        )
        self.add_item(self.tournament_time)

        # Settings
        self.max_players = GoldyBot.nextcord.ui.TextInput(
            style=GoldyBot.nextcord.TextInputStyle.short,
            label="Max Players",
            placeholder="Max players, UwU!",
            default_value="24",
            required=True
        )
        self.add_item(self.max_players)

    async def callback(self, interaction: GoldyBot.nextcord.Interaction) -> None:
        
        # Create the tournament.
        #==========================
        mcf = _tournament_.MCFTournament(mcf_database, self.tournament_date.value, self.tournament_time.value, self.max_players.value)

        await mcf.init()

        if mcf.was_created:
            embed = GoldyBot.utility.goldy.embed.Embed(
                title="✔ MCF Form now open!",
                description=f"""
                **🔥 MCF Form is now open until ``{mcf.date.time().strftime("%H:%M%p")} ({datetime.datetime.now().astimezone().tzinfo})`` on ``{mcf.date.date().strftime("%d/%m/%Y")}`` ✅**

                ``/join_mcf``
                """)

            await interaction.send(embed=embed)
        
        else:
            embed = GoldyBot.utility.goldy.embed.Embed(
                title="❌ MCF already exists!",
                description=f"""
                **🔥 There's already an mcf for that date.** ❌

                ``/mcf_cancel {{{mcf.date.date().strftime("%d/%m/%Y")}}} {{{mcf.date.time().strftime("%H:%M")}}}``
                """)

            await interaction.send(embed=embed)